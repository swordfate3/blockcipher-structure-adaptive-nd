from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: summarize_spn_candidate_evidence.py RESULT_JSONL SUMMARY_CSV")
    result_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    rows = [json.loads(line) for line in result_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise SystemExit("no result rows")
    accuracies = [float(row["val_accuracy"]) for row in rows]
    aucs = [float(row["val_auc"]) for row in rows]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "rows",
                "accuracy_mean",
                "auc_mean",
                "accuracy_values",
                "auc_values",
                "feature_dim",
                "samples_per_class",
                "pairs_per_sample",
                "model",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "rows": len(rows),
                "accuracy_mean": f"{statistics.fmean(accuracies):.10f}",
                "auc_mean": f"{statistics.fmean(aucs):.10f}",
                "accuracy_values": json.dumps(accuracies),
                "auc_values": json.dumps(aucs),
                "feature_dim": rows[0].get("feature_dim"),
                "samples_per_class": rows[0].get("samples_per_class"),
                "pairs_per_sample": rows[0].get("pairs_per_sample"),
                "model": rows[0].get("model"),
            }
        )


if __name__ == "__main__":
    main()
