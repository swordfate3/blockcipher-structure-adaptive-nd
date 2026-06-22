import importlib.util
import json
import pickle
import subprocess
import sys
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "innovation1"
    / "evaluate_zhang_wang_official_checkpoint.py"
)
SPEC = importlib.util.spec_from_file_location("evaluate_zhang_wang_official_checkpoint", SCRIPT)
assert SPEC is not None
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _write_history(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        pickle.dump(
            {
                "val_acc": [0.7116569876670837, 0.7225639820098877],
                "val_loss": [0.19100874662399292, 0.18307027220726013],
                "loss": [0.2, 0.18],
                "acc": [0.7, 0.72],
                "lr": [0.002, 0.0001],
            },
            handle,
        )


def test_summarize_history_reports_official_best_val_acc(tmp_path: Path):
    history_path = tmp_path / "present_hist7r_pairs16_nm.p"
    _write_history(history_path)

    summary = MODULE.summarize_history(history_path)

    assert summary["exists"] is True
    assert summary["epochs"] == 2
    assert summary["best_val_acc"] == 0.7225639820098877
    assert summary["best_val_acc_epoch"] == 2
    assert summary["best_val_acc_minus_reference"] == 0.002063982
    assert summary["best_val_loss"] == 0.18307027220726013


def test_cli_audits_checkpoint_and_history_without_tensorflow(tmp_path: Path):
    audit_root = tmp_path / "audit"
    checkpoint = audit_root / "DATA_Nm_good_trained_nets" / "present_best_7r_pairs16_distinguisher.h5"
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    checkpoint.write_bytes(b"fake-h5")
    _write_history(audit_root / "present_hist7r_pairs16_nm.p")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--audit-root",
            str(audit_root),
            "--raw-pair-count",
            "160",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["checkpoint"]["exists"] is True
    assert summary["checkpoint"]["size_bytes"] == 7
    assert summary["history"]["best_val_acc"] == 0.7225639820098877
    assert summary["protocol"]["grouped_eval_rows"] == 10
    assert summary["evaluation"]["status"] == "not_run"


def test_run_eval_reports_missing_dependencies_before_loading_checkpoint(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(MODULE, "dependency_status", lambda: {"tensorflow": False, "h5py": False})

    result = MODULE.run_checkpoint_eval(
        audit_root=tmp_path,
        checkpoint_path=tmp_path / "missing.h5",
        rounds=7,
        pairs=16,
        diff=0x9,
        raw_pair_count=160,
        batch_size=1000,
    )

    assert result["status"] == "missing_dependencies"
    assert result["missing_dependencies"] == ["tensorflow", "h5py"]
