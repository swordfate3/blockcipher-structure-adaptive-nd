import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models.gohr_speck import (
    GohrSpeckDistinguisher,
    reshape_speck_ciphertext_pair,
)


def test_reshape_speck_ciphertext_pair_uses_four_16_bit_channels():
    features = torch.zeros((2, 64), dtype=torch.float32)
    features[0, 0] = 1.0
    features[0, 16] = 1.0
    features[0, 32] = 1.0
    features[0, 48] = 1.0

    reshaped = reshape_speck_ciphertext_pair(features)

    assert reshaped.shape == (2, 4, 16)
    assert reshaped[0, :, 0].tolist() == [1.0, 1.0, 1.0, 1.0]
    assert reshaped[0, :, 1:].sum().item() == 0.0


def test_gohr_speck_model_uses_word_aware_stem_and_dense_head():
    model = GohrSpeckDistinguisher(input_bits=64, filters=8, blocks=2)
    batch = torch.zeros((3, 64), dtype=torch.float32)

    logits = model(batch)

    assert model.word_bits == 16
    assert model.stem[0].in_channels == 4
    assert model.stem[0].out_channels == 8
    assert model.head[1].in_features == 8 * 16
    assert logits.shape == (3, 1)


def test_build_model_supports_gohr_resnet_speck_key():
    model = build_model("gohr_resnet_speck", input_bits=64, hidden_bits=8)

    assert isinstance(model, GohrSpeckDistinguisher)


def test_build_model_supports_depth10_gohr_resnet_speck_key():
    model = build_model("gohr_resnet_speck_depth10", input_bits=64, hidden_bits=8)

    assert isinstance(model, GohrSpeckDistinguisher)
    assert model.blocks == 10


@pytest.mark.parametrize("input_bits", [63, 96, 384])
def test_gohr_speck_model_rejects_non_original_pair_width(input_bits: int):
    with pytest.raises(ValueError, match="64-bit SPECK32/64 ciphertext-pair input"):
        GohrSpeckDistinguisher(input_bits=input_bits, filters=8)
