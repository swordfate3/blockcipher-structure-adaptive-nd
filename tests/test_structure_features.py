from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.structure_features import (
    STRUCTURE_FEATURE_NAMES,
    structure_feature_vector,
)


def test_structure_feature_vector_marks_arx_traits_and_normalized_sizes():
    vector = structure_feature_vector(CipherProfile.speck32_64(), rounds=7)
    values = dict(zip(STRUCTURE_FEATURE_NAMES, vector.tolist()))

    assert values["is_arx"] == 1.0
    assert values["is_spn"] == 0.0
    assert values["has_modular_addition"] == 1.0
    assert values["has_sbox_layer"] == 0.0
    assert values["block_bits_div_128"] == 0.25
    assert values["key_bits_div_128"] == 0.5
    assert values["rounds_div_32"] == 7 / 32


def test_structure_feature_vector_marks_sm4_as_feistel_like():
    vector = structure_feature_vector(CipherProfile.sm4(), rounds=4)
    values = dict(zip(STRUCTURE_FEATURE_NAMES, vector.tolist()))

    assert values["is_feistel_like"] == 1.0
    assert values["has_sbox_layer"] == 1.0
    assert values["has_linear_diffusion"] == 1.0
    assert values["has_round_recurrence"] == 1.0
