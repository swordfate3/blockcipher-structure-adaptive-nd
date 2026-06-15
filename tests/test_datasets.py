import pytest
from dataclasses import dataclass

from blockcipher_ai_eval.ciphers import Present80, Speck32_64
from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset
from blockcipher_ai_eval.data.cache.disk import _generate_chunk
from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig, DiskDifferentialDataset
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.features.pair_features import int_to_bits


@dataclass(frozen=True)
class _LoggingToyCipher:
    rounds: int
    key: int

    log: list[int] = None  # type: ignore[assignment]
    name: str = "TOY"
    structure: str = "ARX"
    block_bits: int = 16
    key_bits: int = 64

    def __post_init__(self) -> None:
        if self.log is None:
            object.__setattr__(self, "log", [])

    def encrypt(self, plaintext: int) -> int:
        self.log.append(self.key)
        return (plaintext ^ (self.key & 0xFFFF)) & 0xFFFF


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


def test_make_differential_dataset_can_select_feature_bits_after_encoding():
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    base_config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_bits",
    )
    selected_config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_pair_xor_bits",
        selected_bit_indices=(0, 31, 64, 95),
    )

    base_dataset = make_differential_dataset(base_config)
    selected_dataset = make_differential_dataset(selected_config)

    assert selected_dataset.features.shape == (2, 4)
    assert selected_dataset.features[0].tolist() == base_dataset.features[0, [0, 31, 64, 95]].tolist()
    assert selected_dataset.metadata["pair_bits"] == 4
    assert selected_dataset.metadata["base_pair_bits"] == 96
    assert selected_dataset.metadata["selected_bit_indices"] == [0, 31, 64, 95]


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


def test_make_differential_dataset_can_rotate_keys_per_sample_group():
    cipher = _LoggingToyCipher(rounds=1, key=0)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=3,
        seed=7,
        shuffle=False,
        pairs_per_sample=2,
        negative_mode="encrypted_random_plaintexts",
        key_rotation_interval=1,
    )

    dataset = make_differential_dataset(config)

    positive_row_encrypt_keys = [cipher.log[index : index + 4] for index in range(0, 12, 4)]
    assert all(len(set(row_keys)) == 1 for row_keys in positive_row_encrypt_keys)
    assert len({row_keys[0] for row_keys in positive_row_encrypt_keys}) == 3
    assert dataset.metadata["key_rotation_interval"] == 1
    assert dataset.metadata["key_schedule"] == "rotating"


def test_make_differential_dataset_can_reuse_key_for_custom_interval():
    cipher = _LoggingToyCipher(rounds=1, key=0)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=3,
        seed=7,
        shuffle=False,
        pairs_per_sample=1,
        key_rotation_interval=2,
    )

    make_differential_dataset(config)

    positive_row_keys = [cipher.log[index] for index in range(0, 6, 2)]
    assert positive_row_keys[0] == positive_row_keys[1]
    assert positive_row_keys[2] != positive_row_keys[1]


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


def test_chunked_disk_cache_does_not_physically_shuffle_when_requested(tmp_path):
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=6,
        seed=7,
        shuffle=True,
    )

    dataset = make_chunked_differential_dataset(config, cache_dir=tmp_path / "cache", chunk_size=2)

    assert dataset.labels[:6].tolist() == [1, 1, 1, 1, 1, 1]
    assert dataset.labels[6:].tolist() == [0, 0, 0, 0, 0, 0]
    assert dataset.metadata["requested_shuffle"] is True
    assert dataset.metadata["physical_shuffle"] is False
    assert dataset.metadata["training_shuffle"] is True


def test_chunked_disk_cache_reports_generation_progress(tmp_path):
    cipher = Speck32_64(rounds=1, key=0x1918111009080100)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0040,
        samples_per_class=5,
        seed=7,
        shuffle=True,
    )
    events = []

    make_chunked_differential_dataset(
        config,
        cache_dir=tmp_path / "cache",
        chunk_size=3,
        progress_callback=lambda event, payload: events.append((event, payload)),
        progress_context={"split": "train"},
    )

    event_names = [event for event, _ in events]
    assert "cache_start" in event_names
    assert event_names.count("cache_positive_chunk") == 2
    assert event_names.count("cache_negative_chunk") == 2
    assert "cache_flush_start" in event_names
    assert "cache_done" in event_names
    assert events[0][1]["split"] == "train"
    assert events[-1][1]["total_rows"] == 10


def test_differential_dataset_config_is_available_from_canonical_data_module():
    from blockcipher_ai_eval.data.differential import (
        DifferentialDataset,
        DifferentialDatasetConfig,
        DiskDifferentialDataset,
    )

    assert DifferentialDatasetConfig is not None
    assert DifferentialDataset is not None
    assert DiskDifferentialDataset is not None


def test_chunked_dataset_cache_builder_is_available_from_canonical_cache_module():
    from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset

    assert make_chunked_differential_dataset is not None


def test_generate_chunk_streams_rows_into_preallocated_uint8_array():
    calls: list[int] = []

    def make_row(offset: int) -> list[int]:
        calls.append(offset)
        return [offset % 2, 1, 0]

    chunk = _generate_chunk(count=4, input_bits=3, row_factory=make_row)

    assert calls == [0, 1, 2, 3]
    assert chunk.dtype.name == "uint8"
    assert chunk.shape == (4, 3)
    assert chunk.tolist() == [[0, 1, 0], [1, 1, 0], [0, 1, 0], [1, 1, 0]]


def test_generate_chunk_rejects_unexpected_row_width():
    with pytest.raises(ValueError, match="generated row has 2 bits, expected 3"):
        _generate_chunk(count=1, input_bits=3, row_factory=lambda _offset: [1, 0])


def test_make_differential_dataset_can_group_plaintext_integral_nibble_with_p_alignment():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0700000000000700,
        samples_per_class=1,
        seed=7,
        shuffle=False,
        feature_encoding="ciphertext_xor_spn_paligned_bits",
        pairs_per_sample=16,
        negative_mode="encrypted_random_plaintexts",
        sample_structure="plaintext_integral_nibble",
        integral_active_nibble=0,
    )

    dataset = make_differential_dataset(config)
    first_row = dataset.features[0].tolist()
    first_pair = first_row[:128]
    difference = first_pair[:64]
    aligned_difference = first_pair[64:]
    difference_value = int("".join(str(bit) for bit in difference), 2)
    expected_aligned = int_to_bits(Present80.inverse_permutation_layer(difference_value), 64)

    assert dataset.features.shape == (2, 16 * 128)
    assert dataset.labels.tolist() == [1, 0]
    assert aligned_difference == expected_aligned
    assert dataset.metadata["feature_encoding"] == "ciphertext_xor_spn_paligned_bits"
    assert dataset.metadata["pair_bits"] == 128
    assert dataset.metadata["pairs_per_sample"] == 16
    assert dataset.metadata["sample_structure"] == "plaintext_integral_nibble"
    assert dataset.metadata["integral_active_nibble"] == 0


def test_plaintext_integral_nibble_requires_power_of_two_pair_count():
    cipher = Present80(rounds=1, key=0x00000000000000000000)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0700000000000700,
        samples_per_class=1,
        seed=7,
        pairs_per_sample=3,
        sample_structure="plaintext_integral_nibble",
    )

    with pytest.raises(ValueError, match="power-of-two pairs_per_sample"):
        make_differential_dataset(config)
