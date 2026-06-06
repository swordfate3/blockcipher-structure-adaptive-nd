from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


SUMMARY_FIELDS = [
    "trial_id",
    "cipher",
    "model",
    "rounds",
    "seed",
    "trial_seeds",
    "samples_per_class",
    "pairs_per_sample",
    "difference_profile",
    "difference_member",
    "calibrated_accuracy",
    "calibrated_accuracy_std",
    "accuracy",
    "accuracy_std",
    "auc",
    "auc_std",
    "loss",
    "loss_std",
    "gate_temperature",
    "gate_hidden_bits",
    "gate_activation",
    "gate_dropout",
    "pairwise_pooling",
    "spn_token_dim",
    "spn_mixer_depth",
    "spn_token_mlp_ratio",
    "expert_activation",
    "expert_norm",
    "spn_pooling",
    "expert_dropout",
    "learning_rate",
    "weight_decay",
    "optimizer",
    "config_json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize HPO JSONL results to a sorted CSV.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [_summary_row(json.loads(line)) for line in Path(args.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    rows.sort(key=lambda row: float(row.get("calibrated_accuracy") or 0.0), reverse=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} HPO summary rows to {output}")


def _summary_row(row: dict[str, Any]) -> dict[str, Any]:
    metrics = row.get("metrics", {})
    metrics_std = row.get("metrics_std", {})
    config = row.get("config", {})
    components = row.get("moe_components", row.get("gate_config", {}))
    result: dict[str, Any] = {
        "trial_id": row.get("trial_id", ""),
        "cipher": row.get("cipher", ""),
        "model": config.get("model", ""),
        "rounds": row.get("rounds", ""),
        "seed": row.get("seed", ""),
        "trial_seeds": ",".join(str(seed) for seed in row.get("trial_seeds", [])),
        "samples_per_class": row.get("samples_per_class", ""),
        "pairs_per_sample": row.get("pairs_per_sample", ""),
        "difference_profile": row.get("difference_profile", ""),
        "difference_member": row.get("difference_member", ""),
        "calibrated_accuracy": metrics.get("calibrated_accuracy", ""),
        "calibrated_accuracy_std": metrics_std.get("calibrated_accuracy", ""),
        "accuracy": metrics.get("accuracy", ""),
        "accuracy_std": metrics_std.get("accuracy", ""),
        "auc": metrics.get("auc", ""),
        "auc_std": metrics_std.get("auc", ""),
        "loss": metrics.get("loss", ""),
        "loss_std": metrics_std.get("loss", ""),
        "learning_rate": config.get("learning_rate", config.get("lr", "")),
        "weight_decay": config.get("weight_decay", ""),
        "optimizer": config.get("optimizer", ""),
        "config_json": json.dumps(config, sort_keys=True),
    }
    for key in [
        "gate_temperature",
        "gate_hidden_bits",
        "gate_activation",
        "gate_dropout",
        "pairwise_pooling",
        "spn_token_dim",
        "spn_mixer_depth",
        "spn_token_mlp_ratio",
        "expert_activation",
        "expert_norm",
        "spn_pooling",
        "expert_dropout",
    ]:
        result[key] = components.get(key, config.get(key, ""))
    return result


if __name__ == "__main__":
    main()
