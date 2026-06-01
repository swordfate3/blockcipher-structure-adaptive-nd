from __future__ import annotations

from torch import nn

from blockcipher_ai_eval.ciphers import Present80, ReducedRoundCipher, Sm4Reduced, Speck32_64
from blockcipher_ai_eval.models import CnnDistinguisher, MlpDistinguisher


def build_cipher(name: str, rounds: int) -> ReducedRoundCipher:
    if name == "speck32":
        return Speck32_64(rounds=rounds, key=0x1918111009080100)
    if name == "present80":
        return Present80(rounds=rounds, key=0x00000000000000000000)
    if name == "sm4":
        return Sm4Reduced(rounds=rounds, key=0x0123456789ABCDEFFEDCBA9876543210)
    raise ValueError(f"unsupported cipher: {name}")


def default_difference(name: str) -> int:
    if name == "speck32":
        return 0x0040
    if name == "present80":
        return 0x0000000000000040
    if name == "sm4":
        return 0x00000000000000000000000000000040
    raise ValueError(f"unsupported cipher: {name}")


def build_model(name: str, input_bits: int, hidden_bits: int) -> nn.Module:
    if name == "mlp":
        return MlpDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits)
    if name == "cnn":
        return CnnDistinguisher(input_bits=input_bits, channels=hidden_bits)
    raise ValueError(f"unsupported model: {name}")

