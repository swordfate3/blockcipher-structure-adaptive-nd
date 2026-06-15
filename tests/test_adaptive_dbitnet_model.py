import pytest
import torch

from blockcipher_ai_eval.experiments import build_model
from blockcipher_ai_eval.models.structure.adaptive_dbitnet import (
    AdaptiveDBitNetDistinguisher,
    PairwiseAdaptiveDBitNetDistinguisher,
    StructureAdaptivePairSetDBitNetDistinguisher,
    adaptive_dbitnet_dilations,
    structure_conditioned_dilations,
)
from blockcipher_ai_eval.models.structure.arx import (
    ArxRoundFunctionHybridPairSetDistinguisher,
    ArxStructureAdaptivePairSetDBitNetDistinguisher,
    ArxTrailMixerPairSetDistinguisher,
    ArxWordMixerBlock,
    ArxWordMixerPairSetDistinguisher,
)

from blockcipher_ai_eval.models.structure.spn import (
    SpnCellPairSetDBitNetDistinguisher,
    SpnCellPairSetDBitNetDistinguisher as ModularSpnCellPairSetDBitNetDistinguisher,
)
from blockcipher_ai_eval.models.structure.spn import (
    SpnNibbleConvPairSetDistinguisher,
    SpnNibbleConvPairSetDistinguisher as ModularSpnNibbleConvPairSetDistinguisher,
)
from blockcipher_ai_eval.models.structure.spn import (
    PresentPLayerMixerBlock,
    PresentMatrixTrailHybridPairSetDistinguisher,
    PresentPairSetStatsHybridDistinguisher,
    PresentPLayerMixerPairSetDistinguisher,
    PresentTrailMixerPairSetDistinguisher,
    SpnTokenMixerPairSetDistinguisher,
    SpnTokenMixerPairSetDistinguisher as ModularSpnTokenMixerPairSetDistinguisher,
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


def test_build_model_supports_arx_pairset_dbitnet_key():
    model = build_model(
        "arx_structure_adaptive_pairset_dbitnet",
        input_bits=384,
        hidden_bits=8,
        pair_bits=96,
    )
    batch = torch.zeros((3, 384), dtype=torch.float32)

    logits = model(batch)

    assert isinstance(model, ArxStructureAdaptivePairSetDBitNetDistinguisher)
    assert model.structure == "ARX"
    assert model.encoder.structure == "ARX"
    assert model.encoder.dilations[:2] == [15, 5]
    assert logits.shape == (3, 1)


def test_arx_word_mixer_pairset_preserves_word_tokens_and_evidence_pooling():
    model = ArxWordMixerPairSetDistinguisher(
        input_bits=896,
        pair_bits=224,
        base_channels=8,
        token_dim=16,
        mixer_depth=2,
        pooling="topk_logsumexp",
        top_k=2,
        lse_temperature=0.75,
    )
    batch = torch.randn((2, 896), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "ARX"
    assert model.arx_words_per_pair == 7
    assert model.tokens_per_pair == 14
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [2, 2]
    assert logits.shape == (2, 1)


def test_arx_word_mixer_block_uses_rotation_messages_and_carry_proxy():
    block = ArxWordMixerBlock(token_dim=8)
    hidden = torch.randn((2, 14, 8), dtype=torch.float32)
    ror7_message = torch.randn((2, 14, 8), dtype=torch.float32)
    rol2_message = torch.randn((2, 14, 8), dtype=torch.float32)
    carry_proxy = torch.rand((2, 14, 1), dtype=torch.float32)

    mixed = block(hidden, ror7_message, rol2_message, carry_proxy)

    assert mixed.shape == hidden.shape


def test_build_model_supports_arx_word_mixer_pairset_key_and_options():
    model = build_model(
        "arx_word_mixer_pairset",
        input_bits=896,
        hidden_bits=8,
        pair_bits=224,
        structure="ARX",
        model_options={
            "token_dim": 24,
            "mixer_depth": 2,
            "pooling": "topk_mean",
            "top_k": 3,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, ArxWordMixerPairSetDistinguisher)
    assert model.pair_bits == 224
    assert model.arx_words_per_pair == 7
    assert model.tokens_per_pair == 14
    assert model.token_dim == 24
    assert model.mixer_depth == 2
    assert model.pooling == "topk_mean"
    assert model.top_k == 3
    assert model.lse_temperature == 0.5


def test_arx_trail_mixer_pairset_preserves_rx_trail_words_and_evidence_pooling():
    model = ArxTrailMixerPairSetDistinguisher(
        input_bits=1408,
        pair_bits=352,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        role_mixer_depth=1,
        pooling="topk_logsumexp",
        top_k=2,
        lse_temperature=0.75,
    )
    batch = torch.randn((2, 1408), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "ARX"
    assert model.feature_words_per_pair == 11
    assert model.tokens_per_pair == 22
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [2, 2]
    assert logits.shape == (2, 1)


def test_build_model_supports_arx_trail_mixer_pairset_key_and_options():
    model = build_model(
        "arx_trail_mixer_pairset",
        input_bits=1408,
        hidden_bits=8,
        pair_bits=352,
        structure="ARX",
        model_options={
            "token_dim": 24,
            "mixer_depth": 1,
            "role_mixer_depth": 1,
            "pooling": "topk_mean",
            "top_k": 2,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, ArxTrailMixerPairSetDistinguisher)
    assert model.pair_bits == 352
    assert model.feature_words_per_pair == 11
    assert model.token_dim == 24
    assert model.mixer_depth == 1
    assert model.role_mixer_depth == 1
    assert model.pooling == "topk_mean"
    assert model.top_k == 2
    assert model.lse_temperature == 0.5


def test_arx_round_function_hybrid_pairset_preserves_rx_groups_and_evidence_pooling():
    model = ArxRoundFunctionHybridPairSetDistinguisher(
        input_bits=1408,
        pair_bits=352,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        group_mixer_depth=1,
        pooling="topk_logsumexp",
        top_k=2,
        lse_temperature=0.75,
    )
    batch = torch.randn((2, 1408), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "ARX"
    assert model.feature_words_per_pair == 11
    assert model.tokens_per_pair == 22
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [2, 2]
    assert logits.shape == (2, 1)


def test_arx_round_function_hybrid_pairset_exposes_speck_rx_feature_role_groups():
    model = ArxRoundFunctionHybridPairSetDistinguisher(
        input_bits=1408,
        pair_bits=352,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        group_mixer_depth=1,
    )

    assert model.feature_role_names == (
        "left",
        "right",
        "difference",
        "rotation_aligned_difference",
        "partial_inverse_left_y",
        "partial_inverse_right_y",
        "partial_inverse_delta_y",
        "rx_alpha",
        "rx_beta",
        "carry_left_delta",
        "carry_right_delta",
    )
    assert model.round_relation_groups == (
        (0, 1, 2),
        (2, 3),
        (4, 5, 6),
        (7, 8),
        (9, 10),
    )
    assert model.group_summary_bits == 5 * model.token_dim
    assert model.pair_embedding_bits == 14 * model.token_dim


def test_arx_round_function_hybrid_pairset_exposes_carrychain_role_groups():
    model = ArxRoundFunctionHybridPairSetDistinguisher(
        input_bits=2176,
        pair_bits=544,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        group_mixer_depth=1,
    )

    assert model.feature_words_per_pair == 17
    assert model.tokens_per_pair == 34
    assert model.feature_role_names[-6:] == (
        "carry_generate_xy_delta",
        "carry_propagate_xy_delta",
        "carry_edge_xy_delta",
        "carry_generate_rot_pre_delta",
        "carry_propagate_rot_pre_delta",
        "carry_edge_rot_pre_delta",
    )
    assert model.round_relation_groups[-2:] == ((11, 12, 13), (14, 15, 16))
    assert model.group_summary_bits == 7 * model.token_dim
    assert model.pair_embedding_bits == 16 * model.token_dim


def test_arx_round_function_hybrid_pairset_exposes_carrychain_plus_role_groups():
    model = ArxRoundFunctionHybridPairSetDistinguisher(
        input_bits=2944,
        pair_bits=736,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        group_mixer_depth=1,
    )

    assert model.feature_words_per_pair == 23
    assert model.tokens_per_pair == 46
    assert model.feature_role_names[-6:] == (
        "carry_chain_xy_delta",
        "carry_chain_xy_prime_delta",
        "carry_chain_rot_pre_delta",
        "carry_chain_rot_pre_prime_delta",
        "addition_xy_delta",
        "addition_rot_pre_delta",
    )
    assert model.round_relation_groups[-2:] == ((17, 18, 19, 20), (21, 22))
    assert model.group_summary_bits == 9 * model.token_dim
    assert model.pair_embedding_bits == 18 * model.token_dim


def test_build_model_supports_arx_round_function_hybrid_pairset_key_and_options():
    model = build_model(
        "arx_round_function_hybrid_pairset",
        input_bits=1408,
        hidden_bits=8,
        pair_bits=352,
        structure="ARX",
        model_options={
            "token_dim": 24,
            "mixer_depth": 1,
            "group_mixer_depth": 1,
            "pooling": "topk_mean",
            "top_k": 2,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, ArxRoundFunctionHybridPairSetDistinguisher)
    assert model.pair_bits == 352
    assert model.feature_words_per_pair == 11
    assert model.token_dim == 24
    assert model.mixer_depth == 1
    assert model.group_mixer_depth == 1
    assert model.pooling == "topk_mean"
    assert model.top_k == 2
    assert model.lse_temperature == 0.5


def test_present_trail_mixer_pairset_preserves_word_roles_and_evidence_pooling():
    model = PresentTrailMixerPairSetDistinguisher(
        input_bits=1536,
        pair_bits=768,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        role_mixer_depth=1,
        pooling="topk_logsumexp",
        top_k=1,
        lse_temperature=0.75,
    )
    batch = torch.randn((2, 1536), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.words_per_pair == 12
    assert model.nibbles_per_pair == 192
    assert model.role_embedding.shape[1] == 12
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 2)
    assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [1, 1]
    assert logits.shape == (2, 1)


def test_build_model_supports_present_trail_mixer_pairset_key_and_options():
    model = build_model(
        "present_trail_mixer_pairset",
        input_bits=1536,
        hidden_bits=8,
        pair_bits=768,
        structure="SPN",
        model_options={
            "token_dim": 24,
            "mixer_depth": 1,
            "role_mixer_depth": 1,
            "pooling": "topk_mean",
            "top_k": 2,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, PresentTrailMixerPairSetDistinguisher)
    assert model.pair_bits == 768
    assert model.words_per_pair == 12
    assert model.token_dim == 24
    assert model.mixer_depth == 1
    assert model.role_mixer_depth == 1
    assert model.pooling == "topk_mean"
    assert model.top_k == 2
    assert model.lse_temperature == 0.5


def test_present_matrix_trail_hybrid_fuses_matrix_and_trail_pair_evidence():
    model = PresentMatrixTrailHybridPairSetDistinguisher(
        input_bits=1536,
        pair_bits=768,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        role_mixer_depth=1,
        matrix_depth=2,
        pooling="topk_logsumexp",
        top_k=1,
        lse_temperature=0.75,
    )
    batch = torch.randn((2, 1536), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.words_per_pair == 12
    assert model.trail_branch.words_per_pair == 12
    assert model.matrix_depth == 2
    assert model.fused_pair_embedding_bits == (
        model.trail_pair_embedding_bits + model.matrix_pair_embedding_bits
    )
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 2)
    assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [1, 1]
    assert logits.shape == (2, 1)


def test_build_model_supports_present_matrix_trail_hybrid_pairset_key_and_options():
    model = build_model(
        "present_matrix_trail_hybrid_pairset",
        input_bits=1536,
        hidden_bits=8,
        pair_bits=768,
        structure="SPN",
        model_options={
            "token_dim": 24,
            "mixer_depth": 1,
            "role_mixer_depth": 1,
            "matrix_depth": 2,
            "pooling": "topk_mean",
            "top_k": 2,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, PresentMatrixTrailHybridPairSetDistinguisher)
    assert model.pair_bits == 768
    assert model.words_per_pair == 12
    assert model.trail_branch.token_dim == 24
    assert model.trail_branch.mixer_depth == 1
    assert model.trail_branch.role_mixer_depth == 1
    assert model.matrix_depth == 2
    assert model.pooling == "topk_mean"
    assert model.top_k == 2
    assert model.lse_temperature == 0.5


def test_present_pairset_stats_hybrid_fuses_trail_and_cross_pair_statistics():
    model = PresentPairSetStatsHybridDistinguisher(
        input_bits=4992,
        pair_bits=2496,
        base_channels=8,
        token_dim=16,
        mixer_depth=1,
        role_mixer_depth=1,
        stats_hidden_bits=32,
    )
    batch = torch.randn((2, 4992), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.words_per_pair == 39
    assert model.cells_per_word == 16
    assert model.stats_feature_bits == 39 * 16 * 5 + 39 * 8
    assert model.fused_embedding_bits == model.trail_pair_embedding_bits * 3 + 32
    assert logits.shape == (2, 1)


def test_build_model_supports_present_pairset_stats_hybrid_key_and_options():
    model = build_model(
        "present_pairset_stats_hybrid",
        input_bits=4992,
        hidden_bits=8,
        pair_bits=2496,
        structure="SPN",
        model_options={
            "token_dim": 24,
            "mixer_depth": 1,
            "role_mixer_depth": 1,
            "stats_hidden_bits": 48,
            "activation": "silu",
            "norm": "rmsnorm",
            "dropout": 0.05,
        },
    )

    assert isinstance(model, PresentPairSetStatsHybridDistinguisher)
    assert model.pair_bits == 2496
    assert model.token_dim == 24
    assert model.trail_branch.mixer_depth == 1
    assert model.trail_branch.role_mixer_depth == 1
    assert model.stats_hidden_bits == 48
    assert model.activation == "silu"
    assert model.norm == "rmsnorm"
    assert model.dropout == 0.05


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


def test_spn_pairset_models_support_evidence_pooling_modes():
    for cls in (SpnNibbleConvPairSetDistinguisher, SpnTokenMixerPairSetDistinguisher):
        model = cls(
            input_bits=768,
            pair_bits=192,
            base_channels=8,
            pooling="topk_logsumexp",
            top_k=2,
            lse_temperature=0.7,
        )
        batch = torch.randn((2, 768), dtype=torch.float32)

        logits = model(batch)

        assert model.pooling == "topk_logsumexp"
        assert model.top_k == 2
        assert model.lse_temperature == 0.7
        assert model.last_attention_weights is not None
        assert model.last_attention_weights.shape == (2, 4)
        assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [2, 2]
        assert logits.shape == (2, 1)


def test_build_model_passes_spn_token_mixer_evidence_pooling_options():
    model = build_model(
        "spn_token_mixer_pairset",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
        model_options={
            "pooling": "topk_mean",
            "top_k": 3,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, SpnTokenMixerPairSetDistinguisher)
    assert model.pooling == "topk_mean"
    assert model.top_k == 3
    assert model.lse_temperature == 0.5


def test_build_model_passes_spn_nibble_conv_evidence_pooling_options():
    model = build_model(
        "spn_nibble_conv_pairset",
        input_bits=768,
        hidden_bits=8,
        pair_bits=192,
        structure="SPN",
        model_options={
            "pooling": "logsumexp",
            "top_k": 3,
            "lse_temperature": 0.8,
        },
    )

    assert isinstance(model, SpnNibbleConvPairSetDistinguisher)
    assert model.pooling == "logsumexp"
    assert model.top_k == 3
    assert model.lse_temperature == 0.8


def test_present_p_layer_mixer_block_uses_msb_ordered_present_adjacency():
    block = PresentPLayerMixerBlock(words_per_pair=2, token_dim=8)

    # Token 0 is the MSB nibble, i.e. PRESENT nibble 15. Bit 63 maps to itself.
    assert 0 in block.p_sources[0].tolist()
    # Token 15 is the LSB nibble, i.e. PRESENT nibble 0.
    assert block.p_sources.shape[0] == 16
    assert block.p_targets.shape[0] == 16


def test_present_p_layer_mixer_pairset_forward_and_position_mapping():
    model = PresentPLayerMixerPairSetDistinguisher(
        input_bits=512,
        pair_bits=128,
        base_channels=8,
        token_dim=16,
        mixer_depth=2,
        pooling="topk_logsumexp",
        top_k=2,
        lse_temperature=0.7,
    )
    batch = torch.randn((2, 512), dtype=torch.float32)

    logits = model(batch)

    assert model.structure == "SPN"
    assert model.words_per_pair == 2
    assert model.nibbles_per_pair == 32
    assert model.present_bit_to_input_position(63) == 0
    assert model.present_bit_to_input_position(0) == 63
    assert model.last_attention_weights is not None
    assert model.last_attention_weights.shape == (2, 4)
    assert torch.count_nonzero(model.last_attention_weights, dim=1).tolist() == [2, 2]
    assert logits.shape == (2, 1)


def test_build_model_supports_present_p_layer_mixer_pairset_key():
    model = build_model(
        "present_p_layer_mixer_pairset",
        input_bits=512,
        hidden_bits=8,
        pair_bits=128,
        structure="SPN",
        model_options={
            "token_dim": 24,
            "mixer_depth": 2,
            "pooling": "topk_mean",
            "top_k": 3,
            "lse_temperature": 0.5,
        },
    )

    assert isinstance(model, PresentPLayerMixerPairSetDistinguisher)
    assert model.token_dim == 24
    assert model.mixer_depth == 2
    assert model.pooling == "topk_mean"
    assert model.top_k == 3
    assert model.lse_temperature == 0.5


def test_adaptive_dbitnet_rejects_too_small_or_odd_inputs():
    with pytest.raises(ValueError, match="even number of input bits"):
        AdaptiveDBitNetDistinguisher(input_bits=95, base_channels=8)
    with pytest.raises(ValueError, match="at least 16 input bits"):
        AdaptiveDBitNetDistinguisher(input_bits=14, base_channels=8)


def test_spn_experts_are_available_from_modular_spn_module_and_legacy_path():
    assert ModularSpnCellPairSetDBitNetDistinguisher is SpnCellPairSetDBitNetDistinguisher
    assert ModularSpnNibbleConvPairSetDistinguisher is SpnNibbleConvPairSetDistinguisher
    assert ModularSpnTokenMixerPairSetDistinguisher is SpnTokenMixerPairSetDistinguisher
