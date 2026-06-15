import importlib.util
from pathlib import Path

import numpy as np


def _load_module():
    script = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "innovation1"
        / "audit_spn_feature_separation.py"
    )
    spec = importlib.util.spec_from_file_location("audit_spn_feature_separation", script)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_audit_dataset_ranks_separating_bits_words_and_cells():
    module = _load_module()
    features = np.zeros((8, 128), dtype=np.float32)
    labels = np.array([1, 1, 1, 1, 0, 0, 0, 0], dtype=np.uint8)
    features[:4, 0] = 1.0
    features[:4, 4:8] = 1.0
    features[4:, 64] = 1.0

    row = module.audit_dataset(
        features,
        labels,
        pair_bits=64,
        block_bits=64,
        cipher_name="toy-spn",
        rounds=1,
        seed=0,
        feature_encoding="toy_cell_matrix_bits",
        top_k=3,
    )

    assert row["pairs_per_sample"] == 2
    assert row["words_per_pair"] == 1
    assert row["best_bit_auc_advantage"] == 0.5
    assert row["best_cell_auc_advantage"] == 0.5
    assert row["top_bits"][0]["auc_advantage"] == 0.5
    assert {item["index"] for item in row["top_bits"]} & {0, 64}
    assert "global_bit_density" in row["global_scores"]


def test_run_audit_smoke_generates_present_rows(tmp_path):
    module = _load_module()

    class Args:
        cipher = "present80"
        rounds = [1]
        seeds = [0]
        samples_per_class = 4
        pairs_per_sample = 2
        feature_encodings = ["present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits"]
        difference_profile = "present_zhang_wang2022_mcnd"
        difference_member = 0
        negative_mode = "encrypted_random_plaintexts"
        key_rotation_interval = 2
        sample_structure = "zhang_wang_case2_mcnd"
        train_key = None
        top_k = 2
        output = str(tmp_path / "audit.json")

    rows = module.run_audit(Args())

    assert len(rows) == 1
    assert rows[0]["cipher"] == "PRESENT-80"
    assert rows[0]["rounds"] == 1
    assert rows[0]["samples"] == 8
    assert rows[0]["pairs_per_sample"] == 2
    assert rows[0]["top_bits"]
