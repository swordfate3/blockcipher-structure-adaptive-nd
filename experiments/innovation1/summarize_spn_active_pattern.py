from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_spn_active_pattern.py RESULT_JSONL")
    path = Path(sys.argv[1])
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise SystemExit("no result rows")
    accuracies = [float(row["val_accuracy"]) for row in rows]
    aucs = [float(row["val_auc"]) for row in rows]
    print(f"rows={len(rows)}")
    print(f"mean_accuracy={statistics.fmean(accuracies):.6f}")
    print(f"mean_auc={statistics.fmean(aucs):.6f}")
    print(f"feature_dim={rows[0].get('feature_dim')}")


if __name__ == "__main__":
    main()
