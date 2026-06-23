from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import torch

from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import random_int
from blockcipher_ai_eval.experiments.difference_profiles import difference_for_profile
from blockcipher_ai_eval.experiments.factories import build_cipher
from blockcipher_ai_eval.features.spn_candidate_evidence import (
    present_pairset_candidate_evidence_features,
)


DEFAULT_DIFFERENCE_PROFILE = "present_zhang_wang2022_mcnd"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=7)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--samples-per-class", type=int, default=4096)
    parser.add_argument("--pairs-per-sample", type=int, default=16)
    parser.add_argument("--negative-mode", default="encrypted_random_plaintexts")
    parser.add_argument("--sample-structure", default="zhang_wang_case2_mcnd")
    parser.add_argument("--difference-profile", default=DEFAULT_DIFFERENCE_PROFILE)
    parser.add_argument("--difference-member", type=int, default=0)
    parser.add_argument("--train-key", type=lambda value: int(value, 0), default=0)
    parser.add_argument("--validation-key", type=lambda value: int(value, 0), default=(1 << 80) - 1)
    parser.add_argument("--key-rotation-interval", type=int, default=1024)
    parser.add_argument("--beam-width", type=int, default=4)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--feature-cache-root", type=Path, default=None)
    parser.add_argument("--feature-cache-chunk-size", type=int, default=4096)
    parser.add_argument("--progress-output", type=Path, default=None)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--learning-rate", type=float, default=1e-2)
    parser.add_argument("--model", choices=["linear", "mlp"], default="linear")
    parser.add_argument("--device", default="cpu")
    return parser.parse_args()


def make_candidate_dataset(
    *,
    rounds: int,
    key: int,
    input_difference: int,
    seed: int,
    samples_per_class: int,
    pairs_per_sample: int,
    negative_mode: str,
    sample_structure: str,
    key_rotation_interval: int,
    beam_width: int,
    depth: int,
    feature_cache_root: Path | None = None,
    feature_cache_chunk_size: int = 4096,
    progress_output: Path | None = None,
    split: str = "train",
) -> tuple[np.ndarray, np.ndarray]:
    cipher = build_cipher("present80", rounds, key=key)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=input_difference,
        samples_per_class=samples_per_class,
        seed=seed,
        pairs_per_sample=pairs_per_sample,
        negative_mode=negative_mode,
        key_rotation_interval=key_rotation_interval,
        sample_structure=sample_structure,
    )
    metadata = _candidate_cache_metadata(
        split=split,
        rounds=rounds,
        key=key,
        input_difference=input_difference,
        seed=seed,
        samples_per_class=samples_per_class,
        pairs_per_sample=pairs_per_sample,
        negative_mode=negative_mode,
        sample_structure=sample_structure,
        key_rotation_interval=key_rotation_interval,
        beam_width=beam_width,
        depth=depth,
        width=cipher.block_bits,
    )
    if feature_cache_root is not None:
        return make_cached_candidate_dataset(
            config=config,
            metadata=metadata,
            cache_root=feature_cache_root,
            chunk_size=feature_cache_chunk_size,
            progress_output=progress_output,
        )
    _write_progress(progress_output, "candidate_cache_disabled", metadata)
    return _generate_candidate_dataset_in_memory(config, metadata)


