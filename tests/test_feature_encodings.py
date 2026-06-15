from blockcipher_ai_eval.ciphers import Present80, Speck32_64
from blockcipher_ai_eval.ciphers.base import rol, ror
from blockcipher_ai_eval.ciphers.spn.gift import Gift64
from blockcipher_ai_eval.features import is_supported_feature_encoding
from blockcipher_ai_eval.features.pair_features import (
    encode_ciphertext_pair,
    int_to_bits,
    pair_bits_for_encoding,
)


def test_pair_features_module_exposes_bit_helpers_and_pair_widths():
    assert int_to_bits(0xA5, 8) == [1, 0, 1, 0, 0, 1, 0, 1]
    assert pair_bits_for_encoding(64, "ciphertext_pair_bits") == 128
    assert pair_bits_for_encoding(64, "ciphertext_xor_bits") == 64
    assert pair_bits_for_encoding(64, "ciphertext_xor_spn_aligned_bits") == 128
    assert pair_bits_for_encoding(64, "ciphertext_pair_xor_bits") == 192
    assert pair_bits_for_encoding(64, "ciphertext_pair_xor_spn_aligned_bits") == 256
    assert pair_bits_for_encoding(32, "ciphertext_pair_xor_arx_aligned_bits") == 128
    assert pair_bits_for_encoding(32, "ciphertext_pair_xor_arx_partial_inverse_bits") == 224
    assert pair_bits_for_encoding(32, "ciphertext_pair_xor_arx_partial_inverse_rx_bits") == 352


def test_pair_features_module_encodes_spn_aligned_pair_features():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    left = 0x0123456789ABCDEF
    right = 0x0123456789ABCDEF ^ 0x0700000000000700

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=64,
        feature_encoding="ciphertext_pair_xor_spn_aligned_bits",
        cipher=cipher,
    )

    difference = left ^ right
    assert len(encoded) == 256
    assert encoded[:64] == int_to_bits(left, 64)
    assert encoded[64:128] == int_to_bits(right, 64)
    assert encoded[128:192] == int_to_bits(difference, 64)
    assert encoded[192:] == int_to_bits(Present80.inverse_permutation_layer(difference), 64)


def test_pair_features_module_encodes_gift_spn_aligned_pair_features():
    cipher = Gift64(rounds=1, key=0)
    left = 0x0123456789ABCDEF
    right = left ^ 0x000F00000000F000

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=64,
        feature_encoding="ciphertext_pair_xor_spn_aligned_bits",
        cipher=cipher,
    )

    difference = left ^ right
    assert len(encoded) == 256
    assert encoded[128:192] == int_to_bits(difference, 64)
    assert encoded[192:] == int_to_bits(Gift64.inverse_permutation_layer(difference), 64)


def test_spn_aligned_encoding_requires_inverse_permutation_layer():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)

    try:
        encode_ciphertext_pair(
            0,
            1,
            width=32,
            feature_encoding="ciphertext_xor_spn_aligned_bits",
            cipher=cipher,
        )
    except ValueError as exc:
        assert "inverse_permutation_layer" in str(exc)
    else:
        raise AssertionError("expected ValueError for non-SPN aligned encoding")


def test_pair_features_module_encodes_speck_arx_aligned_pair_features():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    left = 0x12345678
    right = left ^ 0x00400080

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=32,
        feature_encoding="ciphertext_pair_xor_arx_aligned_bits",
        cipher=cipher,
    )

    difference = left ^ right
    delta_left = (difference >> 16) & 0xFFFF
    delta_right = difference & 0xFFFF
    aligned_difference = (ror(delta_left, 7, 16) << 16) | rol(delta_right, 2, 16)

    assert len(encoded) == 128
    assert encoded[:32] == int_to_bits(left, 32)
    assert encoded[32:64] == int_to_bits(right, 32)
    assert encoded[64:96] == int_to_bits(difference, 32)
    assert encoded[96:] == int_to_bits(aligned_difference, 32)


def test_arx_aligned_encoding_requires_supported_arx_cipher_profile():
    cipher = Present80(rounds=1, key=0x00000000000000000000)

    try:
        encode_ciphertext_pair(
            0,
            1,
            width=64,
            feature_encoding="ciphertext_pair_xor_arx_aligned_bits",
            cipher=cipher,
        )
    except ValueError as exc:
        assert "ARX aligned feature encoding" in str(exc)
    else:
        raise AssertionError("expected ValueError for unsupported ARX aligned encoding")

def test_pair_features_module_encodes_speck_arx_partial_inverse_pair_features():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    left = 0x12345678
    right = left ^ 0x00400080

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=32,
        feature_encoding="ciphertext_pair_xor_arx_partial_inverse_bits",
        cipher=cipher,
    )

    difference = left ^ right
    delta_left = (difference >> 16) & 0xFFFF
    delta_right = difference & 0xFFFF
    rotation_aligned = (ror(delta_left, 7, 16) << 16) | rol(delta_right, 2, 16)
    x = (left >> 16) & 0xFFFF
    y = left & 0xFFFF
    x_prime = (right >> 16) & 0xFFFF
    y_prime = right & 0xFFFF
    pre_y = ror(y ^ x, 2, 16)
    pre_y_prime = ror(y_prime ^ x_prime, 2, 16)
    delta_pre_y = pre_y ^ pre_y_prime

    assert len(encoded) == 224
    assert encoded[:32] == int_to_bits(left, 32)
    assert encoded[32:64] == int_to_bits(right, 32)
    assert encoded[64:96] == int_to_bits(difference, 32)
    assert encoded[96:128] == int_to_bits(rotation_aligned, 32)
    assert encoded[128:160] == int_to_bits(pre_y, 32)
    assert encoded[160:192] == int_to_bits(pre_y_prime, 32)
    assert encoded[192:224] == int_to_bits(delta_pre_y, 32)


