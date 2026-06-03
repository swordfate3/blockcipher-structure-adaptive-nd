"""Required ARIA and Camellia public vectors.

These tests are intentionally added before the implementations.  They encode
the official standard vectors that future cipher modules must satisfy before
being admitted into the experiment factory coverage matrix.
"""

import pytest
from blockcipher_ai_eval.ciphers.spn.aria import Aria128, Aria192, Aria256


def _be_int(hex_bytes: str) -> int:
    return int(hex_bytes, 16)


def _be_hex(value: int, byte_count: int = 16) -> str:
    return value.to_bytes(byte_count, "big").hex()


def test_aria_rfc5794_vectors() -> None:
    vectors = [
        (
            Aria128,
            "000102030405060708090a0b0c0d0e0f",
            "00112233445566778899aabbccddeeff",
            "d718fbd6ab644c739da95f3be6451778",
        ),
        (
            Aria192,
            "000102030405060708090a0b0c0d0e0f1011121314151617",
            "00112233445566778899aabbccddeeff",
            "26449c1805dbe7aa25a468ce263a9e79",
        ),
        (
            Aria256,
            "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
            "00112233445566778899aabbccddeeff",
            "f92bd7c79fb72e2f2b8f80c1972d24fc",
        ),
    ]

    for cipher_cls, key, plaintext, expected_ciphertext in vectors:
        cipher = cipher_cls(key=_be_int(key))
        assert _be_hex(cipher.encrypt(_be_int(plaintext))) == expected_ciphertext


def test_camellia_rfc3713_vectors() -> None:
    camellia = pytest.importorskip("blockcipher_ai_eval.ciphers.feistel.camellia")
    Camellia128 = camellia.Camellia128
    Camellia192 = camellia.Camellia192
    Camellia256 = camellia.Camellia256

    vectors = [
        (
            Camellia128,
            "0123456789abcdeffedcba9876543210",
            "0123456789abcdeffedcba9876543210",
            "67673138549669730857065648eabe43",
        ),
        (
            Camellia192,
            "0123456789abcdeffedcba98765432100011223344556677",
            "0123456789abcdeffedcba9876543210",
            "b4993401b3e996f84ee5cee7d79b09b9",
        ),
        (
            Camellia256,
            "0123456789abcdeffedcba987654321000112233445566778899aabbccddeeff",
            "0123456789abcdeffedcba9876543210",
            "9acc237dff16d76c20ef7c919e3a7509",
        ),
    ]

    for cipher_cls, key, plaintext, expected_ciphertext in vectors:
        cipher = cipher_cls(key=_be_int(key))
        assert _be_hex(cipher.encrypt(_be_int(plaintext))) == expected_ciphertext
