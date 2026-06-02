import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models import SeResNeXtDistinguisher


def test_senet_resnext_outputs_binary_logits():
    model = SeResNeXtDistinguisher(input_bits=64, channels=8, blocks=2)
    batch = torch.zeros((4, 64), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, torch.nn.Module)
    assert logits.shape == (4, 1)


def test_senet_resnext_rejects_odd_input_width():
    with pytest.raises(ValueError, match="even number of input bits"):
        SeResNeXtDistinguisher(input_bits=63, channels=8)


def test_build_model_supports_senet_resnext_key():
    model = build_model("senet_resnext", input_bits=64, hidden_bits=8)
    batch = torch.zeros((2, 64), dtype=torch.float32)

    assert isinstance(model, SeResNeXtDistinguisher)
    assert model(batch).shape == (2, 1)
