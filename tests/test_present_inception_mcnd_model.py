import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models.structure.spn.present_inception_mcnd import (
    PresentInceptionMCNDDistinguisher,
)


def test_build_model_supports_present_inception_mcnd_for_multipair_present_input():
    model = build_model(
        "present_inception_mcnd",
        input_bits=2048,
        hidden_bits=16,
        pair_bits=128,
        structure="SPN",
        model_options={"branches": 8, "blocks": 2},
    )
    batch = torch.zeros((3, 2048), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, PresentInceptionMCNDDistinguisher)
    assert model.pairs_per_sample == 16
    assert logits.shape == (3, 1)


def test_present_inception_mcnd_rejects_non_pairset_input_width():
    with pytest.raises(ValueError, match="multiple of pair_bits"):
        build_model("present_inception_mcnd", input_bits=2049, hidden_bits=16, pair_bits=128)
