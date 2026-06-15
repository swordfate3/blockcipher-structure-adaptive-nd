import importlib.util
from argparse import Namespace
from pathlib import Path

import numpy as np


def _load_module():
    script = Path(__file__).resolve().parents[1] / "experiments" / "run_score_distribution.py"
    spec = importlib.util.spec_from_file_location("run_score_distribution", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_score_distribution_features_sort_and_aggregate_group_scores():
    module = _load_module()
    probabilities = np.array([0.9, 0.1, 0.4, 0.8, 0.2, 0.6], dtype=np.float32)
    labels = np.array([1, 1, 1, 0, 0, 0], dtype=np.uint8)

    dataset = module.score_distribution_dataset(probabilities, labels, group_size=3)

    assert dataset.features.shape == (2, 9)
    assert dataset.labels.tolist() == [1, 0]
    assert np.allclose(dataset.features[0, :3], [0.1, 0.4, 0.9])
    assert np.allclose(dataset.features[1, :3], [0.2, 0.6, 0.8])
    assert np.isclose(dataset.features[0, 3], np.mean([0.9, 0.1, 0.4]))
    assert np.isclose(dataset.features[1, 4], np.std([0.8, 0.2, 0.6]))


def test_score_distribution_rejects_incomplete_groups():
    module = _load_module()
    probabilities = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
    labels = np.array([0, 0, 1, 1], dtype=np.uint8)

    try:
        module.score_distribution_dataset(probabilities, labels, group_size=3)
    except ValueError as exc:
        assert "multiple of group_size" in str(exc)
    else:
        raise AssertionError("expected incomplete score groups to fail")


def test_parse_selected_bit_indices_accepts_json_list():
    module = _load_module()

    assert module.parse_selected_bit_indices("[0, 2, 5]") == (0, 2, 5)
    assert module.parse_selected_bit_indices("") == ()


def test_parse_selected_bit_indices_rejects_non_integer_values():
    module = _load_module()

    try:
        module.parse_selected_bit_indices("[0, \"bad\"]")
    except ValueError as exc:
        assert "JSON list of integers" in str(exc)
    else:
        raise AssertionError("expected invalid selected bit indices to fail")

def test_make_single_pair_dataset_uses_stage_specific_disk_cache(tmp_path):
    module = _load_module()
    from blockcipher_ai_eval.ciphers import Speck32_64

    args = Namespace(
        cipher="speck32",
        feature_encoding="ciphertext_pair_bits",
        negative_mode="encrypted_random_plaintexts",
        key_rotation_interval=1,
        sample_structure="independent_pairs",
        selected_bit_indices="",
        dataset_cache_root=str(tmp_path / "cache"),
        dataset_cache_chunk_size=2,
        progress_output=None,
    )
    cipher = Speck32_64(rounds=2, key=0)

    dataset = module._make_single_pair_dataset(
        args,
        cipher,
        input_difference=0x0040,
        samples_per_class=3,
        seed=7,
        shuffle=False,
        stage="meta_train_source",
    )

    assert dataset.features.shape == (6, 64)
    assert (
        tmp_path / "cache" / "score_distribution" / "speck32" / "r2" / "meta_train_source" / "seed-7"
    ).exists()


def test_run_score_distribution_experiment_records_selected_bit_indices(tmp_path):
    module = _load_module()
    args = Namespace(
        cipher="speck32",
        rounds=2,
        difference_profile="speck32_gohr2019",
        difference_member=0,
        feature_encoding="ciphertext_pair_bits",
        selected_bit_indices="[0, 1, 32, 33]",
        negative_mode="encrypted_random_plaintexts",
        sample_structure="independent_pairs",
        key_rotation_interval=2,
        base_samples_per_class=8,
        meta_samples_per_class=2,
        score_group_size=2,
        base_model="mlp",
        base_hidden_bits=8,
        base_epochs=1,
        base_batch_size=4,
        base_learning_rate=1e-3,
        base_loss="bce",
        meta_hidden_bits=8,
        meta_epochs=1,
        meta_batch_size=2,
        meta_learning_rate=1e-3,
        seed=3,
        device="cpu",
        progress_output=str(tmp_path / "progress.jsonl"),
        dataset_cache_root=None,
        dataset_cache_chunk_size=2,
    )

    row = module.run_score_distribution_experiment(args)

    assert row["selected_bit_indices"] == [0, 1, 32, 33]
    assert row["training"]["meta_input_features"] == args.score_group_size + 6
