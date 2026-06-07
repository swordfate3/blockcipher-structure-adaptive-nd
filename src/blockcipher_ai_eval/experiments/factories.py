from __future__ import annotations

from torch import nn

from blockcipher_ai_eval.ciphers import (
    Aes128,
    Aes192,
    Aes256,
    Aria128,
    Aria192,
    Aria256,
    Camellia128,
    Camellia192,
    Camellia256,
    Cham64_128,
    Des,
    Gift64,
    Lea128,
    Lea192,
    Lea256,
    Present80,
    ReducedRoundCipher,
    Simeck64_128,
    Simon64_128,
    Sm4Reduced,
    Speck32_64,
    TripleDes,
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
    SpnCellPairSetDBitNetDistinguisher,
    SpnNibbleConvPairSetDistinguisher,
    SpnTokenMixerPairSetDistinguisher,
    StructureAdaptivePairSetDBitNetDistinguisher,
    StructureAwareMoEDistinguisher,
    TransformerEncoderDistinguisher,
)
from blockcipher_ai_eval.structure_features import STRUCTURE_FEATURE_NAMES


MOE_V5_PRESENT_HPO_TRIAL20_OPTIONS = {
    "gate_hidden_bits": 96,
    "gate_activation": "silu",
    "gate_dropout": 0.0,
    "gate_temperature": 1.0,
    "pairwise_pooling": "mean_max",
    "spn_token_dim": 128,
    "spn_mixer_depth": 4,
    "spn_token_mlp_ratio": 2,
    "expert_activation": "gelu",
    "expert_norm": "rmsnorm",
    "spn_pooling": "gated_attention",
    "expert_dropout": 0.05,
}
MOE_V5_PRESENT_HPO_TRIAL20_HIDDEN_BITS = 96
MOE_V5_PRESENT_HPO_MULTISEED_TRIAL11_OPTIONS = {
    "gate_hidden_bits": 32,
    "gate_activation": "relu",
    "gate_dropout": 0.05,
    "gate_temperature": 0.75,
    "pairwise_pooling": "mean",
    "spn_token_dim": 64,
    "spn_mixer_depth": 3,
    "spn_token_mlp_ratio": 3,
    "expert_activation": "silu",
    "expert_norm": "rmsnorm",
    "spn_pooling": "gated_attention",
    "expert_dropout": 0.0,
}
MOE_V5_PRESENT_HPO_MULTISEED_TRIAL11_HIDDEN_BITS = 96


