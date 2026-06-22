import csv
import importlib.util
import json
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "innovation1"
    / "validate_result_plan_alignment.py"
)
SPEC = importlib.util.spec_from_file_location("validate_result_plan_alignment", SCRIPT)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
validate_result_plan_alignment = MODULE.validate_result_plan_alignment


def _write_plan(path: Path, rows: list[dict]) -> None:
    fieldnames = [
        "cipher",
        "structure",
        "model_key",
        "rounds",
        "seed",
        "samples_per_class",
        "feature_encoding",
        "negative_mode",
        "train_key",
        "validation_key",
        "pairs_per_sample",
        "sample_structure",
        "integral_active_nibble",
        "key_rotation_interval",
        "difference_profile",
        "difference_member",
        "loss",
        "learning_rate",
        "optimizer",
        "weight_decay",
        "checkpoint_metric",
        "restore_best_checkpoint",
        "early_stopping_patience",
        "early_stopping_min_delta",
        "pretrain_epochs",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_results(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def _plan_row(rounds: int, seed: int) -> dict:
    return {
        "cipher": "PRESENT-80",
        "structure": "SPN",
        "model_key": "present_inception_mcnd_matrix",
        "rounds": rounds,
        "seed": seed,
        "samples_per_class": 65536,
        "feature_encoding": "present_pair_xor_paligned_sinv_cell_matrix_bits",
        "negative_mode": "encrypted_random_plaintexts",
        "train_key": "0x00000000000000000000",
        "validation_key": "0xffffffffffffffffffff",
        "pairs_per_sample": 16,
        "sample_structure": "zhang_wang_case2_mcnd",
        "integral_active_nibble": 0,
        "key_rotation_interval": 1024,
        "difference_profile": "present_zhang_wang2022_mcnd",
        "difference_member": 0,
        "loss": "mse",
        "learning_rate": 0.0001,
        "optimizer": "adam",
        "weight_decay": 1e-05,
        "checkpoint_metric": "val_auc",
        "restore_best_checkpoint": "true",
        "early_stopping_patience": 0,
        "early_stopping_min_delta": 0.0,
        "pretrain_epochs": 6,
    }


def _result_row(rounds: int, seed: int, *, model_key: str | None = None) -> dict:
    row = _plan_row(rounds, seed)
    if model_key is not None:
        row["model_key"] = model_key
    row["model"] = row.pop("model_key")
    row["selected_model"] = row["model"]
    row["metrics"] = {"auc": 0.67, "calibrated_accuracy": 0.62}
    row["train_key"] = 0
    row["validation_key"] = int("f" * 20, 16)
    row["training"] = {
        "loss": "mse",
        "learning_rate": 0.0001,
        "optimizer": "adam",
        "weight_decay": 1e-05,
        "checkpoint_metric": "val_auc",
        "restore_best_checkpoint": True,
        "early_stopping_patience": 0,
        "early_stopping_min_delta": 0.0,
        "pretraining": {"epochs_ran": 6},
    }
    return row


def test_result_plan_alignment_accepts_exact_round_seed_and_fields(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    _write_plan(plan, [_plan_row(7, 0), _plan_row(7, 1), _plan_row(8, 0)])
    _write_results(results, [_result_row(7, 0), _result_row(7, 1), _result_row(8, 0)])

    report = validate_result_plan_alignment(plan, results, expected_rows=3)

    assert report["status"] == "pass"
    assert report["errors"] == []


def test_result_plan_alignment_rejects_missing_and_unexpected_round_seed(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    _write_plan(plan, [_plan_row(7, 0), _plan_row(7, 1)])
    _write_results(results, [_result_row(7, 0), _result_row(7, 2)])

    report = validate_result_plan_alignment(plan, results, expected_rows=2)

    assert report["status"] == "fail"
    assert report["missing_result_keys"] == [(7, 1, "present_inception_mcnd_matrix", 65536)]
    assert report["unexpected_result_keys"] == [(7, 2, "present_inception_mcnd_matrix", 65536)]


def test_result_plan_alignment_rejects_duplicate_result_round_seed(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    _write_plan(plan, [_plan_row(7, 0), _plan_row(7, 1)])
    _write_results(results, [_result_row(7, 0), _result_row(7, 0)])

    report = validate_result_plan_alignment(plan, results, expected_rows=2)

    assert report["status"] == "fail"
    assert report["duplicate_result_keys"] == [(7, 0, "present_inception_mcnd_matrix", 65536)]
    assert report["missing_result_keys"] == [(7, 1, "present_inception_mcnd_matrix", 65536)]


def test_result_plan_alignment_rejects_field_mismatch(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    bad_result = _result_row(7, 0)
    bad_result["feature_encoding"] = "wrong_feature"
    _write_plan(plan, [_plan_row(7, 0)])
    _write_results(results, [bad_result])

    report = validate_result_plan_alignment(plan, results, expected_rows=1)

    assert report["status"] == "fail"
    assert report["field_mismatches"][0]["plan_field"] == "feature_encoding"


def test_result_plan_alignment_rejects_samples_per_class_mismatch(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    bad_result = _result_row(7, 0)
    bad_result["samples_per_class"] = 131072
    _write_plan(plan, [_plan_row(7, 0)])
    _write_results(results, [bad_result])

    report = validate_result_plan_alignment(plan, results, expected_rows=1)

    assert report["status"] == "fail"
    assert report["missing_result_keys"] == [(7, 0, "present_inception_mcnd_matrix", 65536)]
    assert report["unexpected_result_keys"] == [(7, 0, "present_inception_mcnd_matrix", 131072)]


def test_result_plan_alignment_rejects_training_protocol_mismatch(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    bad_result = _result_row(7, 0)
    bad_result["training"]["optimizer"] = "adamw"
    _write_plan(plan, [_plan_row(7, 0)])
    _write_results(results, [bad_result])

    report = validate_result_plan_alignment(plan, results, expected_rows=1)

    assert report["status"] == "fail"
    assert report["field_mismatches"][0]["plan_field"] == "optimizer"


def test_result_plan_alignment_accepts_same_round_seed_for_distinct_models(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    model_a = "present_matrix_trail_hybrid_pairset"
    model_b = "present_trail_mixer_pairset"
    row_a = _plan_row(7, 0)
    row_a["model_key"] = model_a
    row_b = _plan_row(7, 0)
    row_b["model_key"] = model_b
    _write_plan(plan, [row_a, row_b])
    _write_results(
        results,
        [
            _result_row(7, 0, model_key=model_a),
            _result_row(7, 0, model_key=model_b),
        ],
    )

    report = validate_result_plan_alignment(plan, results, expected_rows=2)

    assert report["status"] == "pass"
    assert report["plan_keys"] == [(7, 0, model_a, 65536), (7, 0, model_b, 65536)]


def test_result_plan_alignment_accepts_scale_ladder_rows_with_same_round_seed_model(tmp_path: Path):
    plan = tmp_path / "plan.csv"
    results = tmp_path / "results.jsonl"
    row_64k = _plan_row(7, 0)
    row_256k = _plan_row(7, 0)
    row_256k["samples_per_class"] = 262144
    result_64k = _result_row(7, 0)
    result_256k = _result_row(7, 0)
    result_256k["samples_per_class"] = 262144
    _write_plan(plan, [row_64k, row_256k])
    _write_results(results, [result_64k, result_256k])

    report = validate_result_plan_alignment(plan, results, expected_rows=2)

    assert report["status"] == "pass"
    assert report["plan_keys"] == [
        (7, 0, "present_inception_mcnd_matrix", 65536),
        (7, 0, "present_inception_mcnd_matrix", 262144),
    ]
