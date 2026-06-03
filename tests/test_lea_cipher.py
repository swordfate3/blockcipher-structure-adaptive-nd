from blockcipher_ai_eval.ciphers.arx.lea import Lea128, Lea192, Lea256


def _le_int(hex_bytes: str) -> int:
    return int.from_bytes(bytes.fromhex(hex_bytes), "little")


def _le_hex(value: int, byte_count: int = 16) -> str:
    return value.to_bytes(byte_count, "little").hex()


def test_lea128_public_test_vector() -> None:
    cipher = Lea128(
        key=_le_int("0f1e2d3c4b5a69788796a5b4c3d2e1f0"),
    )

    ciphertext = cipher.encrypt(_le_int("101112131415161718191a1b1c1d1e1f"))

    assert _le_hex(ciphertext) == "9fc84e3528c6c6185532c7a704648bfd"


def test_lea192_public_test_vector() -> None:
    cipher = Lea192(
        key=_le_int("0f1e2d3c4b5a69788796a5b4c3d2e1f0f0e1d2c3b4a59687"),
    )

    ciphertext = cipher.encrypt(_le_int("202122232425262728292a2b2c2d2e2f"))

    assert _le_hex(ciphertext) == "6fb95e325aad1b878cdcf5357674c6f2"


def test_lea256_public_test_vector() -> None:
    cipher = Lea256(
        key=_le_int(
            "0f1e2d3c4b5a69788796a5b4c3d2e1f0"
            "f0e1d2c3b4a5968778695a4b3c2d1e0f"
        ),
    )

    ciphertext = cipher.encrypt(_le_int("303132333435363738393a3b3c3d3e3f"))

    assert _le_hex(ciphertext) == "d651aff647b189c13a8900ca27f9e197"
