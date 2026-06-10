import pytest

from blockcipher_ai_eval.ciphers import Present80, Speck32_64
from blockcipher_ai_eval.datasets import (
    DifferentialDatasetConfig,
    DiskDifferentialDataset,
    int_to_bits,
    make_chunked_differential_dataset,
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


def test_make_differential_dataset_can_emit_only_xor_difference_bits():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    base_config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_bits",
    )
    xor_config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_xor_bits",
    )

    pair_dataset = make_differential_dataset(base_config)
    xor_dataset = make_differential_dataset(xor_config)

    assert xor_dataset.features.shape == (2, 32)
    assert xor_dataset.features[0].tolist() == pair_dataset.features[0, 64:].tolist()
    assert xor_dataset.metadata["pair_bits"] == 32


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


def test_make_differential_dataset_can_include_spn_aligned_inverse_permutation_bits():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0700000000000700,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_spn_aligned_bits",
    )

    dataset = make_differential_dataset(config)
    first_row = dataset.features[0].tolist()
    left = first_row[:64]
    right = first_row[64:128]
    difference = first_row[128:192]
    aligned_difference = first_row[192:]
    difference_value = int("".join(str(bit) for bit in difference), 2)
    expected_aligned = int_to_bits(Present80.inverse_permutation_layer(difference_value), 64)

    assert dataset.features.shape == (2, 256)
    assert difference == [a ^ b for a, b in zip(left, right)]
    assert aligned_difference == expected_aligned
    assert dataset.metadata["feature_encoding"] == "ciphertext_pair_xor_spn_aligned_bits"
    assert dataset.metadata["pair_bits"] == 256


def test_make_differential_dataset_can_emit_only_spn_aligned_difference_bits():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0700000000000700,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_xor_spn_aligned_bits",
    )

    dataset = make_differential_dataset(config)
    first_row = dataset.features[0].tolist()
    difference = first_row[:64]
    aligned_difference = first_row[64:]
    difference_value = int("".join(str(bit) for bit in difference), 2)
    expected_aligned = int_to_bits(Present80.inverse_permutation_layer(difference_value), 64)

    assert dataset.features.shape == (2, 128)
    assert aligned_difference == expected_aligned
    assert dataset.metadata["feature_encoding"] == "ciphertext_xor_spn_aligned_bits"
    assert dataset.metadata["pair_bits"] == 128


def test_make_differential_dataset_can_generate_negative_pairs_from_encrypted_plaintexts():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=2,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_bits",
        negative_mode="encrypted_random_plaintexts",
    )

    dataset = make_differential_dataset(config)

    assert dataset.features.shape == (4, 64)
    assert dataset.labels.tolist() == [1, 1, 0, 0]
    assert dataset.metadata["negative_mode"] == "encrypted_random_plaintexts"


def test_spn_aligned_feature_encoding_requires_inverse_permutation_layer():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_spn_aligned_bits",
    )

    with pytest.raises(ValueError, match="inverse_permutation_layer"):
        make_differential_dataset(config)


def test_make_chunked_differential_dataset_writes_and_reuses_disk_cache(tmp_path):
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=5,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_bits",
        pairs_per_sample=2,
        negative_mode="encrypted_random_plaintexts",
    )
    cache_dir = tmp_path / "speck_cache"

    dataset = make_chunked_differential_dataset(config, cache_dir=cache_dir, chunk_size=3)
    reused = make_chunked_differential_dataset(config, cache_dir=cache_dir, chunk_size=2)

    assert isinstance(dataset, DiskDifferentialDataset)
    assert dataset.features.shape == (10, 192)
    assert dataset.labels.shape == (10,)
    assert dataset.labels[:5].tolist() == [1, 1, 1, 1, 1]
    assert dataset.labels[5:].tolist() == [0, 0, 0, 0, 0]
    assert dataset.metadata["cache_status"] == "created"
    assert dataset.metadata["generation_chunk_size"] == 3
    assert dataset.metadata["pair_bits"] == 96
    assert (cache_dir / "features.npy").exists()
    assert (cache_dir / "labels.npy").exists()
    assert (cache_dir / "metadata.json").exists()
    assert reused.metadata["cache_status"] == "reused"
    assert reused.features.tolist() == dataset.features.tolist()


def test_differential_dataset_config_is_available_from_canonical_data_module():
    from blockcipher_ai_eval.data.differential import (
        DifferentialDataset,
        DifferentialDatasetConfig,
        DiskDifferentialDataset,
    )

    assert DifferentialDatasetConfig is not None
    assert DifferentialDataset is not None
    assert DiskDifferentialDataset is not None
