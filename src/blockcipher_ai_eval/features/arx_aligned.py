from __future__ import annotations

from blockcipher_ai_eval.ciphers import ReducedRoundCipher
from blockcipher_ai_eval.ciphers.base import rol, ror


def speck32_rotation_aligned_difference(difference: int, width: int) -> int:
    if width != 32:
        raise ValueError("SPECK32/64 ARX aligned feature encoding requires 32-bit blocks")
    word_bits = 16
    mask = (1 << word_bits) - 1
    delta_left = (difference >> word_bits) & mask
    delta_right = difference & mask
    aligned_left = ror(delta_left, 7, word_bits)
    aligned_right = rol(delta_right, 2, word_bits)
    return (aligned_left << word_bits) | aligned_right


def _require_speck32(width: int, cipher: ReducedRoundCipher) -> None:
    if getattr(cipher, "name", "") != "SPECK32/64":
        raise ValueError(
            "ARX aligned feature encoding currently supports SPECK32/64; "
            f"got {getattr(cipher, 'name', type(cipher).__name__)}"
        )
    if width != 32:
        raise ValueError("SPECK32/64 ARX feature encoding requires 32-bit blocks")


def speck32_partial_inverse_words(left: int, right: int, width: int) -> tuple[int, int, int]:
    if width != 32:
        raise ValueError("SPECK32/64 partial-inverse encoding requires 32-bit blocks")
    mask = 0xFFFF
    x = (left >> 16) & mask
    y = left & mask
    x_prime = (right >> 16) & mask
    y_prime = right & mask
    pre_y = ror(y ^ x, 2, 16)
    pre_y_prime = ror(y_prime ^ x_prime, 2, 16)
    return pre_y, pre_y_prime, pre_y ^ pre_y_prime


def speck32_partial_inverse_feature_words(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> tuple[int, ...]:
    _require_speck32(width, cipher)
    rotation_aligned = speck32_rotation_aligned_difference(left ^ right, width)
    pre_y, pre_y_prime, delta_pre_y = speck32_partial_inverse_words(left, right, width)
    return (rotation_aligned, pre_y, pre_y_prime, delta_pre_y)


def speck32_partial_inverse_rx_feature_words(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> tuple[int, ...]:
    _require_speck32(width, cipher)
    base_words = speck32_partial_inverse_feature_words(left, right, width, cipher)
    mask = 0xFFFF
    x = (left >> 16) & mask
    y = left & mask
    x_prime = (right >> 16) & mask
    y_prime = right & mask
    rx_alpha = ((rol(x, 7, 16) ^ x_prime) << 16) | (rol(y, 7, 16) ^ y_prime)
    rx_beta = ((rol(x, 2, 16) ^ x_prime) << 16) | (rol(y, 2, 16) ^ y_prime)
    carry_left = ((x + y) & mask) ^ x ^ y
    carry_right = ((x_prime + y_prime) & mask) ^ x_prime ^ y_prime
    carry_delta = carry_left ^ carry_right
    carry_left_delta = (carry_left << 16) | carry_delta
    carry_right_delta = (carry_right << 16) | carry_delta
    return (*base_words, rx_alpha, rx_beta, carry_left_delta, carry_right_delta)


def arx_aligned_difference(
    difference: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> int:
    _require_speck32(width, cipher)
    return speck32_rotation_aligned_difference(difference, width)


def aligned_difference_bits(
    difference: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    from blockcipher_ai_eval.datasets import int_to_bits

    return int_to_bits(arx_aligned_difference(difference, width, cipher), width)