def make_cached_candidate_dataset(
    *,
    config: DifferentialDatasetConfig,
    metadata: dict[str, Any],
    cache_root: Path,
    chunk_size: int,
    progress_output: Path | None,
) -> tuple[np.ndarray, np.ndarray]:
    if chunk_size < 1:
        raise ValueError("feature_cache_chunk_size must be at least 1")
    cache_dir = _candidate_cache_dir(cache_root, metadata)
    features_path = cache_dir / "features.npy"
    labels_path = cache_dir / "labels.npy"
    metadata_path = cache_dir / "metadata.json"
    if features_path.exists() and labels_path.exists() and metadata_path.exists():
        observed_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if observed_metadata == metadata:
            _write_progress(
                progress_output,
                "candidate_cache_reuse",
                {
                    **metadata,
                    "cache_dir": str(cache_dir),
                    "features_path": str(features_path),
                    "labels_path": str(labels_path),
                },
            )
            return np.load(features_path, mmap_mode="r"), np.load(labels_path, mmap_mode="r")

    cache_dir.mkdir(parents=True, exist_ok=True)
    total_rows = int(metadata["total_rows"])
    feature_dim = int(metadata["feature_dim"])
    _write_progress(
        progress_output,
        "candidate_cache_start",
        {
            **metadata,
            "cache_dir": str(cache_dir),
            "chunk_size": chunk_size,
        },
    )
    features = np.lib.format.open_memmap(features_path, mode="w+", dtype=np.float32, shape=(total_rows, feature_dim))
    labels = np.lib.format.open_memmap(labels_path, mode="w+", dtype=np.uint8, shape=(total_rows,))
    _fill_candidate_cache(
        config=config,
        features=features,
        labels=labels,
        metadata=metadata,
        chunk_size=chunk_size,
        progress_output=progress_output,
        cache_dir=cache_dir,
    )
    _write_progress(progress_output, "candidate_cache_flush_start", {**metadata, "cache_dir": str(cache_dir)})
    features.flush()
    labels.flush()
    metadata_path.write_text(json.dumps(metadata, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    _write_progress(
        progress_output,
        "candidate_cache_done",
        {
            **metadata,
            "cache_dir": str(cache_dir),
            "features_path": str(features_path),
            "labels_path": str(labels_path),
            "metadata_path": str(metadata_path),
        },
    )
    return np.load(features_path, mmap_mode="r"), np.load(labels_path, mmap_mode="r")


def _generate_candidate_dataset_in_memory(
    config: DifferentialDatasetConfig,
    metadata: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    total_rows = int(metadata["total_rows"])
    feature_dim = int(metadata["feature_dim"])
    features = np.empty((total_rows, feature_dim), dtype=np.float32)
    labels = np.empty((total_rows,), dtype=np.uint8)
    _fill_candidate_cache(
        config=config,
        features=features,
        labels=labels,
        metadata=metadata,
        chunk_size=total_rows,
        progress_output=None,
        cache_dir=None,
    )
    return features, labels


def _fill_candidate_cache(
    *,
    config: DifferentialDatasetConfig,
    features: np.ndarray,
    labels: np.ndarray,
    metadata: dict[str, Any],
    chunk_size: int,
    progress_output: Path | None,
    cache_dir: Path | None,
) -> None:
    rng = np.random.default_rng(config.seed)
    mask = (1 << config.cipher.block_bits) - 1
    row_index = 0
    for start in range(0, config.samples_per_class, chunk_size):
        count = min(chunk_size, config.samples_per_class - start)
        for offset in range(count):
            source_row = start + offset
            row_cipher = _cipher_for_row(config, rng, source_row)
            pairs = _positive_pairs(config, rng, row_cipher, mask)
            features[row_index] = _pairset_features(config, pairs, row_cipher, metadata)
            labels[row_index] = 1
            row_index += 1
        _write_progress(
            progress_output,
            "candidate_cache_positive_chunk",
            {
                **metadata,
                "cache_dir": str(cache_dir) if cache_dir is not None else None,
                "rows_done": row_index,
                "class_rows_done": start + count,
                "class_total": config.samples_per_class,
                "chunk_rows": count,
            },
        )
    for start in range(0, config.samples_per_class, chunk_size):
        count = min(chunk_size, config.samples_per_class - start)
        for offset in range(count):
            source_row = start + offset
            row_cipher = _cipher_for_row(config, rng, source_row)
            pairs = _negative_pairs(config, rng, row_cipher, mask)
            features[row_index] = _pairset_features(config, pairs, row_cipher, metadata)
            labels[row_index] = 0
            row_index += 1
        _write_progress(
            progress_output,
            "candidate_cache_negative_chunk",
            {
                **metadata,
                "cache_dir": str(cache_dir) if cache_dir is not None else None,
                "rows_done": row_index,
                "class_rows_done": start + count,
                "class_total": config.samples_per_class,
                "chunk_rows": count,
            },
        )
    order = rng.permutation(labels.size)
    features[:] = features[order]
    labels[:] = labels[order]


def _pairset_features(
    config: DifferentialDatasetConfig,
    pairs: list[tuple[int, int]],
    row_cipher,
    metadata: dict[str, Any],
) -> np.ndarray:
    return present_pairset_candidate_evidence_features(
        pairs,
        width=config.cipher.block_bits,
        cipher=row_cipher,
        beam_width=int(metadata["beam_width"]),
        depth=int(metadata["depth"]),
    )


def _candidate_cache_metadata(
    *,
    split: str,
    rounds: int,
    key: int,
    input_difference: int,
    seed: int,
    samples_per_class: int,
    pairs_per_sample: int,
    negative_mode: str,
    sample_structure: str,
    key_rotation_interval: int,
    beam_width: int,
    depth: int,
    width: int,
) -> dict[str, Any]:
    feature_dim = depth * 20 * 3 + 6
    return {
        "cache_type": "spn_candidate_evidence",
        "cipher": "present80",
        "split": split,
        "rounds": rounds,
        "key": key,
        "input_difference": input_difference,
        "seed": seed,
        "samples_per_class": samples_per_class,
        "total_rows": samples_per_class * 2,
        "pairs_per_sample": pairs_per_sample,
        "negative_mode": negative_mode,
        "sample_structure": sample_structure,
        "key_rotation_interval": key_rotation_interval,
        "beam_width": beam_width,
        "depth": depth,
        "source": "structural_inverse",
        "width": width,
        "feature_dim": feature_dim,
        "feature_dtype": "float32",
        "label_dtype": "uint8",
        "shuffle": True,
        "cache_version": 1,
    }


def _candidate_cache_dir(cache_root: Path, metadata: dict[str, Any]) -> Path:
    encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()[:16]
    return cache_root / str(metadata["split"]) / digest


def _write_progress(path: Path | None, event: str, payload: dict[str, Any] | None = None) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"event": event, **(payload or {})}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def _positive_pairs(config: DifferentialDatasetConfig, rng: np.random.Generator, cipher, mask: int) -> list[tuple[int, int]]:
    base = random_int(rng, cipher.block_bits)
    pairs = []
    for mask_delta in _plaintext_masks(config, rng):
        plaintext = (base ^ mask_delta) & mask
        paired = (plaintext ^ config.input_difference) & mask
        pairs.append((cipher.encrypt(plaintext), cipher.encrypt(paired)))
    return pairs


def _negative_pairs(config: DifferentialDatasetConfig, rng: np.random.Generator, cipher, mask: int) -> list[tuple[int, int]]:
    base = random_int(rng, cipher.block_bits)
    pairs = []
    for mask_delta in _plaintext_masks(config, rng):
        if config.negative_mode == "random_ciphertext":
            pairs.append((random_int(rng, cipher.block_bits), random_int(rng, cipher.block_bits)))
        else:
            plaintext_a = (base ^ mask_delta) & mask
            plaintext_b = random_int(rng, cipher.block_bits)
            pairs.append((cipher.encrypt(plaintext_a), cipher.encrypt(plaintext_b)))
    return pairs


def _plaintext_masks(config: DifferentialDatasetConfig, rng: np.random.Generator) -> list[int]:
    if config.sample_structure == "independent_pairs":
        return [random_int(rng, config.cipher.block_bits) for _ in range(config.pairs_per_sample)]
    if config.sample_structure != "zhang_wang_case2_mcnd":
        raise ValueError(f"unsupported sample_structure for candidate evidence: {config.sample_structure}")
    masks = {0}
    while len(masks) < config.pairs_per_sample:
        masks.add(random_int(rng, config.cipher.block_bits))
    return list(masks)


def _cipher_for_row(config: DifferentialDatasetConfig, rng: np.random.Generator, row_index: int):
    if config.key_rotation_interval == 0:
        return config.cipher
    key_block_index = row_index // config.key_rotation_interval
    key_rng = np.random.default_rng(config.seed + 1_000_003 * (key_block_index + 1))
    key = random_int(key_rng, int(config.cipher.key_bits))
    return replace(config.cipher, key=key)


def build_baseline(input_dim: int, model: str) -> torch.nn.Module:
    if model == "linear":
        return torch.nn.Linear(input_dim, 1)
    return torch.nn.Sequential(
        torch.nn.LayerNorm(input_dim),
        torch.nn.Linear(input_dim, 128),
        torch.nn.GELU(),
        torch.nn.Linear(128, 64),
        torch.nn.GELU(),
        torch.nn.Linear(64, 1),
    )


def train_model(
    features: np.ndarray,
    labels: np.ndarray,
    *,
    model_name: str,
    epochs: int,
    learning_rate: float,
    device: torch.device,
) -> torch.nn.Module:
    torch.manual_seed(0)
    x = torch.from_numpy(features.astype(np.float32)).to(device)
    y = torch.from_numpy(labels.astype(np.float32)).reshape(-1, 1).to(device)
    model = build_baseline(features.shape[1], model_name).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    for _epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
    return model


def binary_accuracy(labels: np.ndarray, probabilities: np.ndarray, *, threshold: float = 0.5) -> float:
    predictions = (probabilities >= threshold).astype(np.uint8)
    return float((predictions == labels.astype(np.uint8)).mean())


def binary_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    label_array = labels.astype(np.uint8)
    positive_count = int(label_array.sum())
    negative_count = int(label_array.size - positive_count)
    if positive_count == 0 or negative_count == 0:
        return 0.5
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty_like(sorted_scores, dtype=np.float64)
    start = 0
    while start < sorted_scores.size:
        end = start + 1
        while end < sorted_scores.size and sorted_scores[end] == sorted_scores[start]:
            end += 1
        ranks[start:end] = (start + 1 + end) / 2.0
        start = end
    original_ranks = np.empty_like(ranks)
    original_ranks[order] = ranks
    positive_rank_sum = float(original_ranks[label_array == 1].sum())
    return (positive_rank_sum - positive_count * (positive_count + 1) / 2.0) / (
        positive_count * negative_count
    )


def main() -> None:
    args = parse_args()
    input_difference = difference_for_profile(args.difference_profile, args.difference_member)
    train_features, train_labels = make_candidate_dataset(
        rounds=args.rounds,
        key=args.train_key,
        input_difference=input_difference,
        seed=args.seed,
        samples_per_class=args.samples_per_class,
        pairs_per_sample=args.pairs_per_sample,
        negative_mode=args.negative_mode,
        sample_structure=args.sample_structure,
        key_rotation_interval=args.key_rotation_interval,
        beam_width=args.beam_width,
        depth=args.depth,
        feature_cache_root=args.feature_cache_root,
        feature_cache_chunk_size=args.feature_cache_chunk_size,
        progress_output=args.progress_output,
        split="train",
    )
    validation_features, validation_labels = make_candidate_dataset(
        rounds=args.rounds,
        key=args.validation_key,
        input_difference=input_difference,
        seed=args.seed + 10_000,
        samples_per_class=max(1024, args.samples_per_class // 4),
        pairs_per_sample=args.pairs_per_sample,
        negative_mode=args.negative_mode,
        sample_structure=args.sample_structure,
        key_rotation_interval=args.key_rotation_interval,
        beam_width=args.beam_width,
        depth=args.depth,
        feature_cache_root=args.feature_cache_root,
        feature_cache_chunk_size=args.feature_cache_chunk_size,
        progress_output=args.progress_output,
        split="validation",
    )
    device = torch.device(args.device)
    model = train_model(
        train_features,
        train_labels,
        model_name=args.model,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        device=device,
    )
    with torch.no_grad():
        logits = (
            model(torch.from_numpy(validation_features.astype(np.float32)).to(device))
            .detach()
            .cpu()
            .numpy()
            .reshape(-1)
        )
    probabilities = 1.0 / (1.0 + np.exp(-logits))
    result = {
        "route": "spn_candidate_evidence_baseline",
        "rounds": args.rounds,
        "seed": args.seed,
        "samples_per_class": args.samples_per_class,
        "validation_samples_per_class": max(1024, args.samples_per_class // 4),
        "pairs_per_sample": args.pairs_per_sample,
        "negative_mode": args.negative_mode,
        "sample_structure": args.sample_structure,
        "difference_profile": args.difference_profile,
        "difference_member": args.difference_member,
        "input_difference": input_difference,
        "key_rotation_interval": args.key_rotation_interval,
        "beam_width": args.beam_width,
        "depth": args.depth,
        "model": args.model,
        "device": args.device,
        "feature_cache_enabled": args.feature_cache_root is not None,
        "feature_cache_root": str(args.feature_cache_root) if args.feature_cache_root is not None else None,
        "feature_cache_chunk_size": args.feature_cache_chunk_size,
        "progress_output": str(args.progress_output) if args.progress_output is not None else None,
        "feature_dim": int(train_features.shape[1]),
        "val_accuracy": binary_accuracy(validation_labels, probabilities),
        "val_auc": binary_auc(validation_labels, probabilities),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
