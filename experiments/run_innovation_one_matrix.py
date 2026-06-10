from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.datasets import (
    DifferentialDatasetConfig,
    make_chunked_differential_dataset,
    make_differential_dataset,
)
from blockcipher_ai_eval.experiments import (
    build_cipher,
    build_model,
    default_difference,
    difference_for_profile,
    literature_difference_profiles,
)
from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.features import structure_feature_vector
from blockcipher_ai_eval.features.encodings import pair_bits_for_encoding
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
        "--feature-encoding",
        default="ciphertext_pair_bits",
        choices=[
            "ciphertext_pair_bits",
            "ciphertext_xor_bits",
            "ciphertext_xor_spn_aligned_bits",
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
    parser.add_argument("--output", default="outputs/innovation_one_matrix_results.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    tasks = _build_tasks(args)

    with output.open("w", encoding="utf-8") as handle:
        for index, task in enumerate(tasks, start=1):
            row = _run_task(task, args)
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            handle.flush()
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
    print(f"wrote {len(tasks)} rows to {output}")


def _run_task(task: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
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
    )
    validation_config = DifferentialDatasetConfig(
        cipher=validation_cipher,
        input_difference=input_difference,
        samples_per_class=max(8, task["samples_per_class"] // 2),
        seed=task["seed"] + 10_000,
        feature_encoding=task["feature_encoding"],
        pairs_per_sample=task["pairs_per_sample"],
        negative_mode=task["negative_mode"],
    )
    train_dataset = _make_task_dataset(train_config, args, task, split="train")
    validation_dataset = _make_task_dataset(validation_config, args, task, split="validation")
    model = build_model(
        model_key,
        input_bits=train_dataset.features.shape[1],
        hidden_bits=args.hidden_bits,
        pair_bits=pair_bits,
        structure=train_cipher.structure,
    )
    _configure_structure_aware_model(model, task["cipher_key"], task["rounds"])
    result = train_binary_classifier(
        model,
        train_dataset,
        validation_dataset,
        TrainingConfig(
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
            optimizer=args.optimizer,
            amsgrad=args.amsgrad,
            weight_decay=args.weight_decay,
            lr_scheduler=args.lr_scheduler,
            max_learning_rate=args.max_learning_rate,
            seed=task["seed"],
            device=args.device,
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
        },
    }



def _make_task_dataset(
    config: DifferentialDatasetConfig,
    args: argparse.Namespace,
    task: dict[str, Any],
    *,
    split: str,
):
    if not args.dataset_cache_root:
        return make_differential_dataset(config)
    return make_chunked_differential_dataset(
        config,
        cache_dir=_dataset_cache_dir(Path(args.dataset_cache_root), task, config, split),
        chunk_size=args.dataset_cache_chunk_size,
    )


def _dataset_cache_dir(
    root: Path,
    task: dict[str, Any],
    config: DifferentialDatasetConfig,
    split: str,
) -> Path:
    key = task.get("train_key") if split == "train" else task.get("validation_key")
    key_part = "key-default" if key is None else f"key-{int(key):x}"
    return root / task["cipher_key"] / f"r{task['rounds']}" / split / (
        f"seed-{config.seed}_samples-{config.samples_per_class}_pairs-{config.pairs_per_sample}_"
        f"diff-{config.input_difference:x}_{config.feature_encoding}_{config.negative_mode}_{key_part}"
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
