from __future__ import annotations

from typing import TypedDict

import numpy as np
from numpy.typing import NDArray


class ActivePatternSummary(TypedDict):
    active_masks: NDArray[np.uint8]
    active_count: NDArray[np.uint8]
    position_frequency: NDArray[np.float32]
    density_mean: NDArray[np.float32]
    density_std: NDArray[np.float32]
    density_span: NDArray[np.float32]


def active_mask16_from_word(word: int) -> NDArray[np.uint8]:
    mask = np.zeros(16, dtype=np.uint8)
    for nibble_index in range(16):
        mask[nibble_index] = 1 if ((int(word) >> (4 * nibble_index)) & 0xF) != 0 else 0
    return mask


def active_masks16_from_words(words: NDArray[np.uint64]) -> NDArray[np.uint8]:
    word_array = np.asarray(words, dtype=np.uint64)
    flat = word_array.reshape(-1)
    masks = np.stack([active_mask16_from_word(int(word)) for word in flat], axis=0)
    return masks.reshape(*word_array.shape, 16)


def active_pattern_summary_from_words(words: NDArray[np.uint64]) -> ActivePatternSummary:
    word_array = np.asarray(words, dtype=np.uint64)
    if word_array.ndim != 2:
        raise ValueError("words must have shape (rows, words_per_row)")
    active_masks = active_masks16_from_words(word_array)
    active_count = active_masks.sum(axis=-1).astype(np.uint8)
    density = active_count.astype(np.float32) / 16.0
    return {
        "active_masks": active_masks,
        "active_count": active_count,
        "position_frequency": active_masks.mean(axis=1, dtype=np.float32),
        "density_mean": density.mean(axis=1, dtype=np.float32),
        "density_std": density.std(axis=1, dtype=np.float32),
        "density_span": (density.max(axis=1) - density.min(axis=1)).astype(np.float32),
    }
