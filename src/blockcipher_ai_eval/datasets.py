from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from blockcipher_ai_eval.ciphers import ReducedRoundCipher


def int_to_bits(value: int, width: int) -> list[int]:
    return [(value >> shift) & 1 for shift in range(width - 1, -1, -1)]


@dataclass(frozen=True)
class DifferentialDatasetConfig:
    cipher: ReducedRoundCipher
    input_difference: int
    samples_per_class: int
    seed: int
    shuffle: bool = True
    feature_encoding: str = "ciphertext_pair_bits"
    pairs_per_sample: int = 1


@dataclass(frozen=True)
class DifferentialDataset:
    features: NDArray[np.uint8]
    labels: NDArray[np.uint8]
    metadata: dict[str, Any]


def make_differential_dataset(config: DifferentialDatasetConfig) -> DifferentialDataset:
    if config.pairs_per_sample < 1:
        raise ValueError("pairs_per_sample must be at least 1")
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
                _encode_pair(
                    ciphertext_a,
                    ciphertext_b,
                    block_bits,
                    config.feature_encoding,
                )
            )
        rows.append(encoded_pairs)
        labels.append(1)

    for _ in range(config.samples_per_class):
        encoded_pairs = []
        for _pair_index in range(config.pairs_per_sample):
            ciphertext_a = _random_int(rng, block_bits)
            ciphertext_b = _random_int(rng, block_bits)
            encoded_pairs.extend(
                _encode_pair(
                    ciphertext_a,
                    ciphertext_b,
                    block_bits,
                    config.feature_encoding,
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
    }
    return DifferentialDataset(features=features, labels=label_array, metadata=metadata)


def _encode_pair(left: int, right: int, width: int, feature_encoding: str) -> list[int]:
    if feature_encoding == "ciphertext_pair_bits":
        return _pair_to_bits(left, right, width)
    if feature_encoding == "ciphertext_pair_xor_bits":
        left_bits = int_to_bits(left, width)
        right_bits = int_to_bits(right, width)
        difference_bits = [left_bit ^ right_bit for left_bit, right_bit in zip(left_bits, right_bits)]
        return left_bits + right_bits + difference_bits
    raise ValueError(f"unsupported feature encoding: {feature_encoding}")


def _pair_to_bits(left: int, right: int, width: int) -> list[int]:
    return int_to_bits(left, width) + int_to_bits(right, width)


def _random_int(rng: np.random.Generator, width: int) -> int:
    byte_count = (width + 7) // 8
    value = int.from_bytes(rng.bytes(byte_count), "big")
    return value & ((1 << width) - 1)
