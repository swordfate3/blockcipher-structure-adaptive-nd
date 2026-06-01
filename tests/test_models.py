import torch

from blockcipher_ai_eval.models import MlpDistinguisher


def test_mlp_distinguisher_is_torch_module_and_outputs_logits():
    model = MlpDistinguisher(input_bits=64, hidden_bits=32)
    batch = torch.zeros((5, 64), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, torch.nn.Module)
    assert logits.shape == (5, 1)
    assert logits.dtype == torch.float32


def test_mlp_distinguisher_rejects_wrong_feature_width():
    model = MlpDistinguisher(input_bits=64, hidden_bits=32)
    batch = torch.zeros((5, 63), dtype=torch.float32)

    try:
        model(batch)
    except ValueError as exc:
        assert "expected 64 input bits" in str(exc)
    else:
        raise AssertionError("expected ValueError for wrong feature width")
