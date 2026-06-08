from __future__ import annotations

from dataclasses import dataclass
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


def _random_int(rng: np.random.Generator, width: int) -> int:
    byte_count = (width + 7) // 8
    value = int.from_bytes(rng.bytes(byte_count), "big")
    return value & ((1 << width) - 1)
