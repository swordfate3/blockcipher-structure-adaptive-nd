from __future__ import annotations

from typing import Any

import torch
from torch import nn

from blockcipher_ai_eval.models.adaptive_dbitnet import AdaptiveDBitNetDistinguisher
from blockcipher_ai_eval.models.cnn import CnnDistinguisher
from blockcipher_ai_eval.models.dbitnet import DBitNetDistinguisher
from blockcipher_ai_eval.models.mlp import MlpDistinguisher
from blockcipher_ai_eval.models.multiscale_dense_resnet import (
    MultiScaleDenseResNetDistinguisher,
)
from blockcipher_ai_eval.models.resnet_bitslice import ResNetBitSliceDistinguisher
from blockcipher_ai_eval.models.senet_resnext import SeResNeXtDistinguisher


EXPERT_KEYS = (
    "resnet_bitslice",
    "dbitnet_dilated_cnn",
    "cnn",
    "mlp",
    "senet_resnext",
    "multiscale_dense_resnet",
)

V2_EXPERT_KEYS = (
    "resnet_bitslice",
    "adaptive_dbitnet",
    "cnn",
    "mlp",
    "senet_resnext",
    "multiscale_dense_resnet",
)

HARD_GATE_WEIGHTS = {
    "ARX": (0.35, 0.20, 0.05, 0.05, 0.10, 0.25),
    "SPN": (0.10, 0.30, 0.30, 0.05, 0.20, 0.05),
    "Feistel-like": (0.20, 0.35, 0.10, 0.05, 0.10, 0.20),
}


class StructureAwareMoEDistinguisher(nn.Module):
    def __init__(
        self,
        input_bits: int,
        hidden_bits: int,
        structure_feature_bits: int,
        gate_mode: str,
        expert_set: str = "legacy",
    ) -> None:
        super().__init__()
        if gate_mode not in {"uniform", "hard", "soft"}:
            raise ValueError(f"unsupported gate_mode: {gate_mode}")
        if expert_set not in {"legacy", "v2_adaptive"}:
            raise ValueError(f"unsupported expert_set: {expert_set}")
        self.input_bits = input_bits
        self.hidden_bits = hidden_bits
        self.structure_feature_bits = structure_feature_bits
        self.gate_mode = gate_mode
        self.expert_set = expert_set
        self.expert_keys = V2_EXPERT_KEYS if expert_set == "v2_adaptive" else EXPERT_KEYS
        self.experts = nn.ModuleList(self._build_experts(input_bits, hidden_bits))
        self.soft_gate = nn.Sequential(
            nn.Linear(structure_feature_bits, hidden_bits),
            nn.ReLU(),
            nn.Linear(hidden_bits, len(self.expert_keys)),
        )
        self.register_buffer(
            "_structure_features",
            torch.zeros(structure_feature_bits, dtype=torch.float32),
        )

    def set_structure_features(self, structure_features: torch.Tensor) -> None:
        if structure_features.shape != (self.structure_feature_bits,):
            raise ValueError(
                "structure_features must have shape "
                f"({self.structure_feature_bits},), got {tuple(structure_features.shape)}"
            )
        self._structure_features.copy_(structure_features.detach().to(self._structure_features))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        expert_logits = torch.cat([expert(features) for expert in self.experts], dim=1)
        weights = self.current_gate_weights(batch_size=features.shape[0]).to(features.device)
        return (expert_logits * weights).sum(dim=1, keepdim=True)

    def current_gate_weights(self, batch_size: int) -> torch.Tensor:
        structure = self._structure_features.unsqueeze(0).expand(batch_size, -1)
        if self.gate_mode == "uniform":
            return torch.full(
                (batch_size, len(self.expert_keys)),
                1.0 / len(self.expert_keys),
                dtype=structure.dtype,
                device=structure.device,
            )
        if self.gate_mode == "hard":
            weights = torch.tensor(
                self._hard_weights_from_structure(),
                dtype=structure.dtype,
                device=structure.device,
            )
            return weights.unsqueeze(0).expand(batch_size, -1)
        return torch.softmax(self.soft_gate(structure), dim=1)

    def gate_summary(self) -> dict[str, Any]:
        weights = self.current_gate_weights(batch_size=1).detach().cpu()[0]
        return {
            "gate_mode": self.gate_mode,
            "expert_set": self.expert_set,
            **{
                f"gate_weight_{key}": round(float(weight), 6)
                for key, weight in zip(self.expert_keys, weights)
            },
        }

    def _build_experts(self, input_bits: int, hidden_bits: int) -> list[nn.Module]:
        return [
            ResNetBitSliceDistinguisher(input_bits=input_bits, channels=hidden_bits),
            self._build_dbitnet_expert(input_bits, hidden_bits),
            CnnDistinguisher(input_bits=input_bits, channels=hidden_bits),
            MlpDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits),
            SeResNeXtDistinguisher(input_bits=input_bits, channels=hidden_bits),
            MultiScaleDenseResNetDistinguisher(
                input_bits=input_bits,
                channels=hidden_bits,
            ),
        ]

    def _build_dbitnet_expert(self, input_bits: int, hidden_bits: int) -> nn.Module:
        if self.expert_set == "v2_adaptive":
            return AdaptiveDBitNetDistinguisher(
                input_bits=input_bits,
                base_channels=hidden_bits,
            )
        return DBitNetDistinguisher(input_bits=input_bits, channels=hidden_bits)

    def _hard_weights_from_structure(self) -> tuple[float, ...]:
        is_arx = bool(self._structure_features[0].item())
        is_spn = bool(self._structure_features[1].item())
        is_feistel_like = bool(self._structure_features[2].item())
        if is_arx:
            return HARD_GATE_WEIGHTS["ARX"]
        if is_spn:
            return HARD_GATE_WEIGHTS["SPN"]
        if is_feistel_like:
            return HARD_GATE_WEIGHTS["Feistel-like"]
        return tuple(1.0 / len(self.expert_keys) for _ in self.expert_keys)
