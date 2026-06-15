from __future__ import annotations

import torch
from torch import nn

from blockcipher_ai_eval.models.structure.adaptive_dbitnet import StructureConditionedDBitNetEncoder
from blockcipher_ai_eval.models.common.components import (
    AttentionPooling,
    EvidencePooling,
    GatedAttentionPooling,
    build_activation,
    build_norm,
)


class SpnCellPairSetDBitNetDistinguisher(nn.Module):
    """SPN-focused PairSet DBitNet with explicit 4-bit cell encoding."""

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 192,
        base_channels: int = 32,
        cell_bits: int = 4,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("SpnCellPairSetDBitNet input_bits must be a multiple of pair_bits")
        if pair_bits % cell_bits != 0:
            raise ValueError("SpnCellPairSetDBitNet pair_bits must be a multiple of cell_bits")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.structure = "SPN"
        self.cell_bits = cell_bits
        self.cells_per_pair = pair_bits // cell_bits
        self.encoder = StructureConditionedDBitNetEncoder(
            pair_bits,
            base_channels=base_channels,
            structure="SPN",
        )
        self.cell_encoder = nn.Sequential(
            nn.Linear(cell_bits, base_channels),
            nn.GELU(),
            nn.Linear(base_channels, base_channels),
            nn.GELU(),
        )
        self.cell_embedding_bits = base_channels * 4
        self.fused_pair_embedding_bits = self.encoder.embedding_bits + self.cell_embedding_bits
        self.cell_projection = nn.Sequential(
            nn.Linear(base_channels * 2, self.cell_embedding_bits),
            nn.GELU(),
        )
        self.attention = nn.Sequential(
            nn.LayerNorm(self.fused_pair_embedding_bits),
            nn.Linear(self.fused_pair_embedding_bits, 128),
            nn.GELU(),
            nn.Linear(128, 1),
        )
        self.classifier = nn.Sequential(
            nn.LayerNorm(self.fused_pair_embedding_bits * 3),
            nn.Linear(self.fused_pair_embedding_bits * 3, 256),
            nn.GELU(),
            nn.Linear(256, 128),
            nn.GELU(),
            nn.Linear(128, 1),
        )
        self.last_attention_weights: torch.Tensor | None = None

    def set_cipher_structure(self, structure: str) -> None:
        if structure != "SPN":
            return
        self.encoder.set_cipher_structure(structure)

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _cell_embedding(self, pair_features: torch.Tensor) -> torch.Tensor:
        cells = pair_features.reshape(
            pair_features.shape[0] * self.cells_per_pair,
            self.cell_bits,
        )
        cell_embeddings = self.cell_encoder(cells).reshape(
            pair_features.shape[0],
            self.cells_per_pair,
            -1,
        )
        mean_embedding = cell_embeddings.mean(dim=1)
        max_embedding = cell_embeddings.max(dim=1).values
        return self.cell_projection(torch.cat([mean_embedding, max_embedding], dim=1))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.float().reshape(
            features.shape[0] * self.pairs_per_sample,
            self.pair_bits,
        )
        dbit_embeddings = self.encoder(pair_features)
        cell_embeddings = self._cell_embedding(pair_features)
        fused_pair_embeddings = torch.cat([dbit_embeddings, cell_embeddings], dim=1).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.fused_pair_embedding_bits,
        )
        attention_logits = self.attention(fused_pair_embeddings).squeeze(-1)
        attention_weights = torch.softmax(attention_logits, dim=1)
        self.last_attention_weights = attention_weights.detach()
        attention_embedding = torch.sum(
            fused_pair_embeddings * attention_weights.unsqueeze(-1),
            dim=1,
        )
        mean_embedding = fused_pair_embeddings.mean(dim=1)
        max_embedding = fused_pair_embeddings.max(dim=1).values
        pooled = torch.cat([attention_embedding, mean_embedding, max_embedding], dim=1)
        return self.classifier(pooled)


