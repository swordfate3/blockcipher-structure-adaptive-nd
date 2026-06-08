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


def arx_aligned_difference(
    difference: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> int:
    if getattr(cipher, "name", "") == "SPECK32/64":
        return speck32_rotation_aligned_difference(difference, width)
    raise ValueError(
        "ARX aligned feature encoding currently supports SPECK32/64; "
        f"got {getattr(cipher, 'name', type(cipher).__name__)}"
    )


def aligned_difference_bits(
    difference: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    from blockcipher_ai_eval.datasets import int_to_bits

    return int_to_bits(arx_aligned_difference(difference, width, cipher), width)
