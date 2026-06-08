#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import itertools
import json
from pathlib import Path
from typing import Any

FIELDNAMES = [
    "cipher",
    "structure",
    "network",
    "model_key",
    "family",
    "architecture_rank",
    "score",
    "rounds",
    "seed",
    "samples_per_class",
    "pairs_per_sample",
    "feature_encoding",
    "negative_mode",
    "train_key",
    "validation_key",
    "difference_profile",
    "difference_member",
    "evidence",
    "literature",
]


def load_plan_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expand_sweep_value(value: Any) -> list[Any]:
    if isinstance(value, dict):
        if set(value) == {"range"}:
            start, stop = value["range"]
            return list(range(int(start), int(stop)))
        raise ValueError(f"unsupported sweep object: {value}")
    if isinstance(value, list):
        return value
    return [value]


def build_plan_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    defaults = dict(config.get("defaults", {}))
    sweep = dict(config.get("sweep", {}))
    if not defaults:
        raise ValueError("plan config requires defaults")
    if not sweep:
        raise ValueError("plan config requires sweep")

    sweep_keys = list(sweep)
    sweep_values = [expand_sweep_value(sweep[key]) for key in sweep_keys]
    rows: list[dict[str, Any]] = []
    for combination in itertools.product(*sweep_values):
        row = dict(defaults)
        row.update(dict(zip(sweep_keys, combination)))
        missing = [field for field in FIELDNAMES if field not in row]
        if missing:
            raise ValueError(f"plan row missing fields: {', '.join(missing)}")
        rows.append({field: row[field] for field in FIELDNAMES})
    return rows


def write_plan(rows: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an experiment CSV plan from a JSON config.")
    parser.add_argument("config", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_plan_config(args.config)
    rows = build_plan_rows(config)
    output = args.output or Path(config["output"])
    write_plan(rows, output)
    print(f"wrote {len(rows)} rows -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
