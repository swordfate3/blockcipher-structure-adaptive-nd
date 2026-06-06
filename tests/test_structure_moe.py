import torch

from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.models import StructureAwareMoEDistinguisher
from blockcipher_ai_eval.models.adaptive_dbitnet import AdaptiveDBitNetDistinguisher
from blockcipher_ai_eval.models.adaptive_dbitnet import PairwiseAdaptiveDBitNetDistinguisher
from blockcipher_ai_eval.models.adaptive_dbitnet import SpnTokenMixerPairSetDistinguisher
from blockcipher_ai_eval.models.structure_moe import (
    EXPERT_KEYS,
    V2_EXPERT_KEYS,
    V3_EXPERT_KEYS,
    V4_EXPERT_KEYS,
    V5_EXPERT_KEYS,
)
from blockcipher_ai_eval.structure_features import structure_feature_vector


def _features(cipher, rounds):
    return torch.tensor(structure_feature_vector(cipher, rounds), dtype=torch.float32)


def test_uniform_moe_outputs_expected_shape_and_equal_weights():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="uniform",
    )
    model.set_structure_features(_features(CipherProfile.speck32_64(), rounds=5))

    output = model(torch.zeros((3, 96), dtype=torch.float32))
    weights = model.current_gate_weights(batch_size=3)

    assert output.shape == (3, 1)
    assert EXPERT_KEYS == (
        "resnet_bitslice",
        "dbitnet_dilated_cnn",
        "cnn",
        "mlp",
        "senet_resnext",
        "multiscale_dense_resnet",
    )
    assert torch.allclose(weights[0], torch.full((6,), 1.0 / 6.0))


def test_hard_moe_prefers_resnet_for_arx_and_dbitnet_for_sm4():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="hard",
    )
    model.set_structure_features(_features(CipherProfile.speck32_64(), rounds=5))

    arx_summary = model.gate_summary()

    assert arx_summary["gate_mode"] == "hard"
    assert arx_summary["gate_weight_resnet_bitslice"] == 0.35
    assert arx_summary["gate_weight_dbitnet_dilated_cnn"] == 0.20
    assert arx_summary["gate_weight_multiscale_dense_resnet"] == 0.25
    assert arx_summary["gate_weight_senet_resnext"] == 0.10

    model.set_structure_features(_features(CipherProfile.sm4(), rounds=4))
    sm4_summary = model.gate_summary()

    assert sm4_summary["gate_weight_dbitnet_dilated_cnn"] == 0.35
    assert sm4_summary["gate_weight_multiscale_dense_resnet"] == 0.20
    assert sm4_summary["gate_weight_resnet_bitslice"] == 0.20


def test_soft_moe_weights_sum_to_one():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="soft",
    )
    model.set_structure_features(_features(CipherProfile.present80(), rounds=4))

    weights = model.current_gate_weights(batch_size=2)

    assert weights.shape == (2, 6)
    assert torch.allclose(weights.sum(dim=1), torch.ones(2), atol=1e-6)


def test_v2_moe_replaces_fixed_dbitnet_with_adaptive_dbitnet_expert():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="hard",
        expert_set="v2_adaptive",
    )
    model.set_structure_features(_features(CipherProfile.sm4(), rounds=4))

    output = model(torch.zeros((2, 96), dtype=torch.float32))
    summary = model.gate_summary()

    assert output.shape == (2, 1)
    assert V2_EXPERT_KEYS == (
        "resnet_bitslice",
        "adaptive_dbitnet",
        "cnn",
        "mlp",
        "senet_resnext",
        "multiscale_dense_resnet",
    )
    assert isinstance(model.experts[1], AdaptiveDBitNetDistinguisher)
    assert summary["gate_weight_adaptive_dbitnet"] == 0.35
    assert "gate_weight_dbitnet_dilated_cnn" not in summary


