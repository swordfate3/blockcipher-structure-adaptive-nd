from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from blockcipher_ai_eval.ciphers import ReducedRoundCipher
from blockcipher_ai_eval.features.encodings import (
    encode_ciphertext_pair,
    int_to_bits,
    pair_bits_for_encoding,
)


@dataclass(frozen=True)
class DifferentialDatasetConfig:
    cipher: ReducedRoundCipher
    input_difference: int
    samples_per_class: int
    seed: int
    shuffle: bool = True
    feature_encoding: str = "ciphertext_pair_bits"
    pairs_per_sample: int = 1
    negative_mode: str = "random_ciphertext"


@dataclass(frozen=True)
class DifferentialDataset:
    features: NDArray[np.uint8]
    labels: NDArray[np.uint8]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class DiskDifferentialDataset(DifferentialDataset):
    cache_dir: Path


def make_differential_dataset(config: DifferentialDatasetConfig) -> DifferentialDataset:
    if config.pairs_per_sample < 1:
        raise ValueError("pairs_per_sample must be at least 1")
    if config.negative_mode not in {"random_ciphertext", "encrypted_random_plaintexts"}:
        raise ValueError(f"unsupported negative_mode: {config.negative_mode}")
    rng = np.random.default_rng(config.seed)
    block_bits = config.cipher.block_bits
    mask = (1 << block_bits) - 1
    rows: list[list[int]] = []
    labels: list[int] = []

    for _ in range(config.samples_per_class):
        encoded_pairs = []
        for _pair_index in range(config.pairs_per_sample):
            plaintext = int(rng.integers(0, 1 << min(block_bits, 63), dtype=np.uint64))
            if block_bits > 63:
                plaintext = _random_int(rng, block_bits)
            paired = (plaintext ^ config.input_difference) & mask
            ciphertext_a = config.cipher.encrypt(plaintext)
            ciphertext_b = config.cipher.encrypt(paired)
            encoded_pairs.extend(
                encode_ciphertext_pair(
                    ciphertext_a,
                    ciphertext_b,
                    width=block_bits,
                    feature_encoding=config.feature_encoding,
                    cipher=config.cipher,
                )
            )
        rows.append(encoded_pairs)
        labels.append(1)

    for _ in range(config.samples_per_class):
        encoded_pairs = []
        for _pair_index in range(config.pairs_per_sample):
            if config.negative_mode == "random_ciphertext":
                ciphertext_a = _random_int(rng, block_bits)
                ciphertext_b = _random_int(rng, block_bits)
            else:
                plaintext_a = _random_int(rng, block_bits)
                plaintext_b = _random_int(rng, block_bits)
                ciphertext_a = config.cipher.encrypt(plaintext_a)
                ciphertext_b = config.cipher.encrypt(plaintext_b)
            encoded_pairs.extend(
                encode_ciphertext_pair(
                    ciphertext_a,
                    ciphertext_b,
                    width=block_bits,
                    feature_encoding=config.feature_encoding,
                    cipher=config.cipher,
                )
            )
        rows.append(encoded_pairs)
        labels.append(0)

    features = np.array(rows, dtype=np.uint8)
    label_array = np.array(labels, dtype=np.uint8)
    if config.shuffle:
        order = rng.permutation(len(label_array))
        features = features[order]
        label_array = label_array[order]

    metadata = {
        "cipher": config.cipher.name,
        "structure": config.cipher.structure,
        "rounds": config.cipher.rounds,
        "block_bits": block_bits,
        "input_difference": config.input_difference,
        "samples_per_class": config.samples_per_class,
        "seed": config.seed,
        "feature_encoding": config.feature_encoding,
        "pairs_per_sample": config.pairs_per_sample,
        "negative_mode": config.negative_mode,
        "pair_bits": pair_bits_for_encoding(block_bits, config.feature_encoding),
    }
    return DifferentialDataset(features=features, labels=label_array, metadata=metadata)


