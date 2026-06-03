from blockcipher_ai_eval.experiments.factories import build_cipher, default_difference


def test_mainstream_cipher_factory_smoke_coverage() -> None:
    expected = {
        "aes128": (128, "SPN"),
        "aes192": (128, "SPN"),
        "aes256": (128, "SPN"),
        "aria128": (128, "SPN"),
        "aria192": (128, "SPN"),
        "aria256": (128, "SPN"),
        "present80": (64, "SPN"),
        "speck32": (32, "ARX"),
        "lea128": (128, "ARX"),
        "lea192": (128, "ARX"),
        "lea256": (128, "ARX"),
        "des": (64, "Feistel-like"),
        "3des": (64, "Feistel-like"),
        "simon64": (64, "Feistel-like"),
        "sm4": (128, "Feistel-like"),
    }

    for name, (block_bits, structure) in expected.items():
        cipher = build_cipher(name, rounds=1)
        assert cipher.block_bits == block_bits
        assert cipher.structure == structure
        assert 0 < default_difference(name) < (1 << block_bits)
        ciphertext = cipher.encrypt(0)
        assert 0 <= ciphertext < (1 << block_bits)
