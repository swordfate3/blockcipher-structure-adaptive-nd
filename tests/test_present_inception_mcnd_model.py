import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models.structure.spn.present_inception_mcnd import (
    PresentInceptionMCNDDistinguisher,
    PresentInceptionMCNDGlobalMatrixDistinguisher,
    PresentInceptionMCNDMatrixDistinguisher,
    PresentInceptionMCNDPairStackMatrixDistinguisher,
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
    assert model.kernel_sizes == (1, 3, 5)
    assert logits.shape == (3, 1)


def test_present_inception_mcnd_rejects_non_pairset_input_width():
    with pytest.raises(ValueError, match="multiple of pair_bits"):
        build_model("present_inception_mcnd", input_bits=2049, hidden_bits=16, pair_bits=128)


def test_build_model_passes_present_inception_kernel_size_options():
    model = build_model(
        "present_inception_mcnd",
        input_bits=2048,
        hidden_bits=16,
        pair_bits=128,
        structure="SPN",
        model_options={"kernel_sizes": [1, 2, 4], "blocks": 1},
    )

    assert isinstance(model, PresentInceptionMCNDDistinguisher)
    assert model.kernel_sizes == (1, 2, 4)
    assert model.blocks == 1


def test_build_model_supports_present_inception_mcnd_matrix_for_cell_layout():
    model = build_model(
        "present_inception_mcnd_matrix",
        input_bits=2048,
        hidden_bits=16,
        pair_bits=128,
        structure="SPN",
        model_options={"branches": 8, "blocks": 2, "kernel_sizes": [[1, 1], [1, 2], [2, 4]]},
    )
    batch = torch.zeros((3, 2048), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, PresentInceptionMCNDMatrixDistinguisher)
    assert model.pairs_per_sample == 16
    assert model.cell_bits == 4
    assert model.cell_width == 32
    assert logits.shape == (3, 1)


def test_build_model_supports_present_inception_mcnd_global_matrix_layout():
    model = build_model(
        "present_inception_mcnd_global_matrix",
        input_bits=2048,
        hidden_bits=16,
        pair_bits=128,
        structure="SPN",
        model_options={"branches": 8, "blocks": 2, "kernel_sizes": [[1, 1], [1, 2], [2, 4]]},
    )
    batch = torch.zeros((3, 2048), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, PresentInceptionMCNDGlobalMatrixDistinguisher)
    assert model.pairs_per_sample == 16
    assert model.cell_bits == 4
    assert model.cell_width == 32
    assert logits.shape == (3, 1)

def test_build_model_supports_present_inception_mcnd_pair_stack_matrix_layout():
    model = build_model(
        "present_inception_mcnd_pair_stack_matrix",
        input_bits=2048,
        hidden_bits=16,
        pair_bits=128,
        structure="SPN",
        model_options={"branches": 8, "blocks": 2, "kernel_sizes": [[1, 1], [1, 2], [2, 4], [4, 4]]},
    )
    batch = torch.zeros((3, 2048), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, PresentInceptionMCNDPairStackMatrixDistinguisher)
    assert model.pairs_per_sample == 16
    assert model.cell_bits == 4
    assert model.cell_width == 32
    assert model.matrix_height == 64
    assert logits.shape == (3, 1)

