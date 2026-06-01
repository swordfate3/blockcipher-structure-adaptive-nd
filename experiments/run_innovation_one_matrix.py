from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.datasets import DifferentialDatasetConfig, make_differential_dataset
from blockcipher_ai_eval.experiments import build_cipher, build_model, default_difference
from blockcipher_ai_eval.training import TrainingConfig, train_binary_classifier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run innovation-one cipher/model experiment matrix and write JSONL."
    )
    parser.add_argument("--ciphers", nargs="+", default=["speck32"])
    parser.add_argument("--models", nargs="+", default=["mlp"])
    parser.add_argument("--rounds", type=int, nargs="+", default=[2])
    parser.add_argument("--seeds", type=int, nargs="+", default=[0])
    parser.add_argument("--samples-per-class", type=int, default=256)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--hidden-bits", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument(
        "--plan",
        default=None,
        help="Optional literature-ranked CSV plan from build_innovation_one_matrix.py.",
    )
    parser.add_argument("--output", default="outputs/innovation_one_matrix_results.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for task in _build_tasks(args):
        cipher = build_cipher(task["cipher_key"], task["rounds"])
        input_difference = default_difference(task["cipher_key"])
        train_dataset = make_differential_dataset(
            DifferentialDatasetConfig(
                cipher=cipher,
                input_difference=input_difference,
                samples_per_class=task["samples_per_class"],
                seed=task["seed"],
            )
        )
        validation_dataset = make_differential_dataset(
            DifferentialDatasetConfig(
                cipher=cipher,
                input_difference=input_difference,
                samples_per_class=max(8, task["samples_per_class"] // 2),
                seed=task["seed"] + 10_000,
            )
        )
        model = build_model(
            task["model_key"],
            input_bits=train_dataset.features.shape[1],
            hidden_bits=args.hidden_bits,
        )
        result = train_binary_classifier(
            model,
            train_dataset,
            validation_dataset,
            TrainingConfig(
                epochs=args.epochs,
                batch_size=args.batch_size,
                learning_rate=args.learning_rate,
                seed=task["seed"],
            ),
        )
        rows.append(
            {
                "cipher": cipher.name,
                "cipher_key": task["cipher_key"],
                "structure": cipher.structure,
                "model": task["model_key"],
                "architecture": task["architecture"],
                "architecture_rank": task.get("architecture_rank"),
                "matching_score": task.get("matching_score"),
                "matching_evidence": task.get("matching_evidence", ""),
                "literature": task.get("literature", ""),
                "rounds": task["rounds"],
                "seed": task["seed"],
                "input_difference": input_difference,
                "samples_per_class": task["samples_per_class"],
                "metrics": result.final_metrics,
                "history": result.history,
                "training": result.metadata,
            }
        )

    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"wrote {len(rows)} rows to {output}")


def _build_tasks(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.plan:
        return _tasks_from_plan(Path(args.plan))

    tasks: list[dict[str, Any]] = []
    for cipher_key in args.ciphers:
        for rounds in args.rounds:
            for seed in args.seeds:
                for model_key in args.models:
                    tasks.append(
                        {
                            "cipher_key": cipher_key,
                            "model_key": model_key,
                            "architecture": model_key,
                            "rounds": rounds,
                            "seed": seed,
                            "samples_per_class": args.samples_per_class,
                        }
                    )
    return tasks


def _tasks_from_plan(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        {
            "cipher_key": _cipher_key(row["cipher"]),
            "model_key": row["model_key"],
            "architecture": row["network"],
            "architecture_rank": int(row["architecture_rank"]),
            "matching_score": int(row["score"]),
            "matching_evidence": row["evidence"],
            "literature": row["literature"],
            "rounds": int(row["rounds"]),
            "seed": int(row["seed"]),
            "samples_per_class": int(row["samples_per_class"]),
        }
        for row in rows
    ]


def _cipher_key(cipher_name: str) -> str:
    mapping = {
        "SPECK32/64": "speck32",
        "PRESENT-80": "present80",
        "SM4": "sm4",
    }
    try:
        return mapping[cipher_name]
    except KeyError as exc:
        raise ValueError(f"unsupported cipher in plan: {cipher_name}") from exc


if __name__ == "__main__":
    main()
