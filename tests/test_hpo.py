import json
import subprocess
import sys
from pathlib import Path

from blockcipher_ai_eval.hpo import expand_search_space, sample_search_space


def test_expand_search_space_builds_grid_trials():
    trials = expand_search_space(
        {
            "model": ["spn_nibble_conv_pairset"],
            "activation": ["gelu", "silu"],
            "norm": ["layernorm"],
            "lr": [0.001, 0.0003],
        }
    )

    assert len(trials) == 4
    assert trials[0]["model"] == "spn_nibble_conv_pairset"
    assert {trial["activation"] for trial in trials} == {"gelu", "silu"}


def test_sample_search_space_is_deterministic_for_seed():
    space = {
        "activation": ["gelu", "silu", "relu"],
        "norm": ["layernorm", "rmsnorm"],
        "lr": [0.001, 0.0003],
    }

    first = sample_search_space(space, trials=5, seed=7)
    second = sample_search_space(space, trials=5, seed=7)

    assert first == second
    assert len(first) == 5


def test_run_hparam_search_writes_trial_rows(tmp_path: Path):
    output_path = tmp_path / "hpo.jsonl"
    space_path = tmp_path / "space.json"
    space_path.write_text(
        json.dumps(
            {
                "cipher": ["present80"],
                "model": ["spn_nibble_conv_pairset"],
                "rounds": [1],
                "pairs_per_sample": [2],
                "activation": ["gelu"],
                "norm": ["layernorm"],
                "pooling": ["attention_mean_max"],
                "learning_rate": [0.001],
                "weight_decay": [0.0],
                "nibble_embed_dim": [16],
                "conv_depth": [2],
                "kernel_size": [5],
                "dropout": [0.05],
            }
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_hparam_search.py",
            "--space",
            str(space_path),
            "--mode",
            "grid",
            "--max-trials",
            "1",
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
    assert len(rows) == 1
    assert rows[0]["trial_id"] == 0
    assert rows[0]["config"]["model"] == "spn_nibble_conv_pairset"
    assert rows[0]["model_options"]["activation"] == "gelu"
    assert rows[0]["model_options"]["norm"] == "layernorm"
    assert rows[0]["model_options"]["pooling"] == "attention_mean_max"
    assert rows[0]["model_options"]["kernel_size"] == 5
    assert rows[0]["metrics"]["calibrated_accuracy"] >= 0.0
