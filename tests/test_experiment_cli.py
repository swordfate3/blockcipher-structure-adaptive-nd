import json
import subprocess
import sys
from pathlib import Path


def test_run_innovation_one_smoke_writes_json_result(tmp_path: Path):
    output_path = tmp_path / "result.json"
    command = [
        sys.executable,
        "experiments/run_innovation_one_smoke.py",
        "--cipher",
        "speck32",
        "--rounds",
        "2",
        "--samples-per-class",
        "16",
        "--epochs",
        "1",
        "--batch-size",
        "16",
        "--hidden-bits",
        "16",
        "--output",
        str(output_path),
    ]

    completed = subprocess.run(command, check=True, capture_output=True, text=True)

    payload = json.loads(output_path.read_text())
    assert completed.returncode == 0
    assert payload["cipher"] == "SPECK32/64"
    assert payload["model"] == "MlpDistinguisher"
    assert payload["rounds"] == 2
    assert payload["samples_per_class"] == 16
    assert 0.0 <= payload["metrics"]["accuracy"] <= 1.0
    assert "accuracy" in completed.stdout
