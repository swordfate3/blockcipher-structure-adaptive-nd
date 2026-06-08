from __future__ import annotations

from typing import Callable

import torch
from torch import nn


class Identity(nn.Module):
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return features


class RmsNorm(nn.Module):
    def __init__(self, normalized_shape: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(normalized_shape))
        self.eps = eps

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        rms = features.pow(2).mean(dim=-1, keepdim=True).add(self.eps).sqrt()
        return features / rms * self.weight


def build_activation(name: str) -> nn.Module:
    key = name.lower()
    if key == "relu":
        return nn.ReLU()
    if key == "gelu":
        return nn.GELU()
    if key == "silu":
        return nn.SiLU()
    if key == "mish":
        return nn.Mish()
    raise ValueError(f"unsupported activation: {name}")


def build_norm(name: str, normalized_shape: int) -> nn.Module:
    key = name.lower()
    if key in {"none", "identity"}:
        return Identity()
    if key == "layernorm":
        return nn.LayerNorm(normalized_shape)
    if key == "rmsnorm":
        return RmsNorm(normalized_shape)
    raise ValueError(f"unsupported norm: {name}")


class GatedAttentionPooling(nn.Module):
    """Attention pooling with a tanh/sigmoid gate, common in MIL models."""

    def __init__(self, embedding_bits: int, hidden_bits: int = 128) -> None:
        super().__init__()
        self.value = nn.Linear(embedding_bits, hidden_bits)
        self.gate = nn.Linear(embedding_bits, hidden_bits)
        self.score = nn.Linear(hidden_bits, 1)

    def forward(self, embeddings: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if embeddings.ndim != 3:
            raise ValueError(f"expected [batch, items, embedding], got {tuple(embeddings.shape)}")
        hidden = torch.tanh(self.value(embeddings)) * torch.sigmoid(self.gate(embeddings))
        logits = self.score(hidden).squeeze(-1)
        weights = torch.softmax(logits, dim=1)
        pooled = torch.sum(embeddings * weights.unsqueeze(-1), dim=1)
        return pooled, weights


class AttentionPooling(nn.Module):
    def __init__(
        self,
        embedding_bits: int,
        hidden_bits: int = 128,
        activation: str = "gelu",
        norm: str = "layernorm",
    ) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            build_norm(norm, embedding_bits),
            nn.Linear(embedding_bits, hidden_bits),
            build_activation(activation),
            nn.Linear(hidden_bits, 1),
        )

    def forward(self, embeddings: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        logits = self.layers(embeddings).squeeze(-1)
        weights = torch.softmax(logits, dim=1)
        pooled = torch.sum(embeddings * weights.unsqueeze(-1), dim=1)
        return pooled, weights
