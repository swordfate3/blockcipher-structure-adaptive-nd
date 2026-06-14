import csv
from pathlib import Path


def _rows(path: str):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_debug_large_gpu0_plan_covers_speck_and_present():
    rows = _rows("experiments/innovation1/plans/innovation1_debug_large_gpu0.csv")

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
    rows = _rows("experiments/innovation1/plans/innovation1_debug_large_gpu1.csv")

    assert len(rows) == 108
    assert {row["cipher"] for row in rows} == {"SM4"}
    assert {row["rounds"] for row in rows} == {"3", "4"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_xor_bits"}
    assert {row["difference_profile"] for row in rows} == {"sm4_yu2023_conv_resnet"}


def test_debug_large_plans_use_expected_model_set():
    rows = _rows("experiments/innovation1/plans/innovation1_debug_large_gpu0.csv") + _rows("experiments/innovation1/plans/innovation1_debug_large_gpu1.csv")

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
    rows = _rows("experiments/innovation1/plans/innovation1_structure_pairset_gpu0.csv")

    assert len(rows) == 72
    assert {row["cipher"] for row in rows} == {"SPECK32/64", "PRESENT-80"}
    assert {row["rounds"] for row in rows if row["cipher"] == "SPECK32/64"} == {"5", "6"}
    assert {row["rounds"] for row in rows if row["cipher"] == "PRESENT-80"} == {"4", "5"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}


def test_structure_pairset_gpu1_plan_covers_sm4():
    rows = _rows("experiments/innovation1/plans/innovation1_structure_pairset_gpu1.csv")

    assert len(rows) == 36
    assert {row["cipher"] for row in rows} == {"SM4"}
    assert {row["rounds"] for row in rows} == {"3", "4"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["pairs_per_sample"] for row in rows} == {"1", "2", "4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}


def test_structure_pairset_plans_use_expected_model_set():
    rows = _rows("experiments/innovation1/plans/innovation1_structure_pairset_gpu0.csv") + _rows("experiments/innovation1/plans/innovation1_structure_pairset_gpu1.csv")

    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "structure_adaptive_pairset_dbitnet",
        "moe_v4_soft",
    }


def test_spn_pairset_v2_plan_targets_present_with_expected_models():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_pairset_v2_present.csv")

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
    rows = _rows("experiments/innovation1/plans/innovation1_spn_token_mixer_present.csv")

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
    rows = _rows("experiments/innovation1/plans/innovation1_moe_v5_present.csv")

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


def test_moe_v5_hpo_best_validation_plan_targets_fixed_multiseed_protocol():
    rows = _rows("experiments/innovation1/plans/innovation1_moe_v5_hpo_best_validate_present.csv")

    assert len(rows) == 20
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"5"}
    assert {row["seed"] for row in rows} == {"0", "1", "2", "3", "4"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_xor_bits"}
    assert {row["difference_profile"] for row in rows} == {"present_wang_jain2021"}
    assert {row["difference_member"] for row in rows} == {"0"}
    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "moe_v4_soft",
        "moe_v5_soft",
        "moe_v5_soft_hpo_present_best",
    }


def test_moe_v5_hpo_multiseed_best_validation_plan_targets_fixed_multiseed_protocol():
    rows = _rows("experiments/innovation1/plans/innovation1_moe_v5_hpo_multiseed_best_validate_present.csv")

    assert len(rows) == 25
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"5"}
    assert {row["seed"] for row in rows} == {"0", "1", "2", "3", "4"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_xor_bits"}
    assert {row["difference_profile"] for row in rows} == {"present_wang_jain2021"}
    assert {row["difference_member"] for row in rows} == {"0"}
    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "moe_v4_soft",
        "moe_v5_soft",
        "moe_v5_soft_hpo_present_best",
        "moe_v5_soft_hpo_multiseed_present_best",
    }


def test_spn_aligned_present_plan_compares_raw_and_aligned_inputs():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_aligned_present.csv")

    assert len(rows) == 30
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"5"}
    assert {row["seed"] for row in rows} == {"0", "1", "2", "3", "4"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_spn_aligned_bits",
    }
    assert {row["model_key"] for row in rows} == {
        "adaptive_dbitnet_pairwise",
        "spn_token_mixer_pairset",
        "moe_v5_soft_hpo_present_best",
    }


