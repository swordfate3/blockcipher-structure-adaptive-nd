import torch

from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.models import StructureAwareMoEDistinguisher
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
    assert torch.allclose(weights[0], torch.tensor([0.25, 0.25, 0.25, 0.25]))


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
    assert arx_summary["gate_weight_resnet_bitslice"] == 0.55
    assert arx_summary["gate_weight_dbitnet_dilated_cnn"] == 0.30

    model.set_structure_features(_features(CipherProfile.sm4(), rounds=4))
    sm4_summary = model.gate_summary()

    assert sm4_summary["gate_weight_dbitnet_dilated_cnn"] == 0.50
    assert sm4_summary["gate_weight_resnet_bitslice"] == 0.30


def test_soft_moe_weights_sum_to_one():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="soft",
    )
    model.set_structure_features(_features(CipherProfile.present80(), rounds=4))

    weights = model.current_gate_weights(batch_size=2)

    assert weights.shape == (2, 4)
    assert torch.allclose(weights.sum(dim=1), torch.ones(2), atol=1e-6)
