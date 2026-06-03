from __future__ import annotations

from torch import nn

from blockcipher_ai_eval.ciphers import (
    Aes128,
    Aes192,
    Aes256,
    Present80,
    ReducedRoundCipher,
    Simon64_128,
    Sm4Reduced,
    Speck32_64,
)
from blockcipher_ai_eval.models import (
    AdaptiveDBitNetDistinguisher,
    CnnDistinguisher,
    DBitNetDistinguisher,
    GohrSpeckDistinguisher,
    LstmRoundSeqDistinguisher,
    MlpDistinguisher,
    MultiScaleDenseResNetDistinguisher,
    PairwiseAdaptiveDBitNetDistinguisher,
    ResNetBitSliceDistinguisher,
    SeResNeXtDistinguisher,
    StructureAwareMoEDistinguisher,
    TransformerEncoderDistinguisher,
)
from blockcipher_ai_eval.structure_features import STRUCTURE_FEATURE_NAMES


def build_cipher(name: str, rounds: int) -> ReducedRoundCipher:
    if name == "aes128":
        return Aes128(rounds=rounds, key=0x000102030405060708090A0B0C0D0E0F)
    if name == "aes192":
        return Aes192(rounds=rounds, key=0x000102030405060708090A0B0C0D0E0F1011121314151617)
    if name == "aes256":
        return Aes256(
            rounds=rounds,
            key=0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F,
        )
    if name == "speck32":
        return Speck32_64(rounds=rounds, key=0x1918111009080100)
    if name == "simon64":
        return Simon64_128(rounds=rounds, key=0x1B1A1918131211100B0A090803020100)
    if name == "present80":
        return Present80(rounds=rounds, key=0x00000000000000000000)
    if name == "sm4":
        return Sm4Reduced(rounds=rounds, key=0x0123456789ABCDEFFEDCBA9876543210)
    raise ValueError(f"unsupported cipher: {name}")


def default_difference(name: str) -> int:
    if name in {"aes128", "aes192", "aes256"}:
        return 0x00000000000000000000000000000040
    if name == "speck32":
        return 0x0040
    if name == "simon64":
        return 0x0000000000000040
    if name == "present80":
        return 0x0000000000000040
    if name == "sm4":
        return 0x00000000000000000000000000000040
    raise ValueError(f"unsupported cipher: {name}")


def build_model(
    name: str,
    input_bits: int,
    hidden_bits: int,
    pair_bits: int | None = None,
) -> nn.Module:
    if name == "mlp":
        return MlpDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits)
    if name == "cnn":
        return CnnDistinguisher(input_bits=input_bits, channels=hidden_bits)
    if name == "resnet_bitslice":
        return ResNetBitSliceDistinguisher(input_bits=input_bits, channels=hidden_bits)
    if name == "dbitnet_dilated_cnn":
        return DBitNetDistinguisher(input_bits=input_bits, channels=hidden_bits)
    if name == "adaptive_dbitnet":
        return AdaptiveDBitNetDistinguisher(input_bits=input_bits, base_channels=hidden_bits)
    pairwise_pooling_keys = {
        "adaptive_dbitnet_pairwise": "mean_max",
        "adaptive_dbitnet_pairwise_mean": "mean",
        "adaptive_dbitnet_pairwise_max": "max",
        "adaptive_dbitnet_pairwise_mean_max": "mean_max",
    }
    if name in pairwise_pooling_keys:
        return PairwiseAdaptiveDBitNetDistinguisher(
            input_bits=input_bits,
            pair_bits=pair_bits or 96,
            base_channels=hidden_bits,
            pooling=pairwise_pooling_keys[name],
        )
    if name == "gohr_resnet_speck":
        return GohrSpeckDistinguisher(input_bits=input_bits, filters=hidden_bits)
    if name == "gohr_resnet_speck_depth10":
        return GohrSpeckDistinguisher(input_bits=input_bits, filters=hidden_bits, blocks=10)
    if name == "senet_resnext":
        return SeResNeXtDistinguisher(input_bits=input_bits, channels=hidden_bits)
    if name == "multiscale_dense_resnet":
        return MultiScaleDenseResNetDistinguisher(
            input_bits=input_bits,
            channels=hidden_bits,
        )
    if name == "lstm_roundseq":
        return LstmRoundSeqDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits)
    if name == "transformer_encoder":
        return TransformerEncoderDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits)
    if name == "moe_uniform":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="uniform",
        )
    if name == "moe_hard":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="hard",
        )
    if name == "moe_soft":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
        )
    if name == "moe_v2_uniform":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="uniform",
            expert_set="v2_adaptive",
        )
    if name == "moe_v2_hard":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="hard",
            expert_set="v2_adaptive",
        )
    if name == "moe_v2_soft":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
            expert_set="v2_adaptive",
        )
    if name == "moe_v3_uniform":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="uniform",
            expert_set="v3_pairwise",
            pair_bits=pair_bits,
        )
    if name == "moe_v3_hard":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="hard",
            expert_set="v3_pairwise",
            pair_bits=pair_bits,
        )
    if name == "moe_v3_soft":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
            expert_set="v3_pairwise",
            pair_bits=pair_bits,
        )
    raise ValueError(f"unsupported model: {name}")
