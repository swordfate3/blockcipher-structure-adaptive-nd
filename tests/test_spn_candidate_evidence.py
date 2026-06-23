import importlib.util
from pathlib import Path

import numpy as np

from blockcipher_ai_eval.ciphers import Present80
from blockcipher_ai_eval.features.spn_candidate_evidence import (
    present_pair_candidate_evidence_features,
    present_pair_candidate_evidence_layers,
    present_pairset_candidate_evidence_features,
)

_RUNNER_PATH = (
    Path(__file__).resolve().parents[1] / "experiments" / "innovation1" / "run_spn_candidate_evidence_baseline.py"
)
_RUNNER_SPEC = importlib.util.spec_from_file_location("run_spn_candidate_evidence_baseline", _RUNNER_PATH)
assert _RUNNER_SPEC is not None
_RUNNER = importlib.util.module_from_spec(_RUNNER_SPEC)
assert _RUNNER_SPEC.loader is not None
_RUNNER_SPEC.loader.exec_module(_RUNNER)
make_candidate_dataset = _RUNNER.make_candidate_dataset


def test_present_pair_candidate_evidence_layers_have_stable_words():
    cipher = Present80(rounds=7, key=0)
    left = cipher.encrypt(0x0123456789ABCDEF)
    right = cipher.encrypt(0x0123456789ABCDEF ^ 0x9)

    layers = present_pair_candidate_evidence_layers(
        left,
        right,
        width=64,
        cipher=cipher,
        beam_width=4,
        depth=3,
    )

    assert len(layers) == 3
    assert all(0 <= layer.top_word < (1 << 64) for layer in layers)
    assert any(layer.confidence_word != 0 for layer in layers)


def test_present_pair_candidate_evidence_features_are_normalized():
    cipher = Present80(rounds=7, key=0)
    left = cipher.encrypt(0x0123456789ABCDEF)
    right = cipher.encrypt(0x0123456789ABCDEF ^ 0x9)

    features = present_pair_candidate_evidence_features(
        left,
        right,
        width=64,
        cipher=cipher,
        beam_width=4,
        depth=3,
    )

    assert features.shape == (3 * 20,)
    assert features.dtype == np.float32
    assert float(features.min()) >= 0.0
    assert float(features.max()) <= 1.0


def test_present_pairset_candidate_evidence_features_include_consistency_stats():
    cipher = Present80(rounds=7, key=0)
    pairs = [
        (
            cipher.encrypt(0x0123456789ABCDEF ^ mask),
            cipher.encrypt((0x0123456789ABCDEF ^ mask) ^ 0x9),
        )
        for mask in (0, 1, 2, 3)
    ]

    features = present_pairset_candidate_evidence_features(
        pairs,
        width=64,
        cipher=cipher,
        beam_width=4,
        depth=3,
    )

    assert features.shape == (3 * 20 * 3 + 6,)
    assert features.dtype == np.float32
    assert np.isfinite(features).all()


def test_candidate_evidence_dataset_cache_writes_and_reuses(tmp_path):
    progress_path = tmp_path / "progress.jsonl"
    features, labels = make_candidate_dataset(
        rounds=7,
        key=0,
        input_difference=0x9,
        seed=3,
        samples_per_class=4,
        pairs_per_sample=2,
        negative_mode="encrypted_random_plaintexts",
        sample_structure="zhang_wang_case2_mcnd",
        key_rotation_interval=2,
        beam_width=2,
        depth=2,
        feature_cache_root=tmp_path / "candidate_cache",
        feature_cache_chunk_size=2,
        progress_output=progress_path,
        split="train",
    )

    assert features.shape == (8, 126)
    assert labels.shape == (8,)
    assert set(np.unique(labels).tolist()) == {0, 1}
    cache_dirs = [path for path in (tmp_path / "candidate_cache" / "train").iterdir() if path.is_dir()]
    assert len(cache_dirs) == 1
    cache_dir = cache_dirs[0]
    assert (cache_dir / "features.npy").exists()
    assert (cache_dir / "labels.npy").exists()
    assert (cache_dir / "metadata.json").exists()
    progress_text = progress_path.read_text(encoding="utf-8")
    assert "candidate_cache_start" in progress_text
    assert "candidate_cache_positive_chunk" in progress_text
    assert "candidate_cache_negative_chunk" in progress_text
    assert "candidate_cache_done" in progress_text

    reused_features, reused_labels = make_candidate_dataset(
        rounds=7,
        key=0,
        input_difference=0x9,
        seed=3,
        samples_per_class=4,
        pairs_per_sample=2,
        negative_mode="encrypted_random_plaintexts",
        sample_structure="zhang_wang_case2_mcnd",
        key_rotation_interval=2,
        beam_width=2,
        depth=2,
        feature_cache_root=tmp_path / "candidate_cache",
        feature_cache_chunk_size=2,
        progress_output=progress_path,
        split="train",
    )

    assert np.array_equal(np.asarray(features), np.asarray(reused_features))
    assert np.array_equal(np.asarray(labels), np.asarray(reused_labels))
    assert "candidate_cache_reuse" in progress_path.read_text(encoding="utf-8")


def test_candidate_evidence_dataset_cache_metadata_separates_parameters(tmp_path):
    common = {
        "rounds": 7,
        "key": 0,
        "input_difference": 0x9,
        "seed": 5,
        "samples_per_class": 2,
        "pairs_per_sample": 2,
        "negative_mode": "encrypted_random_plaintexts",
        "sample_structure": "zhang_wang_case2_mcnd",
        "key_rotation_interval": 2,
        "beam_width": 2,
        "feature_cache_root": tmp_path / "candidate_cache",
        "feature_cache_chunk_size": 2,
        "progress_output": tmp_path / "progress.jsonl",
        "split": "train",
    }
    make_candidate_dataset(depth=2, **common)
    make_candidate_dataset(depth=3, **common)

    cache_dirs = [path for path in (tmp_path / "candidate_cache" / "train").iterdir() if path.is_dir()]
    assert len(cache_dirs) == 2
