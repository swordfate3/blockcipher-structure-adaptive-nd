import json
import subprocess
import sys
from pathlib import Path


def test_run_innovation_one_matrix_writes_jsonl_rows(tmp_path: Path):
    output_path = tmp_path / "matrix.jsonl"
    command = [
        sys.executable,
        "experiments/run_innovation_one_matrix.py",
        "--ciphers",
        "speck32",
        "present80",
        "sm4",
        "--models",
        "mlp",
        "cnn",
        "--rounds",
        "1",
        "--seeds",
        "0",
        "--samples-per-class",
        "8",
        "--epochs",
        "1",
        "--batch-size",
        "8",
        "--hidden-bits",
        "8",
        "--output",
        str(output_path),
    ]

    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 6
    assert {(row["cipher"], row["model"]) for row in rows} == {
        ("SPECK32/64", "mlp"),
        ("SPECK32/64", "cnn"),
        ("PRESENT-80", "mlp"),
        ("PRESENT-80", "cnn"),
        ("SM4", "mlp"),
        ("SM4", "cnn"),
    }
    assert all(0.0 <= row["metrics"]["accuracy"] <= 1.0 for row in rows)
    assert "wrote 6 rows" in completed.stdout
