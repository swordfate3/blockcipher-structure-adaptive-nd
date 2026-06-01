from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


GROUP_FIELDS = (
    "cipher",
    "structure",
    "model",
    "architecture",
    "architecture_rank",
    "matching_score",
    "literature",
    "rounds",
    "samples_per_class",
)
METRIC_FIELDS = ("accuracy", "best_accuracy", "auc", "advantage", "loss")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize innovation-one JSONL results to CSV.")
    parser.add_argument("--input", required=True, help="Input JSONL result file.")
    parser.add_argument("--output", required=True, help="Output CSV summary file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = _load_rows(Path(args.input))
    summary = summarize_rows(rows)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(GROUP_FIELDS) + ["runs"]
    for metric in METRIC_FIELDS:
        fieldnames.extend([f"{metric}_mean", f"{metric}_std"])
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)
    print(f"wrote {len(summary)} summary rows to {output}")


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key = tuple(_group_value(row, field) for field in GROUP_FIELDS)
        groups[key].append(row)

    summary = []
    for key, group_rows in sorted(groups.items()):
        out = dict(zip(GROUP_FIELDS, key))
        out["runs"] = len(group_rows)
        for metric in METRIC_FIELDS:
            values = [_metric_value(row["metrics"], metric) for row in group_rows]
            out[f"{metric}_mean"] = round(mean(values), 10)
            out[f"{metric}_std"] = round(pstdev(values), 10) if len(values) > 1 else 0.0
        summary.append(out)
    return summary


def _metric_value(metrics: dict[str, Any], metric: str) -> float:
    if metric in metrics:
        return float(metrics[metric])
    if metric == "best_accuracy":
        return float(metrics["accuracy"])
    raise KeyError(metric)


def _group_value(row: dict[str, Any], field: str) -> Any:
    if field == "architecture":
        return row.get("architecture", row["model"])
    return row.get(field, "")


def _load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


if __name__ == "__main__":
    main()
