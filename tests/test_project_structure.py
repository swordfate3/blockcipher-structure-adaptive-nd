from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cipher_algorithms_are_split_into_package_modules():
    ciphers_dir = PROJECT_ROOT / "src" / "blockcipher_ai_eval" / "ciphers"

    assert ciphers_dir.is_dir()
    assert (ciphers_dir / "__init__.py").is_file()
    assert (ciphers_dir / "base.py").is_file()
    assert (ciphers_dir / "speck.py").is_file()
    assert (ciphers_dir / "present.py").is_file()
    assert (ciphers_dir / "sm4.py").is_file()
    assert not (PROJECT_ROOT / "src" / "blockcipher_ai_eval" / "ciphers.py").exists()


def test_cipher_modules_have_single_algorithm_responsibility():
    ciphers_dir = PROJECT_ROOT / "src" / "blockcipher_ai_eval" / "ciphers"

    assert "class Speck32_64" in (ciphers_dir / "speck.py").read_text()
    assert "class Present80" not in (ciphers_dir / "speck.py").read_text()
    assert "class Sm4Reduced" not in (ciphers_dir / "speck.py").read_text()

    assert "class Present80" in (ciphers_dir / "present.py").read_text()
    assert "class Speck32_64" not in (ciphers_dir / "present.py").read_text()
    assert "class Sm4Reduced" not in (ciphers_dir / "present.py").read_text()

    assert "class Sm4Reduced" in (ciphers_dir / "sm4.py").read_text()
    assert "class Speck32_64" not in (ciphers_dir / "sm4.py").read_text()
    assert "class Present80" not in (ciphers_dir / "sm4.py").read_text()
