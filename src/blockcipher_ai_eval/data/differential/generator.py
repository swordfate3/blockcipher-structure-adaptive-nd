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
    _validate_config(config)
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
        "sample_structure": config.sample_structure,
        "integral_active_nibble": config.integral_active_nibble,
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
    if config.sample_structure == "plaintext_integral_nibble":
        return _generate_integral_positive_row(config, rng, block_bits, mask, row_index)
    if config.sample_structure == "zhang_wang_case2_mcnd":
        return _generate_zhang_wang_case2_positive_row(config, rng, block_bits, mask, row_index)
    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    for _pair_index in range(config.pairs_per_sample):
        plaintext = random_int(rng, block_bits)
        paired = (plaintext ^ config.input_difference) & mask
        ciphertext_a = cipher.encrypt(plaintext)
        ciphertext_b = cipher.encrypt(paired)
        encoded_pairs.extend(_encode_pair(ciphertext_a, ciphertext_b, block_bits, config, cipher))
    return encoded_pairs


def _generate_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    row_index: int,
) -> list[int]:
    if config.sample_structure == "plaintext_integral_nibble":
        return _generate_integral_negative_row(config, rng, block_bits, row_index)
    if config.sample_structure == "zhang_wang_case2_mcnd":
        return _generate_zhang_wang_case2_negative_row(config, rng, block_bits, row_index)
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
        encoded_pairs.extend(_encode_pair(ciphertext_a, ciphertext_b, block_bits, config, cipher))
    return encoded_pairs


def _generate_integral_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
    row_index: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    base = _integral_base_plaintext(config, rng, block_bits)
    for variant in _integral_variants(config):
        plaintext = base | variant
        paired = (plaintext ^ config.input_difference) & mask
        encoded_pairs.extend(
            _encode_pair(cipher.encrypt(plaintext), cipher.encrypt(paired), block_bits, config, cipher)
        )
    return encoded_pairs


def _generate_integral_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    row_index: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    base = _integral_base_plaintext(config, rng, block_bits)
    for variant in _integral_variants(config):
        plaintext = base | variant
        if config.negative_mode == "random_ciphertext":
            ciphertext_a = random_int(rng, block_bits)
            ciphertext_b = random_int(rng, block_bits)
        else:
            plaintext_b = random_int(rng, block_bits)
            ciphertext_a = cipher.encrypt(plaintext)
            ciphertext_b = cipher.encrypt(plaintext_b)
        encoded_pairs.extend(_encode_pair(ciphertext_a, ciphertext_b, block_bits, config, cipher))
    return encoded_pairs


def _generate_zhang_wang_case2_positive_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    mask: int,
    row_index: int,
) -> list[int]:
    """Generate a grouped MCND sample inspired by Zhang/Wang 2022 Case 2.

    Each sample contains m ciphertext pairs derived from one base plaintext and
    m random public masks. This keeps pairs in one sample correlated through the
    same base block, unlike independent pair-set generation.
    """

    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    base = random_int(rng, block_bits)
    for mask_delta in _mcnd_plaintext_masks(config, rng, block_bits):
        plaintext = (base ^ mask_delta) & mask
        paired = (plaintext ^ config.input_difference) & mask
        encoded_pairs.extend(
            _encode_pair(cipher.encrypt(plaintext), cipher.encrypt(paired), block_bits, config, cipher)
        )
    return encoded_pairs


def _generate_zhang_wang_case2_negative_row(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
    row_index: int,
) -> list[int]:
    encoded_pairs: list[int] = []
    cipher = _cipher_for_row(config, rng, row_index)
    base = random_int(rng, block_bits)
    for mask_delta in _mcnd_plaintext_masks(config, rng, block_bits):
        if config.negative_mode == "random_ciphertext":
            ciphertext_a = random_int(rng, block_bits)
            ciphertext_b = random_int(rng, block_bits)
        else:
            plaintext_a = base ^ mask_delta
            plaintext_b = random_int(rng, block_bits)
            ciphertext_a = cipher.encrypt(plaintext_a)
            ciphertext_b = cipher.encrypt(plaintext_b)
        encoded_pairs.extend(_encode_pair(ciphertext_a, ciphertext_b, block_bits, config, cipher))
    return encoded_pairs


def _mcnd_plaintext_masks(
    config: DifferentialDatasetConfig,
    rng: np.random.Generator,
    block_bits: int,
) -> list[int]:
    if config.pairs_per_sample == 1:
        return [0]
    masks = {0}
    while len(masks) < config.pairs_per_sample:
        masks.add(random_int(rng, block_bits))
    return list(masks)


def _encode_pair(left: int, right: int, block_bits: int, config: DifferentialDatasetConfig, cipher) -> list[int]:
    return encode_ciphertext_pair(
        left,
        right,
        width=block_bits,
        feature_encoding=config.feature_encoding,
        cipher=cipher,
    )


def _integral_base_plaintext(
    config: DifferentialDatasetConfig, rng: np.random.Generator, block_bits: int
) -> int:
    active_mask = _integral_active_mask(config, block_bits)
    return random_int(rng, block_bits) & ~active_mask


def _integral_variants(config: DifferentialDatasetConfig) -> list[int]:
    shift = config.integral_active_nibble * 4
    return [value << shift for value in range(config.pairs_per_sample)]


def _integral_active_mask(config: DifferentialDatasetConfig, block_bits: int) -> int:
    shift = config.integral_active_nibble * 4
    return ((1 << (config.pairs_per_sample.bit_length() - 1)) - 1) << shift




def _validate_config(config: DifferentialDatasetConfig) -> None:
    if config.key_rotation_interval < 0:
        raise ValueError("key_rotation_interval must be non-negative")
    if config.negative_mode not in {"random_ciphertext", "encrypted_random_plaintexts"}:
        raise ValueError(f"unsupported negative_mode: {config.negative_mode}")
    if config.sample_structure not in {
        "independent_pairs",
        "plaintext_integral_nibble",
        "zhang_wang_case2_mcnd",
    }:
        raise ValueError(f"unsupported sample_structure: {config.sample_structure}")
    if config.sample_structure == "plaintext_integral_nibble":
        if config.pairs_per_sample < 2 or config.pairs_per_sample & (config.pairs_per_sample - 1):
            raise ValueError("plaintext_integral_nibble requires power-of-two pairs_per_sample >= 2")
        if config.pairs_per_sample > 16:
            raise ValueError("plaintext_integral_nibble currently supports at most one active nibble")
        max_nibble = config.cipher.block_bits // 4
        if config.integral_active_nibble < 0 or config.integral_active_nibble >= max_nibble:
            raise ValueError("integral_active_nibble is outside the cipher block")
    if config.sample_structure == "zhang_wang_case2_mcnd" and config.pairs_per_sample < 1:
        raise ValueError("zhang_wang_case2_mcnd requires pairs_per_sample >= 1")

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
