import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models import (
    AdaptiveDBitNetDistinguisher,
    DBitNetDistinguisher,
    GohrSpeckDistinguisher,
    LstmRoundSeqDistinguisher,
    MultiScaleDenseResNetDistinguisher,
    SeResNeXtDistinguisher,
    TransformerEncoderDistinguisher,
)


@pytest.mark.parametrize(
    ("model_key", "model_type"),
    [
        ("adaptive_dbitnet", AdaptiveDBitNetDistinguisher),
        ("dbitnet_dilated_cnn", DBitNetDistinguisher),
        ("gohr_resnet_speck", GohrSpeckDistinguisher),
        ("gohr_resnet_speck_depth10", GohrSpeckDistinguisher),
        ("senet_resnext", SeResNeXtDistinguisher),
        ("multiscale_dense_resnet", MultiScaleDenseResNetDistinguisher),
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
    [
        "dbitnet_dilated_cnn",
        "adaptive_dbitnet",
        "senet_resnext",
        "multiscale_dense_resnet",
        "lstm_roundseq",
        "transformer_encoder",
    ],
)
def test_innovation_one_candidate_models_reject_odd_pair_width(model_key: str):
    with pytest.raises(ValueError, match="even number of input bits"):
        build_model(model_key, input_bits=63, hidden_bits=8)


def test_gohr_resnet_speck_requires_original_speck_pair_width():
    with pytest.raises(ValueError, match="64-bit SPECK32/64 ciphertext-pair input"):
        build_model("gohr_resnet_speck", input_bits=96, hidden_bits=8)


def test_depth10_gohr_resnet_speck_requires_original_speck_pair_width():
    with pytest.raises(ValueError, match="64-bit SPECK32/64 ciphertext-pair input"):
        build_model("gohr_resnet_speck_depth10", input_bits=96, hidden_bits=8)
