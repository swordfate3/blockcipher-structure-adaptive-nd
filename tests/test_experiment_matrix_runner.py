import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_matrix_runner():
    script = Path(__file__).resolve().parents[1] / "experiments" / "run_innovation_one_matrix.py"
    spec = importlib.util.spec_from_file_location("run_innovation_one_matrix", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



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


def test_run_innovation_one_matrix_writes_progress_jsonl(tmp_path: Path):
    output_path = tmp_path / "matrix.jsonl"
    progress_path = tmp_path / "progress.jsonl"

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
            "--progress-output",
            str(progress_path),
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    progress_rows = [json.loads(line) for line in progress_path.read_text().splitlines()]
    events = [row["event"] for row in progress_rows]

    assert completed.returncode == 0
    assert events[:3] == ["run_start", "row_start", "cache_ready"]
    assert events.index("train_start") < events.index("epoch_end") < events.index("train_done")
    assert events[-2:] == ["row_done", "run_done"]
    assert progress_rows[1]["cipher_key"] == "speck32"
    cache_ready = next(row for row in progress_rows if row["event"] == "cache_ready")
    row_done = next(row for row in progress_rows if row["event"] == "row_done")
    assert cache_ready["train_rows"] == 16
    assert cache_ready["validation_rows"] == 16
    assert row_done["selected_model"] == "mlp"
    assert progress_rows[-1]["total"] == 1


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


def test_run_innovation_one_matrix_can_execute_gift_spn_aligned_plan(tmp_path: Path):
    plan_path = tmp_path / "gift_plan.csv"
    output_path = tmp_path / "gift_results.jsonl"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,difference_profile,difference_member,evidence,literature",
                "GIFT-64,SPN,SPN-TokenMixer-PairSet,spn_token_mixer_pairset,spn_token_mixer,0,68,1,0,8,2,ciphertext_pair_xor_spn_aligned_bits,encrypted_random_plaintexts,0x00000000000000000000000000000000,0x11111111111111111111111111111111,gift64_shen2024_spn_screen,0,gift spn aligned smoke,Shen 2024 GIFT neural distinguisher",
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
    assert len(rows) == 1
    assert rows[0]["cipher"] == "GIFT-64"
    assert rows[0]["structure"] == "SPN"
    assert rows[0]["feature_encoding"] == "ciphertext_pair_xor_spn_aligned_bits"
    assert rows[0]["difference_profile"] == "gift64_shen2024_spn_screen"
    assert rows[0]["input_difference"] == 0x0000000000000040
    assert rows[0]["training"]["input_bits"] == 512


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


def test_run_innovation_one_matrix_plan_supports_keys_negative_mode_and_xor_aligned_input(
    tmp_path: Path,
):
    plan_path = tmp_path / "crosskey_plan.csv"
    output_path = tmp_path / "crosskey_results.jsonl"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key",
                "PRESENT-80,SPN,MLP,mlp,mlp,1,1,1,0,8,1,ciphertext_xor_spn_aligned_bits,encrypted_random_plaintexts,0x0,0x11111111111111111111",
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
    assert rows[0]["cipher"] == "PRESENT-80"
    assert rows[0]["feature_encoding"] == "ciphertext_xor_spn_aligned_bits"
    assert rows[0]["negative_mode"] == "encrypted_random_plaintexts"
    assert rows[0]["train_key"] == 0
    assert rows[0]["validation_key"] == 0x11111111111111111111
    assert rows[0]["training"]["input_bits"] == 128
    assert rows[0]["training"]["pair_bits"] == 128
    assert rows[0]["validation"]["negative_mode"] == "encrypted_random_plaintexts"


def test_run_innovation_one_matrix_plan_supports_key_rotation_interval(
    tmp_path: Path,
):
    plan_path = tmp_path / "key_rotation_plan.csv"
    output_path = tmp_path / "key_rotation_results.jsonl"
    cache_root = tmp_path / "cache"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,key_rotation_interval",
                "SPECK32/64,ARX,MLP,mlp,mlp,1,1,1,0,8,2,ciphertext_pair_bits,encrypted_random_plaintexts,0x1918111009080100,0x0f0e0d0c0b0a0908,1",
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
            "--device",
            "cpu",
            "--dataset-cache-root",
            str(cache_root),
            "--dataset-cache-chunk-size",
            "4",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]
    metadata_files = list(cache_root.rglob("metadata.json"))
    metadata_rows = [json.loads(path.read_text(encoding="utf-8")) for path in metadata_files]

    assert completed.returncode == 0
    assert rows[0]["key_rotation_interval"] == 1
    assert rows[0]["training"]["key_rotation_interval"] == 1
    assert all(row["key_rotation_interval"] == 1 for row in metadata_rows)
    assert all(row["key_schedule"] == "rotating" for row in metadata_rows)


