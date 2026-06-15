import csv
import importlib.util
import json
import sys
from pathlib import Path


def _load_build_plan_module():
    script_path = Path(__file__).resolve().parents[1] / "experiments" / "build_plan.py"
    spec = importlib.util.spec_from_file_location("build_plan", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_plan_generates_cartesian_csv_from_json_config(tmp_path: Path):
    module = _load_build_plan_module()
    config_path = tmp_path / "plan.json"
    output_path = tmp_path / "generated.csv"
    config_path.write_text(
        json.dumps(
            {
                "output": str(output_path),
                "defaults": {
                    "cipher": "PRESENT-80",
                    "structure": "SPN",
                    "network": "SPN-TokenMixer-PairSet",
                    "model_key": "spn_token_mixer_pairset",
                    "family": "spn_token_mixer",
                    "architecture_rank": 0,
                    "score": 70,
                    "samples_per_class": 32768,
                    "pairs_per_sample": 4,
                    "negative_mode": "encrypted_random_plaintexts",
                    "train_key": "0x00000000000000000000",
                    "validation_key": "0x11111111111111111111",
                    "difference_profile": "present_wang_jain2021",
                    "difference_member": 0,
                    "evidence": "test evidence",
                    "literature": "test literature",
                },
                "sweep": {
                    "rounds": [5, 6],
                    "feature_encoding": [
                        "ciphertext_pair_xor_bits",
                        "ciphertext_pair_xor_spn_aligned_bits",
                    ],
                    "seed": {"range": [0, 3]},
                },
            }
        ),
        encoding="utf-8",
    )

    rows = module.build_plan_rows(module.load_plan_config(config_path))
    module.write_plan(rows, output_path)

    with output_path.open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))

    assert len(csv_rows) == 12
    assert {row["rounds"] for row in csv_rows} == {"5", "6"}
    assert {row["seed"] for row in csv_rows} == {"0", "1", "2"}
    assert {row["feature_encoding"] for row in csv_rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_spn_aligned_bits",
    }
    assert csv_rows[0]["cipher"] == "PRESENT-80"
    assert csv_rows[0]["model_key"] == "spn_token_mixer_pairset"


def test_existing_present_strict_config_matches_committed_plan_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "spn_present_strict_crosskey_10seed.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 40
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {str(row["rounds"]) for row in rows} == {"5", "6"}
    assert {str(row["seed"]) for row in rows} == {str(seed) for seed in range(10)}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_spn_aligned_bits",
    }
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}


def test_gift64_spn_aligned_screen_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "spn_gift64_aligned_screen.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 24
    assert {row["cipher"] for row in rows} == {"GIFT-64"}
    assert {str(row["rounds"]) for row in rows} == {"4", "5", "6"}
    assert {str(row["seed"]) for row in rows} == {"0", "1", "2", "3"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_spn_aligned_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"gift64_shen2024_spn_screen"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}


def test_gift64_spn_aligned_confirm_10seed_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "spn_gift64_aligned_confirm_10seed.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 40
    assert {row["cipher"] for row in rows} == {"GIFT-64"}
    assert {str(row["rounds"]) for row in rows} == {"5", "6"}
    assert {str(row["seed"]) for row in rows} == {str(seed) for seed in range(10)}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_spn_aligned_bits",
    }
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}
    assert {row["difference_profile"] for row in rows} == {"gift64_shen2024_spn_screen"}

def test_speck32_arx_aligned_screen_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "arx_speck32_aligned_screen.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 16
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {str(row["rounds"]) for row in rows} == {"6", "7"}
    assert {str(row["seed"]) for row in rows} == {"0", "1", "2", "3"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_aligned_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}

def test_speck32_arx_v2_feature_screen_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "arx_speck32_v2_feature_screen.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 32
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {str(row["rounds"]) for row in rows} == {"6", "7"}
    assert {str(row["seed"]) for row in rows} == {"0", "1", "2", "3"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_aligned_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
        "ciphertext_pair_xor_arx_partial_inverse_rx_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}

def test_speck32_arx_v2_confirm_10seed_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "arx_speck32_v2_confirm_10seed.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 30
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {str(row["rounds"]) for row in rows} == {"7"}
    assert {str(row["seed"]) for row in rows} == {str(seed) for seed in range(10)}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_aligned_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}
    assert {row["negative_mode"] for row in rows} == {"encrypted_random_plaintexts"}

def test_speck32_arx_v2_scale_m_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "arx_speck32_v2_scale_m.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 8
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {str(row["rounds"]) for row in rows} == {"7"}
    assert {str(row["seed"]) for row in rows} == {"0", "1", "2", "3"}
    assert {str(row["samples_per_class"]) for row in rows} == {"131072"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}


def test_speck32_arx_round_hybrid_rx_smoke_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "arx_speck32_round_hybrid_rx_smoke.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 4
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {"arx_round_function_hybrid_pairset"}
    assert {row["family"] for row in rows} == {"arx_round_function_hybrid_rx_smoke"}
    assert {str(row["rounds"]) for row in rows} == {"6", "7"}
    assert {str(row["seed"]) for row in rows} == {"0", "1"}
    assert {str(row["samples_per_class"]) for row in rows} == {"32768"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_arx_partial_inverse_rx_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}