class SpnNibbleConvPairSetDistinguisher(nn.Module):
    """SPN-focused pair-set model that preserves nibble position before pooling.

    Unlike SpnCellPairSetDBitNetDistinguisher, this model keeps the 4-bit cell
    sequence inside each pair and applies residual 1D convolutions across cells
    before aggregating multiple pairs.  It is intended as the SPN expert for
    innovation-one structure-adaptive experiments.
    """

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 192,
        base_channels: int = 32,
        nibble_bits: int = 4,
        nibble_embed_dim: int | None = None,
        conv_depth: int = 3,
        kernel_size: int = 3,
        activation: str = "gelu",
        norm: str = "layernorm",
        pooling: str = "attention_mean_max",
        dropout: float = 0.0,
        top_k: int = 4,
        lse_temperature: float = 1.0,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("SpnNibbleConvPairSet input_bits must be a multiple of pair_bits")
        if pair_bits % nibble_bits != 0:
            raise ValueError("SpnNibbleConvPairSet pair_bits must be a multiple of nibble_bits")
        if conv_depth < 1:
            raise ValueError("SpnNibbleConvPairSet conv_depth must be >= 1")
        if kernel_size < 1 or kernel_size % 2 == 0:
            raise ValueError("SpnNibbleConvPairSet kernel_size must be a positive odd integer")
        if pooling not in {"attention", "attention_mean_max", "mean_max", "gated_attention", "topk_mean", "logsumexp", "topk_logsumexp"}:
            raise ValueError(f"unsupported pooling: {pooling}")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.structure = "SPN"
        self.nibble_bits = nibble_bits
        self.nibbles_per_pair = pair_bits // nibble_bits
        self.nibble_embed_dim = nibble_embed_dim or max(16, base_channels * 2)
        self.conv_depth = conv_depth
        self.kernel_size = kernel_size
        self.activation = activation
        self.norm = norm
        self.pooling = pooling
        self.dropout = dropout
        self.top_k = top_k
        self.lse_temperature = lse_temperature

        self.nibble_encoder = nn.Sequential(
            nn.Linear(nibble_bits, self.nibble_embed_dim),
            build_activation(activation),
            build_norm(norm, self.nibble_embed_dim),
        )
        conv_blocks: list[nn.Module] = []
        for _ in range(conv_depth):
            conv_blocks.append(
                nn.Sequential(
                    nn.Conv1d(
                        self.nibble_embed_dim,
                        self.nibble_embed_dim,
                        kernel_size=kernel_size,
                        padding=kernel_size // 2,
                    ),
                    build_activation(activation),
                    nn.Dropout(dropout),
                    nn.Conv1d(
                        self.nibble_embed_dim,
                        self.nibble_embed_dim,
                        kernel_size=1,
                    ),
                )
            )
        self.conv_blocks = nn.ModuleList(conv_blocks)
        self.sequence_norm = build_norm(norm, self.nibble_embed_dim)
        self.pair_embedding_bits = self.nibble_embed_dim * 3
        self.pair_projection = nn.Sequential(
            nn.Linear(self.pair_embedding_bits, max(64, base_channels * 8)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 8), max(32, base_channels * 4)),
            build_activation(activation),
        )
        self.projected_pair_embedding_bits = max(32, base_channels * 4)
        if pooling == "gated_attention":
            self.attention = GatedAttentionPooling(
                self.projected_pair_embedding_bits,
                hidden_bits=max(32, base_channels * 4),
            )
        elif pooling in {"topk_mean", "logsumexp", "topk_logsumexp"}:
            self.attention = EvidencePooling(
                self.projected_pair_embedding_bits,
                hidden_bits=max(32, base_channels * 4),
                mode=pooling,
                top_k=top_k,
                lse_temperature=lse_temperature,
                activation=activation,
                norm=norm,
            )
        else:
            self.attention = AttentionPooling(
                self.projected_pair_embedding_bits,
                hidden_bits=max(32, base_channels * 4),
                activation=activation,
                norm=norm,
            )
        pooling_multiplier = 3 if pooling == "attention_mean_max" else 2 if pooling == "mean_max" else 1
        self.classifier = nn.Sequential(
            build_norm(norm, self.projected_pair_embedding_bits * pooling_multiplier),
            nn.Linear(self.projected_pair_embedding_bits * pooling_multiplier, 256),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            build_activation(activation),
            nn.Linear(128, 1),
        )
        self.last_attention_weights: torch.Tensor | None = None

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _encode_pairs(self, pair_features: torch.Tensor) -> torch.Tensor:
        nibbles = pair_features.reshape(
            pair_features.shape[0],
            self.nibbles_per_pair,
            self.nibble_bits,
        )
        hidden = self.nibble_encoder(nibbles)
        for block in self.conv_blocks:
            residual = hidden
            conv_hidden = block(hidden.transpose(1, 2)).transpose(1, 2)
            hidden = self.sequence_norm(residual + conv_hidden)
        mean_embedding = hidden.mean(dim=1)
        max_embedding = hidden.max(dim=1).values
        first_last_delta = hidden[:, -1, :] - hidden[:, 0, :]
        pair_embedding = torch.cat([mean_embedding, max_embedding, first_last_delta], dim=1)
        return self.pair_projection(pair_embedding)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.float().reshape(
            features.shape[0] * self.pairs_per_sample,
            self.pair_bits,
        )
        pair_embeddings = self._encode_pairs(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.projected_pair_embedding_bits,
        )
        attention_embedding, attention_weights = self.attention(pair_embeddings)
        self.last_attention_weights = attention_weights.detach()
        mean_embedding = pair_embeddings.mean(dim=1)
        max_embedding = pair_embeddings.max(dim=1).values
        if self.pooling in {"attention", "gated_attention", "topk_mean", "logsumexp", "topk_logsumexp"}:
            pooled = attention_embedding
        elif self.pooling == "mean_max":
            pooled = torch.cat([mean_embedding, max_embedding], dim=1)
        else:
            pooled = torch.cat([attention_embedding, mean_embedding, max_embedding], dim=1)
        return self.classifier(pooled)


