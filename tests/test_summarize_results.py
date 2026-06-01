import csv
import json
import subprocess
import sys
from pathlib import Path


def test_summarize_innovation_one_results_writes_csv(tmp_path: Path):
    input_path = tmp_path / "results.jsonl"
    output_path = tmp_path / "summary.csv"
    rows = [
        {
            "cipher": "SPECK32/64",
            "structure": "ARX",
            "model": "mlp",
            "architecture": "MLP-Baseline",
            "architecture_rank": 2,
            "matching_score": 2,
            "literature": "protocol evidence",
            "rounds": 1,
            "seed": 0,
            "difference_profile": "speck32_gohr2019",
            "difference_member": 0,
            "difference_source": "Gohr 2019 SPECK32/64 neural distinguisher",
            "samples_per_class": 8,
            "metrics": {"accuracy": 0.60, "auc": 0.70, "advantage": 0.20, "loss": 0.6},
        },
        {
            "cipher": "SPECK32/64",
            "structure": "ARX",
            "model": "mlp",
            "architecture": "MLP-Baseline",
            "architecture_rank": 2,
            "matching_score": 2,
            "literature": "protocol evidence",
            "rounds": 1,
            "seed": 1,
            "difference_profile": "speck32_gohr2019",
            "difference_member": 0,
            "difference_source": "Gohr 2019 SPECK32/64 neural distinguisher",
            "samples_per_class": 8,
            "metrics": {"accuracy": 0.80, "auc": 0.90, "advantage": 0.60, "loss": 0.4},
        },
    ]
    input_path.write_text("\n".join(json.dumps(row) for row in rows))

    subprocess.run(
        [
            sys.executable,
            "experiments/summarize_innovation_one_results.py",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        check=True,
    )

    summary_rows = list(csv.DictReader(output_path.open()))
    assert len(summary_rows) == 1
    assert summary_rows[0]["cipher"] == "SPECK32/64"
    assert summary_rows[0]["model"] == "mlp"
    assert summary_rows[0]["architecture"] == "MLP-Baseline"
    assert summary_rows[0]["architecture_rank"] == "2"
    assert summary_rows[0]["matching_score"] == "2"
    assert summary_rows[0]["literature"] == "protocol evidence"
    assert summary_rows[0]["difference_profile"] == "speck32_gohr2019"
    assert summary_rows[0]["difference_member"] == "0"
    assert "Gohr 2019" in summary_rows[0]["difference_source"]
    assert float(summary_rows[0]["accuracy_mean"]) == 0.70
    assert "calibrated_accuracy_mean" in summary_rows[0]
    assert int(summary_rows[0]["runs"]) == 2