def test_speck32_arx_round_hybrid_rx_r7_confirm_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 10
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {"arx_round_function_hybrid_pairset"}
    assert {row["family"] for row in rows} == {"arx_round_function_hybrid_rx_confirm"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {str(seed) for seed in range(10)}
    assert {row["samples_per_class"] for row in rows} == {"131072"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_arx_partial_inverse_rx_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["loss"] for row in rows} == {"mse"}
    assert {row["lr_scheduler"] for row in rows} == {"cyclic"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows} == {"6"}
    assert {row["pretrain_epochs"] for row in rows} == {"6"}


def test_present_delta_sinv_beamstats4deep3_r7_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_spn_present_delta_sinv_beamstats4deep3_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 4
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["samples_per_class"] for row in rows} == {"65536"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {
        "present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"zhang_wang_case2_mcnd"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows} == {"6"}
    assert {row["pretrain_epochs"] for row in rows} == {"6"}
    assert {row["model_key"] for row in rows} == {
        "present_matrix_trail_hybrid_pairset",
        "present_trail_mixer_pairset",
    }


def test_present_delta_only_structural_r7_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_spn_present_delta_only_structural_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 12
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0", "1", "2"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {
        "present_xor_paligned_cell_matrix_bits",
        "present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits",
    }
    assert {row["samples_per_class"] for row in rows if row["rounds"] == "6"} == {"32768"}
    assert {row["samples_per_class"] for row in rows if row["rounds"] == "7"} == {"65536"}
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"zhang_wang_case2_mcnd"}
    assert {row["difference_profile"] for row in rows} == {"present_zhang_wang2022_mcnd"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows if row["rounds"] == "7"} == {"6"}
    assert {row["pretrain_epochs"] for row in rows if row["rounds"] == "7"} == {"4"}
    assert {row["model_key"] for row in rows} == {
        "present_inception_mcnd_matrix",
        "present_matrix_trail_hybrid_pairset",
    }


