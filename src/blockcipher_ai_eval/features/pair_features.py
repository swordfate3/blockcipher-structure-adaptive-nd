from __future__ import annotations

from blockcipher_ai_eval.ciphers import ReducedRoundCipher
from blockcipher_ai_eval.features.arx_aligned import (
    arx_aligned_difference,
    speck32_partial_inverse_feature_words,
    speck32_partial_inverse_rx_feature_words,
)
from blockcipher_ai_eval.features.spn_aligned import inverse_permutation_difference


def int_to_bits(value: int, width: int) -> list[int]:
    return [(value >> shift) & 1 for shift in range(width - 1, -1, -1)]


def encode_ciphertext_pair(
    left: int,
    right: int,
    *,
    width: int,
    feature_encoding: str,
    cipher: ReducedRoundCipher,
) -> list[int]:
    if feature_encoding == "ciphertext_pair_bits":
        return pair_to_bits(left, right, width)
    if feature_encoding == "ciphertext_xor_bits":
        return xor_bits(left, right, width)
    if feature_encoding in {"ciphertext_xor_spn_aligned_bits", "ciphertext_xor_spn_paligned_bits"}:
        difference = left ^ right
        return int_to_bits(difference, width) + int_to_bits(
            inverse_permutation_difference(difference, width, cipher),
            width,
        )
    if feature_encoding == "ciphertext_pair_xor_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        return left_bits + right_bits + difference_bits
    if feature_encoding == "ciphertext_pair_xor_spn_aligned_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        aligned_difference = inverse_permutation_difference(left ^ right, width, cipher)
        return left_bits + right_bits + difference_bits + int_to_bits(aligned_difference, width)
    if feature_encoding == "ciphertext_pair_xor_arx_aligned_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        aligned_difference = arx_aligned_difference(left ^ right, width, cipher)
        return left_bits + right_bits + difference_bits + int_to_bits(aligned_difference, width)
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        extra_bits = []
        for word in speck32_partial_inverse_feature_words(left, right, width, cipher):
            extra_bits.extend(int_to_bits(word, width))
        return left_bits + right_bits + difference_bits + extra_bits
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_rx_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        extra_bits = []
        for word in speck32_partial_inverse_rx_feature_words(left, right, width, cipher):
            extra_bits.extend(int_to_bits(word, width))
        return left_bits + right_bits + difference_bits + extra_bits
    raise ValueError(f"unsupported feature encoding: {feature_encoding}")


def pair_to_bits(left: int, right: int, width: int) -> list[int]:
    return int_to_bits(left, width) + int_to_bits(right, width)


def xor_bits(left: int, right: int, width: int) -> list[int]:
    return int_to_bits(left ^ right, width)


def pair_xor_bits(left: int, right: int, width: int) -> tuple[list[int], list[int], list[int]]:
    left_bits = int_to_bits(left, width)
    right_bits = int_to_bits(right, width)
    difference_bits = [left_bit ^ right_bit for left_bit, right_bit in zip(left_bits, right_bits)]
    return left_bits, right_bits, difference_bits


def pair_bits_for_encoding(block_bits: int, feature_encoding: str) -> int:
    if feature_encoding == "ciphertext_pair_bits":
        return block_bits * 2
    if feature_encoding == "ciphertext_xor_bits":
        return block_bits
    if feature_encoding in {"ciphertext_xor_spn_aligned_bits", "ciphertext_xor_spn_paligned_bits"}:
        return block_bits * 2
    if feature_encoding == "ciphertext_pair_xor_bits":
        return block_bits * 3
    if feature_encoding == "ciphertext_pair_xor_spn_aligned_bits":
        return block_bits * 4
    if feature_encoding == "ciphertext_pair_xor_arx_aligned_bits":
        return block_bits * 4
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_bits":
        return block_bits * 7
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_rx_bits":
        return block_bits * 11
    raise ValueError(f"unsupported feature encoding: {feature_encoding}")
