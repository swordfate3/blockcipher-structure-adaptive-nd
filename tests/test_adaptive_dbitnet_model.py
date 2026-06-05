import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models.adaptive_dbitnet import (
    AdaptiveDBitNetDistinguisher,
    PairwiseAdaptiveDBitNetDistinguisher,
    SpnCellPairSetDBitNetDistinguisher,
    SpnNibbleConvPairSetDistinguisher,
    SpnTokenMixerPairSetDistinguisher,
    StructureAdaptivePairSetDBitNetDistinguisher,
    adaptive_dbitnet_dilations,
    structure_conditioned_dilations,
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


def test_pairwise_adaptive_dbitnet_uses_shared_pair_encoder_and_pooling():
    model = PairwiseAdaptiveDBitNetDistinguisher(
        input_bits=384,
        pair_bits=96,
        base_channels=8,
    )
    batch = torch.zeros((3, 384), dtype=torch.float32)

    logits = model(batch)

    assert model.pair_bits == 96
    assert model.pairs_per_sample == 4
    assert model.encoder.dilations == [47, 23, 11, 5]
    assert logits.shape == (3, 1)
    assert model.classifier[0].in_features == model.encoder.embedding_bits * 2


@pytest.mark.parametrize(
    ("pooling", "expected_multiplier"),
    [
        ("mean", 1),
        ("max", 1),
        ("mean_max", 2),
    ],
)
def test_pairwise_adaptive_dbitnet_supports_pooling_ablation_variants(
    pooling: str,
    expected_multiplier: int,
):
    model = PairwiseAdaptiveDBitNetDistinguisher(
        input_bits=384,
        pair_bits=96,
        base_channels=8,
        pooling=pooling,
    )
    batch = torch.zeros((3, 384), dtype=torch.float32)

    logits = model(batch)

    assert model.pooling == pooling
    assert logits.shape == (3, 1)
    assert model.classifier[0].in_features == (
        model.encoder.embedding_bits * expected_multiplier
    )


def test_pairwise_adaptive_dbitnet_rejects_unknown_pooling():
    with pytest.raises(ValueError, match="unsupported pooling"):
        PairwiseAdaptiveDBitNetDistinguisher(
            input_bits=384,
            pair_bits=96,
            base_channels=8,
            pooling="median",
        )


def test_build_model_supports_pairwise_adaptive_dbitnet_key():
    model = build_model("adaptive_dbitnet_pairwise", input_bits=384, hidden_bits=8)

    assert isinstance(model, PairwiseAdaptiveDBitNetDistinguisher)
    assert model.pair_bits == 96
    assert model.pairs_per_sample == 4
    assert model.pooling == "mean_max"


@pytest.mark.parametrize(
    ("model_key", "expected_pooling"),
    [
        ("adaptive_dbitnet_pairwise_mean", "mean"),
        ("adaptive_dbitnet_pairwise_max", "max"),
        ("adaptive_dbitnet_pairwise_mean_max", "mean_max"),
    ],
)
def test_build_model_supports_pairwise_pooling_ablation_keys(
    model_key: str,
    expected_pooling: str,
):
    model = build_model(model_key, input_bits=384, hidden_bits=8)

    assert isinstance(model, PairwiseAdaptiveDBitNetDistinguisher)
    assert model.pooling == expected_pooling
    assert model.pair_bits == 96
    assert model.pairs_per_sample == 4


def test_build_model_can_configure_pairwise_adaptive_dbitnet_pair_width():
    model = build_model(
        "adaptive_dbitnet_pairwise",
        input_bits=384,
        hidden_bits=8,
        pair_bits=192,
    )

    assert isinstance(model, PairwiseAdaptiveDBitNetDistinguisher)
    assert model.pair_bits == 192
    assert model.pairs_per_sample == 2


def test_pairwise_adaptive_dbitnet_rejects_non_multiple_pair_width():
    with pytest.raises(ValueError, match="multiple of pair_bits"):
        PairwiseAdaptiveDBitNetDistinguisher(input_bits=320, pair_bits=96, base_channels=8)


@pytest.mark.parametrize(
    ("structure", "expected_first_rates"),
    [
        ("ARX", [15, 5]),
        ("SPN", [3, 7]),
        ("Feistel-like", [47, 23]),
    ],
)
def test_structure_conditioned_dilations_add_structure_specific_receptive_fields(
    structure: str,
    expected_first_rates: list[int],
):
    dilations = structure_conditioned_dilations(96, structure=structure)

    assert dilations[:2] == expected_first_rates
    assert 47 in dilations
    assert len(dilations) == len(set(dilations))


def test_structure_adaptive_pairset_dbitnet_uses_attention_pooling_and_bit_mask():
    model = StructureAdaptivePairSetDBitNetDistinguisher(
        input_bits=384,
        pair_bits=96,
        base_channels=8,
        structure="ARX",
        pooling="attention_mean_max",
    )
    batch = torch.zeros((3, 384), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "ARX"
    assert model.pair_bits == 96
    assert model.pairs_per_sample == 4
    assert model.pooling == "attention_mean_max"
    assert model.encoder.structure == "ARX"
    assert model.encoder.dilations[:2] == [15, 5]
    assert model.encoder.bit_mask.shape == (96,)
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (3, 4)
    assert torch.allclose(
        model.last_attention_weights.sum(dim=1),
        torch.ones(3),
        atol=1e-5,
    )
    assert logits.shape == (3, 1)


def test_structure_adaptive_pairset_dbitnet_can_update_structure_after_build():
    model = StructureAdaptivePairSetDBitNetDistinguisher(
        input_bits=384,
        pair_bits=96,
        base_channels=8,
        structure="ARX",
    )

    model.set_cipher_structure("SPN")

    assert model.structure == "SPN"
    assert model.encoder.structure == "SPN"
    assert model.encoder.dilations[:2] == [15, 5]
    assert model.encoder.bit_mask[:4].tolist() == pytest.approx([1.3, 1.3, 1.3, 1.3])


def test_build_model_supports_structure_adaptive_pairset_key():
    model = build_model(
        "structure_adaptive_pairset_dbitnet",
        input_bits=384,
        hidden_bits=8,
        pair_bits=96,
    )
    batch = torch.zeros((3, 384), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, StructureAdaptivePairSetDBitNetDistinguisher)
    assert logits.shape == (3, 1)


def test_spn_cell_pairset_dbitnet_adds_cell_encoder_to_pair_embedding():
    model = SpnCellPairSetDBitNetDistinguisher(
        input_bits=768,
        pair_bits=192,
        base_channels=8,
        cell_bits=4,
    )
    batch = torch.zeros((2, 768), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.cell_bits == 4
    assert model.cells_per_pair == 48
    assert model.cell_embedding_bits == 8 * 4
    assert model.encoder.dilations[:2] == [3, 7]
    assert model.fused_pair_embedding_bits == (
        model.encoder.embedding_bits + model.cell_embedding_bits
    )
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert logits.shape == (2, 1)


def test_build_model_supports_spn_pairset_dbitnet_v2_key():
    model = build_model(
        "spn_pairset_dbitnet_v2",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
    )
    batch = torch.zeros((2, 768), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, SpnCellPairSetDBitNetDistinguisher)
    assert logits.shape == (2, 1)


def test_spn_nibble_conv_pairset_preserves_nibble_sequence_before_pair_pooling():
    model = SpnNibbleConvPairSetDistinguisher(
        input_bits=768,
        pair_bits=192,
        base_channels=8,
        nibble_bits=4,
        nibble_embed_dim=16,
        conv_depth=3,
        kernel_size=3,
        activation="gelu",
        norm="layernorm",
        pooling="gated_attention",
    )
    batch = torch.zeros((2, 768), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.nibble_bits == 4
    assert model.nibbles_per_pair == 48
    assert model.nibble_embed_dim == 16
    assert model.conv_depth == 3
    assert model.pooling == "gated_attention"
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert torch.allclose(
        model.last_attention_weights.sum(dim=1),
        torch.ones(2),
        atol=1e-5,
    )
    assert logits.shape == (2, 1)


def test_build_model_supports_spn_nibble_conv_pairset_key():
    model = build_model(
        "spn_nibble_conv_pairset",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
    )
    batch = torch.zeros((2, 768), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, SpnNibbleConvPairSetDistinguisher)
    assert logits.shape == (2, 1)



def test_build_model_passes_spn_nibble_component_options():
    model = build_model(
        "spn_nibble_conv_pairset",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
        model_options={
            "activation": "silu",
            "norm": "rmsnorm",
            "pooling": "gated_attention",
            "nibble_embed_dim": 24,
            "conv_depth": 2,
            "kernel_size": 5,
            "dropout": 0.05,
        },
    )

    assert isinstance(model, SpnNibbleConvPairSetDistinguisher)
    assert model.activation == "silu"
    assert model.norm == "rmsnorm"
    assert model.pooling == "gated_attention"
    assert model.nibble_embed_dim == 24
    assert model.conv_depth == 2
    assert model.kernel_size == 5
    assert model.dropout == 0.05


def test_spn_token_mixer_pairset_preserves_position_and_mixes_nibbles():
    model = SpnTokenMixerPairSetDistinguisher(
        input_bits=768,
        pair_bits=192,
        base_channels=8,
        nibble_bits=4,
        token_dim=16,
        mixer_depth=2,
        token_mlp_ratio=2,
        activation="gelu",
        norm="rmsnorm",
        pooling="gated_attention",
        dropout=0.05,
    )
    batch = torch.zeros((2, 768), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.nibble_bits == 4
    assert model.nibbles_per_pair == 48
    assert model.token_dim == 16
    assert model.mixer_depth == 2
    assert model.token_mlp_ratio == 2
    assert model.position_embedding.shape == (1, 48, 16)
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert torch.allclose(
        model.last_attention_weights.sum(dim=1),
        torch.ones(2),
        atol=1e-5,
    )
    assert logits.shape == (2, 1)


def test_build_model_passes_spn_token_mixer_component_options():
    model = build_model(
        "spn_token_mixer_pairset",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
        model_options={
            "activation": "silu",
            "norm": "layernorm",
            "pooling": "attention_mean_max",
            "token_dim": 24,
            "mixer_depth": 3,
            "token_mlp_ratio": 3,
            "dropout": 0.10,
        },
    )

    assert isinstance(model, SpnTokenMixerPairSetDistinguisher)
    assert model.activation == "silu"
    assert model.norm == "layernorm"
    assert model.pooling == "attention_mean_max"
    assert model.token_dim == 24
    assert model.mixer_depth == 3
    assert model.token_mlp_ratio == 3
    assert model.dropout == 0.10


def test_adaptive_dbitnet_rejects_too_small_or_odd_inputs():
    with pytest.raises(ValueError, match="even number of input bits"):
        AdaptiveDBitNetDistinguisher(input_bits=95, base_channels=8)
    with pytest.raises(ValueError, match="at least 16 input bits"):
        AdaptiveDBitNetDistinguisher(input_bits=14, base_channels=8)
