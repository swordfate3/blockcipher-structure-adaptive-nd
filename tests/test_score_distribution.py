import importlib.util
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
