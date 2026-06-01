import torch

from blockcipher_ai_eval.models import CnnDistinguisher


def test_cnn_distinguisher_outputs_binary_logits():
    model = CnnDistinguisher(input_bits=64, channels=8)
    batch = torch.zeros((4, 64), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, torch.nn.Module)
    assert logits.shape == (4, 1)


def test_cnn_distinguisher_rejects_odd_input_width():
    try:
        CnnDistinguisher(input_bits=63, channels=8)
    except ValueError as exc:
        assert "even number of input bits" in str(exc)
    else:
        raise AssertionError("expected ValueError for odd input width")
