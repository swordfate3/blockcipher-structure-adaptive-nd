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
            "gate_mode": "hard",
            "samples_per_class": 8,
            "pairs_per_sample": 1,
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
            "gate_mode": "hard",
            "samples_per_class": 8,
            "pairs_per_sample": 1,
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
    assert summary_rows[0]["gate_mode"] == "hard"
    assert summary_rows[0]["pairs_per_sample"] == "1"
    assert float(summary_rows[0]["accuracy_mean"]) == 0.70
    assert "calibrated_accuracy_mean" in summary_rows[0]
    assert int(summary_rows[0]["runs"]) == 2


def test_summarize_innovation_one_results_runs_from_non_repo_cwd(tmp_path: Path):
    input_path = tmp_path / "results.jsonl"
    output_path = tmp_path / "summary.csv"
    input_path.write_text(
        json.dumps({
            "cipher": "PRESENT-80",
            "structure": "SPN",
            "model": "present_inception_mcnd",
            "architecture": "Present-Inception-MCND",
            "rounds": 7,
            "seed": 0,
            "samples_per_class": 8,
            "pairs_per_sample": 4,
            "metrics": {"accuracy": 0.5, "auc": 0.51, "advantage": 0.0, "loss": 0.69},
        })
        + "\n",
        encoding="utf-8",
    )
    script = Path.cwd() / "experiments" / "summarize_innovation_one_results.py"

    subprocess.run(
        [
            sys.executable,
            str(script),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=tmp_path,
        check=True,
    )

    summary_rows = list(csv.DictReader(output_path.open()))
    assert len(summary_rows) == 1
    assert summary_rows[0]["cipher"] == "PRESENT-80"


def test_summarize_innovation_one_results_keeps_pair_counts_separate(tmp_path: Path):
    input_path = tmp_path / "results.jsonl"
    output_path = tmp_path / "summary.csv"
    base_row = {
        "cipher": "SPECK32/64",
        "structure": "ARX",
        "model": "mlp",
        "architecture": "MLP-Baseline",
        "architecture_rank": "",
        "matching_score": "",
        "literature": "",
        "rounds": 6,
        "difference_profile": "speck32_gohr2019",
        "difference_member": 0,
        "difference_source": "Gohr 2019 SPECK32/64 neural distinguisher",
        "gate_mode": "",
        "samples_per_class": 8,
    }
    rows = [
        {
            **base_row,
            "seed": 0,
            "pairs_per_sample": 1,
            "metrics": {"accuracy": 0.55, "auc": 0.57, "advantage": 0.10, "loss": 0.7},
        },
        {
            **base_row,
            "seed": 0,
            "pairs_per_sample": 4,
            "metrics": {"accuracy": 0.63, "auc": 0.66, "advantage": 0.26, "loss": 0.6},
        },
    ]
    input_path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")

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
    assert len(summary_rows) == 2
    assert {row["pairs_per_sample"] for row in summary_rows} == {"1", "4"}