class SpnTokenMixerBlock(nn.Module):
    def __init__(
        self,
        nibbles_per_pair: int,
        token_dim: int,
        token_mlp_ratio: int = 2,
        activation: str = "gelu",
        norm: str = "layernorm",
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        if token_mlp_ratio < 1:
            raise ValueError("SpnTokenMixerBlock token_mlp_ratio must be >= 1")
        token_hidden = max(nibbles_per_pair, nibbles_per_pair * token_mlp_ratio)
        channel_hidden = max(token_dim, token_dim * token_mlp_ratio)
        self.token_norm = build_norm(norm, token_dim)
        self.token_mixer = nn.Sequential(
            nn.Linear(nibbles_per_pair, token_hidden),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(token_hidden, nibbles_per_pair),
        )
        self.channel_norm = build_norm(norm, token_dim)
        self.channel_mixer = nn.Sequential(
            nn.Linear(token_dim, channel_hidden),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(channel_hidden, token_dim),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        token_hidden = self.token_norm(features).transpose(1, 2)
        features = features + self.token_mixer(token_hidden).transpose(1, 2)
        features = features + self.channel_mixer(self.channel_norm(features))
        return features


class SpnTokenMixerPairSetDistinguisher(nn.Module):
    """SPN pair-set expert with position-preserving nibble token mixing.

    PRESENT-like SPN ciphers combine local 4-bit S-box substitution with a
    position permutation layer.  This expert therefore encodes each nibble as a
    token, adds a learned position embedding, mixes across token positions, and
    only then aggregates multiple ciphertext pairs.
    """

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 192,
        base_channels: int = 32,
        nibble_bits: int = 4,
        token_dim: int | None = None,
        mixer_depth: int = 3,
        token_mlp_ratio: int = 2,
        activation: str = "gelu",
        norm: str = "layernorm",
        pooling: str = "attention_mean_max",
        dropout: float = 0.0,
        top_k: int = 4,
        lse_temperature: float = 1.0,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("SpnTokenMixerPairSet input_bits must be a multiple of pair_bits")
        if pair_bits % nibble_bits != 0:
            raise ValueError("SpnTokenMixerPairSet pair_bits must be a multiple of nibble_bits")
        if mixer_depth < 1:
            raise ValueError("SpnTokenMixerPairSet mixer_depth must be >= 1")
        if token_mlp_ratio < 1:
            raise ValueError("SpnTokenMixerPairSet token_mlp_ratio must be >= 1")
        if pooling not in {"attention", "attention_mean_max", "mean_max", "gated_attention", "topk_mean", "logsumexp", "topk_logsumexp"}:
            raise ValueError(f"unsupported pooling: {pooling}")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.structure = "SPN"
        self.nibble_bits = nibble_bits
        self.nibbles_per_pair = pair_bits // nibble_bits
        self.token_dim = token_dim or max(16, base_channels * 2)
        self.mixer_depth = mixer_depth
        self.token_mlp_ratio = token_mlp_ratio
        self.activation = activation
        self.norm = norm
        self.pooling = pooling
        self.dropout = dropout
        self.top_k = top_k
        self.lse_temperature = lse_temperature

        self.nibble_encoder = nn.Sequential(
            nn.Linear(nibble_bits, self.token_dim),
            build_activation(activation),
            build_norm(norm, self.token_dim),
        )
        self.position_embedding = nn.Parameter(
            torch.zeros(1, self.nibbles_per_pair, self.token_dim)
        )
        nn.init.trunc_normal_(self.position_embedding, std=0.02)
        self.mixer_blocks = nn.ModuleList(
            [
                SpnTokenMixerBlock(
                    nibbles_per_pair=self.nibbles_per_pair,
                    token_dim=self.token_dim,
                    token_mlp_ratio=token_mlp_ratio,
                    activation=activation,
                    norm=norm,
                    dropout=dropout,
                )
                for _ in range(mixer_depth)
            ]
        )
        self.sequence_norm = build_norm(norm, self.token_dim)
        self.pair_embedding_bits = self.token_dim * 4
        projected_bits = max(32, base_channels * 4)
        self.pair_projection = nn.Sequential(
            nn.Linear(self.pair_embedding_bits, max(64, base_channels * 8)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 8), projected_bits),
            build_activation(activation),
        )
        self.projected_pair_embedding_bits = projected_bits
        if pooling == "gated_attention":
            self.attention = GatedAttentionPooling(
                projected_bits,
                hidden_bits=max(32, base_channels * 4),
            )
        elif pooling in {"topk_mean", "logsumexp", "topk_logsumexp"}:
            self.attention = EvidencePooling(
                projected_bits,
                hidden_bits=max(32, base_channels * 4),
                mode=pooling,
                top_k=top_k,
                lse_temperature=lse_temperature,
                activation=activation,
                norm=norm,
            )
        else:
            self.attention = AttentionPooling(
                projected_bits,
                hidden_bits=max(32, base_channels * 4),
                activation=activation,
                norm=norm,
            )
        pooling_multiplier = 3 if pooling == "attention_mean_max" else 2 if pooling == "mean_max" else 1
        self.classifier = nn.Sequential(
            build_norm(norm, projected_bits * pooling_multiplier),
            nn.Linear(projected_bits * pooling_multiplier, 256),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            build_activation(activation),
            nn.Linear(128, 1),
        )
        self.last_attention_weights: torch.Tensor | None = None

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _encode_pairs(self, pair_features: torch.Tensor) -> torch.Tensor:
        nibbles = pair_features.reshape(
            pair_features.shape[0],
            self.nibbles_per_pair,
            self.nibble_bits,
        )
        hidden = self.nibble_encoder(nibbles) + self.position_embedding
        for block in self.mixer_blocks:
            hidden = block(hidden)
        hidden = self.sequence_norm(hidden)
        mean_embedding = hidden.mean(dim=1)
        max_embedding = hidden.max(dim=1).values
        first_last_delta = hidden[:, -1, :] - hidden[:, 0, :]
        active_embedding = torch.sum(hidden * nibbles.mean(dim=2, keepdim=True), dim=1) / (
            nibbles.mean(dim=2, keepdim=True).sum(dim=1).clamp_min(1.0)
        )
        pair_embedding = torch.cat(
            [mean_embedding, max_embedding, first_last_delta, active_embedding],
            dim=1,
        )
        return self.pair_projection(pair_embedding)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.float().reshape(
            features.shape[0] * self.pairs_per_sample,
            self.pair_bits,
        )
        pair_embeddings = self._encode_pairs(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.projected_pair_embedding_bits,
        )
        attention_embedding, attention_weights = self.attention(pair_embeddings)
        self.last_attention_weights = attention_weights.detach()
        mean_embedding = pair_embeddings.mean(dim=1)
        max_embedding = pair_embeddings.max(dim=1).values
        if self.pooling in {"attention", "gated_attention", "topk_mean", "logsumexp", "topk_logsumexp"}:
            pooled = attention_embedding
        elif self.pooling == "mean_max":
            pooled = torch.cat([mean_embedding, max_embedding], dim=1)
        else:
            pooled = torch.cat([attention_embedding, mean_embedding, max_embedding], dim=1)
        return self.classifier(pooled)



def _present_nibble_adjacency_indices() -> list[list[int]]:
    groups: list[list[int]] = []
    inverse_multiplier = pow(16, -1, 63)
    for token_index in range(16):
        output_nibble = 15 - token_index
        source_tokens = set()
        for output_bit in range(output_nibble * 4, output_nibble * 4 + 4):
            source_bit = 63 if output_bit == 63 else inverse_multiplier * output_bit % 63
            source_tokens.add(15 - (source_bit // 4))
        groups.append(sorted(source_tokens))
    return groups


class PresentPLayerMixerBlock(nn.Module):
    """PRESENT-specific token mixer using public P-layer nibble adjacency."""

    def __init__(
        self,
        words_per_pair: int,
        token_dim: int,
        token_mlp_ratio: int = 2,
        activation: str = "gelu",
        norm: str = "layernorm",
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        if token_mlp_ratio < 1:
            raise ValueError("PresentPLayerMixerBlock token_mlp_ratio must be >= 1")
        self.words_per_pair = words_per_pair
        self.token_dim = token_dim
        adjacency = _present_nibble_adjacency_indices()
        self.register_buffer(
            "p_sources",
            torch.tensor(adjacency, dtype=torch.long),
            persistent=False,
        )
        inverse: list[list[int]] = [[] for _ in range(16)]
        for target, sources in enumerate(adjacency):
            for source in sources:
                inverse[source].append(target)
        max_inverse = max(len(items) for items in inverse)
        inverse_padded = [items + [items[-1]] * (max_inverse - len(items)) for items in inverse]
        self.register_buffer(
            "p_targets",
            torch.tensor(inverse_padded, dtype=torch.long),
            persistent=False,
        )
        channel_hidden = max(token_dim, token_dim * token_mlp_ratio)
        self.local_norm = build_norm(norm, token_dim)
        self.local_mlp = nn.Sequential(
            nn.Linear(token_dim, channel_hidden),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(channel_hidden, token_dim),
        )
        self.message_norm = build_norm(norm, token_dim * 3)
        self.message_mlp = nn.Sequential(
            nn.Linear(token_dim * 3, channel_hidden),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(channel_hidden, token_dim),
        )
        self.channel_norm = build_norm(norm, token_dim)
        self.channel_mlp = nn.Sequential(
            nn.Linear(token_dim, channel_hidden),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(channel_hidden, token_dim),
        )

    def _gather_by_nibble(self, hidden: torch.Tensor, indices: torch.Tensor) -> torch.Tensor:
        batch, tokens, channels = hidden.shape
        by_word = hidden.reshape(batch, self.words_per_pair, 16, channels)
        flat_indices = indices.reshape(-1)
        gathered = by_word.index_select(dim=2, index=flat_indices).reshape(
            batch,
            self.words_per_pair,
            indices.shape[0],
            indices.shape[1],
            channels,
        )
        return gathered.mean(dim=3).reshape(batch, tokens, channels)

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        hidden = hidden + self.local_mlp(self.local_norm(hidden))
        p_message = self._gather_by_nibble(hidden, self.p_sources)
        invp_message = self._gather_by_nibble(hidden, self.p_targets)
        message_input = torch.cat([hidden, p_message, invp_message], dim=-1)
        hidden = hidden + self.message_mlp(self.message_norm(message_input))
        hidden = hidden + self.channel_mlp(self.channel_norm(hidden))
        return hidden


class PresentPLayerMixerPairSetDistinguisher(nn.Module):
    """PRESENT-specific pair-set model with public P-layer message passing."""

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 128,
        base_channels: int = 32,
        nibble_bits: int = 4,
        token_dim: int | None = None,
        mixer_depth: int = 3,
        token_mlp_ratio: int = 2,
        activation: str = "gelu",
        norm: str = "layernorm",
        pooling: str = "topk_logsumexp",
        dropout: float = 0.0,
        top_k: int = 4,
        lse_temperature: float = 1.0,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("PresentPLayerMixerPairSet input_bits must be a multiple of pair_bits")
        if pair_bits % 64 != 0:
            raise ValueError("PresentPLayerMixerPairSet currently requires 64-bit PRESENT word groups")
        if pair_bits % nibble_bits != 0:
            raise ValueError("PresentPLayerMixerPairSet pair_bits must be a multiple of nibble_bits")
        if mixer_depth < 1:
            raise ValueError("PresentPLayerMixerPairSet mixer_depth must be >= 1")
        if pooling not in {"attention", "attention_mean_max", "mean_max", "gated_attention", "topk_mean", "logsumexp", "topk_logsumexp"}:
            raise ValueError(f"unsupported pooling: {pooling}")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.structure = "SPN"
        self.nibble_bits = nibble_bits
        self.words_per_pair = pair_bits // 64
        self.nibbles_per_pair = pair_bits // nibble_bits
        self.token_dim = token_dim or max(16, base_channels * 2)
        self.mixer_depth = mixer_depth
        self.token_mlp_ratio = token_mlp_ratio
        self.activation = activation
        self.norm = norm
        self.pooling = pooling
        self.dropout = dropout
        self.top_k = top_k
        self.lse_temperature = lse_temperature

        self.nibble_encoder = nn.Sequential(
            nn.Linear(nibble_bits, self.token_dim),
            build_activation(activation),
            build_norm(norm, self.token_dim),
        )
        self.word_embedding = nn.Parameter(torch.zeros(1, self.words_per_pair, 1, self.token_dim))
        self.nibble_embedding = nn.Parameter(torch.zeros(1, 1, 16, self.token_dim))
        nn.init.trunc_normal_(self.word_embedding, std=0.02)
        nn.init.trunc_normal_(self.nibble_embedding, std=0.02)
        self.mixer_blocks = nn.ModuleList(
            [
                PresentPLayerMixerBlock(
                    words_per_pair=self.words_per_pair,
                    token_dim=self.token_dim,
                    token_mlp_ratio=token_mlp_ratio,
                    activation=activation,
                    norm=norm,
                    dropout=dropout,
                )
                for _ in range(mixer_depth)
            ]
        )
        self.sequence_norm = build_norm(norm, self.token_dim)
        self.pair_embedding_bits = self.token_dim * 4
        projected_bits = max(32, base_channels * 4)
        self.pair_projection = nn.Sequential(
            nn.Linear(self.pair_embedding_bits, max(64, base_channels * 8)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 8), projected_bits),
            build_activation(activation),
        )
        self.projected_pair_embedding_bits = projected_bits
        if pooling == "gated_attention":
            self.attention = GatedAttentionPooling(projected_bits, hidden_bits=max(32, base_channels * 4))
        elif pooling in {"topk_mean", "logsumexp", "topk_logsumexp"}:
            self.attention = EvidencePooling(
                projected_bits,
                hidden_bits=max(32, base_channels * 4),
                mode=pooling,
                top_k=top_k,
                lse_temperature=lse_temperature,
                activation=activation,
                norm=norm,
            )
        else:
            self.attention = AttentionPooling(
                projected_bits,
                hidden_bits=max(32, base_channels * 4),
                activation=activation,
                norm=norm,
            )
        pooling_multiplier = 3 if pooling == "attention_mean_max" else 2 if pooling == "mean_max" else 1
        self.classifier = nn.Sequential(
            build_norm(norm, projected_bits * pooling_multiplier),
            nn.Linear(projected_bits * pooling_multiplier, 256),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            build_activation(activation),
            nn.Linear(128, 1),
        )
        self.last_attention_weights: torch.Tensor | None = None

    @staticmethod
    def present_bit_to_input_position(bit_index: int, width: int = 64) -> int:
        if bit_index < 0 or bit_index >= width:
            raise ValueError("bit_index out of PRESENT block range")
        return width - 1 - bit_index

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _encode_pairs(self, pair_features: torch.Tensor) -> torch.Tensor:
        nibbles = pair_features.reshape(pair_features.shape[0], self.words_per_pair, 16, self.nibble_bits)
        hidden = self.nibble_encoder(nibbles) + self.word_embedding + self.nibble_embedding
        hidden = hidden.reshape(pair_features.shape[0], self.nibbles_per_pair, self.token_dim)
        for block in self.mixer_blocks:
            hidden = block(hidden)
        hidden = self.sequence_norm(hidden)
        mean_embedding = hidden.mean(dim=1)
        max_embedding = hidden.max(dim=1).values
        first_last_delta = hidden[:, -1, :] - hidden[:, 0, :]
        active_weights = nibbles.reshape(pair_features.shape[0], self.nibbles_per_pair, self.nibble_bits).mean(dim=2, keepdim=True)
        active_embedding = torch.sum(hidden * active_weights, dim=1) / active_weights.sum(dim=1).clamp_min(1.0)
        pair_embedding = torch.cat([mean_embedding, max_embedding, first_last_delta, active_embedding], dim=1)
        return self.pair_projection(pair_embedding)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.float().reshape(features.shape[0] * self.pairs_per_sample, self.pair_bits)
        pair_embeddings = self._encode_pairs(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.projected_pair_embedding_bits,
        )
        attention_embedding, attention_weights = self.attention(pair_embeddings)
        self.last_attention_weights = attention_weights.detach()
        mean_embedding = pair_embeddings.mean(dim=1)
        max_embedding = pair_embeddings.max(dim=1).values
        if self.pooling in {"attention", "gated_attention", "topk_mean", "logsumexp", "topk_logsumexp"}:
            pooled = attention_embedding
        elif self.pooling == "mean_max":
            pooled = torch.cat([mean_embedding, max_embedding], dim=1)
        else:
            pooled = torch.cat([attention_embedding, mean_embedding, max_embedding], dim=1)
        return self.classifier(pooled)
