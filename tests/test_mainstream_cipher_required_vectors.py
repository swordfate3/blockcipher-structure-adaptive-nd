"""Required correctness vectors for mainstream cipher coverage.

This file intentionally keeps newer algorithms separate from the historical
`test_ciphers.py` suite.  It is a checklist expressed as tests: a cipher should
not be considered part of the completed implementation matrix until its public
vector passes here and it is also reachable through the experiment factory.
"""

from blockcipher_ai_eval.ciphers.arx.lea import Lea128, Lea192, Lea256


def _le_int(hex_bytes: str) -> int:
    return int.from_bytes(bytes.fromhex(hex_bytes), "little")


def _le_hex(value: int, byte_count: int) -> str:
    return value.to_bytes(byte_count, "little").hex()


def test_lea_128_192_256_public_vectors() -> None:
    vectors = [
        (
            Lea128,
            "0f1e2d3c4b5a69788796a5b4c3d2e1f0",
            "101112131415161718191a1b1c1d1e1f",
            "9fc84e3528c6c6185532c7a704648bfd",
        ),
        (
            Lea192,
            "0f1e2d3c4b5a69788796a5b4c3d2e1f0f0e1d2c3b4a59687",
            "202122232425262728292a2b2c2d2e2f",
            "6fb95e325aad1b878cdcf5357674c6f2",
        ),
        (
            Lea256,
            "0f1e2d3c4b5a69788796a5b4c3d2e1f0"
            "f0e1d2c3b4a5968778695a4b3c2d1e0f",
            "303132333435363738393a3b3c3d3e3f",
            "d651aff647b189c13a8900ca27f9e197",
        ),
    ]

    for cipher_cls, key, plaintext, expected_ciphertext in vectors:
        cipher = cipher_cls(key=_le_int(key))
        assert _le_hex(cipher.encrypt(_le_int(plaintext)), 16) == expected_ciphertext