def build_cipher(name: str, rounds: int, key: int | None = None) -> ReducedRoundCipher:
    if name == "aes128":
        return Aes128(rounds=rounds, key=0x000102030405060708090A0B0C0D0E0F)
    if name == "aes192":
        return Aes192(rounds=rounds, key=0x000102030405060708090A0B0C0D0E0F1011121314151617)
    if name == "aes256":
        return Aes256(
            rounds=rounds,
            key=0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F,
        )
    if name == "aria128":
        return Aria128(rounds=rounds, key=0x000102030405060708090A0B0C0D0E0F)
    if name == "aria192":
        return Aria192(rounds=rounds, key=0x000102030405060708090A0B0C0D0E0F1011121314151617)
    if name == "aria256":
        return Aria256(
            rounds=rounds,
            key=0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F,
        )
    if name == "camellia128":
        return Camellia128(rounds=rounds, key=0x0123456789ABCDEFFEDCBA9876543210)
    if name == "camellia192":
        return Camellia192(rounds=rounds, key=0x0123456789ABCDEFFEDCBA98765432100011223344556677)
    if name == "camellia256":
        return Camellia256(
            rounds=rounds,
            key=0x0123456789ABCDEFFEDCBA987654321000112233445566778899AABBCCDDEEFF,
        )
    if name == "des":
        return Des(rounds=rounds, key=0x133457799BBCDFF1)
    if name == "3des":
        return TripleDes(
            rounds=rounds,
            key1=0x0123456789ABCDEF,
            key2=0x23456789ABCDEF01,
            key3=0x456789ABCDEF0123,
        )
    if name == "speck32":
        return Speck32_64(rounds=rounds, key=0x1918111009080100)
    if name == "cham64":
        return Cham64_128(rounds=rounds, key=0x010003020504070609080B0A0D0C0F0E)
    if name == "lea128":
        key = int.from_bytes(bytes.fromhex("0f1e2d3c4b5a69788796a5b4c3d2e1f0"), "little")
        return Lea128(rounds=rounds, key=key)
    if name == "lea192":
        key = int.from_bytes(
            bytes.fromhex("0f1e2d3c4b5a69788796a5b4c3d2e1f0f0e1d2c3b4a59687"),
            "little",
        )
        return Lea192(rounds=rounds, key=key)
    if name == "lea256":
        key = int.from_bytes(
            bytes.fromhex(
                "0f1e2d3c4b5a69788796a5b4c3d2e1f0"
                "f0e1d2c3b4a5968778695a4b3c2d1e0f"
            ),
            "little",
        )
        return Lea256(rounds=rounds, key=key)
    if name == "simon64":
        return Simon64_128(rounds=rounds, key=0x1B1A1918131211100B0A090803020100)
    if name == "simeck64":
        return Simeck64_128(rounds=rounds, key=0x1B1A1918131211100B0A090803020100)
    if name == "present80":
        return Present80(rounds=rounds, key=0x00000000000000000000 if key is None else key)
    if name == "gift64":
        return Gift64(rounds=rounds, key=0x00000000000000000000000000000000)
    if name == "sm4":
        return Sm4Reduced(rounds=rounds, key=0x0123456789ABCDEFFEDCBA9876543210)
    raise ValueError(f"unsupported cipher: {name}")


def default_difference(name: str) -> int:
    if name in {"aes128", "aes192", "aes256", "aria128", "aria192", "aria256", "camellia128", "camellia192", "camellia256", "lea128", "lea192", "lea256"}:
        return 0x00000000000000000000000000000040
    if name in {"des", "3des"}:
        return 0x0000000000000040
    if name == "speck32":
        return 0x0040
    if name == "cham64":
        return 0x0000000000000040
    if name in {"simon64", "simeck64"}:
        return 0x0000000000000040
    if name in {"present80", "gift64"}:
        return 0x0000000000000040
    if name == "sm4":
        return 0x00000000000000000000000000000040
    raise ValueError(f"unsupported cipher: {name}")


