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
        "--feature-encoding",
        "ciphertext_pair_xor_bits",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
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
    assert rows[0]["feature_encoding"] == "ciphertext_pair_xor_bits"
    assert rows[0]["training"]["input_bits"] == 96
    assert rows[1]["cipher"] == "PRESENT-80"
    assert "wrote 2 rows" in completed.stdout


def test_run_innovation_one_matrix_can_use_literature_difference_profile(tmp_path: Path):
    output_path = tmp_path / "speck_profile.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "mlp",
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
            "--difference-profile",
            "speck32_gohr2019",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["input_difference"] == 0x00400000
    assert rows[0]["difference_profile"] == "speck32_gohr2019"
    assert rows[0]["difference_member"] == 0
    assert "Gohr 2019" in rows[0]["difference_source"]


def test_run_innovation_one_matrix_records_multi_pair_samples(tmp_path: Path):
    output_path = tmp_path / "multi_pair.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "mlp",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["pairs_per_sample"] == 2
    assert rows[0]["training"]["pairs_per_sample"] == 2
    assert rows[0]["training"]["input_bits"] == 192


def test_run_innovation_one_matrix_accepts_explicit_device(tmp_path: Path):
    output_path = tmp_path / "device.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "mlp",
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
            "--device",
            "cpu",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["training"]["device"] == "cpu"


def test_run_innovation_one_matrix_passes_gohr_style_training_options(tmp_path: Path):
    output_path = tmp_path / "training_options.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "gohr_resnet_speck_depth10",
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
            "--difference-profile",
            "speck32_gohr2019",
            "--optimizer",
            "adamw",
            "--amsgrad",
            "--weight-decay",
            "0.0001",
            "--lr-scheduler",
            "cyclic",
            "--max-learning-rate",
            "0.003",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["model"] == "gohr_resnet_speck_depth10"
    assert rows[0]["training"]["optimizer"] == "adamw"
    assert rows[0]["training"]["amsgrad"] is True
    assert rows[0]["training"]["weight_decay"] == 0.0001
    assert rows[0]["training"]["lr_scheduler"] == "cyclic"
    assert rows[0]["training"]["max_learning_rate"] == 0.003


def test_run_innovation_one_matrix_can_train_structure_moe(tmp_path: Path):
    output_path = tmp_path / "moe.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "moe_hard",
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
            "--difference-profile",
            "speck32_gohr2019",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["model"] == "moe_hard"
    assert rows[0]["gate_mode"] == "hard"
    assert rows[0]["gate_weights_mean"]["resnet_bitslice"] == 0.35
    assert rows[0]["gate_weights_mean"]["dbitnet_dilated_cnn"] == 0.20
    assert rows[0]["gate_weights_mean"]["senet_resnext"] == 0.10
    assert rows[0]["gate_weights_mean"]["multiscale_dense_resnet"] == 0.25


def test_run_innovation_one_matrix_can_train_adaptive_moe_v2(tmp_path: Path):
    output_path = tmp_path / "moe_v2.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "moe_v2_hard",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--difference-profile",
            "speck32_gohr2019",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["model"] == "moe_v2_hard"
    assert rows[0]["gate_mode"] == "hard"
    assert rows[0]["expert_set"] == "v2_adaptive"
    assert rows[0]["gate_weights_mean"]["adaptive_dbitnet"] == 0.20
    assert "dbitnet_dilated_cnn" not in rows[0]["gate_weights_mean"]


def test_run_innovation_one_matrix_infers_pair_bits_for_pairwise_model(tmp_path: Path):
    output_path = tmp_path / "pairwise_present.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "present80",
            "--models",
            "adaptive_dbitnet_pairwise",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["cipher"] == "PRESENT-80"
    assert rows[0]["model"] == "adaptive_dbitnet_pairwise"
    assert rows[0]["training"]["input_bits"] == 384
    assert rows[0]["training"]["pair_bits"] == 192


def test_run_innovation_one_matrix_can_train_structure_adaptive_pairset_dbitnet(
    tmp_path: Path,
):
    output_path = tmp_path / "structure_pairset.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "present80",
            "sm4",
            "--models",
            "structure_adaptive_pairset_dbitnet",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 3
    assert all(row["model"] == "structure_adaptive_pairset_dbitnet" for row in rows)
    assert {row["cipher"]: row["training"]["pair_bits"] for row in rows} == {
        "SPECK32/64": 96,
        "PRESENT-80": 192,
        "SM4": 384,
    }
    assert "wrote 3 rows" in completed.stdout


def test_run_innovation_one_matrix_can_train_spn_pairset_dbitnet_v2(
    tmp_path: Path,
):
    output_path = tmp_path / "spn_pairset_v2.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "present80",
            "--models",
            "spn_pairset_dbitnet_v2",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["cipher"] == "PRESENT-80"
    assert rows[0]["model"] == "spn_pairset_dbitnet_v2"
    assert rows[0]["training"]["pair_bits"] == 192
    assert "wrote 1 rows" in completed.stdout


