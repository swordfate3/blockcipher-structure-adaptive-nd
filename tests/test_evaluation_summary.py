from blockcipher_ai_eval.evaluation import (
    hparam_summary_rows,
    innovation_one_summary_rows,
)


def test_innovation_one_summary_rows_groups_runs_and_fills_calibrated_metrics():
    rows = [
        {
            "cipher": "SPECK32/64",
            "structure": "ARX",
            "model": "mlp",
            "rounds": 6,
            "samples_per_class": 8,
            "pairs_per_sample": 1,
            "metrics": {"accuracy": 0.60, "auc": 0.70, "advantage": 0.20, "loss": 0.6},
        },
        {
            "cipher": "SPECK32/64",
            "structure": "ARX",
            "model": "mlp",
            "rounds": 6,
            "samples_per_class": 8,
            "pairs_per_sample": 1,
            "metrics": {"accuracy": 0.80, "auc": 0.90, "advantage": 0.60, "loss": 0.4},
        },
    ]

    summary = innovation_one_summary_rows(rows)

    assert len(summary) == 1
    assert summary[0]["architecture"] == "mlp"
    assert summary[0]["runs"] == 2
    assert summary[0]["accuracy_mean"] == 0.7
    assert summary[0]["calibrated_accuracy_mean"] == 0.7
    assert summary[0]["calibrated_advantage_mean"] == 0.4


def test_hparam_summary_rows_sort_by_calibrated_accuracy_and_keep_component_config():
    rows = [
        {
            "trial_id": 0,
            "cipher": "PRESENT-80",
            "rounds": 5,
            "seed": "0",
            "trial_seeds": [0],
            "samples_per_class": 16,
            "pairs_per_sample": 4,
            "config": {"model": "moe_v5_soft", "learning_rate": 0.001},
            "metrics": {"calibrated_accuracy": 0.70, "accuracy": 0.69},
            "moe_components": {"gate_temperature": 1.0},
        },
        {
            "trial_id": 1,
            "cipher": "PRESENT-80",
            "rounds": 5,
            "seed": "1",
            "trial_seeds": [1],
            "samples_per_class": 16,
            "pairs_per_sample": 4,
            "config": {"model": "moe_v5_soft", "learning_rate": 0.0003},
            "metrics": {"calibrated_accuracy": 0.75, "accuracy": 0.72},
            "moe_components": {"gate_temperature": 0.75},
        },
    ]

    summary = hparam_summary_rows(rows)

    assert [row["trial_id"] for row in summary] == [1, 0]
    assert summary[0]["calibrated_accuracy"] == 0.75
    assert summary[0]["gate_temperature"] == 0.75
    assert summary[0]["learning_rate"] == 0.0003
    assert summary[0]["trial_seeds"] == "1"
    assert "config_json" in summary[0]
