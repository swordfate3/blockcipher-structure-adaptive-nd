import numpy as np

from blockcipher_ai_eval.ciphers import Present80
from blockcipher_ai_eval.features.spn_candidate_evidence import (
    present_pair_candidate_evidence_features,
    present_pair_candidate_evidence_layers,
    present_pairset_candidate_evidence_features,
)


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
