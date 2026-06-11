#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render experiment progress JSONL as readable status lines.")
    parser.add_argument("progress", type=Path, help="Path to *_progress.jsonl")
    parser.add_argument("--lines", type=int, default=30, help="Number of recent progress events to render.")
    parser.add_argument("--interval", type=float, default=5.0, help="Refresh interval in seconds.")
    parser.add_argument("--once", action="store_true", help="Render once and exit.")
    parser.add_argument("--no-clear", action="store_true", help="Do not clear the terminal between refreshes.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    while True:
        if not args.no_clear and not args.once:
            os.system("cls" if os.name == "nt" else "clear")
        print(f"progress: {args.progress}")
        print(time.strftime("updated: %Y-%m-%d %H:%M:%S"))
        print()
        rows = read_recent_events(args.progress, args.lines)
        if not rows:
            print("waiting for progress events...")
        else:
            for row in rows:
                print(format_event(row))
        if args.once:
            return 0
        time.sleep(max(0.5, args.interval))


def read_recent_events(path: Path, lines: int) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    rows: list[dict[str, Any]] = []
    for line in raw_lines[-max(1, lines) :]:
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"event": "unparseable", "raw": line})
    return rows


def format_event(row: dict[str, Any]) -> str:
    event = str(row.get("event", "unknown"))
    if event.startswith("cache_"):
        return format_cache_event(row)
    if event in {"train_start", "epoch_start", "train_batch", "validation_start", "epoch_end", "train_done"}:
        return format_training_event(row)
    return format_generic_event(row)


def format_cache_event(row: dict[str, Any]) -> str:
    prefix = _row_prefix(row, "dataset_cache")
    split = row.get("split", "?")
    event = row.get("event", "cache")
    if "class_rows_done" in row and "class_total" in row:
        done = int(row["class_rows_done"])
        total = int(row["class_total"])
        percent = _percent(done, total)
        rows_done = row.get("rows_done", "?")
        total_rows = row.get("total_rows", "?")
        return f"{prefix} {split} {event} {done}/{total} {percent} rows={rows_done}/{total_rows}"
    if "total_rows" in row:
        return f"{prefix} {split} {event} total_rows={row['total_rows']} input_bits={row.get('input_bits', '?')}"
    return f"{prefix} {split} {event}"


def format_training_event(row: dict[str, Any]) -> str:
    prefix = _row_prefix(row, "training")
    event = str(row.get("event", "training"))
    if event == "train_batch":
        step = int(row.get("step", 0))
        steps = int(row.get("steps_per_epoch", 0))
        percent = _percent(step, steps)
        return (
            f"{prefix} epoch {row.get('epoch', '?')}/{row.get('epochs', '?')} "
            f"step {step}/{steps} {percent} loss={_float(row.get('train_loss'))} "
            f"lr={_float(row.get('learning_rate'))}"
        )
    if event == "epoch_end":
        return (
            f"{prefix} epoch {row.get('epoch', '?')}/{row.get('epochs', '?')} done "
            f"train_loss={_float(row.get('train_loss'))} val_acc={_float(row.get('val_accuracy'))} "
            f"val_auc={_float(row.get('val_auc'))}"
        )
    if event == "train_done":
        return (
            f"{prefix} done epochs={row.get('epochs', '?')} "
            f"acc={_float(row.get('accuracy'))} auc={_float(row.get('auc'))}"
        )
    return f"{prefix} {event} epoch={row.get('epoch', '?')}/{row.get('epochs', '?')}"


def format_generic_event(row: dict[str, Any]) -> str:
    prefix = _row_prefix(row, str(row.get("stage", "run")))
    event = row.get("event", "unknown")
    extras = []
    for key in ("cipher_key", "model", "rounds", "seed", "samples_per_class"):
        if key in row:
            extras.append(f"{key}={row[key]}")
    return f"{prefix} {event}" + (" " + " ".join(extras) if extras else "")


def _row_prefix(row: dict[str, Any], stage: str) -> str:
    index = row.get("index", "?")
    total = row.get("total", "?")
    return f"{stage} row {index}/{total}"


def _percent(done: int, total: int) -> str:
    if total <= 0:
        return "0.0%"
    return f"{100.0 * done / total:.1f}%"


def _float(value: Any) -> str:
    if value is None:
        return "?"
    try:
        return f"{float(value):.5g}"
    except (TypeError, ValueError):
        return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
