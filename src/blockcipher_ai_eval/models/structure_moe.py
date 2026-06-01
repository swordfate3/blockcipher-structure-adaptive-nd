from __future__ import annotations

from typing import Any

import torch
from torch import nn

from blockcipher_ai_eval.models.cnn import CnnDistinguisher
from blockcipher_ai_eval.models.dbitnet import DBitNetDistinguisher
from blockcipher_ai_eval.models.mlp import MlpDistinguisher
from blockcipher_ai_eval.models.resnet_bitslice import ResNetBitSliceDistinguisher


EXPERT_KEYS = (
    "resnet_bitslice",
    "dbitnet_dilated_cnn",
    "cnn",
    "mlp",
)

HARD_GATE_WEIGHTS = {
    "ARX": (0.55, 0.30, 0.10, 0.05),
    "SPN": (0.10, 0.45, 0.40, 0.05),
    "Feistel-like": (0.30, 0.50, 0.15, 0.05),
}


class StructureAwareMoEDistinguisher(nn.Module):
    def __init__(
        self,
        input_bits: int,
        hidden_bits: int,
        structure_feature_bits: int,
        gate_mode: str,
    ) -> None:
        super().__init__()
        if gate_mode not in {"uniform", "hard", "soft"}:
            raise ValueError(f"unsupported gate_mode: {gate_mode}")
        self.input_bits = input_bits
        self.hidden_bits = hidden_bits
        self.structure_feature_bits = structure_feature_bits
        self.gate_mode = gate_mode
        self.experts = nn.ModuleList(
            [
                ResNetBitSliceDistinguisher(input_bits=input_bits, channels=hidden_bits),
                DBitNetDistinguisher(input_bits=input_bits, channels=hidden_bits),
                CnnDistinguisher(input_bits=input_bits, channels=hidden_bits),
                MlpDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits),
            ]
        )
        self.soft_gate = nn.Sequential(
            nn.Linear(structure_feature_bits, hidden_bits),
            nn.ReLU(),
            nn.Linear(hidden_bits, len(EXPERT_KEYS)),
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
                (batch_size, len(EXPERT_KEYS)),
                1.0 / len(EXPERT_KEYS),
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
            **{
                f"gate_weight_{key}": round(float(weight), 6)
                for key, weight in zip(EXPERT_KEYS, weights)
            },
        }

    def _hard_weights_from_structure(self) -> tuple[float, float, float, float]:
        is_arx = bool(self._structure_features[0].item())
        is_spn = bool(self._structure_features[1].item())
        is_feistel_like = bool(self._structure_features[2].item())
        if is_arx:
            return HARD_GATE_WEIGHTS["ARX"]
        if is_spn:
            return HARD_GATE_WEIGHTS["SPN"]
        if is_feistel_like:
            return HARD_GATE_WEIGHTS["Feistel-like"]
        return (0.25, 0.25, 0.25, 0.25)
