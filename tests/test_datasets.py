from blockcipher_ai_eval.ciphers import Speck32_64
from blockcipher_ai_eval.datasets import (
    DifferentialDatasetConfig,
    int_to_bits,
    make_differential_dataset,
)


def test_int_to_bits_uses_fixed_width_big_endian_encoding():
    assert int_to_bits(0b101, 4) == [0, 1, 0, 1]
    assert int_to_bits(0xA5, 8) == [1, 0, 1, 0, 0, 1, 0, 1]


def test_make_differential_dataset_is_balanced_and_bit_encoded():
    cipher = Speck32_64(rounds=3, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=8,
        seed=7,
    )

    dataset = make_differential_dataset(config)

    assert dataset.features.shape == (16, 64)
    assert dataset.labels.tolist().count(1) == 8
    assert dataset.labels.tolist().count(0) == 8
    assert set(dataset.features.flatten().tolist()) <= {0, 1}
    assert dataset.metadata["cipher"] == "SPECK32/64"
    assert dataset.metadata["structure"] == "ARX"
    assert dataset.metadata["rounds"] == 3
    assert dataset.metadata["feature_encoding"] == "ciphertext_pair_bits"


def test_make_differential_dataset_can_include_xor_difference_bits():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_bits",
    )

    dataset = make_differential_dataset(config)
    first_row = dataset.features[0].tolist()
    left = first_row[:32]
    right = first_row[32:64]
    difference = first_row[64:]

    assert dataset.features.shape == (2, 96)
    assert difference == [a ^ b for a, b in zip(left, right)]
    assert dataset.metadata["feature_encoding"] == "ciphertext_pair_xor_bits"


def test_make_differential_dataset_can_group_multiple_pairs_per_sample():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=2,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_bits",
        pairs_per_sample=2,
    )

    dataset = make_differential_dataset(config)

    assert dataset.features.shape == (4, 192)
    assert dataset.labels.tolist() == [1, 1, 0, 0]
    assert dataset.metadata["pairs_per_sample"] == 2


def test_make_differential_dataset_is_reproducible_for_same_seed():
    cipher = Speck32_64(rounds=3, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=4,
        seed=123,
    )

    first = make_differential_dataset(config)
    second = make_differential_dataset(config)

    assert first.labels.tolist() == second.labels.tolist()
    assert first.features.tolist() == second.features.tolist()


def test_make_differential_dataset_changes_with_seed():
    cipher = Speck32_64(rounds=3, key=0x1918111009080100)
    base = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=4,
        seed=123,
    )
    other = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=4,
        seed=124,
    )

    first = make_differential_dataset(base)
    second = make_differential_dataset(other)

    assert first.features.tolist() != second.features.tolist()
