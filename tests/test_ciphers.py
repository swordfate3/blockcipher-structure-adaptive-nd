from blockcipher_ai_eval.ciphers import (
    Aes128,
    Aes192,
    Aes256,
    Des,
    Present80,
    ReducedRoundCipher,
    Simon64_128,
    Speck32_64,
    Sm4Reduced,
    TripleDes,
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


def test_present80_permutation_layer_round_trips_through_inverse():
    samples = [
        0x0000000000000000,
        0xFFFFFFFFFFFFFFFF,
        0x0123456789ABCDEF,
        0x8000000000000001,
    ]

    for state in samples:
        permuted = Present80.permutation_layer(state)
        restored = Present80.inverse_permutation_layer(permuted)

        assert restored == state


def test_sm4_full_round_matches_public_test_vector():
    cipher = Sm4Reduced(rounds=32, key=0x0123456789ABCDEFFEDCBA9876543210)

    first = cipher.encrypt(0x0123456789ABCDEFFEDCBA9876543210)
    second = cipher.encrypt(0x0123456789ABCDEFFEDCBA9876543210)

    assert first == second
    assert 0 <= first < 2**128
    assert first == 0x681EDF34D206965E86B3E94F536E4246


def test_des_full_round_matches_public_test_vector():
    cipher = Des(rounds=16, key=0x133457799BBCDFF1)

    first = cipher.encrypt(0x0123456789ABCDEF)
    second = cipher.encrypt(0x0123456789ABCDEF)

    assert first == second
    assert 0 <= first < 2**64
    assert first == 0x85E813540F0AB405
    assert cipher.decrypt(first) == 0x0123456789ABCDEF


def test_des_reduced_round_counts_change_ciphertext():
    plaintext = 0x0123456789ABCDEF
    key = 0x133457799BBCDFF1

    round_3 = Des(rounds=3, key=key).encrypt(plaintext)
    round_4 = Des(rounds=4, key=key).encrypt(plaintext)

    assert round_3 != round_4


def test_triple_des_degenerate_keys_match_des():
    plaintext = 0x0123456789ABCDEF
    key = 0x133457799BBCDFF1
    des = Des(rounds=16, key=key)
    triple_des = TripleDes(rounds=16, key1=key, key2=key, key3=key)

    ciphertext = triple_des.encrypt(plaintext)

    assert ciphertext == des.encrypt(plaintext)
    assert triple_des.decrypt(ciphertext) == plaintext


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


def test_build_cipher_accepts_present80_key_override():
    default_cipher = build_cipher("present80", rounds=5)
    keyed_cipher = build_cipher("present80", rounds=5, key=0x11111111111111111111)

    assert default_cipher.name == "PRESENT-80"
    assert keyed_cipher.name == "PRESENT-80"
    assert default_cipher.encrypt(0x0123456789ABCDEF) != keyed_cipher.encrypt(0x0123456789ABCDEF)


def test_build_cipher_honors_speck32_key_override():
    default_cipher = build_cipher("speck32", rounds=5)
    keyed_cipher = build_cipher("speck32", rounds=5, key=0x0F0E0D0C0B0A0908)

    assert default_cipher.key == 0x1918111009080100
    assert keyed_cipher.key == 0x0F0E0D0C0B0A0908
    assert default_cipher.encrypt(0x6574694C) != keyed_cipher.encrypt(0x6574694C)


def test_build_cipher_supports_simon64():
    cipher = build_cipher("simon64", rounds=44)

    assert cipher.name == "SIMON64/128"
    assert cipher.encrypt(0x656B696C20646E75) == 0x44C8FC20B9DFA07A


def test_build_cipher_supports_des_variants():
    des = build_cipher("des", rounds=16)
    triple_des = build_cipher("3des", rounds=16)

    assert des.name == "DES"
    assert triple_des.name == "3DES"
    assert des.encrypt(0x0123456789ABCDEF) == 0x85E813540F0AB405
    assert 0 <= triple_des.encrypt(0x0123456789ABCDEF) < 2**64


def test_cipher_profile_interface_exposes_metadata():
    cipher: ReducedRoundCipher = Speck32_64(rounds=3, key=0)

    assert cipher.name == "SPECK32/64"
    assert cipher.block_bits == 32
    assert cipher.structure == "ARX"
    assert cipher.rounds == 3


def test_build_cipher_gift64_honors_explicit_key():
    default_cipher = build_cipher("gift64", rounds=5)
    keyed_cipher = build_cipher("gift64", rounds=5, key=0x11111111111111111111111111111111)

    assert default_cipher.key == 0
    assert keyed_cipher.key == 0x11111111111111111111111111111111
    assert default_cipher.encrypt(0x0123456789ABCDEF) != keyed_cipher.encrypt(0x0123456789ABCDEF)
