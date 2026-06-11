from __future__ import annotations

from dataclasses import is_dataclass, replace

import numpy as np

from blockcipher_ai_eval.data.differential.config import (
    DifferentialDataset,
    DifferentialDatasetConfig,
)
from blockcipher_ai_eval.features.pair_features import encode_ciphertext_pair, pair_bits_for_encoding


def make_differential_dataset(config: DifferentialDatasetConfig) -> DifferentialDataset:
    if config.pairs_per_sample < 1:
        raise ValueError("pairs_per_sample must be at least 1")
    if config.key_rotation_interval < 0:
        raise ValueError("key_rotation_interval must be non-negative")
    if config.negative_mode not in {"random_ciphertext", "encrypted_random_plaintexts"}:
        raise ValueError(f"unsupported negative_mode: {config.negative_mode}")
    rng = np.random.default_rng(config.seed)
    block_bits = config.cipher.block_bits
    mask = (1 << block_bits) - 1
    rows: list[list[int]] = []
    labels: list[int] = []

    for row_index in range(config.samples_per_class):
        rows.append(_generate_positive_row(config, rng, block_bits, mask, row_index=row_index))
        labels.append(1)

    for row_index in range(config.samples_per_class):
        rows.append(_generate_negative_row(config, rng, block_bits, row_index=row_index))
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
        "key_rotation_interval": config.key_rotation_interval,
        "key_schedule": "rotating" if config.key_rotation_interval > 0 else "fixed",
        "pair_bits": pair_bits_for_encoding(block_bits, config.feature_encoding),
    }


def generate_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
    row_index: int = 0,
) -> list[int]:
    return _generate_positive_row(config, rng, block_bits, mask, row_index=row_index)


def generate_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    row_index: int = 0,
) -> list[int]:
    return _generate_negative_row(config, rng, block_bits, row_index=row_index)


def _generate_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
    row_index: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    for _pair_index in range(config.pairs_per_sample):
        plaintext = random_int(rng, block_bits)
        paired = (plaintext ^ config.input_difference) & mask
        ciphertext_a = cipher.encrypt(plaintext)
        ciphertext_b = cipher.encrypt(paired)
        encoded_pairs.extend(
            encode_ciphertext_pair(
                ciphertext_a,
                ciphertext_b,
                width=block_bits,
                feature_encoding=config.feature_encoding,
                cipher=cipher,
            )
        )
    return encoded_pairs


def _generate_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    row_index: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    for _pair_index in range(config.pairs_per_sample):
        if config.negative_mode == "random_ciphertext":
            ciphertext_a = random_int(rng, block_bits)
            ciphertext_b = random_int(rng, block_bits)
        else:
            plaintext_a = random_int(rng, block_bits)
            plaintext_b = random_int(rng, block_bits)
            ciphertext_a = cipher.encrypt(plaintext_a)
            ciphertext_b = cipher.encrypt(plaintext_b)
        encoded_pairs.extend(
            encode_ciphertext_pair(
                ciphertext_a,
                ciphertext_b,
                width=block_bits,
                feature_encoding=config.feature_encoding,
                cipher=cipher,
            )
        )
    return encoded_pairs


def _cipher_for_row(config: DifferentialDatasetConfig, rng: np.random.Generator, row_index: int):
    if config.key_rotation_interval == 0:
        return config.cipher
    key_block_index = row_index // config.key_rotation_interval
    row_key = _key_for_block(config, rng, key_block_index)
    return _cipher_with_key(config.cipher, row_key)


def _key_for_block(config: DifferentialDatasetConfig, rng: np.random.Generator, block_index: int) -> int:
    if not hasattr(config.cipher, "key_bits"):
        raise ValueError("rotating key schedule requires cipher.key_bits")
    key_bits = int(config.cipher.key_bits)
    state = rng.bit_generator.state
    try:
        key_rng = np.random.default_rng(config.seed + 1_000_003 * (block_index + 1))
        return random_int(key_rng, key_bits)
    finally:
        rng.bit_generator.state = state


def _cipher_with_key(cipher, key: int):
    if not hasattr(cipher, "rounds"):
        raise ValueError("rotating key schedule requires cipher.rounds")
    if is_dataclass(cipher) and hasattr(cipher, "key"):
        return replace(cipher, key=key)
    try:
        return type(cipher)(rounds=int(cipher.rounds), key=key)
    except TypeError:
        pass
    raise ValueError(f"rotating key schedule is not supported for cipher {type(cipher).__name__}")


def random_int(rng: np.random.Generator, width: int) -> int:
    byte_count = (width + 7) // 8
    value = int.from_bytes(rng.bytes(byte_count), "big")
    return value & ((1 << width) - 1)
