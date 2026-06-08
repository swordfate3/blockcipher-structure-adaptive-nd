from blockcipher_ai_eval.ciphers import Present80, Speck32_64
from blockcipher_ai_eval.ciphers.base import rol, ror
from blockcipher_ai_eval.ciphers.spn.gift import Gift64
from blockcipher_ai_eval.datasets import int_to_bits as legacy_int_to_bits
from blockcipher_ai_eval.features.encodings import (
    encode_ciphertext_pair,
    int_to_bits,
    pair_bits_for_encoding,
)


def test_feature_encoding_module_exposes_bit_helpers_and_pair_widths():
    assert int_to_bits(0xA5, 8) == [1, 0, 1, 0, 0, 1, 0, 1]
    assert legacy_int_to_bits(0xA5, 8) == int_to_bits(0xA5, 8)
    assert pair_bits_for_encoding(64, "ciphertext_pair_bits") == 128
    assert pair_bits_for_encoding(64, "ciphertext_xor_bits") == 64
    assert pair_bits_for_encoding(64, "ciphertext_xor_spn_aligned_bits") == 128
    assert pair_bits_for_encoding(64, "ciphertext_pair_xor_bits") == 192
    assert pair_bits_for_encoding(64, "ciphertext_pair_xor_spn_aligned_bits") == 256
    assert pair_bits_for_encoding(32, "ciphertext_pair_xor_arx_aligned_bits") == 128


def test_feature_encoding_module_encodes_spn_aligned_pair_features():
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


def test_feature_encoding_module_encodes_gift_spn_aligned_pair_features():
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


def test_feature_encoding_module_encodes_speck_arx_aligned_pair_features():
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
