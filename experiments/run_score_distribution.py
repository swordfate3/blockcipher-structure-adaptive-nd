from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.data.differential import DifferentialDataset, DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.experiments import build_cipher, build_model, difference_for_profile
from blockcipher_ai_eval.training import (
    TrainingConfig,
    predict_binary_probabilities,
    train_binary_classifier,
)


def score_distribution_dataset(
    probabilities: np.ndarray,
    labels: np.ndarray,
    *,
    group_size: int,
) -> DifferentialDataset:
    if group_size < 1:
        raise ValueError("group_size must be >= 1")
    if len(probabilities) != len(labels):
        raise ValueError("probabilities and labels must have the same length")
    if len(probabilities) % group_size != 0:
        raise ValueError("probability count must be a multiple of group_size")
    score_groups = probabilities.astype(np.float32).reshape(-1, group_size)
    label_groups = labels.astype(np.uint8).reshape(-1, group_size)
    if not np.all(label_groups == label_groups[:, :1]):
        raise ValueError("each score group must contain a single class label")

    sorted_scores = np.sort(score_groups, axis=1)
    means = score_groups.mean(axis=1, keepdims=True)
    stds = score_groups.std(axis=1, keepdims=True)
    mins = score_groups.min(axis=1, keepdims=True)
    maxs = score_groups.max(axis=1, keepdims=True)
    q25 = np.quantile(score_groups, 0.25, axis=1, keepdims=True).astype(np.float32)
    q75 = np.quantile(score_groups, 0.75, axis=1, keepdims=True).astype(np.float32)
    features = np.concatenate([sorted_scores, means, stds, mins, maxs, q25, q75], axis=1).astype(np.float32)
    return DifferentialDataset(
        features=features,
        labels=label_groups[:, 0].astype(np.uint8),
        metadata={
            "feature_encoding": "score_distribution",
            "group_size": group_size,
            "input_bits": int(features.shape[1]),
            "samples": int(features.shape[0]),
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Two-stage score-distribution neural distinguisher experiment.")
    parser.add_argument("--cipher", default="present80")
    parser.add_argument("--rounds", type=int, required=True)
    parser.add_argument("--difference-profile", default="present_entropy2026_gohr")
    parser.add_argument("--difference-member", type=int, default=0)
    parser.add_argument("--feature-encoding", default="ciphertext_pair_bits")
    parser.add_argument("--selected-bit-indices", default="")
    parser.add_argument("--negative-mode", default="encrypted_random_plaintexts")
    parser.add_argument("--sample-structure", default="independent_pairs")
    parser.add_argument("--key-rotation-interval", type=int, default=1024)
    parser.add_argument("--base-samples-per-class", type=int, default=65536)
    parser.add_argument("--meta-samples-per-class", type=int, default=4096)
    parser.add_argument("--score-group-size", type=int, default=16)
    parser.add_argument("--base-model", default="mlp")
    parser.add_argument("--base-hidden-bits", type=int, default=64)
    parser.add_argument("--base-epochs", type=int, default=10)
    parser.add_argument("--base-batch-size", type=int, default=512)
    parser.add_argument("--base-learning-rate", type=float, default=1e-3)
    parser.add_argument("--base-loss", default="bce", choices=["bce", "mse"])
    parser.add_argument("--meta-hidden-bits", type=int, default=64)
    parser.add_argument("--meta-epochs", type=int, default=10)
    parser.add_argument("--meta-batch-size", type=int, default=512)
    parser.add_argument("--meta-learning-rate", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--progress-output", default=None)
    parser.add_argument("--output", default="outputs/score_distribution.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _reset_progress(args.progress_output)
    row = run_score_distribution_experiment(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"wrote score-distribution result to {output}")


def parse_selected_bit_indices(value: str | None) -> tuple[int, ...]:
    if value is None:
        return ()
    value = value.strip()
    if not value:
        return ()
    parsed = json.loads(value)
    if not isinstance(parsed, list) or not all(isinstance(item, int) for item in parsed):
        raise ValueError("selected_bit_indices must be a JSON list of integers")
    return tuple(parsed)


def _reset_progress(path: str | None) -> None:
    if not path:
        return
    progress_path = Path(path)
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    progress_path.write_text("", encoding="utf-8")


def _write_progress(path: str | None, event: str, payload: dict[str, Any] | None = None) -> None:
    if not path:
        return
    progress_path = Path(path)
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    with progress_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"event": event, "time": time.time(), **(payload or {})}, sort_keys=True) + "\n")


def _progress_callback(path: str | None, stage: str):
    def callback(event: str, payload: dict[str, Any]) -> None:
        _write_progress(path, event, {"stage": stage, **payload})

    return callback


def run_score_distribution_experiment(args: argparse.Namespace) -> dict[str, Any]:
    selected_bit_indices = parse_selected_bit_indices(args.selected_bit_indices)
    _write_progress(args.progress_output, "run_start", {"rounds": args.rounds, "score_group_size": args.score_group_size})
    cipher = build_cipher(args.cipher, args.rounds)
    validation_cipher = build_cipher(args.cipher, args.rounds, key=0x11111111111111111111)
    input_difference = difference_for_profile(args.difference_profile, args.difference_member)

    base_train = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=cipher,
            input_difference=input_difference,
            samples_per_class=args.base_samples_per_class,
            seed=args.seed,
            feature_encoding=args.feature_encoding,
            pairs_per_sample=1,
            negative_mode=args.negative_mode,
            key_rotation_interval=args.key_rotation_interval,
            sample_structure=args.sample_structure,
            selected_bit_indices=selected_bit_indices,
            shuffle=True,
        )
    )
    base_validation = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=validation_cipher,
            input_difference=input_difference,
            samples_per_class=max(8, args.base_samples_per_class // 2),
            seed=args.seed + 10_000,
            feature_encoding=args.feature_encoding,
            pairs_per_sample=1,
            negative_mode=args.negative_mode,
            key_rotation_interval=args.key_rotation_interval,
            sample_structure=args.sample_structure,
            selected_bit_indices=selected_bit_indices,
            shuffle=True,
        )
    )
    _write_progress(args.progress_output, "base_dataset_ready", {"train_rows": int(base_train.features.shape[0]), "validation_rows": int(base_validation.features.shape[0]), "input_bits": int(base_train.features.shape[1])})
    base_model = build_model(
        args.base_model,
        input_bits=base_train.features.shape[1],
        hidden_bits=args.base_hidden_bits,
        pair_bits=base_train.metadata["pair_bits"],
        structure=cipher.structure,
    )
    base_result = train_binary_classifier(
        base_model,
        base_train,
        base_validation,
        TrainingConfig(
            epochs=args.base_epochs,
            batch_size=args.base_batch_size,
            learning_rate=args.base_learning_rate,
            seed=args.seed,
            device=args.device,
            loss=args.base_loss,
            checkpoint_metric="val_auc",
            restore_best_checkpoint=True,
        ),
        progress_callback=_progress_callback(args.progress_output, "base_training"),
    )

    _write_progress(args.progress_output, "base_training_done", {"accuracy": base_result.final_metrics["accuracy"], "auc": base_result.final_metrics["auc"]})
    meta_train_source = _make_unshuffled_single_pair_dataset(args, cipher, input_difference, args.seed + 20_000)
    meta_validation_source = _make_unshuffled_single_pair_dataset(
        args,
        validation_cipher,
        input_difference,
        args.seed + 30_000,
    )
    _write_progress(args.progress_output, "meta_source_ready", {"train_rows": int(meta_train_source.features.shape[0]), "validation_rows": int(meta_validation_source.features.shape[0])})
    train_scores = predict_binary_probabilities(
        base_model,
        meta_train_source,
        batch_size=args.base_batch_size,
        device=args.device,
    )
    validation_scores = predict_binary_probabilities(
        base_model,
        meta_validation_source,
        batch_size=args.base_batch_size,
        device=args.device,
    )
    meta_train = score_distribution_dataset(train_scores, meta_train_source.labels, group_size=args.score_group_size)
    meta_validation = score_distribution_dataset(
        validation_scores,
        meta_validation_source.labels,
        group_size=args.score_group_size,
    )
    _write_progress(args.progress_output, "score_distribution_ready", {"train_rows": int(meta_train.features.shape[0]), "validation_rows": int(meta_validation.features.shape[0]), "input_features": int(meta_train.features.shape[1])})
    meta_model = build_model(
        "mlp",
        input_bits=meta_train.features.shape[1],
        hidden_bits=args.meta_hidden_bits,
        structure="generic",
    )
    meta_result = train_binary_classifier(
        meta_model,
        meta_train,
        meta_validation,
        TrainingConfig(
            epochs=args.meta_epochs,
            batch_size=args.meta_batch_size,
            learning_rate=args.meta_learning_rate,
            seed=args.seed + 1,
            device=args.device,
            checkpoint_metric="val_auc",
            restore_best_checkpoint=True,
        ),
        progress_callback=_progress_callback(args.progress_output, "meta_training"),
    )
    _write_progress(args.progress_output, "run_done", {"accuracy": meta_result.final_metrics["accuracy"], "auc": meta_result.final_metrics["auc"]})
    return {
        "cipher": cipher.name,
        "cipher_key": args.cipher,
        "structure": cipher.structure,
        "rounds": args.rounds,
        "seed": args.seed,
        "difference_profile": args.difference_profile,
        "difference_member": args.difference_member,
        "input_difference": input_difference,
        "feature_encoding": args.feature_encoding,
        "negative_mode": args.negative_mode,
        "selected_bit_indices": list(selected_bit_indices),
        "key_rotation_interval": args.key_rotation_interval,
        "score_group_size": args.score_group_size,
        "base_model": args.base_model,
        "base_metrics": base_result.final_metrics,
        "base_history": base_result.history,
        "meta_model": "score_distribution_mlp",
        "metrics": meta_result.final_metrics,
        "history": meta_result.history,
        "training": {
            "base_samples_per_class": args.base_samples_per_class,
            "meta_samples_per_class": args.meta_samples_per_class,
            "meta_input_features": int(meta_train.features.shape[1]),
            "base_training": base_result.metadata,
            "meta_training": meta_result.metadata,
        },
    }


def _make_unshuffled_single_pair_dataset(
    args: argparse.Namespace,
    cipher,
    input_difference: int,
    seed: int,
) -> DifferentialDataset:
    return make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=cipher,
            input_difference=input_difference,
            samples_per_class=args.meta_samples_per_class * args.score_group_size,
            seed=seed,
            feature_encoding=args.feature_encoding,
            pairs_per_sample=1,
            negative_mode=args.negative_mode,
            key_rotation_interval=args.key_rotation_interval,
            sample_structure=args.sample_structure,
            selected_bit_indices=parse_selected_bit_indices(args.selected_bit_indices),
            shuffle=False,
        )
    )


if __name__ == "__main__":
    main()
