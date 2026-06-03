from __future__ import annotations

import math

import torch
from torch import nn


def adaptive_dbitnet_dilations(input_bits: int) -> list[int]:
    if input_bits % 2 != 0:
        raise ValueError("AdaptiveDBitNet requires an even number of input bits")
    if input_bits < 16:
        raise ValueError("AdaptiveDBitNet requires at least 16 input bits")

    rates: list[int] = []
    dilation = input_bits // 2 - 1
    while dilation >= 3:
        rates.append(dilation)
        dilation = (dilation + 1) // 2 - 1
    return rates


class AdaptiveDBitNetBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, dilation: int) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv1d(
                in_channels,
                out_channels,
                kernel_size=2,
                dilation=dilation,
                padding=0,
            ),
            nn.BatchNorm1d(out_channels),
            nn.ReLU(),
            nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_channels),
            nn.ReLU(),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.layers(features)


class AdaptiveDBitNetEncoder(nn.Module):
    def __init__(self, input_bits: int, base_channels: int = 32) -> None:
        super().__init__()
        if input_bits % 2 != 0:
            raise ValueError("AdaptiveDBitNet requires an even number of input bits")
        if input_bits < 16:
            raise ValueError("AdaptiveDBitNet requires at least 16 input bits")
        self.input_bits = input_bits
        self.dilations = adaptive_dbitnet_dilations(input_bits)
        self.output_width = self._output_width(input_bits, self.dilations)
        self.output_channels = base_channels + (len(self.dilations) - 1) * 16
        self.embedding_bits = self.output_channels * self.output_width

        in_channels = 1
        blocks: list[nn.Module] = []
        for index, dilation in enumerate(self.dilations):
            out_channels = base_channels + index * 16
            blocks.append(AdaptiveDBitNetBlock(in_channels, out_channels, dilation))
            in_channels = out_channels
        self.features = nn.Sequential(*blocks)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        hidden = features.float().unsqueeze(1)
        hidden = self.features(hidden)
        return hidden.flatten(start_dim=1)

    @staticmethod
    def _output_width(input_bits: int, dilations: list[int]) -> int:
        width = input_bits
        for dilation in dilations:
            width -= dilation
            if width <= 0:
                raise ValueError(
                    "AdaptiveDBitNet dilation schedule collapsed the feature width"
                )
        return width


class AdaptiveDBitNetDistinguisher(nn.Module):
    """Input-size adaptive DBitNet-style dilated CNN.

    This follows the DBitNet idea of deriving long-range dilation rates from the
    input width, then using a fixed strong prediction head across input sizes.
    """

    def __init__(self, input_bits: int, base_channels: int = 32) -> None:
        super().__init__()
        self.encoder = AdaptiveDBitNetEncoder(input_bits, base_channels)
        self.input_bits = self.encoder.input_bits
        self.dilations = self.encoder.dilations
        self.output_width = self.encoder.output_width
        self.output_channels = self.encoder.output_channels
        self.classifier = nn.Sequential(
            nn.Linear(self.encoder.embedding_bits, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.encoder(features))


class PairwiseAdaptiveDBitNetDistinguisher(nn.Module):
    """Shared pair encoder plus cross-pair pooling for multi-pair inputs."""

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 96,
        base_channels: int = 32,
        pooling: str = "mean_max",
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("PairwiseAdaptiveDBitNet input_bits must be a multiple of pair_bits")
        if pooling not in {"mean", "max", "mean_max"}:
            raise ValueError(f"unsupported pooling: {pooling}")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pooling = pooling
        self.pairs_per_sample = input_bits // pair_bits
        self.encoder = AdaptiveDBitNetEncoder(pair_bits, base_channels)
        pooling_multiplier = 2 if pooling == "mean_max" else 1
        self.classifier = nn.Sequential(
            nn.Linear(self.encoder.embedding_bits * pooling_multiplier, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.float().reshape(
            features.shape[0] * self.pairs_per_sample,
            self.pair_bits,
        )
        embeddings = self.encoder(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.encoder.embedding_bits,
        )
        mean_embedding = embeddings.mean(dim=1)
        max_embedding = embeddings.max(dim=1).values
        if self.pooling == "mean":
            pooled = mean_embedding
        elif self.pooling == "max":
            pooled = max_embedding
        else:
            pooled = torch.cat([mean_embedding, max_embedding], dim=1)
        return self.classifier(pooled)
