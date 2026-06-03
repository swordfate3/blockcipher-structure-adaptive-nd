from blockcipher_ai_eval.ciphers.feistel.simeck import Simeck64_128


def test_simeck64_128_matches_ches2015_vector() -> None:
    cipher = Simeck64_128(rounds=44, key=0x1B1A1918131211100B0A090803020100)

    assert cipher.encrypt(0x656B696C20646E75) == 0x45CE69025F7AB7ED
