from __future__ import annotations

import argparse
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
    parser.add_argument("--output", default="outputs/innovation_one_matrix_results.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for cipher_name in args.ciphers:
        for rounds in args.rounds:
            cipher = build_cipher(cipher_name, rounds)
            input_difference = default_difference(cipher_name)
            for seed in args.seeds:
                train_dataset = make_differential_dataset(
                    DifferentialDatasetConfig(
                        cipher=cipher,
                        input_difference=input_difference,
                        samples_per_class=args.samples_per_class,
                        seed=seed,
                    )
                )
                validation_dataset = make_differential_dataset(
                    DifferentialDatasetConfig(
                        cipher=cipher,
                        input_difference=input_difference,
                        samples_per_class=max(8, args.samples_per_class // 2),
                        seed=seed + 10_000,
                    )
                )
                for model_name in args.models:
                    model = build_model(
                        model_name,
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
                            seed=seed,
                        ),
                    )
                    rows.append(
                        {
                            "cipher": cipher.name,
                            "cipher_key": cipher_name,
                            "structure": cipher.structure,
                            "model": model_name,
                            "rounds": rounds,
                            "seed": seed,
                            "input_difference": input_difference,
                            "samples_per_class": args.samples_per_class,
                            "metrics": result.final_metrics,
                            "history": result.history,
                            "training": result.metadata,
                        }
                    )

    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
