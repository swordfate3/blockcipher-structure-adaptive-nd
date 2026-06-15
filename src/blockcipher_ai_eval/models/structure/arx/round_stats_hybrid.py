from __future__ import annotations

import torch
from torch import nn

from blockcipher_ai_eval.models.common.components import build_activation, build_norm
from blockcipher_ai_eval.models.structure.arx.round_function_hybrid import (
    ArxRoundFunctionHybridPairSetDistinguisher,
)


class ArxRoundStatsHybridPairSetDistinguisher(nn.Module):
    """SPECK pair-set model with round-function tokens and cross-pair ARX statistics."""

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 736,
        base_channels: int = 32,
        word_bits: int = 16,
        token_dim: int | None = None,
        mixer_depth: int = 3,
        group_mixer_depth: int = 2,
        token_mlp_ratio: int = 2,
        activation: str = "gelu",
        norm: str = "layernorm",
        dropout: float = 0.0,
        stats_hidden_bits: int | None = None,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("ArxRoundStatsHybrid input_bits must be a multiple of pair_bits")
        if pair_bits % 32 != 0:
            raise ValueError("ArxRoundStatsHybrid pair_bits must be a multiple of 32-bit ARX feature words")
        if word_bits != 16:
            raise ValueError("ArxRoundStatsHybrid currently supports 16-bit SPECK32 words")
        if input_bits // pair_bits < 2:
            raise ValueError("ArxRoundStatsHybrid needs at least two pairs per sample")

        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.structure = "ARX"
        self.word_bits = word_bits
        self.feature_words_per_pair = pair_bits // 32
        self.half_words_per_feature = 2
        self.token_dim = token_dim or max(16, base_channels * 2)
        self.stats_hidden_bits = stats_hidden_bits or max(64, base_channels * 8)
        self.activation = activation
        self.norm = norm
        self.dropout = dropout

        self.round_branch = ArxRoundFunctionHybridPairSetDistinguisher(
            input_bits=pair_bits,
            pair_bits=pair_bits,
            base_channels=base_channels,
            word_bits=word_bits,
            token_dim=self.token_dim,
            mixer_depth=mixer_depth,
            group_mixer_depth=group_mixer_depth,
            token_mlp_ratio=token_mlp_ratio,
            activation=activation,
            norm=norm,
            pooling="attention",
            dropout=dropout,
            top_k=1,
            lse_temperature=1.0,
        )
        self.round_pair_embedding_bits = self.round_branch.projected_pair_embedding_bits

        self.role_group_count = len(self.round_branch.round_relation_groups)
        self.stats_feature_bits = (
            self.feature_words_per_pair * self.half_words_per_feature * 5
            + self.feature_words_per_pair * 8
            + self.role_group_count * 5
            + 6
        )
        self.stats_projection = nn.Sequential(
            build_norm(norm, self.stats_feature_bits),
            nn.Linear(self.stats_feature_bits, self.stats_hidden_bits),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(self.stats_hidden_bits, self.stats_hidden_bits),
            build_activation(activation),
        )
        self.fused_embedding_bits = self.round_pair_embedding_bits * 3 + self.stats_hidden_bits
        self.classifier = nn.Sequential(
            build_norm(norm, self.fused_embedding_bits),
            nn.Linear(self.fused_embedding_bits, max(128, base_channels * 8)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(128, base_channels * 8), max(64, base_channels * 4)),
            build_activation(activation),
            nn.Linear(max(64, base_channels * 4), 1),
        )

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _pairset_statistics(self, features: torch.Tensor) -> torch.Tensor:
        batch_size = features.shape[0]
        halves = features.float().reshape(
            batch_size,
            self.pairs_per_sample,
            self.feature_words_per_pair,
            self.half_words_per_feature,
            self.word_bits,
        )
        half_active = halves.mean(dim=-1)
        half_mean = half_active.mean(dim=1)
        half_var = half_active.var(dim=1, unbiased=False)
        half_max = half_active.amax(dim=1)
        half_min = half_active.amin(dim=1)
        first_last_half_delta = half_active[:, -1] - half_active[:, 0]

        word_active = half_active.mean(dim=-1)
        word_mean = word_active.mean(dim=1)
        word_var = word_active.var(dim=1, unbiased=False)
        word_max = word_active.amax(dim=1)
        word_min = word_active.amin(dim=1)
        word_edge = half_active[:, :, :, 0].mean(dim=1) - half_active[:, :, :, 1].mean(dim=1)
        first_last_word_delta = word_active[:, -1] - word_active[:, 0]
        even_odd_delta = (
            word_active[:, :, ::2].mean(dim=(1, 2), keepdim=True)
            - word_active[:, :, 1::2].mean(dim=(1, 2), keepdim=True)
        ).expand(-1, 1, self.feature_words_per_pair).squeeze(1)
        word_span = word_max - word_min

        group_values = []
        for group in self.round_branch.round_relation_groups:
            group_values.append(word_active[:, :, group].mean(dim=(1, 2)))
        group_active = torch.stack(group_values, dim=1)
        group_mean = group_active
        group_var = group_active.var(dim=1, unbiased=False).unsqueeze(1).expand(-1, self.role_group_count)
        group_max_delta = group_active.amax(dim=1, keepdim=True) - group_active
        group_min_delta = group_active - group_active.amin(dim=1, keepdim=True)
        group_edge = (group_active[:, -1:] - group_active[:, :1]).expand(-1, self.role_group_count)

        carry_start = 9 if self.feature_words_per_pair > 10 else max(0, self.feature_words_per_pair - 2)
        carry_active = word_active[:, :, carry_start:].mean(dim=(1, 2))
        base_active = word_active[:, :, : min(4, self.feature_words_per_pair)].mean(dim=(1, 2))
        partial_active = (
            word_active[:, :, 4:7].mean(dim=(1, 2))
            if self.feature_words_per_pair > 6
            else word_active.mean(dim=(1, 2))
        )
        rx_active = (
            word_active[:, :, 7:9].mean(dim=(1, 2))
            if self.feature_words_per_pair > 8
            else word_active.mean(dim=(1, 2))
        )
        global_stats = torch.stack(
            [
                base_active,
                partial_active,
                rx_active,
                carry_active,
                carry_active - base_active,
                rx_active - partial_active,
            ],
            dim=1,
        )

        return torch.cat(
            [
                half_mean.flatten(1),
                half_var.flatten(1),
                half_max.flatten(1),
                half_min.flatten(1),
                first_last_half_delta.flatten(1),
                word_mean,
                word_var,
                word_max,
                word_min,
                word_edge,
                first_last_word_delta,
                even_odd_delta,
                word_span,
                group_mean,
                group_var,
                group_max_delta,
                group_min_delta,
                group_edge,
                global_stats,
            ],
            dim=1,
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.float().reshape(
            features.shape[0] * self.pairs_per_sample,
            self.pair_bits,
        )
        round_embeddings = self.round_branch._encode_pairs(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.round_pair_embedding_bits,
        )
        round_mean = round_embeddings.mean(dim=1)
        round_max = round_embeddings.max(dim=1).values
        round_std = round_embeddings.std(dim=1, unbiased=False)
        stats_embedding = self.stats_projection(self._pairset_statistics(features))
        return self.classifier(torch.cat([round_mean, round_max, round_std, stats_embedding], dim=1))


__all__ = ["ArxRoundStatsHybridPairSetDistinguisher"]
