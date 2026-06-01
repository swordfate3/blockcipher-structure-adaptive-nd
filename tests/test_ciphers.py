from blockcipher_ai_eval.ciphers import (
    Present80,
    ReducedRoundCipher,
    Speck32_64,
    Sm4Reduced,
)


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


def test_cipher_profile_interface_exposes_metadata():
    cipher: ReducedRoundCipher = Speck32_64(rounds=3, key=0)

    assert cipher.name == "SPECK32/64"
    assert cipher.block_bits == 32
    assert cipher.structure == "ARX"
    assert cipher.rounds == 3
