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
    config_path = repo_root / "experiments" / "configs" / "innovation1" / "spn_present_strict_crosskey_10seed.json"
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
