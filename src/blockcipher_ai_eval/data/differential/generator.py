from __future__ import annotations

import numpy as np

from blockcipher_ai_eval.data.differential.config import (
    DifferentialDataset,
    DifferentialDatasetConfig,
)
from blockcipher_ai_eval.features.pair_features import encode_ciphertext_pair, pair_bits_for_encoding


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
        rows.append(_generate_positive_row(config, rng, block_bits, mask))
        labels.append(1)

    for _ in range(config.samples_per_class):
        rows.append(_generate_negative_row(config, rng, block_bits))
        labels.append(0)

    features = np.array(rows, dtype=np.uint8)
    label_array = np.array(labels, dtype=np.uint8)
    if config.shuffle:
        order = rng.permutation(len(label_array))
        features = features[order]
        label_array = label_array[order]

    return DifferentialDataset(
        features=features,
        labels=label_array,
        metadata=dataset_metadata(config),
    )


def dataset_metadata(config: DifferentialDatasetConfig) -> dict[str, int | str | bool]:
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


def generate_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
) -> list[int]:
    return _generate_positive_row(config, rng, block_bits, mask)


def generate_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
) -> list[int]:
    return _generate_negative_row(config, rng, block_bits)


def _generate_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    for _pair_index in range(config.pairs_per_sample):
        plaintext = random_int(rng, block_bits)
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
            ciphertext_a = random_int(rng, block_bits)
            ciphertext_b = random_int(rng, block_bits)
        else:
            plaintext_a = random_int(rng, block_bits)
            plaintext_b = random_int(rng, block_bits)
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


def random_int(rng: np.random.Generator, width: int) -> int:
    byte_count = (width + 7) // 8
    value = int.from_bytes(rng.bytes(byte_count), "big")
    return value & ((1 << width) - 1)
