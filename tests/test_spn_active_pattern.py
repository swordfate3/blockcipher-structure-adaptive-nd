import numpy as np

from blockcipher_ai_eval.features.spn_active_pattern import (
    active_label_diagnostics,
    active_mask16_from_word,
    active_pattern_summary_from_words,
    extract_active_pattern_features,
    uint64_words_from_bit_rows,
)


def test_active_mask16_from_word_marks_nonzero_nibbles_only():
    word = 0x0000000000F0000A

    mask = active_mask16_from_word(word)

    assert mask.dtype == np.uint8
    assert mask.shape == (16,)
    assert mask.tolist() == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_active_pattern_summary_from_words_counts_positions_and_density():
    words = np.array(
        [
            [0x000000000000000F, 0x00000000000000F0],
            [0x0000000000000000, 0x0000000000000F00],
        ],
        dtype=np.uint64,
    )

    summary = active_pattern_summary_from_words(words)

    assert summary["active_masks"].shape == (2, 2, 16)
    assert summary["active_count"].tolist() == [[1, 1], [0, 1]]
    assert summary["position_frequency"].shape == (2, 16)
    assert summary["position_frequency"][0, :3].tolist() == [0.5, 0.5, 0.0]
    assert summary["density_mean"].tolist() == [0.0625, 0.03125]


def test_uint64_words_from_bit_rows_round_trips_big_endian_words():
    rows = np.array(
        [
            [int(bit) for bit in f"{0x8000000000000001:064b}{0x00000000000000F0:064b}"],
        ],
        dtype=np.uint8,
    )

    words = uint64_words_from_bit_rows(rows, words_per_row=2)

    assert words.shape == (1, 2)
    assert words[0, 0] == 0x8000000000000001
    assert words[0, 1] == 0x00000000000000F0


def test_extract_active_pattern_features_has_stable_shape():
    rows = np.zeros((3, 4 * 64), dtype=np.uint8)
    rows[0, 63] = 1
    rows[0, 127] = 1
    rows[1, 60:64] = 1

    features = extract_active_pattern_features(rows, words_per_row=4)

    assert features.shape == (3, 16 + 4 + 4)
    assert features.dtype == np.float32
    assert features[0, 0] > 0.0


def test_active_label_diagnostics_reports_all_inactive_baseline():
    labels = np.array(
        [
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
        ],
        dtype=np.uint8,
    )

    metrics = active_label_diagnostics(labels)

    assert metrics["active_positive_rate"] == 2 / 12
    assert metrics["all_inactive_accuracy"] == 10 / 12
    assert metrics["positions"] == 4