def test_v3_moe_replaces_adaptive_dbitnet_with_pairwise_expert():
    model = StructureAwareMoEDistinguisher(
        input_bits=384,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="hard",
        expert_set="v3_pairwise",
        pair_bits=96,
    )
    model.set_structure_features(_features(CipherProfile.speck32_64(), rounds=6))

    output = model(torch.zeros((2, 384), dtype=torch.float32))
    summary = model.gate_summary()

    assert output.shape == (2, 1)
    assert V3_EXPERT_KEYS == (
        "resnet_bitslice",
        "adaptive_dbitnet_pairwise",
        "cnn",
        "mlp",
        "senet_resnext",
        "multiscale_dense_resnet",
    )
    assert isinstance(model.experts[1], PairwiseAdaptiveDBitNetDistinguisher)
    assert summary["expert_set"] == "v3_pairwise"
    assert summary["gate_weight_adaptive_dbitnet_pairwise"] == 0.20


def test_v4_moe_applies_structure_adapter_before_pairwise_experts():
    model = StructureAwareMoEDistinguisher(
        input_bits=384,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="hard",
        expert_set="v4_structure_adapter",
        pair_bits=96,
    )
    model.set_structure_features(_features(CipherProfile.speck32_64(), rounds=6))

    output = model(torch.zeros((2, 384), dtype=torch.float32))
    summary = model.gate_summary()

    assert output.shape == (2, 1)
    assert V4_EXPERT_KEYS == (
        "resnet_bitslice",
        "adaptive_dbitnet_pairwise",
        "cnn",
        "mlp",
        "senet_resnext",
        "multiscale_dense_resnet",
    )
    assert isinstance(model.experts[1], PairwiseAdaptiveDBitNetDistinguisher)
    assert summary["expert_set"] == "v4_structure_adapter"
    assert summary["adapter_mode"] == "structure"
    assert summary["adapter_name"] == "arx_word_mix"


def test_v5_moe_includes_spn_token_mixer_expert_for_spn_structure():
    model = StructureAwareMoEDistinguisher(
        input_bits=768,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="hard",
        expert_set="v5_structure_experts",
        pair_bits=192,
    )
    model.set_structure_features(_features(CipherProfile.present80(), rounds=5))

    output = model(torch.zeros((2, 768), dtype=torch.float32))
    summary = model.gate_summary()

    assert output.shape == (2, 1)
    assert V5_EXPERT_KEYS == (
        "adaptive_dbitnet_pairwise",
        "spn_token_mixer_pairset",
        "resnet_bitslice",
        "senet_resnext",
        "multiscale_dense_resnet",
    )
    assert isinstance(model.experts[1], SpnTokenMixerPairSetDistinguisher)
    assert summary["expert_set"] == "v5_structure_experts"
    assert summary["adapter_mode"] == "none"
    assert summary["gate_weight_spn_token_mixer_pairset"] == 0.45



def test_v5_moe_soft_gate_temperature_and_component_summary():
    model = StructureAwareMoEDistinguisher(
        input_bits=768,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="soft",
        expert_set="v5_structure_experts",
        pair_bits=192,
        gate_hidden_bits=12,
        gate_activation="silu",
        gate_temperature=1.5,
        spn_token_dim=24,
        spn_mixer_depth=2,
        spn_token_mlp_ratio=3,
        expert_activation="silu",
        expert_norm="rmsnorm",
        spn_pooling="gated_attention",
        expert_dropout=0.05,
    )
    model.set_structure_features(_features(CipherProfile.present80(), rounds=5))

    weights = model.current_gate_weights(batch_size=2)
    summary = model.gate_summary()

    assert weights.shape == (2, 5)
    assert torch.allclose(weights.sum(dim=1), torch.ones(2), atol=1e-6)
    assert summary["gate_hidden_bits"] == 12
    assert summary["gate_activation"] == "silu"
    assert summary["gate_temperature"] == 1.5
    assert summary["spn_token_dim"] == 24
    assert summary["spn_mixer_depth"] == 2
    assert summary["spn_token_mlp_ratio"] == 3
    assert summary["expert_activation"] == "silu"
    assert summary["expert_norm"] == "rmsnorm"
    assert summary["spn_pooling"] == "gated_attention"
    assert summary["expert_dropout"] == 0.05
