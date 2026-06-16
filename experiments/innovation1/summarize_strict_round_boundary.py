from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


FIELDNAMES = [
    "rounds",
    "runs",
    "expected_runs",
    "complete",
    "model",
    "feature_encoding",
    "sample_structure",
    "key_rotation_interval",
    "auc_mean",
    "auc_std",
    "auc_min",
    "auc_max",
    "calibrated_accuracy_mean",
    "calibrated_accuracy_std",
    "calibrated_accuracy_min",
    "calibrated_accuracy_max",
    "verdict",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def summarize_boundary_rows(
    rows: list[dict[str, Any]],
    *,
    expected_r7: int,
    expected_r8: int,
    r7_auc_mean_threshold: float,
    r7_auc_min_threshold: float,
    r8_auc_mean_threshold: float,
) -> list[dict[str, Any]]:
    groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[int(row["rounds"])].append(row)

    summaries = []
    for rounds in sorted(groups):
        group = groups[rounds]
        expected_runs = expected_r7 if rounds == 7 else expected_r8 if rounds == 8 else len(group)
        auc_values = [_metric(row, "auc") for row in group]
        cal_acc_values = [_metric(row, "calibrated_accuracy") for row in group]
        complete = len(group) == expected_runs
        auc_mean = mean(auc_values)
        auc_min = min(auc_values)
        row0 = group[0]
        summaries.append(
            {
                "rounds": rounds,
                "runs": len(group),
                "expected_runs": expected_runs,
                "complete": str(complete).lower(),
                "model": row0.get("model", ""),
                "feature_encoding": row0.get("feature_encoding", ""),
                "sample_structure": row0.get("sample_structure", ""),
                "key_rotation_interval": row0.get("key_rotation_interval", ""),
                "auc_mean": _round(auc_mean),
                "auc_std": _round(pstdev(auc_values) if len(auc_values) > 1 else 0.0),
                "auc_min": _round(auc_min),
                "auc_max": _round(max(auc_values)),
                "calibrated_accuracy_mean": _round(mean(cal_acc_values)),
                "calibrated_accuracy_std": _round(pstdev(cal_acc_values) if len(cal_acc_values) > 1 else 0.0),
                "calibrated_accuracy_min": _round(min(cal_acc_values)),
                "calibrated_accuracy_max": _round(max(cal_acc_values)),
                "verdict": _verdict(
                    rounds=rounds,
                    complete=complete,
                    auc_mean=auc_mean,
                    auc_min=auc_min,
                    r7_auc_mean_threshold=r7_auc_mean_threshold,
                    r7_auc_min_threshold=r7_auc_min_threshold,
                    r8_auc_mean_threshold=r8_auc_mean_threshold,
                ),
            }
        )
    return summaries


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def _metric(row: dict[str, Any], name: str) -> float:
    metrics = row.get("metrics", {})
    if name in metrics:
        return float(metrics[name])
    if name == "calibrated_accuracy":
        return float(metrics["accuracy"])
    raise KeyError(name)


def _verdict(
    *,
    rounds: int,
    complete: bool,
    auc_mean: float,
    auc_min: float,
    r7_auc_mean_threshold: float,
    r7_auc_min_threshold: float,
    r8_auc_mean_threshold: float,
) -> str:
    if not complete:
        return "incomplete"
    if rounds == 7:
        if auc_mean >= r7_auc_mean_threshold and auc_min >= r7_auc_min_threshold:
            return "r7_strict_candidate"
        return "r7_not_confirmed"
    if rounds == 8:
        if auc_mean >= r8_auc_mean_threshold:
            return "r8_boundary_signal"
        return "r8_no_boundary_signal"
    return "unscored_round"


def _round(value: float) -> str:
    return f"{value:.10f}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize strict r7/r8 round-boundary JSONL results.")
    parser.add_argument("--input", required=True, help="Input strict JSONL result file.")
    parser.add_argument("--output", required=True, help="Output CSV file.")
    parser.add_argument("--expected-r7", type=int, default=10)
    parser.add_argument("--expected-r8", type=int, default=4)
    parser.add_argument("--r7-auc-mean-threshold", type=float, default=0.65)
    parser.add_argument("--r7-auc-min-threshold", type=float, default=0.60)
    parser.add_argument("--r8-auc-mean-threshold", type=float, default=0.55)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl(Path(args.input))
    summary_rows = summarize_boundary_rows(
        rows,
        expected_r7=args.expected_r7,
        expected_r8=args.expected_r8,
        r7_auc_mean_threshold=args.r7_auc_mean_threshold,
        r7_auc_min_threshold=args.r7_auc_min_threshold,
        r8_auc_mean_threshold=args.r8_auc_mean_threshold,
    )
    write_csv(Path(args.output), summary_rows)
    print(f"wrote {len(summary_rows)} strict boundary summary rows to {args.output}")


if __name__ == "__main__":
    main()