def test_run_innovation_one_matrix_infers_pair_bits_for_single_pair_pairwise_model(
    tmp_path: Path,
):
    output_path = tmp_path / "single_pair_pairwise.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "present80",
            "sm4",
            "--models",
            "adaptive_dbitnet_pairwise",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "1",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert {row["cipher"]: row["training"]["input_bits"] for row in rows} == {
        "PRESENT-80": 192,
        "SM4": 384,
    }
    assert {row["cipher"]: row["training"]["pair_bits"] for row in rows} == {
        "PRESENT-80": 192,
        "SM4": 384,
    }


def test_run_innovation_one_matrix_can_train_pairwise_moe_v3(tmp_path: Path):
    output_path = tmp_path / "moe_v3.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "moe_v3_hard",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--difference-profile",
            "speck32_gohr2019",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["model"] == "moe_v3_hard"
    assert rows[0]["expert_set"] == "v3_pairwise"
    assert rows[0]["training"]["pair_bits"] == 96
    assert rows[0]["gate_weights_mean"]["adaptive_dbitnet_pairwise"] == 0.20
    assert "adaptive_dbitnet" not in rows[0]["gate_weights_mean"]


def test_run_innovation_one_matrix_can_train_structure_adapter_moe_v4(tmp_path: Path):
    output_path = tmp_path / "moe_v4.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "present80",
            "sm4",
            "--models",
            "moe_v4_hard",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 3
    assert {row["cipher"]: row["adapter_name"] for row in rows} == {
        "SPECK32/64": "arx_word_mix",
        "PRESENT-80": "spn_cell_mix",
        "SM4": "feistel_branch_mix",
    }
    assert {row["cipher"]: row["expert_set"] for row in rows} == {
        "SPECK32/64": "v4_structure_adapter",
        "PRESENT-80": "v4_structure_adapter",
        "SM4": "v4_structure_adapter",
    }


def test_run_innovation_one_matrix_can_train_pairwise_pooling_ablations(tmp_path: Path):
    output_path = tmp_path / "pairwise_pooling.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "adaptive_dbitnet_pairwise_mean",
            "adaptive_dbitnet_pairwise_max",
            "adaptive_dbitnet_pairwise_mean_max",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--difference-profile",
            "speck32_gohr2019",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 3
    assert {row["model"] for row in rows} == {
        "adaptive_dbitnet_pairwise_mean",
        "adaptive_dbitnet_pairwise_max",
        "adaptive_dbitnet_pairwise_mean_max",
    }
    assert all(row["selected_model"] == row["model"] for row in rows)
    assert all(row["training"]["pair_bits"] == 96 for row in rows)


def test_run_innovation_one_matrix_can_train_structure_rule_selector(tmp_path: Path):
    output_path = tmp_path / "selector_rule.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "present80",
            "sm4",
            "--models",
            "selector_rule",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 3
    assert {row["cipher"]: row["selected_model"] for row in rows} == {
        "SPECK32/64": "adaptive_dbitnet_pairwise",
        "PRESENT-80": "senet_resnext",
        "SM4": "multiscale_dense_resnet",
    }
    assert rows[0]["model"] == "selector_rule"


def test_run_innovation_one_matrix_can_train_structure_rule_v2_selector(tmp_path: Path):
    output_path = tmp_path / "selector_rule_v2.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "present80",
            "sm4",
            "--models",
            "selector_rule_v2",
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
            "--feature-encoding",
            "ciphertext_pair_xor_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert len(rows) == 3
    assert {row["cipher"]: row["selected_model"] for row in rows} == {
        "SPECK32/64": "adaptive_dbitnet_pairwise",
        "PRESENT-80": "adaptive_dbitnet_pairwise",
        "SM4": "adaptive_dbitnet_pairwise",
    }
    assert rows[0]["model"] == "selector_rule_v2"


def test_run_innovation_one_matrix_prints_task_progress(tmp_path: Path):
    output_path = tmp_path / "progress.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
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
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "[1/2] SPECK32/64 r=1 model=mlp seed=0 pairs=1" in completed.stdout
    assert "[2/2] SPECK32/64 r=1 model=cnn seed=0 pairs=1" in completed.stdout


def test_run_innovation_one_matrix_accepts_spn_aligned_feature_encoding(tmp_path: Path):
    output_path = tmp_path / "spn_aligned.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "present80",
            "--models",
            "mlp",
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
            "--feature-encoding",
            "ciphertext_pair_xor_spn_aligned_bits",
            "--pairs-per-sample",
            "2",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["feature_encoding"] == "ciphertext_pair_xor_spn_aligned_bits"
    assert rows[0]["training"]["pair_bits"] == 256
    assert rows[0]["training"]["input_bits"] == 512
