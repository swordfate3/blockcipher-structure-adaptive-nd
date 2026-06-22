import numpy as np

from blockcipher_ai_eval.features.spn_active_pattern import (
    active_mask16_from_word,
    active_pattern_summary_from_words,
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
