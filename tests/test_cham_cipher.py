from blockcipher_ai_eval.ciphers.arx.cham import Cham64_128


def test_cham64_128_matches_paper_appendix_vector() -> None:
    cipher = Cham64_128(rounds=80, key=0x010003020504070609080B0A0D0C0F0E)

    assert cipher.encrypt(0x1100332255447766) == 0x453C63BCDCFABF4E
