
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