def test_spn_aligned_present_confirm_plan_extends_to_ten_seeds():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_aligned_present_confirm.csv")

    assert len(rows) == 40
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"5"}
    assert {row["seed"] for row in rows} == {str(seed) for seed in range(10)}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_spn_aligned_bits",
    }
    assert {row["model_key"] for row in rows} == {
        "spn_token_mixer_pairset",
        "moe_v5_soft_hpo_present_best",
    }


def test_spn_present_highround_aligned_screen_targets_r7_r8_aligned_only():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_present_highround_aligned_screen.csv")

    assert len(rows) == 8
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"7", "8"}
    assert {row["seed"] for row in rows} == {"0", "1", "2", "3"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["samples_per_class"] for row in rows} == {"65536"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_xor_spn_aligned_bits"}
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["difference_profile"] for row in rows} == {"present_wang_jain2021"}
    assert {row["model_key"] for row in rows} == {"spn_token_mixer_pairset"}


def test_spn_present_paligned_integral_screen_uses_plaintext_integral_structure():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_present_paligned_integral_screen.csv")

    assert len(rows) == 8
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0", "1", "2", "3"}
    assert {row["samples_per_class"] for row in rows} == {"8192"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_xor_spn_paligned_bits"}
    assert {row["sample_structure"] for row in rows} == {"plaintext_integral_nibble"}
    assert {row["integral_active_nibble"] for row in rows} == {"0"}
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["model_key"] for row in rows} == {"spn_token_mixer_pairset"}


def test_spn_present_paligned_integral_nibble_scan_covers_all_active_nibbles():
    rows = []
    rows.extend(_rows("experiments/innovation1/plans/innovation1_spn_present_paligned_integral_nibble_scan_gpu0.csv"))
    rows.extend(_rows("experiments/innovation1/plans/innovation1_spn_present_paligned_integral_nibble_scan_gpu1.csv"))

    assert len(rows) == 32
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["samples_per_class"] for row in rows} == {"4096"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_xor_spn_paligned_bits"}
    assert {row["sample_structure"] for row in rows} == {"plaintext_integral_nibble"}
    assert {row["integral_active_nibble"] for row in rows} == {str(index) for index in range(16)}
    assert {row["model_key"] for row in rows} == {"spn_token_mixer_pairset"}


def test_spn_present_paligned_integral_selected_nibbles_confirm_plan():
    rows = []
    rows.extend(_rows("experiments/innovation1/plans/innovation1_spn_present_paligned_integral_selected_nibbles_confirm_gpu0.csv"))
    rows.extend(_rows("experiments/innovation1/plans/innovation1_spn_present_paligned_integral_selected_nibbles_confirm_gpu1.csv"))

    assert len(rows) == 30
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {str(seed) for seed in range(10)}
    assert {row["samples_per_class"] for row in rows} == {"16384"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_xor_spn_paligned_bits"}
    assert {row["sample_structure"] for row in rows} == {"plaintext_integral_nibble"}
    assert {row["integral_active_nibble"] for row in rows} == {"1", "7", "13"}
    assert sum(1 for row in rows if row["integral_active_nibble"] == "1") == 10
    assert sum(1 for row in rows if row["integral_active_nibble"] == "7") == 10
    assert sum(1 for row in rows if row["integral_active_nibble"] == "13") == 10
    assert {row["model_key"] for row in rows} == {"spn_token_mixer_pairset"}


def test_spn_present_inception_mcnd_smoke_plan_targets_present_r7_multipair_baseline():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_present_inception_mcnd_smoke.csv")

    assert len(rows) == 3
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0"}
    assert {row["samples_per_class"] for row in rows} == {"256"}
    assert {row["pairs_per_sample"] for row in rows} == {"4", "8", "16"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_bits"}
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["difference_profile"] for row in rows} == {"present_wang_jain2021"}
    assert {row["model_key"] for row in rows} == {"present_inception_mcnd"}


def test_spn_present_inception_mcnd_medium_plan_covers_r6_r7_multipair_baseline():
    rows = _rows("experiments/innovation1/plans/innovation1_spn_present_inception_mcnd_medium.csv")

    assert len(rows) == 18
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0", "1", "2"}
    assert {row["samples_per_class"] for row in rows} == {"8192"}
    assert {row["pairs_per_sample"] for row in rows} == {"4", "8", "16"}
    assert {row["feature_encoding"] for row in rows} == {"ciphertext_pair_bits"}
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["difference_profile"] for row in rows} == {"present_wang_jain2021"}
    assert {row["model_key"] for row in rows} == {"present_inception_mcnd"}
