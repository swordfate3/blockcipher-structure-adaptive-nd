import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models import ResNetBitSliceDistinguisher


def test_resnet_bitslice_distinguisher_outputs_binary_logits():
    model = ResNetBitSliceDistinguisher(input_bits=64, channels=8, blocks=2)
    batch = torch.zeros((4, 64), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, torch.nn.Module)
    assert logits.shape == (4, 1)


def test_resnet_bitslice_requires_even_input_width_for_ciphertext_pairs():
    try:
        ResNetBitSliceDistinguisher(input_bits=63, channels=8)
    except ValueError as exc:
        assert "even number of input bits" in str(exc)
    else:
        raise AssertionError("expected ValueError for odd input width")


def test_build_model_supports_resnet_bitslice_key():
    model = build_model("resnet_bitslice", input_bits=64, hidden_bits=8)
    batch = torch.zeros((2, 64), dtype=torch.float32)

    assert isinstance(model, ResNetBitSliceDistinguisher)
    assert model(batch).shape == (2, 1)

