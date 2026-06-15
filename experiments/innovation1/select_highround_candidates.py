from __future__ import annotations

import argparse
import csv
import glob
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Candidate:
    row: dict[str, str]
    score: float


def load_summary_rows(patterns: Iterable[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for pattern in patterns:
        for path_text in sorted(glob.glob(pattern)):
            path = Path(path_text)
            with path.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    row = dict(row)
                    row["_summary_path"] = str(path)
                    rows.append(row)
    return rows


def select_candidates(
    rows: list[dict[str, str]],
    *,
    cipher: str = "PRESENT-80",
    min_rounds: int = 7,
    min_calibrated_accuracy: float = 0.505,
    min_auc: float = 0.505,
    limit: int = 3,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    for row in rows:
        if row.get("cipher") != cipher:
            continue
        rounds = _to_int(row.get("rounds"))
        if rounds < min_rounds:
            continue
        calibrated_accuracy = _to_float(row.get("calibrated_accuracy_mean"))
        auc = _to_float(row.get("auc_mean"))
        if calibrated_accuracy < min_calibrated_accuracy and auc < min_auc:
            continue
        samples_per_class = max(1, _to_int(row.get("samples_per_class")))
        runs = max(1, _to_int(row.get("runs")))
        score = (
            rounds * 10.0
            + max(calibrated_accuracy - 0.5, 0.0) * 1000.0
            + max(auc - 0.5, 0.0) * 250.0
            + runs * 0.1
            + min(samples_per_class, 262144) / 262144.0
        )
        candidates.append(Candidate(row=row, score=score))
    candidates.sort(
        key=lambda candidate: (
            candidate.score,
            _to_int(candidate.row.get("rounds")),
            _to_float(candidate.row.get("calibrated_accuracy_mean")),
            _to_float(candidate.row.get("auc_mean")),
        ),
        reverse=True,
    )
    return candidates[:limit]


def load_plan_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build_confirm_rows(
    candidates: list[Candidate],
    source_plan_rows: list[dict[str, str]],
    *,
    seeds: list[int],
    samples_per_class: int,
) -> list[dict[str, str]]:
    plan_index = _index_plan_rows(source_plan_rows)
    confirm_rows: list[dict[str, str]] = []
    for candidate in candidates:
        row = candidate.row
        key = (
            row.get("model"),
            row.get("architecture"),
            row.get("rounds"),
            row.get("feature_encoding"),
            row.get("difference_profile"),
            row.get("difference_member"),
            row.get("pairs_per_sample"),
        )
        template = plan_index.get(key) or _fallback_template(row, source_plan_rows)
        for seed in seeds:
            out = dict(template)
            out["seed"] = str(seed)
            out["samples_per_class"] = str(samples_per_class)
            out["network"] = f"{template.get('network', template.get('model_key', 'candidate'))}-confirm"
            out["evidence"] = (
                f"High-round confirm selected from {row.get('_summary_path', 'summary')} "
                f"with cal_acc={row.get('calibrated_accuracy_mean')} auc={row.get('auc_mean')}"
            )
            confirm_rows.append(out)
    return confirm_rows


def write_plan(rows: list[dict[str, str]], output: Path) -> None:
    if not rows:
        raise ValueError("no confirm rows to write")
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    for row in rows[1:]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _index_plan_rows(rows: list[dict[str, str]]) -> dict[tuple[str | None, ...], dict[str, str]]:
    index: dict[tuple[str | None, ...], dict[str, str]] = {}
    for row in rows:
        key = (
            row.get("model_key"),
            row.get("network"),
            row.get("rounds"),
            row.get("feature_encoding"),
            row.get("difference_profile"),
            row.get("difference_member"),
            row.get("pairs_per_sample"),
        )
        index.setdefault(key, row)
    return index


def _fallback_template(summary_row: dict[str, str], source_plan_rows: list[dict[str, str]]) -> dict[str, str]:
    if not source_plan_rows:
        raise ValueError("source plan is empty")
    for row in source_plan_rows:
        if (
            row.get("model_key") == summary_row.get("model")
            and (
                not summary_row.get("feature_encoding")
                or row.get("feature_encoding") == summary_row.get("feature_encoding")
            )
            and row.get("rounds") == summary_row.get("rounds")
            and (
                not summary_row.get("pairs_per_sample")
                or row.get("pairs_per_sample") == summary_row.get("pairs_per_sample")
            )
        ):
            return row
    raise ValueError(
        "could not find source-plan row for "
        f"{summary_row.get('model')} r{summary_row.get('rounds')} "
        f"{summary_row.get('feature_encoding')}"
    )


def _to_float(value: str | None) -> float:
    if value in {None, ""}:
        return 0.0
    return float(value)


def _to_int(value: str | None) -> int:
    if value in {None, ""}:
        return 0
    return int(float(value))


def parse_seeds(text: str) -> list[int]:
    seeds: list[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if ".." in part:
            start, end = part.split("..", 1)
            seeds.extend(range(int(start), int(end) + 1))
        else:
            seeds.append(int(part))
    return seeds


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select high-round innovation-one candidates and emit confirm CSV plan.")
    parser.add_argument("--summary-glob", action="append", required=True)
    parser.add_argument("--source-plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cipher", default="PRESENT-80")
    parser.add_argument("--min-rounds", type=int, default=7)
    parser.add_argument("--min-calibrated-accuracy", type=float, default=0.505)
    parser.add_argument("--min-auc", type=float, default=0.505)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--seeds", default="0..4")
    parser.add_argument("--samples-per-class", type=int, default=131072)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = load_summary_rows(args.summary_glob)
    candidates = select_candidates(
        rows,
        cipher=args.cipher,
        min_rounds=args.min_rounds,
        min_calibrated_accuracy=args.min_calibrated_accuracy,
        min_auc=args.min_auc,
        limit=args.limit,
    )
    source_plan_rows = load_plan_rows(args.source_plan)
    confirm_rows = build_confirm_rows(
        candidates,
        source_plan_rows,
        seeds=parse_seeds(args.seeds),
        samples_per_class=args.samples_per_class,
    )
    write_plan(confirm_rows, args.output)
    print(f"selected {len(candidates)} candidates; wrote {len(confirm_rows)} rows to {args.output}")
    for candidate in candidates:
        row = candidate.row
        print(
            f"candidate score={candidate.score:.4f} "
            f"r={row.get('rounds')} model={row.get('model')} "
            f"cal_acc={row.get('calibrated_accuracy_mean')} auc={row.get('auc_mean')} "
            f"feature={row.get('feature_encoding')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
