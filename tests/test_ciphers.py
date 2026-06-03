from blockcipher_ai_eval.ciphers import (
    Aes128,
    Aes192,
    Aes256,
    Present80,
    ReducedRoundCipher,
    Simon64_128,
    Speck32_64,
    Sm4Reduced,
)
from blockcipher_ai_eval.experiments import build_cipher


def test_speck32_64_full_round_matches_public_test_vector():
    cipher = Speck32_64(rounds=22, key=0x1918111009080100)

    first = cipher.encrypt(0x6574694C)
    second = cipher.encrypt(0x6574694C)

    assert first == second
    assert 0 <= first < 2**32
    assert first == 0xA86842F2


def test_speck32_64_different_round_counts_change_ciphertext():
    plaintext = 0x6574694C
    key = 0x1918111009080100

    round_3 = Speck32_64(rounds=3, key=key).encrypt(plaintext)
    round_4 = Speck32_64(rounds=4, key=key).encrypt(plaintext)

    assert round_3 != round_4


def test_simon64_128_full_round_matches_public_test_vector():
    cipher = Simon64_128(rounds=44, key=0x1B1A1918131211100B0A090803020100)

    first = cipher.encrypt(0x656B696C20646E75)
    second = cipher.encrypt(0x656B696C20646E75)

    assert first == second
    assert 0 <= first < 2**64
    assert first == 0x44C8FC20B9DFA07A


def test_simon64_128_different_round_counts_change_ciphertext():
    plaintext = 0x656B696C20646E75
    key = 0x1B1A1918131211100B0A090803020100

    round_3 = Simon64_128(rounds=3, key=key).encrypt(plaintext)
    round_4 = Simon64_128(rounds=4, key=key).encrypt(plaintext)

    assert round_3 != round_4


def test_present80_full_round_matches_public_test_vector():
    cipher = Present80(rounds=31, key=0x00000000000000000000)

    first = cipher.encrypt(0x0000000000000000)
    second = cipher.encrypt(0x0000000000000000)

    assert first == second
    assert 0 <= first < 2**64
    assert first == 0x5579C1387B228445


def test_sm4_full_round_matches_public_test_vector():
    cipher = Sm4Reduced(rounds=32, key=0x0123456789ABCDEFFEDCBA9876543210)

    first = cipher.encrypt(0x0123456789ABCDEFFEDCBA9876543210)
    second = cipher.encrypt(0x0123456789ABCDEFFEDCBA9876543210)

    assert first == second
    assert 0 <= first < 2**128
    assert first == 0x681EDF34D206965E86B3E94F536E4246


def test_aes128_full_round_matches_fips197_test_vector():
    cipher = Aes128(rounds=10, key=0x000102030405060708090A0B0C0D0E0F)

    first = cipher.encrypt(0x00112233445566778899AABBCCDDEEFF)
    second = cipher.encrypt(0x00112233445566778899AABBCCDDEEFF)

    assert first == second
    assert 0 <= first < 2**128
    assert first == 0x69C4E0D86A7B0430D8CDB78070B4C55A


def test_aes192_full_round_matches_fips197_test_vector():
    cipher = Aes192(rounds=12, key=0x000102030405060708090A0B0C0D0E0F1011121314151617)

    first = cipher.encrypt(0x00112233445566778899AABBCCDDEEFF)
    second = cipher.encrypt(0x00112233445566778899AABBCCDDEEFF)

    assert first == second
    assert 0 <= first < 2**128
    assert first == 0xDDA97CA4864CDFE06EAF70A0EC0D7191


def test_aes256_full_round_matches_fips197_test_vector():
    cipher = Aes256(
        rounds=14,
        key=0x000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F,
    )

    first = cipher.encrypt(0x00112233445566778899AABBCCDDEEFF)
    second = cipher.encrypt(0x00112233445566778899AABBCCDDEEFF)

    assert first == second
    assert 0 <= first < 2**128
    assert first == 0x8EA2B7CA516745BFEAFC49904B496089


def test_aes_reduced_round_counts_change_ciphertext():
    plaintext = 0x00112233445566778899AABBCCDDEEFF
    key = 0x000102030405060708090A0B0C0D0E0F

    round_3 = Aes128(rounds=3, key=key).encrypt(plaintext)
    round_4 = Aes128(rounds=4, key=key).encrypt(plaintext)

    assert round_3 != round_4


def test_build_cipher_supports_aes_variants():
    aes128 = build_cipher("aes128", rounds=10)
    aes192 = build_cipher("aes192", rounds=12)
    aes256 = build_cipher("aes256", rounds=14)

    assert aes128.name == "AES-128"
    assert aes192.name == "AES-192"
    assert aes256.name == "AES-256"
    assert aes128.encrypt(0x00112233445566778899AABBCCDDEEFF) == 0x69C4E0D86A7B0430D8CDB78070B4C55A
    assert aes192.encrypt(0x00112233445566778899AABBCCDDEEFF) == 0xDDA97CA4864CDFE06EAF70A0EC0D7191
    assert aes256.encrypt(0x00112233445566778899AABBCCDDEEFF) == 0x8EA2B7CA516745BFEAFC49904B496089


def test_build_cipher_supports_simon64():
    cipher = build_cipher("simon64", rounds=44)

    assert cipher.name == "SIMON64/128"
    assert cipher.encrypt(0x656B696C20646E75) == 0x44C8FC20B9DFA07A


def test_cipher_profile_interface_exposes_metadata():
    cipher: ReducedRoundCipher = Speck32_64(rounds=3, key=0)

    assert cipher.name == "SPECK32/64"
    assert cipher.block_bits == 32
    assert cipher.structure == "ARX"
    assert cipher.rounds == 3
