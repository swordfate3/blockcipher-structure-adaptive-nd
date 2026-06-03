from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_cipher_algorithms_are_split_into_package_modules():
    ciphers_dir = PROJECT_ROOT / "src" / "blockcipher_ai_eval" / "ciphers"

    assert ciphers_dir.is_dir()
    assert (ciphers_dir / "__init__.py").is_file()
    assert (ciphers_dir / "base.py").is_file()
    assert (ciphers_dir / "arx" / "__init__.py").is_file()
    assert (ciphers_dir / "arx" / "speck.py").is_file()
    assert (ciphers_dir / "arx" / "lea.py").is_file()
    assert (ciphers_dir / "spn" / "__init__.py").is_file()
    assert (ciphers_dir / "spn" / "present.py").is_file()
    assert (ciphers_dir / "feistel" / "__init__.py").is_file()
    assert (ciphers_dir / "feistel" / "sm4.py").is_file()
    assert not (PROJECT_ROOT / "src" / "blockcipher_ai_eval" / "ciphers.py").exists()


def test_cipher_modules_have_single_algorithm_responsibility():
    ciphers_dir = PROJECT_ROOT / "src" / "blockcipher_ai_eval" / "ciphers"

    speck_module = (ciphers_dir / "arx" / "speck.py").read_text()
    lea_module = (ciphers_dir / "arx" / "lea.py").read_text()
    present_module = (ciphers_dir / "spn" / "present.py").read_text()
    sm4_module = (ciphers_dir / "feistel" / "sm4.py").read_text()

    assert "class Speck32_64" in speck_module
    assert "class Lea" not in speck_module
    assert "class Present80" not in speck_module
    assert "class Sm4Reduced" not in speck_module

    assert "class Lea" in lea_module
    assert "class Speck32_64" not in lea_module
    assert "class Present80" not in lea_module
    assert "class Sm4Reduced" not in lea_module

    assert "class Present80" in present_module
    assert "class Speck32_64" not in present_module
    assert "class Lea" not in present_module
    assert "class Sm4Reduced" not in present_module

    assert "class Sm4Reduced" in sm4_module
    assert "class Speck32_64" not in sm4_module
    assert "class Lea" not in sm4_module
    assert "class Present80" not in sm4_module
