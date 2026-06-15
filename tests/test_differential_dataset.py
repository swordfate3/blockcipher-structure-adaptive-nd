
from blockcipher_ai_eval.ciphers import Present80
from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.experiments.difference_profiles import difference_for_profile


def test_zhang_wang_case2_mcnd_generates_grouped_present_samples():
    cipher = Present80(rounds=1, key=0)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=difference_for_profile("present_zhang_wang2022_mcnd"),
        samples_per_class=4,
        seed=7,
        feature_encoding="ciphertext_pair_bits",
        pairs_per_sample=16,
        negative_mode="encrypted_random_plaintexts",
        sample_structure="zhang_wang_case2_mcnd",
    )

    dataset = make_differential_dataset(config)

    assert dataset.features.shape == (8, 2048)
    assert dataset.labels.shape == (8,)
    assert dataset.metadata["sample_structure"] == "zhang_wang_case2_mcnd"
    assert dataset.metadata["input_difference"] == 0x0000000000000009
    assert dataset.metadata["pair_bits"] == 128

class _RecordingIdentityCipher:
    name = "RecordingIdentity"
    structure = "SPN"
    block_bits = 16
    key_bits = 16
    rounds = 1

    def __init__(self):
        self.inputs = []

    def encrypt(self, plaintext: int) -> int:
        self.inputs.append(plaintext)
        return plaintext


def test_zhang_wang_case2_independent_mcnd_uses_independent_plaintext_pairs():
    cipher = _RecordingIdentityCipher()
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0009,
        samples_per_class=1,
        seed=7,
        feature_encoding="ciphertext_pair_bits",
        pairs_per_sample=4,
        negative_mode="encrypted_random_plaintexts",
        sample_structure="zhang_wang_case2_independent_mcnd",
        shuffle=False,
    )

    dataset = make_differential_dataset(config)

    assert dataset.features.shape == (2, 128)
    positive_inputs = cipher.inputs[:8]
    positive_lefts = positive_inputs[0::2]
    positive_rights = positive_inputs[1::2]
    assert [left ^ right for left, right in zip(positive_lefts, positive_rights)] == [0x0009] * 4
    assert len(set(positive_lefts)) == 4

    negative_inputs = cipher.inputs[8:]
    negative_lefts = negative_inputs[0::2]
    negative_rights = negative_inputs[1::2]
    assert len(negative_lefts) == 4
    assert len(negative_rights) == 4
    assert all((left ^ right) != 0x0009 for left, right in zip(negative_lefts, negative_rights))
    assert dataset.metadata["sample_structure"] == "zhang_wang_case2_independent_mcnd"

