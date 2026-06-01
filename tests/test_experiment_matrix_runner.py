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
        "resnet_bitslice",
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
    assert len(rows) == 9
    assert {(row["cipher"], row["model"]) for row in rows} == {
        ("SPECK32/64", "mlp"),
        ("SPECK32/64", "cnn"),
        ("SPECK32/64", "resnet_bitslice"),
        ("PRESENT-80", "mlp"),
        ("PRESENT-80", "cnn"),
        ("PRESENT-80", "resnet_bitslice"),
        ("SM4", "mlp"),
        ("SM4", "cnn"),
        ("SM4", "resnet_bitslice"),
    }
    assert all(0.0 <= row["metrics"]["accuracy"] <= 1.0 for row in rows)
    assert "wrote 9 rows" in completed.stdout


def test_run_innovation_one_matrix_can_execute_literature_ranked_plan(tmp_path: Path):
    plan_path = tmp_path / "plan.csv"
    output_path = tmp_path / "planned_results.jsonl"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,evidence,literature",
                "SPECK32/64,ARX,ResNet-BitSlice,resnet_bitslice,residual_cnn,1,26,1,0,8,gohr evidence,Gohr 2019",
                "PRESENT-80,SPN,CNN-SBoxLocal,cnn,cnn,1,22,1,0,8,spn evidence,Jain 2020",
            ]
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--plan",
            str(plan_path),
            "--epochs",
            "1",
            "--batch-size",
            "8",
            "--hidden-bits",
            "8",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 2
    assert rows[0]["model"] == "resnet_bitslice"
    assert rows[0]["architecture"] == "ResNet-BitSlice"
    assert rows[0]["architecture_rank"] == 1
    assert rows[0]["matching_score"] == 26
    assert rows[0]["matching_evidence"] == "gohr evidence"
    assert rows[0]["literature"] == "Gohr 2019"
    assert rows[1]["cipher"] == "PRESENT-80"
    assert "wrote 2 rows" in completed.stdout
