from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset
from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.experiments import (
    build_cipher,
    build_model,
    default_difference,
    difference_for_profile,
    literature_difference_profiles,
)
from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.features.profile import structure_feature_vector
from blockcipher_ai_eval.features.registry import pair_bits_for_encoding
from blockcipher_ai_eval.training import TrainingConfig, TrainingResult, train_binary_classifier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run innovation-one cipher/model experiment matrix and write JSONL."
    )
    parser.add_argument("--ciphers", nargs="+", default=["speck32"])
    parser.add_argument("--models", nargs="+", default=["mlp"])
    parser.add_argument("--rounds", type=int, nargs="+", default=[2])
    parser.add_argument("--seeds", type=int, nargs="+", default=[0])
    parser.add_argument("--samples-per-class", type=int, default=256)
    parser.add_argument("--pairs-per-sample", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--hidden-bits", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument(
        "--device",
        default="auto",
        help="Training device passed to PyTorch, e.g. auto, cpu, cuda, cuda:0, cuda:1.",
    )
    parser.add_argument(
        "--optimizer",
        default="adam",
        choices=["adam", "adamw", "lion"],
        help="Optimizer used for neural distinguisher training.",
    )
    parser.add_argument(
        "--amsgrad",
        action="store_true",
        help="Enable AMSGrad in Adam/AdamW.",
    )
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument(
        "--loss",
        default="bce",
        choices=["bce", "mse"],
        help="Training loss. Use mse for Zhang/Wang-style probability regression.",
    )
    parser.add_argument(
        "--lr-scheduler",
        default="none",
        choices=["none", "cyclic", "cosine_warmup"],
        help="Optional learning-rate scheduler.",
    )
    parser.add_argument(
        "--max-learning-rate",
        type=float,
        default=None,
        help="Maximum learning rate for cyclic scheduling.",
    )
    parser.add_argument(
        "--checkpoint-metric",
        default="val_accuracy",
        choices=["val_accuracy", "val_auc", "val_loss"],
        help="Validation metric used to select the best checkpoint.",
    )
    parser.add_argument(
        "--restore-best-checkpoint",
        action="store_true",
        help="Evaluate and report the best validation checkpoint instead of the final epoch.",
    )
    parser.add_argument(
        "--early-stopping-patience",
        type=int,
        default=0,
        help="Stop after this many non-improving epochs; 0 disables early stopping.",
    )
    parser.add_argument(
        "--early-stopping-min-delta",
        type=float,
        default=0.0,
        help="Minimum checkpoint metric improvement required to reset patience.",
    )
    parser.add_argument(
        "--pretrain-rounds",
        type=int,
        default=None,
        help="Optional curriculum pretraining round count before each target row.",
    )
    parser.add_argument(
        "--pretrain-epochs",
        type=int,
        default=0,
        help="Optional curriculum pretraining epochs before each target row.",
    )
    parser.add_argument(
        "--feature-encoding",
        default="ciphertext_pair_bits",
        choices=[
            "ciphertext_pair_bits",
            "present_mcnd_cell_matrix_bits",
            "present_xor_paligned_cell_matrix_bits",
            "present_pair_xor_paligned_cell_matrix_bits",
            "present_pair_xor_paligned_sinv_cell_matrix_bits",
            "present_pair_xor_cell_matrix_bits",
            "ciphertext_xor_bits",
            "ciphertext_xor_spn_aligned_bits",
            "ciphertext_xor_spn_paligned_bits",
            "ciphertext_pair_xor_bits",
            "ciphertext_pair_xor_spn_aligned_bits",
            "ciphertext_pair_xor_arx_aligned_bits",
            "ciphertext_pair_xor_arx_partial_inverse_bits",
            "ciphertext_pair_xor_arx_partial_inverse_rx_bits",
        ],
        help="Feature encoding for generated ciphertext pairs.",
    )
    parser.add_argument(
        "--negative-mode",
        default="random_ciphertext",
        choices=["random_ciphertext", "encrypted_random_plaintexts"],
        help="How negative-class ciphertext pairs are generated.",
    )
    parser.add_argument(
        "--key-rotation-interval",
        type=int,
        default=0,
        help=(
            "Number of sample groups that share one random key. "
            "Use 0 for the fixed cipher key from the plan/CLI."
        ),
    )
    parser.add_argument(
        "--sample-structure",
        default="independent_pairs",
        choices=["independent_pairs", "plaintext_integral_nibble", "zhang_wang_case2_mcnd", "zhang_wang_case2_independent_mcnd"],
        help="How multiple pairs inside one sample are organized.",
    )
    parser.add_argument(
        "--integral-active-nibble",
        type=int,
        default=0,
        help="Active plaintext nibble index for plaintext_integral_nibble samples.",
    )
    parser.add_argument(
        "--difference-profile",
        default=None,
        help="Optional literature-backed input-difference profile.",
    )
    parser.add_argument(
        "--difference-member",
        type=int,
        default=0,
        help="Member index for multi-fixed difference profiles.",
    )
    parser.add_argument(
        "--plan",
        default=None,
        help="Optional literature-ranked CSV plan from build_innovation_one_matrix.py.",
    )
    parser.add_argument(
        "--dataset-cache-root",
        default=None,
        help="Optional root directory for chunk-generated disk-backed datasets.",
    )
    parser.add_argument(
        "--dataset-cache-chunk-size",
        type=int,
        default=8192,
        help="Rows per class generated before flushing to dataset cache.",
    )
    parser.add_argument(
        "--progress-output",
        default=None,
        help="Optional JSONL path for run progress events.",
    )
    parser.add_argument("--output", default="outputs/innovation_one_matrix_results.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    tasks = _build_tasks(args)
    _reset_progress(args.progress_output)
    _write_progress(
        args.progress_output,
        "run_start",
        {
            "total": len(tasks),
            "output": str(output),
            "dataset_cache_root": args.dataset_cache_root,
        },
    )

    try:
        with output.open("w", encoding="utf-8") as handle:
            for index, task in enumerate(tasks, start=1):
                _write_progress(
                    args.progress_output,
                    "row_start",
                    {
                        "index": index,
                        "total": len(tasks),
                        **_task_progress_payload(task),
                    },
                )
                row = _run_task(
                    task,
                    args,
                    progress_path=args.progress_output,
                    index=index,
                    total=len(tasks),
                )
                handle.write(json.dumps(row, sort_keys=True) + "\n")
                handle.flush()
                _write_progress(
                    args.progress_output,
                    "row_done",
                    {
                        "index": index,
                        "total": len(tasks),
                        "accuracy": row["metrics"]["accuracy"],
                        "selected_model": row["selected_model"],
                        **_task_progress_payload(task),
                    },
                )
                print(
                    "[{index}/{total}] {cipher} r={rounds} model={model} "
                    "seed={seed} pairs={pairs}".format(
                        index=index,
                        total=len(tasks),
                        cipher=row["cipher"],
                        rounds=row["rounds"],
                        model=row["model"],
                        seed=row["seed"],
                        pairs=row["pairs_per_sample"],
                    ),
                    flush=True,
                )
    except Exception as exc:
        _write_progress(
            args.progress_output,
            "run_failed",
            {
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
        raise
    _write_progress(
        args.progress_output,
        "run_done",
        {
            "total": len(tasks),
            "output": str(output),
        },
    )
    print(f"wrote {len(tasks)} rows to {output}")


def _run_task(
    task: dict[str, Any],
    args: argparse.Namespace,
    *,
    progress_path: str | None = None,
    index: int | None = None,
    total: int | None = None,
) -> dict[str, Any]:
    train_key = task.get("train_key")
    validation_key = task.get("validation_key")
    if validation_key is None:
        validation_key = train_key
    train_cipher = build_cipher(task["cipher_key"], task["rounds"], key=train_key)
    validation_cipher = build_cipher(
        task["cipher_key"],
        task["rounds"],
        key=validation_key,
    )
    input_difference = task["input_difference"]
    model_key = _select_model_key(task["model_key"], train_cipher.structure, task["pairs_per_sample"])
    pair_bits = _infer_pair_bits(
        train_cipher.block_bits,
        task["feature_encoding"],
        task["pairs_per_sample"],
    )
    train_config = DifferentialDatasetConfig(
        cipher=train_cipher,
        input_difference=input_difference,
        samples_per_class=task["samples_per_class"],
        seed=task["seed"],
        feature_encoding=task["feature_encoding"],
        pairs_per_sample=task["pairs_per_sample"],
        negative_mode=task["negative_mode"],
        key_rotation_interval=task["key_rotation_interval"],
        sample_structure=task["sample_structure"],
        integral_active_nibble=task["integral_active_nibble"],
        selected_bit_indices=task["selected_bit_indices"],
    )
    validation_config = DifferentialDatasetConfig(
        cipher=validation_cipher,
        input_difference=input_difference,
        samples_per_class=max(8, task["samples_per_class"] // 2),
        seed=task["seed"] + 10_000,
        feature_encoding=task["feature_encoding"],
        pairs_per_sample=task["pairs_per_sample"],
        negative_mode=task["negative_mode"],
        key_rotation_interval=task["key_rotation_interval"],
        sample_structure=task["sample_structure"],
        integral_active_nibble=task["integral_active_nibble"],
        selected_bit_indices=task["selected_bit_indices"],
    )
    train_dataset = _make_task_dataset(
        train_config,
        args,
        task,
        split="train",
        progress_path=progress_path,
        index=index,
        total=total,
    )
    validation_dataset = _make_task_dataset(
        validation_config,
        args,
        task,
        split="validation",
        progress_path=progress_path,
        index=index,
        total=total,
    )
    _write_progress(
        progress_path,
        "cache_ready",
        {
            "index": index,
            "total": total,
            "dataset_cache_enabled": bool(args.dataset_cache_root),
            "train_rows": int(train_dataset.features.shape[0]),
            "validation_rows": int(validation_dataset.features.shape[0]),
            "input_bits": int(train_dataset.features.shape[1]),
            **_task_progress_payload(task),
        },
    )
    model = build_model(
        model_key,
        input_bits=train_dataset.features.shape[1],
        hidden_bits=args.hidden_bits,
        pair_bits=pair_bits,
        structure=train_cipher.structure,
        model_options=task.get("model_options"),
    )
    _configure_structure_aware_model(model, task["cipher_key"], task["rounds"])
    pretrain_result = _run_optional_pretraining(
        model,
        task,
        args,
        pair_bits=pair_bits,
        progress_path=progress_path,
        index=index,
        total=total,
    )
    _configure_structure_aware_model(model, task["cipher_key"], task["rounds"])
    result = train_binary_classifier(
        model,
        train_dataset,
        validation_dataset,
        _training_config(task, args, epochs=args.epochs, seed=task["seed"]),
        progress_callback=_progress_callback(
            progress_path,
            "training",
            task,
            index=index,
            total=total,
        ),
    )
    return {
        "cipher": train_cipher.name,
        "cipher_key": task["cipher_key"],
        "structure": train_cipher.structure,
        "model": task["model_key"],
        "selected_model": model_key,
        "architecture": task["architecture"],
        "architecture_rank": task.get("architecture_rank"),
        "matching_score": task.get("matching_score"),
        "matching_evidence": task.get("matching_evidence", ""),
        "literature": task.get("literature", ""),
        "rounds": task["rounds"],
        "seed": task["seed"],
        "train_key": train_key,
        "validation_key": validation_key,
        "input_difference": input_difference,
        "difference_profile": task.get("difference_profile", ""),
        "difference_member": task.get("difference_member", ""),
        "difference_source": task.get("difference_source", ""),
        "samples_per_class": task["samples_per_class"],
        "pairs_per_sample": task["pairs_per_sample"],
        "feature_encoding": task["feature_encoding"],
        "negative_mode": task["negative_mode"],
        "key_rotation_interval": task["key_rotation_interval"],
        "sample_structure": task["sample_structure"],
        "integral_active_nibble": task["integral_active_nibble"],
        "metrics": result.final_metrics,
        "history": result.history,
        "training": {
            **result.metadata,
            "dataset_cache_root": args.dataset_cache_root,
            "dataset_cache_chunk_size": args.dataset_cache_chunk_size if args.dataset_cache_root else None,
            "input_bits": int(train_dataset.features.shape[1]),
            "feature_encoding": task["feature_encoding"],
            "pairs_per_sample": task["pairs_per_sample"],
            "pair_bits": pair_bits,
            "key_rotation_interval": task["key_rotation_interval"],
            "sample_structure": task["sample_structure"],
            "integral_active_nibble": task["integral_active_nibble"],
            "model_options": task.get("model_options", {}),
            "selected_bit_indices": task["selected_bit_indices"],
            "pretraining": _pretraining_metadata(pretrain_result),
        },
        **_model_metadata(model),
        "validation": {
            "cipher": validation_cipher.name,
            "structure": validation_cipher.structure,
            "rounds": validation_cipher.rounds,
            "feature_encoding": validation_dataset.metadata["feature_encoding"],
            "negative_mode": validation_dataset.metadata["negative_mode"],
            "pairs_per_sample": validation_dataset.metadata["pairs_per_sample"],
            "samples_per_class": validation_dataset.metadata["samples_per_class"],
            "key_rotation_interval": validation_dataset.metadata["key_rotation_interval"],
            "sample_structure": validation_dataset.metadata["sample_structure"],
            "integral_active_nibble": validation_dataset.metadata["integral_active_nibble"],
        },
    }


def _run_optional_pretraining(
    model: torch.nn.Module,
    task: dict[str, Any],
    args: argparse.Namespace,
    *,
    pair_bits: int | None,
    progress_path: str | None,
    index: int | None,
    total: int | None,
) -> TrainingResult | None:
    pretrain_epochs = int(
        task.get("pretrain_epochs")
        if task.get("pretrain_epochs") is not None
        else args.pretrain_epochs
    )
    pretrain_rounds = (
        int(task["pretrain_rounds"])
        if task.get("pretrain_rounds") is not None
        else args.pretrain_rounds
    )
    if pretrain_epochs <= 0 or pretrain_rounds is None:
        return None
    if pretrain_rounds == task["rounds"]:
        raise ValueError("pretrain_rounds must differ from target rounds")

    pretrain_task = {**task, "rounds": pretrain_rounds}
    _configure_structure_aware_model(model, pretrain_task["cipher_key"], pretrain_rounds)
    pretrain_cipher = build_cipher(
        pretrain_task["cipher_key"],
        pretrain_rounds,
        key=pretrain_task.get("train_key"),
    )
    validation_key = pretrain_task.get("validation_key")
    if validation_key is None:
        validation_key = pretrain_task.get("train_key")
    pretrain_validation_cipher = build_cipher(
        pretrain_task["cipher_key"],
        pretrain_rounds,
        key=validation_key,
    )
    input_difference = pretrain_task["input_difference"]
    pretrain_train_config = DifferentialDatasetConfig(
        cipher=pretrain_cipher,
        input_difference=input_difference,
        samples_per_class=pretrain_task["samples_per_class"],
        seed=pretrain_task["seed"] + 20_000,
        feature_encoding=pretrain_task["feature_encoding"],
        pairs_per_sample=pretrain_task["pairs_per_sample"],
        negative_mode=pretrain_task["negative_mode"],
        key_rotation_interval=pretrain_task["key_rotation_interval"],
        sample_structure=pretrain_task["sample_structure"],
        integral_active_nibble=pretrain_task["integral_active_nibble"],
        selected_bit_indices=pretrain_task["selected_bit_indices"],
    )
    pretrain_validation_config = DifferentialDatasetConfig(
        cipher=pretrain_validation_cipher,
        input_difference=input_difference,
        samples_per_class=max(8, pretrain_task["samples_per_class"] // 2),
        seed=pretrain_task["seed"] + 30_000,
        feature_encoding=pretrain_task["feature_encoding"],
        pairs_per_sample=pretrain_task["pairs_per_sample"],
        negative_mode=pretrain_task["negative_mode"],
        key_rotation_interval=pretrain_task["key_rotation_interval"],
        sample_structure=pretrain_task["sample_structure"],
        integral_active_nibble=pretrain_task["integral_active_nibble"],
        selected_bit_indices=pretrain_task["selected_bit_indices"],
    )
    pretrain_dataset = _make_task_dataset(
        pretrain_train_config,
        args,
        pretrain_task,
        split="pretrain_train",
        progress_path=progress_path,
        index=index,
        total=total,
    )
    pretrain_validation_dataset = _make_task_dataset(
        pretrain_validation_config,
        args,
        pretrain_task,
        split="pretrain_validation",
        progress_path=progress_path,
        index=index,
        total=total,
    )
    expected_input_bits = int(pretrain_dataset.features.shape[1])
    if pair_bits is not None and expected_input_bits % pair_bits != 0:
        raise ValueError("pretraining feature width is incompatible with target pair_bits")
    _write_progress(
        progress_path,
        "pretrain_cache_ready",
        {
            "index": index,
            "total": total,
            "target_rounds": task["rounds"],
            "pretrain_rounds": pretrain_rounds,
            "pretrain_epochs": pretrain_epochs,
            "train_rows": int(pretrain_dataset.features.shape[0]),
            "validation_rows": int(pretrain_validation_dataset.features.shape[0]),
            "input_bits": expected_input_bits,
            **_task_progress_payload(pretrain_task),
        },
    )
    return train_binary_classifier(
        model,
        pretrain_dataset,
        pretrain_validation_dataset,
        _training_config(
            pretrain_task,
            args,
            epochs=pretrain_epochs,
            seed=pretrain_task["seed"] + 40_000,
        ),
        progress_callback=_progress_callback(
            progress_path,
            "pretraining",
            pretrain_task,
            index=index,
            total=total,
        ),
    )


def _training_config(
    task: dict[str, Any],
    args: argparse.Namespace,
    *,
    epochs: int,
    seed: int,
) -> TrainingConfig:
    return TrainingConfig(
        epochs=epochs,
        batch_size=args.batch_size,
        learning_rate=float(task.get("learning_rate") or args.learning_rate),
        optimizer=str(task.get("optimizer") or args.optimizer),
        amsgrad=args.amsgrad,
        weight_decay=float(task.get("weight_decay") if task.get("weight_decay") is not None else args.weight_decay),
        lr_scheduler=str(task.get("lr_scheduler") or args.lr_scheduler),
        max_learning_rate=task.get("max_learning_rate") if task.get("max_learning_rate") is not None else args.max_learning_rate,
        checkpoint_metric=str(task.get("checkpoint_metric") or args.checkpoint_metric),
        restore_best_checkpoint=bool(task.get("restore_best_checkpoint") if task.get("restore_best_checkpoint") is not None else args.restore_best_checkpoint),
        early_stopping_patience=int(task.get("early_stopping_patience") if task.get("early_stopping_patience") is not None else args.early_stopping_patience),
        early_stopping_min_delta=float(
            task.get("early_stopping_min_delta")
            if task.get("early_stopping_min_delta") is not None
            else args.early_stopping_min_delta
        ),
        loss=str(task.get("loss", args.loss)),
        seed=seed,
        device=args.device,
    )


def _pretraining_metadata(result: TrainingResult | None) -> dict[str, Any]:
    if result is None:
        return {"enabled": False}
    return {
        "enabled": True,
        "metrics": result.final_metrics,
        "epochs_ran": result.metadata.get("epochs_ran"),
        "best_epoch": result.metadata.get("best_epoch"),
        "best_checkpoint_metric": result.metadata.get("best_checkpoint_metric"),
        "selected_checkpoint": result.metadata.get("selected_checkpoint"),
    }


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
    record = {
        "event": event,
        "time": time.time(),
        **(payload or {}),
    }
    with progress_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def _progress_callback(
    path: str | None,
    stage: str,
    task: dict[str, Any],
    *,
    index: int | None,
    total: int | None,
    split: str | None = None,
):
    def callback(event: str, payload: dict[str, Any]) -> None:
        record = {
            "stage": stage,
            "index": index,
            "total": total,
            **_task_progress_payload(task),
            **payload,
        }
        if split is not None:
            record["split"] = split
        _write_progress(path, event, record)

    return callback


def _task_progress_payload(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "cipher_key": task["cipher_key"],
        "model": task["model_key"],
        "architecture": task["architecture"],
        "rounds": task["rounds"],
        "seed": task["seed"],
        "samples_per_class": task["samples_per_class"],
        "pairs_per_sample": task["pairs_per_sample"],
        "feature_encoding": task["feature_encoding"],
        "negative_mode": task["negative_mode"],
        "key_rotation_interval": task["key_rotation_interval"],
        "difference_profile": task.get("difference_profile", ""),
        "difference_member": task.get("difference_member", ""),
        "sample_structure": task["sample_structure"],
        "integral_active_nibble": task["integral_active_nibble"],
        "selected_bit_indices": task["selected_bit_indices"],
        "loss": task.get("loss", ""),
        "pretrain_rounds": task.get("pretrain_rounds"),
        "pretrain_epochs": task.get("pretrain_epochs"),
    }



def _make_task_dataset(
    config: DifferentialDatasetConfig,
    args: argparse.Namespace,
    task: dict[str, Any],
    *,
    split: str,
    progress_path: str | None = None,
    index: int | None = None,
    total: int | None = None,
):
    if not args.dataset_cache_root:
        return make_differential_dataset(config)
    return make_chunked_differential_dataset(
        config,
        cache_dir=_dataset_cache_dir(Path(args.dataset_cache_root), task, config, split),
        chunk_size=args.dataset_cache_chunk_size,
        progress_callback=_progress_callback(
            progress_path,
            "dataset_cache",
            task,
            index=index,
            total=total,
            split=split,
        ),
        progress_context={"split": split},
    )


def _dataset_cache_dir(
    root: Path,
    task: dict[str, Any],
    config: DifferentialDatasetConfig,
    split: str,
) -> Path:
    cache_identity = {
        "cipher_key": task["cipher_key"],
        "rounds": task["rounds"],
        "split": split,
        "seed": config.seed,
        "samples_per_class": config.samples_per_class,
        "pairs_per_sample": config.pairs_per_sample,
        "input_difference": config.input_difference,
        "feature_encoding": config.feature_encoding,
        "negative_mode": config.negative_mode,
        "key_rotation_interval": config.key_rotation_interval,
        "sample_structure": config.sample_structure,
        "integral_active_nibble": config.integral_active_nibble,
        "selected_bit_indices": config.selected_bit_indices,
        "key": task.get("train_key") if split in {"train", "pretrain_train"} else task.get("validation_key"),
    }
    digest = hashlib.sha256(
        json.dumps(cache_identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    return (
        root
        / task["cipher_key"]
        / f"r{task['rounds']}"
        / split
        / f"seed-{config.seed}_{digest}"
    )


def _build_tasks(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.plan:
        return _tasks_from_plan(
            Path(args.plan),
            feature_encoding=args.feature_encoding,
            pairs_per_sample=args.pairs_per_sample,
            difference_profile=args.difference_profile,
            difference_member=args.difference_member,
        )

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
                            "pairs_per_sample": args.pairs_per_sample,
                            "feature_encoding": args.feature_encoding,
                            "negative_mode": args.negative_mode,
                            "key_rotation_interval": args.key_rotation_interval,
                            "sample_structure": args.sample_structure,
                            "integral_active_nibble": args.integral_active_nibble,
                            "selected_bit_indices": (),
                            "loss": args.loss,
                            "pretrain_rounds": args.pretrain_rounds,
                            "pretrain_epochs": args.pretrain_epochs,
                            "model_options": {},
                            "train_key": None,
                            "validation_key": None,
                            **_difference_metadata(
                                cipher_key,
                                args.difference_profile,
                                args.difference_member,
                            ),
                        }
                    )
    return tasks


def _tasks_from_plan(
    path: Path,
    feature_encoding: str,
    pairs_per_sample: int,
    difference_profile: str | None,
    difference_member: int,
) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        _plan_task(
            row,
            feature_encoding,
            pairs_per_sample,
            difference_profile,
            difference_member,
        )
        for row in rows
    ]


def _plan_task(
    row: dict[str, str],
    feature_encoding: str,
    pairs_per_sample: int,
    difference_profile: str | None,
    difference_member: int,
) -> dict[str, Any]:
    cipher_key = _cipher_key(row["cipher"])
    task = {
        "cipher_key": cipher_key,
            "model_key": row["model_key"],
            "architecture": row["network"],
            "architecture_rank": int(row["architecture_rank"]),
            "matching_score": int(row["score"]),
            "matching_evidence": row.get("evidence", ""),
            "literature": row.get("literature", ""),
            "rounds": int(row["rounds"]),
            "seed": int(row["seed"]),
            "samples_per_class": int(row["samples_per_class"]),
            "pairs_per_sample": int(row.get("pairs_per_sample") or pairs_per_sample),
            "feature_encoding": row.get("feature_encoding") or feature_encoding,
            "negative_mode": row.get("negative_mode") or "random_ciphertext",
            "key_rotation_interval": _optional_int(row.get("key_rotation_interval"))
            if row.get("key_rotation_interval") not in {None, ""}
            else 0,
            "sample_structure": row.get("sample_structure") or "independent_pairs",
            "integral_active_nibble": _optional_int(row.get("integral_active_nibble"))
            if row.get("integral_active_nibble") not in {None, ""}
            else 0,
            "loss": row.get("loss") or "bce",
            "learning_rate": _optional_float(row.get("learning_rate")),
            "optimizer": row.get("optimizer") or None,
            "weight_decay": _optional_float(row.get("weight_decay")),
            "lr_scheduler": row.get("lr_scheduler") or None,
            "max_learning_rate": _optional_float(row.get("max_learning_rate")),
            "checkpoint_metric": row.get("checkpoint_metric") or None,
            "restore_best_checkpoint": _optional_bool(row.get("restore_best_checkpoint")),
            "early_stopping_patience": _optional_int(row.get("early_stopping_patience")),
            "early_stopping_min_delta": _optional_float(row.get("early_stopping_min_delta")),
            "pretrain_rounds": _optional_int(row.get("pretrain_rounds")),
            "pretrain_epochs": _optional_int(row.get("pretrain_epochs")),
            "model_options": _optional_json(row.get("model_options")),
            "selected_bit_indices": _optional_int_tuple(row.get("selected_bit_indices")),
            "train_key": _optional_int(row.get("train_key")),
            "validation_key": _optional_int(row.get("validation_key")),
    }
    task.update(
        _difference_metadata(
            cipher_key,
            row.get("difference_profile") or difference_profile,
            int(row.get("difference_member") or difference_member),
        )
    )
    return task


def _difference_metadata(
    cipher_key: str,
    profile_name: str | None,
    member_index: int,
) -> dict[str, Any]:
    if not profile_name:
        return {
            "input_difference": default_difference(cipher_key),
            "difference_profile": "",
            "difference_member": "",
            "difference_source": "",
        }
    profile = literature_difference_profiles()[profile_name]
    if profile.cipher != cipher_key:
        raise ValueError(
            f"difference profile {profile_name} is for {profile.cipher}, not {cipher_key}"
        )
    return {
        "input_difference": difference_for_profile(profile_name, member_index),
        "difference_profile": profile_name,
        "difference_member": member_index,
        "difference_source": profile.source,
    }


def _configure_structure_aware_model(model: Any, cipher_key: str, rounds: int) -> None:
    if not hasattr(model, "set_structure_features"):
        return
    vector = structure_feature_vector(_cipher_profile(cipher_key), rounds)
    model.set_structure_features(torch.tensor(vector, dtype=torch.float32))


def _model_metadata(model: Any) -> dict[str, Any]:
    if not hasattr(model, "gate_summary"):
        return {}
    summary = model.gate_summary()
    gate_weights = {
        key.removeprefix("gate_weight_"): value
        for key, value in summary.items()
        if key.startswith("gate_weight_")
    }
    return {
        "gate_mode": summary["gate_mode"],
        "expert_set": summary.get("expert_set", "legacy"),
        "adapter_mode": summary.get("adapter_mode", "none"),
        "adapter_name": summary.get("adapter_name", "identity"),
        "gate_weights_mean": gate_weights,
    }


def _infer_pair_bits(
    block_bits: int,
    feature_encoding: str,
    pairs_per_sample: int,
) -> int | None:
    try:
        return pair_bits_for_encoding(block_bits, feature_encoding)
    except ValueError:
        return None


def _optional_json(value: str | None) -> dict[str, Any]:
    if value is None:
        return {}
    value = value.strip()
    if not value:
        return {}
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("model_options must be a JSON object")
    return parsed



def _optional_int_tuple(value: str | None) -> tuple[int, ...]:
    if value is None:
        return ()
    value = value.strip()
    if not value:
        return ()
    parsed = json.loads(value)
    if not isinstance(parsed, list) or not all(isinstance(item, int) for item in parsed):
        raise ValueError("selected_bit_indices must be a JSON list of integers")
    return tuple(parsed)


def _optional_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return float(value)


def _optional_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    value = value.strip().lower()
    if not value:
        return None
    if value in {"1", "true", "yes", "y"}:
        return True
    if value in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"unsupported boolean value: {value}")

def _optional_int(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    return int(value, 0)


def _select_model_key(model_key: str, structure: str, pairs_per_sample: int) -> str:
    if model_key not in {"selector_rule", "selector_rule_v2"}:
        return model_key
    if model_key == "selector_rule_v2" and pairs_per_sample > 1:
        return "adaptive_dbitnet_pairwise"
    if structure == "ARX" and pairs_per_sample > 1:
        return "adaptive_dbitnet_pairwise"
    if structure == "ARX":
        return "resnet_bitslice"
    if structure == "SPN":
        return "senet_resnext"
    if structure == "Feistel-like":
        return "multiscale_dense_resnet"
    return "mlp"


def _cipher_profile(cipher_key: str) -> CipherProfile:
    mapping = {
        "speck32": CipherProfile.speck32_64,
        "present80": CipherProfile.present80,
        "gift64": CipherProfile.gift64,
        "sm4": CipherProfile.sm4,
    }
    try:
        return mapping[cipher_key]()
    except KeyError as exc:
        raise ValueError(f"unsupported cipher key: {cipher_key}") from exc


def _cipher_key(cipher_name: str) -> str:
    mapping = {
        "SPECK32/64": "speck32",
        "PRESENT-80": "present80",
        "GIFT-64": "gift64",
        "SM4": "sm4",
    }
    try:
        return mapping[cipher_name]
    except KeyError as exc:
        raise ValueError(f"unsupported cipher in plan: {cipher_name}") from exc


if __name__ == "__main__":
    main()