def test_run_innovation_one_matrix_plan_defaults_validation_key_to_train_key(
    tmp_path: Path,
):
    plan_path = tmp_path / "samekey_plan.csv"
    output_path = tmp_path / "samekey_results.jsonl"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,train_key,validation_key",
                "PRESENT-80,SPN,MLP,mlp,mlp,1,1,1,0,8,0x11111111111111111111,",
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
    assert rows[0]["train_key"] == 0x11111111111111111111
    assert rows[0]["validation_key"] == 0x11111111111111111111


def test_run_innovation_one_matrix_can_execute_speck_arx_aligned_plan(tmp_path: Path):
    plan_path = tmp_path / "speck_arx_plan.csv"
    output_path = tmp_path / "speck_arx_results.jsonl"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,difference_profile,difference_member,evidence,literature",
                "SPECK32/64,ARX,StructureAdaptive-PairSet-DBitNet,structure_adaptive_pairset_dbitnet,structure_pairset,0,66,1,0,8,2,ciphertext_pair_xor_arx_aligned_bits,encrypted_random_plaintexts,0x1918111009080100,0x0f0e0d0c0b0a0908,speck32_gohr2019,0,speck arx aligned smoke,Gohr 2019 SPECK32 neural distinguisher",
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
    assert len(rows) == 1
    assert rows[0]["cipher"] == "SPECK32/64"
    assert rows[0]["structure"] == "ARX"
    assert rows[0]["feature_encoding"] == "ciphertext_pair_xor_arx_aligned_bits"
    assert rows[0]["difference_profile"] == "speck32_gohr2019"
    assert rows[0]["input_difference"] == 0x00400000
    assert rows[0]["training"]["pair_bits"] == 128
    assert rows[0]["training"]["input_bits"] == 256


def test_run_innovation_one_matrix_can_use_chunked_dataset_cache(tmp_path: Path):
    plan_path = tmp_path / "cache_plan.csv"
    output_path = tmp_path / "cache_results.jsonl"
    cache_root = tmp_path / "dataset_cache"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,difference_profile,difference_member,evidence,literature",
                "SPECK32/64,ARX,MLP,mlp,mlp,0,1,1,0,8,2,ciphertext_pair_xor_bits,encrypted_random_plaintexts,0x1918111009080100,0x0f0e0d0c0b0a0908,speck32_gohr2019,0,cache smoke,Gohr 2019",
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
            "--device",
            "cpu",
            "--dataset-cache-root",
            str(cache_root),
            "--dataset-cache-chunk-size",
            "3",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["training"]["train_dataset_storage"] == "disk"
    assert rows[0]["training"]["validation_dataset_storage"] == "disk"
    assert rows[0]["training"]["dataset_cache_root"] == str(cache_root)
    assert rows[0]["training"]["dataset_cache_chunk_size"] == 3
    assert list(cache_root.rglob("features.npy"))
    assert list(cache_root.rglob("labels.npy"))
    cache_dirs = [path.parent for path in cache_root.rglob("metadata.json")]
    assert cache_dirs
    assert all(len(path.name) <= 32 for path in cache_dirs)
    assert all("encrypted_random_plaintexts" not in path.name for path in cache_dirs)
    assert all("ciphertext_pair_xor_bits" not in path.name for path in cache_dirs)


def test_plan_task_reads_plaintext_integral_sample_structure(tmp_path):
    plan = tmp_path / "plan.csv"
    plan.write_text(
        "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,key_rotation_interval,sample_structure,integral_active_nibble,difference_profile,difference_member,evidence,literature\n"
        "PRESENT-80,SPN,SPN-TokenMixer-PairSet,spn_token_mixer_pairset,spn_token_mixer,0,72,6,0,4,16,ciphertext_xor_spn_paligned_bits,encrypted_random_plaintexts,0x0,0x1,1024,plaintext_integral_nibble,0,present_wang_jain2021,0,evidence,literature\n",
        encoding="utf-8",
    )

    runner = _load_matrix_runner()
    tasks = runner._tasks_from_plan(
        plan,
        feature_encoding="ciphertext_pair_bits",
        pairs_per_sample=1,
        difference_profile=None,
        difference_member=0,
    )

    assert tasks[0]["sample_structure"] == "plaintext_integral_nibble"
    assert tasks[0]["integral_active_nibble"] == 0
    assert tasks[0]["feature_encoding"] == "ciphertext_xor_spn_paligned_bits"
    assert tasks[0]["pairs_per_sample"] == 16