def make_chunked_differential_dataset(
    config: DifferentialDatasetConfig,
    *,
    cache_dir: str | Path,
    chunk_size: int = 8192,
    reuse: bool = True,
) -> DiskDifferentialDataset:
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    if config.pairs_per_sample < 1:
        raise ValueError("pairs_per_sample must be at least 1")
    if config.negative_mode not in {"random_ciphertext", "encrypted_random_plaintexts"}:
        raise ValueError(f"unsupported negative_mode: {config.negative_mode}")

    cache_path = Path(cache_dir)
    features_path = cache_path / "features.npy"
    labels_path = cache_path / "labels.npy"
    metadata_path = cache_path / "metadata.json"
    expected_metadata = _dataset_metadata(config)
    total_rows = config.samples_per_class * 2
    input_bits = expected_metadata["pair_bits"] * config.pairs_per_sample

    if reuse and features_path.exists() and labels_path.exists() and metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if _cache_matches(metadata, expected_metadata, total_rows, input_bits):
            metadata = {**metadata, "cache_status": "reused"}
            features = np.load(features_path, mmap_mode="r")
            labels = np.load(labels_path, mmap_mode="r")
            return DiskDifferentialDataset(
                features=features,
                labels=labels,
                metadata=metadata,
                cache_dir=cache_path,
            )

    cache_path.mkdir(parents=True, exist_ok=True)
    features = np.lib.format.open_memmap(
        features_path,
        mode="w+",
        dtype=np.uint8,
        shape=(total_rows, input_bits),
    )
    labels = np.lib.format.open_memmap(
        labels_path,
        mode="w+",
        dtype=np.uint8,
        shape=(total_rows,),
    )
    rng = np.random.default_rng(config.seed)
    block_bits = config.cipher.block_bits
    mask = (1 << block_bits) - 1

    row_index = 0
    for start in range(0, config.samples_per_class, chunk_size):
        count = min(chunk_size, config.samples_per_class - start)
        chunk_rows = [
            _generate_positive_row(config, rng, block_bits, mask) for _ in range(count)
        ]
        features[row_index : row_index + count] = np.asarray(chunk_rows, dtype=np.uint8)
        labels[row_index : row_index + count] = 1
        row_index += count

    for start in range(0, config.samples_per_class, chunk_size):
        count = min(chunk_size, config.samples_per_class - start)
        chunk_rows = [
            _generate_negative_row(config, rng, block_bits) for _ in range(count)
        ]
        features[row_index : row_index + count] = np.asarray(chunk_rows, dtype=np.uint8)
        labels[row_index : row_index + count] = 0
        row_index += count

    if config.shuffle:
        order = rng.permutation(total_rows)
        shuffled_features = features[order].copy()
        shuffled_labels = labels[order].copy()
        features[:] = shuffled_features
        labels[:] = shuffled_labels

    features.flush()
    labels.flush()
    metadata = {
        **expected_metadata,
        "total_rows": total_rows,
        "input_bits": input_bits,
        "generation_chunk_size": chunk_size,
        "cache_status": "created",
    }
    metadata_path.write_text(json.dumps(metadata, sort_keys=True, indent=2), encoding="utf-8")
    return DiskDifferentialDataset(
        features=np.load(features_path, mmap_mode="r"),
        labels=np.load(labels_path, mmap_mode="r"),
        metadata=metadata,
        cache_dir=cache_path,
    )


def _dataset_metadata(config: DifferentialDatasetConfig) -> dict[str, Any]:
    block_bits = config.cipher.block_bits
    return {
        "cipher": config.cipher.name,
        "structure": config.cipher.structure,
        "rounds": config.cipher.rounds,
        "block_bits": block_bits,
        "input_difference": config.input_difference,
        "samples_per_class": config.samples_per_class,
        "seed": config.seed,
        "shuffle": config.shuffle,
        "feature_encoding": config.feature_encoding,
        "pairs_per_sample": config.pairs_per_sample,
        "negative_mode": config.negative_mode,
        "pair_bits": pair_bits_for_encoding(block_bits, config.feature_encoding),
    }


def _cache_matches(
    metadata: dict[str, Any], expected_metadata: dict[str, Any], total_rows: int, input_bits: int
) -> bool:
    for key, value in expected_metadata.items():
        if metadata.get(key) != value:
            return False
    return metadata.get("total_rows") == total_rows and metadata.get("input_bits") == input_bits


def _generate_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    for _pair_index in range(config.pairs_per_sample):
        plaintext = _random_int(rng, block_bits)
        paired = (plaintext ^ config.input_difference) & mask
        ciphertext_a = config.cipher.encrypt(plaintext)
        ciphertext_b = config.cipher.encrypt(paired)
        encoded_pairs.extend(
            encode_ciphertext_pair(
                ciphertext_a,
                ciphertext_b,
                width=block_bits,
                feature_encoding=config.feature_encoding,
                cipher=config.cipher,
            )
        )
    return encoded_pairs


def _generate_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    for _pair_index in range(config.pairs_per_sample):
        if config.negative_mode == "random_ciphertext":
            ciphertext_a = _random_int(rng, block_bits)
            ciphertext_b = _random_int(rng, block_bits)
        else:
            plaintext_a = _random_int(rng, block_bits)
            plaintext_b = _random_int(rng, block_bits)
            ciphertext_a = config.cipher.encrypt(plaintext_a)
            ciphertext_b = config.cipher.encrypt(plaintext_b)
        encoded_pairs.extend(
            encode_ciphertext_pair(
                ciphertext_a,
                ciphertext_b,
                width=block_bits,
                feature_encoding=config.feature_encoding,
                cipher=config.cipher,
            )
        )
    return encoded_pairs


def _random_int(rng: np.random.Generator, width: int) -> int:
    byte_count = (width + 7) // 8
    value = int.from_bytes(rng.bytes(byte_count), "big")
    return value & ((1 << width) - 1)
