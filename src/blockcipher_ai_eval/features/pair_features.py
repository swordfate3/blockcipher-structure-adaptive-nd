from __future__ import annotations

from blockcipher_ai_eval.ciphers import ReducedRoundCipher
from blockcipher_ai_eval.features.arx_aligned import (
    arx_aligned_difference,
    speck32_partial_inverse_feature_words,
    speck32_partial_inverse_rx_feature_words,
)
from blockcipher_ai_eval.features.spn_aligned import inverse_permutation_difference


def _present_sbox_ddt() -> list[list[int]]:
    from blockcipher_ai_eval.ciphers.spn.present import PRESENT_SBOX

    table = [[0 for _ in range(16)] for _ in range(16)]
    for input_difference in range(16):
        for value in range(16):
            output_difference = PRESENT_SBOX[value] ^ PRESENT_SBOX[value ^ input_difference]
            table[input_difference][output_difference] += 1
    return table


PRESENT_SBOX_DDT = _present_sbox_ddt()


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
    if feature_encoding == "present_mcnd_cell_matrix_bits":
        return present_mcnd_cell_matrix_bits(left, right, width)
    if feature_encoding == "present_pair_xor_cell_matrix_bits":
        return present_pair_xor_cell_matrix_bits(left, right, width)
    if feature_encoding == "present_pair_xor_paligned_cell_matrix_bits":
        return present_pair_xor_paligned_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sinv_cell_matrix_bits":
        return present_pair_xor_paligned_sinv_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sboxddt_cell_matrix_bits":
        return present_pair_xor_paligned_sboxddt_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_xor_paligned_cell_matrix_bits":
        return present_xor_paligned_cell_matrix_bits(left, right, width, cipher)
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


def present_mcnd_cell_matrix_bits(left: int, right: int, width: int) -> list[int]:
    return words_to_present_cell_matrix_bits([left, right], width, "present_mcnd_cell_matrix_bits")


def present_pair_xor_cell_matrix_bits(left: int, right: int, width: int) -> list[int]:
    return words_to_present_cell_matrix_bits([left, right, left ^ right], width, "present_pair_xor_cell_matrix_bits")


def present_pair_xor_paligned_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference],
        width,
        "present_pair_xor_paligned_cell_matrix_bits",
    )


def present_pair_xor_paligned_sinv_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    structural_inverse_difference = present_structural_inverse_sbox_difference(left, right, width, cipher)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference, structural_inverse_difference],
        width,
        "present_pair_xor_paligned_sinv_cell_matrix_bits",
    )


def present_pair_xor_paligned_sboxddt_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    best_input_difference, ddt_confidence = present_sbox_ddt_words(aligned_difference, width)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference, best_input_difference, ddt_confidence],
        width,
        "present_pair_xor_paligned_sboxddt_cell_matrix_bits",
    )


def present_sbox_ddt_words(aligned_difference: int, width: int) -> tuple[int, int]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_words requires a 4-bit cell block size")
    best_word = 0
    confidence_word = 0
    for nibble_index in range(width // 4):
        output_difference = (aligned_difference >> (4 * nibble_index)) & 0xF
        column = [PRESENT_SBOX_DDT[input_difference][output_difference] for input_difference in range(16)]
        best_input_difference = max(range(16), key=lambda input_difference: column[input_difference])
        best_count = column[best_input_difference]
        confidence = min(15, round(best_count * 15 / 16))
        best_word |= best_input_difference << (4 * nibble_index)
        confidence_word |= confidence << (4 * nibble_index)
    return best_word, confidence_word


def present_structural_inverse_sbox_difference(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> int:
    inverse_sbox = getattr(cipher, "inverse_sbox_layer", None)
    if inverse_sbox is None or not callable(inverse_sbox):
        raise ValueError(
            "present_pair_xor_paligned_sinv_cell_matrix_bits requires a cipher with "
            "inverse_sbox_layer"
        )
    left_aligned = inverse_permutation_difference(left, width, cipher)
    right_aligned = inverse_permutation_difference(right, width, cipher)
    mask = (1 << width) - 1
    return (int(inverse_sbox(left_aligned)) ^ int(inverse_sbox(right_aligned))) & mask


def present_xor_paligned_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    return words_to_present_cell_matrix_bits(
        [difference, aligned_difference],
        width,
        "present_xor_paligned_cell_matrix_bits",
    )


def words_to_present_cell_matrix_bits(words: list[int], width: int, feature_encoding: str) -> list[int]:
    if width % 4 != 0:
        raise ValueError(f"{feature_encoding} requires a 4-bit cell block size")
    bits = []
    for word in words:
        bits.extend(int_to_bits(word, width))
    cells = [bits[index : index + 4] for index in range(0, len(bits), 4)]
    return [cell[bit_index] for bit_index in range(4) for cell in cells]


def xor_bits(left: int, right: int, width: int) -> list[int]:
    return int_to_bits(left ^ right, width)


def pair_xor_bits(left: int, right: int, width: int) -> tuple[list[int], list[int], list[int]]:
    left_bits = int_to_bits(left, width)
    right_bits = int_to_bits(right, width)
    difference_bits = [left_bit ^ right_bit for left_bit, right_bit in zip(left_bits, right_bits)]
    return left_bits, right_bits, difference_bits


def pair_bits_for_encoding(block_bits: int, feature_encoding: str) -> int:
    if feature_encoding in {"ciphertext_pair_bits", "present_mcnd_cell_matrix_bits"}:
        return block_bits * 2
    if feature_encoding == "present_pair_xor_cell_matrix_bits":
        return block_bits * 3
    if feature_encoding == "present_pair_xor_paligned_cell_matrix_bits":
        return block_bits * 4
    if feature_encoding == "present_pair_xor_paligned_sinv_cell_matrix_bits":
        return block_bits * 5
    if feature_encoding == "present_pair_xor_paligned_sboxddt_cell_matrix_bits":
        return block_bits * 6
    if feature_encoding == "present_xor_paligned_cell_matrix_bits":
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