def test_pair_features_module_encodes_speck_arx_partial_inverse_rx_pair_features():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    left = 0x12345678
    right = left ^ 0x00400080

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=32,
        feature_encoding="ciphertext_pair_xor_arx_partial_inverse_rx_bits",
        cipher=cipher,
    )

    difference = left ^ right
    delta_left = (difference >> 16) & 0xFFFF
    delta_right = difference & 0xFFFF
    x = (left >> 16) & 0xFFFF
    y = left & 0xFFFF
    x_prime = (right >> 16) & 0xFFFF
    y_prime = right & 0xFFFF
    pre_y = ror(y ^ x, 2, 16)
    pre_y_prime = ror(y_prime ^ x_prime, 2, 16)
    delta_pre_y = pre_y ^ pre_y_prime
    rx_alpha = (rol(x, 7, 16) ^ x_prime) << 16 | (rol(y, 7, 16) ^ y_prime)
    rx_beta = (rol(x, 2, 16) ^ x_prime) << 16 | (rol(y, 2, 16) ^ y_prime)
    carry_left = ((x + y) & 0xFFFF) ^ x ^ y
    carry_right = ((x_prime + y_prime) & 0xFFFF) ^ x_prime ^ y_prime
    carry_delta = carry_left ^ carry_right
    carry_proxy = (carry_left << 16) | carry_delta

    assert len(encoded) == 352
    assert encoded[192:224] == int_to_bits(delta_pre_y, 32)
    assert encoded[224:256] == int_to_bits(rx_alpha, 32)
    assert encoded[256:288] == int_to_bits(rx_beta, 32)
    assert encoded[288:320] == int_to_bits(carry_proxy, 32)
    assert encoded[320:352] == int_to_bits(carry_right << 16 | carry_delta, 32)


def test_present_mcnd_cell_matrix_encoding_orders_pair_bits_as_four_bit_planes():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    left = 0x0123456789ABCDEF
    right = 0xFEDCBA9876543210

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=64,
        feature_encoding="present_mcnd_cell_matrix_bits",
        cipher=cipher,
    )

    pair_bits = int_to_bits(left, 64) + int_to_bits(right, 64)
    nibbles = [pair_bits[index : index + 4] for index in range(0, 128, 4)]
    expected = [nibble[bit_index] for bit_index in range(4) for nibble in nibbles]
    assert pair_bits_for_encoding(64, "present_mcnd_cell_matrix_bits") == 128
    assert encoded == expected
    assert len(encoded) == 4 * 32


def test_present_mcnd_cell_matrix_encoding_is_registered():
    assert is_supported_feature_encoding("present_mcnd_cell_matrix_bits")


def _cell_matrix_bit_planes(words: list[int], width: int) -> list[int]:
    bits = []
    for word in words:
        bits.extend(int_to_bits(word, width))
    cells = [bits[index : index + 4] for index in range(0, len(bits), 4)]
    return [cell[bit_index] for bit_index in range(4) for cell in cells]


def test_present_pair_xor_cell_matrix_encoding_orders_pair_xor_bits_as_bit_planes():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    left = 0x0123456789ABCDEF
    right = 0xFEDCBA9876543210

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=64,
        feature_encoding="present_pair_xor_cell_matrix_bits",
        cipher=cipher,
    )

    expected = _cell_matrix_bit_planes([left, right, left ^ right], 64)
    assert pair_bits_for_encoding(64, "present_pair_xor_cell_matrix_bits") == 192
    assert encoded == expected
    assert len(encoded) == 4 * 48


def test_present_pair_xor_paligned_cell_matrix_encoding_includes_inverse_p_difference():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    left = 0x0123456789ABCDEF
    right = 0x0123456789ABCDEF ^ 0x0700000000000700

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=64,
        feature_encoding="present_pair_xor_paligned_cell_matrix_bits",
        cipher=cipher,
    )

    difference = left ^ right
    aligned_difference = Present80.inverse_permutation_layer(difference)
    expected = _cell_matrix_bit_planes([left, right, difference, aligned_difference], 64)
    assert pair_bits_for_encoding(64, "present_pair_xor_paligned_cell_matrix_bits") == 256
    assert encoded == expected
    assert len(encoded) == 4 * 64


def test_present_xor_paligned_cell_matrix_encoding_keeps_only_difference_planes():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    left = 0x0123456789ABCDEF
    right = 0x0123456789ABCDEF ^ 0x0700000000000700

    encoded = encode_ciphertext_pair(
        left,
        right,
        width=64,
        feature_encoding="present_xor_paligned_cell_matrix_bits",
        cipher=cipher,
    )

    difference = left ^ right
    aligned_difference = Present80.inverse_permutation_layer(difference)
    expected = _cell_matrix_bit_planes([difference, aligned_difference], 64)
    assert pair_bits_for_encoding(64, "present_xor_paligned_cell_matrix_bits") == 128
    assert encoded == expected
    assert len(encoded) == 4 * 32


def test_present_cell_matrix_extended_encodings_are_registered():
    assert is_supported_feature_encoding("present_pair_xor_cell_matrix_bits")
    assert is_supported_feature_encoding("present_pair_xor_paligned_cell_matrix_bits")
    assert is_supported_feature_encoding("present_xor_paligned_cell_matrix_bits")
