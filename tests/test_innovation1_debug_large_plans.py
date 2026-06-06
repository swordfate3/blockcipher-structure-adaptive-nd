import csv
from pathlib import Path


def _rows(path: str):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_debug_large_gpu0_plan_covers_speck_and_present():
    rows = _rows("experiments/plans/innovation1_debug_large_gpu0.csv")

    assert len(rows) == 216
    assert {row["cipher"] for row in rows} == {"SPECK32/64", "PRESENT-80"}
    assert {row["rounds"] for row in rows if row["cipher"] == "SPECK32/64"} == {"5", "6"}
    assert {row["rounds"] for row in rows if row["cipher"] == "PRESENT-80"} == {"4", "5"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_xor_bits"}
    assert {row["difference_profile"] for row in rows if row["cipher"] == "SPECK32/64"} == {"speck32_gohr2019"}
    assert {row["difference_profile"] for row in rows if row["cipher"] == "PRESENT-80"} == {"present_wang_jain2021"}


def test_debug_large_gpu1_plan_covers_sm4():
    rows = _rows("experiments/plans/innovation1_debug_large_gpu1.csv")

    assert len(rows) == 108
    assert {row["cipher"] for row in rows} == {"SM4"}
    assert {row["rounds"] for row in rows} == {"3", "4"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_xor_bits"}
    assert {row["difference_profile"] for row in rows} == {"sm4_yu2023_conv_resnet"}


def test_debug_large_plans_use_expected_model_set():
    rows = _rows("experiments/plans/innovation1_debug_large_gpu0.csv") + _rows("experiments/plans/innovation1_debug_large_gpu1.csv")

    assert {row["model_key"] for row in rows} == {
        "mlp",
        "adaptive_dbitnet",
        "adaptive_dbitnet_pairwise",
        "resnet_bitslice",
        "senet_resnext",
        "multiscale_dense_resnet",
        "moe_v4_hard",
        "moe_v4_soft",
        "selector_rule_v2",
    }


def test_structure_pairset_gpu0_plan_covers_speck_and_present():
    rows = _rows("experiments/plans/innovation1_structure_pairset_gpu0.csv")

    assert len(rows) == 72
    assert {row["cipher"] for row in rows} == {"SPECK32/64", "PRESENT-80"}
    assert {row["rounds"] for row in rows if row["cipher"] == "SPECK32/64"} == {"5", "6"}
    assert {row["rounds"] for row in rows if row["cipher"] == "PRESENT-80"} == {"4", "5"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}


def test_structure_pairset_gpu1_plan_covers_sm4():
    rows = _rows("experiments/plans/innovation1_structure_pairset_gpu1.csv")

    assert len(rows) == 36
    assert {row["cipher"] for row in rows} == {"SM4"}
    assert {row["rounds"] for row in rows} == {"3", "4"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}


def test_structure_pairset_plans_use_expected_model_set():
    rows = _rows("experiments/plans/innovation1_structure_pairset_gpu0.csv") + _rows("experiments/plans/innovation1_structure_pairset_gpu1.csv")

    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "structure_adaptive_pairset_dbitnet",
        "moe_v4_soft",
    }


def test_spn_pairset_v2_plan_targets_present_with_expected_models():
    rows = _rows("experiments/plans/innovation1_spn_pairset_v2_present.csv")

    assert len(rows) == 48
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"4", "5"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "structure_adaptive_pairset_dbitnet",
        "spn_pairset_dbitnet_v2",
        "moe_v4_soft",
    }


def test_spn_token_mixer_plan_targets_present_r5_pairset_comparison():
    rows = _rows("experiments/plans/innovation1_spn_token_mixer_present.csv")

    assert len(rows) == 10
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"5"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "spn_pairset_dbitnet_v2",
        "spn_nibble_conv_pairset",
        "spn_token_mixer_pairset",
        "moe_v4_soft",
    }


def test_moe_v5_plan_targets_present_r5_structure_expert_comparison():
    rows = _rows("experiments/plans/innovation1_moe_v5_present.csv")

    assert len(rows) == 10
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"5"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "spn_token_mixer_pairset",
        "moe_v4_soft",
        "moe_v5_hard",
        "moe_v5_soft",
    }
