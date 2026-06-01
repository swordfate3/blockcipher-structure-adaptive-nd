import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models import (
    DBitNetDistinguisher,
    LstmRoundSeqDistinguisher,
    TransformerEncoderDistinguisher,
)


@pytest.mark.parametrize(
    ("model_key", "model_type"),
    [
        ("dbitnet_dilated_cnn", DBitNetDistinguisher),
        ("lstm_roundseq", LstmRoundSeqDistinguisher),
        ("transformer_encoder", TransformerEncoderDistinguisher),
    ],
)
def test_build_model_supports_all_innovation_one_candidate_keys(
    model_key: str,
    model_type: type[torch.nn.Module],
):
    model = build_model(model_key, input_bits=64, hidden_bits=8)
    batch = torch.zeros((3, 64), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, model_type)
    assert logits.shape == (3, 1)


@pytest.mark.parametrize(
    "model_key",
    ["dbitnet_dilated_cnn", "lstm_roundseq", "transformer_encoder"],
)
def test_innovation_one_candidate_models_reject_odd_pair_width(model_key: str):
    with pytest.raises(ValueError, match="even number of input bits"):
        build_model(model_key, input_bits=63, hidden_bits=8)