def test_speck32_arx_carrychain_micro_smoke_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_carrychain_micro_smoke.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 2
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {"arx_round_function_hybrid_pairset"}
    assert {row["family"] for row in rows} == {"arx_round_function_hybrid_carrychain_micro_smoke"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0"}
    assert {row["samples_per_class"] for row in rows} == {"8192"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["loss"] for row in rows} == {"mse"}
    assert {row["lr_scheduler"] for row in rows} == {"cyclic"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows if row["rounds"] == "7"} == {"6"}
    assert {row["pretrain_epochs"] for row in rows if row["rounds"] == "7"} == {"2"}


def test_speck32_arx_carrychain_plus_micro_smoke_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_carrychain_plus_micro_smoke.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 2
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {"arx_round_function_hybrid_pairset"}
    assert {row["family"] for row in rows} == {"arx_round_function_hybrid_carrychain_plus_micro_smoke"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0"}
    assert {row["samples_per_class"] for row in rows} == {"8192"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_plus_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["loss"] for row in rows} == {"mse"}
    assert {row["lr_scheduler"] for row in rows} == {"cyclic"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows if row["rounds"] == "7"} == {"6"}
    assert {row["pretrain_epochs"] for row in rows if row["rounds"] == "7"} == {"2"}


def test_speck32_arx_gohr_protocol_alignment_smoke_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_gohr_protocol_alignment_smoke.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 10
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0"}
    assert {row["samples_per_class"] for row in rows} == {"16384"}
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows if row["rounds"] == "7"} == {"6"}
    assert {row["pretrain_epochs"] for row in rows if row["rounds"] == "7"} == {"3"}

    single_pair_rows = [row for row in rows if row["model_key"] == "gohr_resnet_speck_depth10"]
    assert len(single_pair_rows) == 2
    assert {row["pairs_per_sample"] for row in single_pair_rows} == {"1"}
    assert {row["feature_encoding"] for row in single_pair_rows} == {"ciphertext_pair_bits"}

    pairset_rows = [row for row in rows if row["model_key"] != "gohr_resnet_speck_depth10"]
    assert len(pairset_rows) == 8
    assert {row["pairs_per_sample"] for row in pairset_rows} == {"4"}
    assert {row["feature_encoding"] for row in pairset_rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
        "ciphertext_pair_xor_arx_partial_inverse_rx_bits",
        "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits",
    }


def test_present_sinv_curriculum_r7_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_spn_present_sinv_curriculum_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 6
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["model_key"] for row in rows} == {"present_inception_mcnd_matrix"}
    assert {row["family"] for row in rows} == {"present_sinv_curriculum_matrix"}
    assert {row["rounds"] for row in rows} == {"6", "7"}
    assert {row["seed"] for row in rows} == {"0", "1", "2"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["samples_per_class"] for row in rows if row["rounds"] == "6"} == {"32768"}
    assert {row["samples_per_class"] for row in rows if row["rounds"] == "7"} == {"65536"}
    assert {row["feature_encoding"] for row in rows} == {
        "present_pair_xor_paligned_sinv_cell_matrix_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"zhang_wang_case2_mcnd"}
    assert {row["loss"] for row in rows} == {"mse"}
    assert {row["lr_scheduler"] for row in rows} == {"cyclic"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows if row["rounds"] == "7"} == {"6"}
    assert {row["pretrain_epochs"] for row in rows if row["rounds"] == "7"} == {"6"}


def test_present_parameterized_sboxddt_beam8deep4_r7_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_spn_present_parameterized_sboxddt_beam8deep4_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 8
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["samples_per_class"] for row in rows} == {"65536"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {
        "present_pair_xor_paligned_sboxddt_beam8deep4_cell_matrix_bits",
        "present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits",
    }
    assert {row["model_key"] for row in rows} == {
        "present_matrix_trail_hybrid_pairset",
        "present_trail_mixer_pairset",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"zhang_wang_case2_mcnd"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows} == {"6"}
    assert {row["pretrain_epochs"] for row in rows} == {"6"}


def test_present_stats_hybrid_beamstats8deep4_r7_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 4
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["model_key"] for row in rows} == {"present_pairset_stats_hybrid"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["samples_per_class"] for row in rows} == {"65536"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {
        "present_pair_xor_paligned_sboxddt_beam8deep4_cell_matrix_bits",
        "present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"zhang_wang_case2_mcnd"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows} == {"6"}
    assert {row["pretrain_epochs"] for row in rows} == {"6"}


def test_present_histogram_hybrid_beamstats8deep4_r7_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_spn_present_histogram_hybrid_beamstats8deep4_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 4
    assert {row["cipher"] for row in rows} == {"PRESENT-80"}
    assert {row["structure"] for row in rows} == {"SPN"}
    assert {row["model_key"] for row in rows} == {"present_pairset_histogram_hybrid"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["samples_per_class"] for row in rows} == {"65536"}
    assert {row["pairs_per_sample"] for row in rows} == {"16"}
    assert {row["feature_encoding"] for row in rows} == {
        "present_pair_xor_paligned_sboxddt_beam8deep4_cell_matrix_bits",
        "present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"zhang_wang_case2_mcnd"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows} == {"6"}
    assert {row["pretrain_epochs"] for row in rows} == {"6"}


def test_speck32_arx_partial_inverse_r7_clean_ablation_10seed_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_partial_inverse_r7_clean_ablation_10seed.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 20
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {"structure_adaptive_pairset_dbitnet"}
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {str(seed) for seed in range(10)}
    assert {row["samples_per_class"] for row in rows} == {"131072"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}


def test_speck32_arx_partial_inverse_r8_boundary_10seed_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_partial_inverse_r8_boundary_10seed.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 20
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {"structure_adaptive_pairset_dbitnet"}
    assert {row["rounds"] for row in rows} == {"8"}
    assert {row["seed"] for row in rows} == {str(seed) for seed in range(10)}
    assert {row["samples_per_class"] for row in rows} == {"262144"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}


def test_speck32_arx_stats_hybrid_r7_screen_plan_shape():
    repo_root = Path(__file__).resolve().parents[1]
    plan_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "plans"
        / "innovation1_arx_speck32_stats_hybrid_r7_screen.csv"
    )

    with plan_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 4
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {row["model_key"] for row in rows} == {
        "structure_adaptive_pairset_dbitnet",
        "arx_pairset_stats_hybrid",
    }
    assert {row["rounds"] for row in rows} == {"7"}
    assert {row["seed"] for row in rows} == {"0", "1"}
    assert {row["samples_per_class"] for row in rows} == {"131072"}
    assert {row["pairs_per_sample"] for row in rows} == {"4"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_arx_partial_inverse_bits",
    }
    assert {row["key_rotation_interval"] for row in rows} == {"1024"}
    assert {row["sample_structure"] for row in rows} == {"independent_pairs"}
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {row["checkpoint_metric"] for row in rows} == {"val_auc"}
    assert {row["pretrain_rounds"] for row in rows} == {"6"}
    assert {row["pretrain_epochs"] for row in rows} == {"4"}


def test_speck32_arx_v2_scale_l_config_shape():
    module = _load_build_plan_module()
    repo_root = Path(__file__).resolve().parents[1]
    config_path = repo_root / "experiments" / "innovation1" / "configs" / "arx_speck32_v2_scale_l.json"
    rows = module.build_plan_rows(module.load_plan_config(config_path))

    assert len(rows) == 8
    assert {row["cipher"] for row in rows} == {"SPECK32/64"}
    assert {row["structure"] for row in rows} == {"ARX"}
    assert {str(row["rounds"]) for row in rows} == {"7"}
    assert {str(row["seed"]) for row in rows} == {"0", "1", "2", "3"}
    assert {str(row["samples_per_class"]) for row in rows} == {"524288"}
    assert {row["feature_encoding"] for row in rows} == {
        "ciphertext_pair_xor_bits",
        "ciphertext_pair_xor_arx_partial_inverse_bits",
    }
    assert {row["difference_profile"] for row in rows} == {"speck32_gohr2019"}
    assert {str(row["pairs_per_sample"]) for row in rows} == {"4"}