def build_model(
    name: str,
    input_bits: int,
    hidden_bits: int,
    pair_bits: int | None = None,
    structure: str = "generic",
    model_options: dict[str, object] | None = None,
) -> nn.Module:
    options = model_options or {}
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
    pairset_pooling_keys = {
        "structure_adaptive_pairset_dbitnet": "attention_mean_max",
        "structure_adaptive_pairset_dbitnet_attention": "attention",
        "structure_adaptive_pairset_dbitnet_mean_max": "mean_max",
    }
    if name in pairset_pooling_keys:
        return StructureAdaptivePairSetDBitNetDistinguisher(
            input_bits=input_bits,
            pair_bits=pair_bits or 96,
            base_channels=hidden_bits,
            structure=structure,
            pooling=pairset_pooling_keys[name],
        )
    if name == "spn_pairset_dbitnet_v2":
        return SpnCellPairSetDBitNetDistinguisher(
            input_bits=input_bits,
            pair_bits=pair_bits or 192,
            base_channels=hidden_bits,
        )
    if name == "spn_nibble_conv_pairset":
        return SpnNibbleConvPairSetDistinguisher(
            input_bits=input_bits,
            pair_bits=pair_bits or 192,
            base_channels=hidden_bits,
            nibble_embed_dim=_int_option(options, "nibble_embed_dim"),
            conv_depth=_int_option(options, "conv_depth", 3),
            kernel_size=_int_option(options, "kernel_size", 3),
            activation=str(options.get("activation", "gelu")),
            norm=str(options.get("norm", "layernorm")),
            pooling=str(options.get("pooling", "attention_mean_max")),
            dropout=float(options.get("dropout", 0.0)),
        )
    if name == "spn_token_mixer_pairset":
        return SpnTokenMixerPairSetDistinguisher(
            input_bits=input_bits,
            pair_bits=pair_bits or 192,
            base_channels=hidden_bits,
            token_dim=_int_option(options, "token_dim"),
            mixer_depth=_int_option(options, "mixer_depth", 3),
            token_mlp_ratio=_int_option(options, "token_mlp_ratio", 2),
            activation=str(options.get("activation", "gelu")),
            norm=str(options.get("norm", "layernorm")),
            pooling=str(options.get("pooling", "attention_mean_max")),
            dropout=float(options.get("dropout", 0.0)),
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
    if name == "moe_v4_uniform":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="uniform",
            expert_set="v4_structure_adapter",
            pair_bits=pair_bits,
        )
    if name == "moe_v4_hard":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="hard",
            expert_set="v4_structure_adapter",
            pair_bits=pair_bits,
        )
    if name == "moe_v4_soft":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
            expert_set="v4_structure_adapter",
            pair_bits=pair_bits,
        )
    if name == "moe_v5_uniform":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="uniform",
            expert_set="v5_structure_experts",
            pair_bits=pair_bits,
            **_moe_v5_options(options),
        )
    if name == "moe_v5_hard":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="hard",
            expert_set="v5_structure_experts",
            pair_bits=pair_bits,
            **_moe_v5_options(options),
        )
    if name == "moe_v5_soft":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
            expert_set="v5_structure_experts",
            pair_bits=pair_bits,
            **_moe_v5_options(options),
        )
    if name == "moe_v5_soft_hpo_present_best":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=MOE_V5_PRESENT_HPO_TRIAL20_HIDDEN_BITS,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
            expert_set="v5_structure_experts",
            pair_bits=pair_bits or 192,
            **MOE_V5_PRESENT_HPO_TRIAL20_OPTIONS,
        )
    if name == "moe_v5_soft_hpo_multiseed_present_best":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=MOE_V5_PRESENT_HPO_MULTISEED_TRIAL11_HIDDEN_BITS,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
            expert_set="v5_structure_experts",
            pair_bits=pair_bits or 192,
            **MOE_V5_PRESENT_HPO_MULTISEED_TRIAL11_OPTIONS,
        )
    raise ValueError(f"unsupported model: {name}")




def _moe_v5_options(options: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    int_keys = {
        "gate_hidden_bits",
        "spn_token_dim",
        "spn_mixer_depth",
        "spn_token_mlp_ratio",
    }
    float_keys = {"gate_dropout", "gate_temperature", "expert_dropout"}
    string_keys = {
        "gate_activation",
        "pairwise_pooling",
        "expert_activation",
        "expert_norm",
        "spn_pooling",
    }
    aliases = {
        "token_dim": "spn_token_dim",
        "mixer_depth": "spn_mixer_depth",
        "pooling": "spn_pooling",
        "dropout": "expert_dropout",
    }
    expanded_options = dict(options)
    for key, target in aliases.items():
        if key in expanded_options and target not in expanded_options:
            expanded_options[target] = expanded_options[key]
    for key in int_keys:
        if key in expanded_options:
            result[key] = int(expanded_options[key])
    for key in float_keys:
        if key in expanded_options:
            result[key] = float(expanded_options[key])
    for key in string_keys:
        if key in expanded_options:
            result[key] = str(expanded_options[key])
    return result


def _int_option(options: dict[str, object], key: str, default: int | None = None) -> int | None:
    value = options.get(key, default)
    if value is None:
        return None
    return int(value)
