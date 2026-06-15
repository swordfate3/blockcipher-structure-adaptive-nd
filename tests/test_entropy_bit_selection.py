import importlib.util
from pathlib import Path

import numpy as np


def _load_module():
    script_path = Path(__file__).resolve().parents[1] / "experiments" / "select_entropy_bits.py"
    spec = importlib.util.spec_from_file_location("select_entropy_bits", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_select_entropy_bits_prefers_bits_from_low_entropy_triplets():
    module = _load_module()
    differences = np.zeros((16, 8), dtype=np.uint8)
    rng = np.random.default_rng(7)
    differences[:, 3:] = rng.integers(0, 2, size=(16, 5), dtype=np.uint8)

    selected = module.select_entropy_bits_from_matrix(differences, triplet_size=3, target_bits=3, top_triplets=1)

    assert selected == [0, 1, 2]


def test_pair_selected_indices_maps_difference_bits_to_both_ciphertexts():
    module = _load_module()

    assert module.pair_selected_indices([0, 2, 7], block_bits=8) == [0, 2, 7, 8, 10, 15]
