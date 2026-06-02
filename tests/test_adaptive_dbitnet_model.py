import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models.adaptive_dbitnet import (
    AdaptiveDBitNetDistinguisher,
    adaptive_dbitnet_dilations,
)


@pytest.mark.parametrize(
    ("input_bits", "expected"),
    [
        (64, [31, 15, 7, 3]),
        (96, [47, 23, 11, 5]),
        (128, [63, 31, 15, 7, 3]),
        (384, [191, 95, 47, 23, 11, 5]),
    ],
)
def test_adaptive_dbitnet_dilations_follow_input_size(input_bits: int, expected: list[int]):
    assert adaptive_dbitnet_dilations(input_bits) == expected


def test_adaptive_dbitnet_uses_input_adaptive_dilated_blocks_and_strong_head():
    model = AdaptiveDBitNetDistinguisher(input_bits=96, base_channels=8)
    batch = torch.zeros((3, 96), dtype=torch.float32)

    logits = model(batch)

    assert model.dilations == [47, 23, 11, 5]
    assert model.output_width == 10
    assert model.output_channels == 56
    assert logits.shape == (3, 1)
    assert isinstance(model.classifier[0], torch.nn.Linear)
    assert model.classifier[0].in_features == 56 * 10
    assert model.classifier[0].out_features == 256
    assert model.classifier[2].out_features == 256
    assert model.classifier[4].out_features == 64


def test_build_model_supports_adaptive_dbitnet_key():
    model = build_model("adaptive_dbitnet", input_bits=96, hidden_bits=8)

    assert isinstance(model, AdaptiveDBitNetDistinguisher)


def test_adaptive_dbitnet_rejects_too_small_or_odd_inputs():
    with pytest.raises(ValueError, match="even number of input bits"):
        AdaptiveDBitNetDistinguisher(input_bits=95, base_channels=8)
    with pytest.raises(ValueError, match="at least 16 input bits"):
        AdaptiveDBitNetDistinguisher(input_bits=14, base_channels=8)
