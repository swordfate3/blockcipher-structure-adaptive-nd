from blockcipher_ai_eval.ciphers.spn.gift import Gift64


def _be_int(hex_bytes: str) -> int:
    return int(hex_bytes, 16)


def _be_hex(value: int, byte_count: int) -> str:
    return value.to_bytes(byte_count, "big").hex()


def test_gift64_official_vectors() -> None:
    vectors = [
        (
            "00000000000000000000000000000000",
            "0000000000000000",
            "f62bc3ef34f775ac",
        ),
        (
            "fedcba9876543210fedcba9876543210",
            "fedcba9876543210",
            "c1b71f66160ff587",
        ),
        (
            "bd91731eb6bc2713a1f9f6ffc75044e7",
            "c450c7727a9b8a7d",
            "e3272885fa94ba8b",
        ),
    ]

    for key, plaintext, expected_ciphertext in vectors:
        cipher = Gift64(key=_be_int(key))
        assert _be_hex(cipher.encrypt(_be_int(plaintext)), 8) == expected_ciphertext
