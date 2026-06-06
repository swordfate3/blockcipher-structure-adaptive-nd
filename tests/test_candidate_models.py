import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models import (
    AdaptiveDBitNetDistinguisher,
    DBitNetDistinguisher,
    GohrSpeckDistinguisher,
    LstmRoundSeqDistinguisher,
    MultiScaleDenseResNetDistinguisher,
    PairwiseAdaptiveDBitNetDistinguisher,
    SeResNeXtDistinguisher,
    SpnTokenMixerPairSetDistinguisher,
    StructureAwareMoEDistinguisher,
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


def test_build_model_supports_pairwise_adaptive_dbitnet_candidate_key():
    model = build_model("adaptive_dbitnet_pairwise", input_bits=384, hidden_bits=8)
    batch = torch.zeros((3, 384), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, PairwiseAdaptiveDBitNetDistinguisher)
    assert logits.shape == (3, 1)


def test_build_model_supports_moe_v5_soft_key():
    model = build_model(
        "moe_v5_soft",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
    )
    batch = torch.zeros((2, 768), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, StructureAwareMoEDistinguisher)
    assert model.expert_set == "v5_structure_experts"
    assert logits.shape == (2, 1)


def test_gohr_resnet_speck_requires_original_speck_pair_width():
    with pytest.raises(ValueError, match="64-bit SPECK32/64 ciphertext-pair input"):
        build_model("gohr_resnet_speck", input_bits=96, hidden_bits=8)


def test_depth10_gohr_resnet_speck_requires_original_speck_pair_width():
    with pytest.raises(ValueError, match="64-bit SPECK32/64 ciphertext-pair input"):
        build_model("gohr_resnet_speck_depth10", input_bits=96, hidden_bits=8)



def test_build_model_forwards_moe_v5_component_options():
    model = build_model(
        "moe_v5_soft",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
        model_options={
            "gate_hidden_bits": 12,
            "gate_activation": "silu",
            "gate_dropout": 0.05,
            "gate_temperature": 1.5,
            "pairwise_pooling": "mean",
            "spn_token_dim": 24,
            "spn_mixer_depth": 2,
            "spn_token_mlp_ratio": 3,
            "expert_activation": "silu",
            "expert_norm": "rmsnorm",
            "spn_pooling": "gated_attention",
            "expert_dropout": 0.05,
        },
    )

    assert isinstance(model, StructureAwareMoEDistinguisher)
    assert model.gate_hidden_bits == 12
    assert model.gate_activation == "silu"
    assert model.gate_temperature == 1.5
    assert isinstance(model.experts[0], PairwiseAdaptiveDBitNetDistinguisher)
    assert model.experts[0].pooling == "mean"
    assert isinstance(model.experts[1], SpnTokenMixerPairSetDistinguisher)
    assert model.experts[1].token_dim == 24
    assert model.experts[1].mixer_depth == 2
    assert model.experts[1].token_mlp_ratio == 3
    assert model.experts[1].activation == "silu"
    assert model.experts[1].norm == "rmsnorm"
    assert model.experts[1].pooling == "gated_attention"
    assert model.experts[1].dropout == 0.05
