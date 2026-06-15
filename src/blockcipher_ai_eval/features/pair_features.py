from __future__ import annotations

from blockcipher_ai_eval.ciphers import ReducedRoundCipher
from blockcipher_ai_eval.features.arx_aligned import (
    arx_aligned_difference,
    speck32_partial_inverse_feature_words,
    speck32_partial_inverse_rx_carrychain_feature_words,
    speck32_partial_inverse_rx_feature_words,
)
from blockcipher_ai_eval.features.spn_aligned import inverse_permutation_difference


def _present_sbox_ddt() -> list[list[int]]:
    from blockcipher_ai_eval.ciphers.spn.present import PRESENT_SBOX

    table = [[0 for _ in range(16)] for _ in range(16)]
    for input_difference in range(16):
        for value in range(16):
            output_difference = PRESENT_SBOX[value] ^ PRESENT_SBOX[value ^ input_difference]
            table[input_difference][output_difference] += 1
    return table


PRESENT_SBOX_DDT = _present_sbox_ddt()


def int_to_bits(value: int, width: int) -> list[int]:
    return [(value >> shift) & 1 for shift in range(width - 1, -1, -1)]


def encode_ciphertext_pair(
    left: int,
    right: int,
    *,
    width: int,
    feature_encoding: str,
    cipher: ReducedRoundCipher,
) -> list[int]:
    if feature_encoding == "ciphertext_pair_bits":
        return pair_to_bits(left, right, width)
    if feature_encoding == "present_mcnd_cell_matrix_bits":
        return present_mcnd_cell_matrix_bits(left, right, width)
    if feature_encoding == "present_pair_xor_cell_matrix_bits":
        return present_pair_xor_cell_matrix_bits(left, right, width)
    if feature_encoding == "present_pair_xor_paligned_cell_matrix_bits":
        return present_pair_xor_paligned_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sinv_cell_matrix_bits":
        return present_pair_xor_paligned_sinv_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits":
        return present_pair_xor_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits":
        return present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits":
        return present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sboxddt_cell_matrix_bits":
        return present_pair_xor_paligned_sboxddt_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits":
        return present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sboxddt_back2_cell_matrix_bits":
        return present_pair_xor_paligned_sboxddt_back2_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits":
        return present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits":
        return present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "present_xor_paligned_cell_matrix_bits":
        return present_xor_paligned_cell_matrix_bits(left, right, width, cipher)
    if feature_encoding == "ciphertext_xor_bits":
        return xor_bits(left, right, width)
    if feature_encoding in {"ciphertext_xor_spn_aligned_bits", "ciphertext_xor_spn_paligned_bits"}:
        difference = left ^ right
        return int_to_bits(difference, width) + int_to_bits(
            inverse_permutation_difference(difference, width, cipher),
            width,
        )
    if feature_encoding == "ciphertext_pair_xor_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        return left_bits + right_bits + difference_bits
    if feature_encoding == "ciphertext_pair_xor_spn_aligned_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        aligned_difference = inverse_permutation_difference(left ^ right, width, cipher)
        return left_bits + right_bits + difference_bits + int_to_bits(aligned_difference, width)
    if feature_encoding == "ciphertext_pair_xor_arx_aligned_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        aligned_difference = arx_aligned_difference(left ^ right, width, cipher)
        return left_bits + right_bits + difference_bits + int_to_bits(aligned_difference, width)
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        extra_bits = []
        for word in speck32_partial_inverse_feature_words(left, right, width, cipher):
            extra_bits.extend(int_to_bits(word, width))
        return left_bits + right_bits + difference_bits + extra_bits
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_rx_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        extra_bits = []
        for word in speck32_partial_inverse_rx_feature_words(left, right, width, cipher):
            extra_bits.extend(int_to_bits(word, width))
        return left_bits + right_bits + difference_bits + extra_bits
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits":
        left_bits, right_bits, difference_bits = pair_xor_bits(left, right, width)
        extra_bits = []
        for word in speck32_partial_inverse_rx_carrychain_feature_words(left, right, width, cipher):
            extra_bits.extend(int_to_bits(word, width))
        return left_bits + right_bits + difference_bits + extra_bits
    raise ValueError(f"unsupported feature encoding: {feature_encoding}")


def pair_to_bits(left: int, right: int, width: int) -> list[int]:
    return int_to_bits(left, width) + int_to_bits(right, width)


def present_mcnd_cell_matrix_bits(left: int, right: int, width: int) -> list[int]:
    return words_to_present_cell_matrix_bits([left, right], width, "present_mcnd_cell_matrix_bits")


def present_pair_xor_cell_matrix_bits(left: int, right: int, width: int) -> list[int]:
    return words_to_present_cell_matrix_bits([left, right, left ^ right], width, "present_pair_xor_cell_matrix_bits")


def present_pair_xor_paligned_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference],
        width,
        "present_pair_xor_paligned_cell_matrix_bits",
    )


def present_pair_xor_paligned_sinv_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    structural_inverse_difference = present_structural_inverse_sbox_difference(left, right, width, cipher)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference, structural_inverse_difference],
        width,
        "present_pair_xor_paligned_sinv_cell_matrix_bits",
    )


def present_pair_xor_paligned_sboxddt_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    best_input_difference, ddt_confidence = present_sbox_ddt_words(aligned_difference, width)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference, best_input_difference, ddt_confidence],
        width,
        "present_pair_xor_paligned_sboxddt_cell_matrix_bits",
    )


def present_sbox_ddt_words(aligned_difference: int, width: int) -> tuple[int, int]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_words requires a 4-bit cell block size")
    best_word = 0
    confidence_word = 0
    for nibble_index in range(width // 4):
        output_difference = (aligned_difference >> (4 * nibble_index)) & 0xF
        column = [PRESENT_SBOX_DDT[input_difference][output_difference] for input_difference in range(16)]
        best_input_difference = max(range(16), key=lambda input_difference: column[input_difference])
        best_count = column[best_input_difference]
        confidence = min(15, round(best_count * 15 / 16))
        best_word |= best_input_difference << (4 * nibble_index)
        confidence_word |= confidence << (4 * nibble_index)
    return best_word, confidence_word


def present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    top1, top2, confidence1, confidence2 = present_sbox_ddt_top2_words(aligned_difference, width)
    return words_to_present_cell_matrix_bits(
        [left, right, difference, aligned_difference, top1, top2, confidence1, confidence2],
        width,
        "present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits",
    )


def present_sbox_ddt_top2_words(aligned_difference: int, width: int) -> tuple[int, int, int, int]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_top2_words requires a 4-bit cell block size")
    top1_word = 0
    top2_word = 0
    confidence1_word = 0
    confidence2_word = 0
    for nibble_index in range(width // 4):
        output_difference = (aligned_difference >> (4 * nibble_index)) & 0xF
        ranked = sorted(
            range(16),
            key=lambda input_difference: (
                PRESENT_SBOX_DDT[input_difference][output_difference],
                -input_difference,
            ),
            reverse=True,
        )
        top1 = ranked[0]
        top2 = ranked[1]
        count1 = PRESENT_SBOX_DDT[top1][output_difference]
        count2 = PRESENT_SBOX_DDT[top2][output_difference]
        confidence1 = min(15, round(count1 * 15 / 16))
        confidence2 = min(15, round(count2 * 15 / 16))
        top1_word |= top1 << (4 * nibble_index)
        top2_word |= top2 << (4 * nibble_index)
        confidence1_word |= confidence1 << (4 * nibble_index)
        confidence2_word |= confidence2 << (4 * nibble_index)
    return top1_word, top2_word, confidence1_word, confidence2_word


def present_sbox_ddt_top2_margin_words(aligned_difference: int, width: int) -> tuple[int, int, int, int, int]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_top2_margin_words requires a 4-bit cell block size")
    top1_word = 0
    top2_word = 0
    confidence1_word = 0
    confidence2_word = 0
    margin_word = 0
    for nibble_index in range(width // 4):
        output_difference = (aligned_difference >> (4 * nibble_index)) & 0xF
        ranked = sorted(
            range(16),
            key=lambda input_difference: (
                PRESENT_SBOX_DDT[input_difference][output_difference],
                -input_difference,
            ),
            reverse=True,
        )
        top1 = ranked[0]
        top2 = ranked[1]
        count1 = PRESENT_SBOX_DDT[top1][output_difference]
        count2 = PRESENT_SBOX_DDT[top2][output_difference]
        confidence1 = min(15, round(count1 * 15 / 16))
        confidence2 = min(15, round(count2 * 15 / 16))
        margin = min(15, max(0, count1 - count2))
        top1_word |= top1 << (4 * nibble_index)
        top2_word |= top2 << (4 * nibble_index)
        confidence1_word |= confidence1 << (4 * nibble_index)
        confidence2_word |= confidence2 << (4 * nibble_index)
        margin_word |= margin << (4 * nibble_index)
    return top1_word, top2_word, confidence1_word, confidence2_word, margin_word


def present_pair_xor_paligned_sboxddt_back2_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    layer1, confidence1 = present_sbox_ddt_words(aligned_difference, width)
    layer1_paligned = inverse_permutation_difference(layer1, width, cipher)
    layer2, confidence2 = present_sbox_ddt_words(layer1_paligned, width)
    return words_to_present_cell_matrix_bits(
        [
            left,
            right,
            difference,
            aligned_difference,
            layer1,
            confidence1,
            layer1_paligned,
            layer2,
            confidence2,
        ],
        width,
        "present_pair_xor_paligned_sboxddt_back2_cell_matrix_bits",
    )


def present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    layer1_top1, layer1_top2, confidence1, confidence2, margin1 = present_sbox_ddt_top2_margin_words(
        aligned_difference,
        width,
    )
    layer1_top1_paligned = inverse_permutation_difference(layer1_top1, width, cipher)
    layer1_top2_paligned = inverse_permutation_difference(layer1_top2, width, cipher)
    layer2_from_top1, _layer2_confidence1 = present_sbox_ddt_words(layer1_top1_paligned, width)
    layer2_from_top2, _layer2_confidence2 = present_sbox_ddt_words(layer1_top2_paligned, width)
    beam_disagreement = layer2_from_top1 ^ layer2_from_top2
    return words_to_present_cell_matrix_bits(
        [
            left,
            right,
            difference,
            aligned_difference,
            layer1_top1,
            layer1_top2,
            confidence1,
            confidence2,
            margin1,
            layer2_from_top1,
            layer2_from_top2,
            beam_disagreement,
        ],
        width,
        "present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits",
    )


def present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    trail_words = present_sbox_ddt_beam_words(
        aligned_difference,
        width,
        cipher,
        beam_width=4,
        depth=3,
    )
    return words_to_present_cell_matrix_bits(
        [
            left,
            right,
            difference,
            aligned_difference,
            *trail_words,
        ],
        width,
        "present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits",
    )


def present_pair_xor_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    structural_inverse_difference = present_structural_inverse_sbox_difference(left, right, width, cipher)
    trail_words = present_sbox_ddt_beam_words(
        structural_inverse_difference,
        width,
        cipher,
        beam_width=4,
        depth=3,
    )
    return words_to_present_cell_matrix_bits(
        [
            left,
            right,
            difference,
            aligned_difference,
            structural_inverse_difference,
            *trail_words,
        ],
        width,
        "present_pair_xor_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits",
    )


def present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    structural_inverse_difference = present_structural_inverse_sbox_difference(left, right, width, cipher)
    trail_words = present_sbox_ddt_beam_words(
        structural_inverse_difference,
        width,
        cipher,
        beam_width=4,
        depth=3,
    )
    return words_to_present_cell_matrix_bits(
        [
            difference,
            aligned_difference,
            structural_inverse_difference,
            *trail_words,
        ],
        width,
        "present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits",
    )


def present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    structural_inverse_difference = present_structural_inverse_sbox_difference(left, right, width, cipher)
    trail_stats = present_sbox_ddt_beam_statistics_words(
        structural_inverse_difference,
        width,
        cipher,
        beam_width=4,
        depth=3,
    )
    return words_to_present_cell_matrix_bits(
        [
            difference,
            aligned_difference,
            structural_inverse_difference,
            *trail_stats,
        ],
        width,
        "present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits",
    )


def present_sbox_ddt_beam_statistics_words(
    aligned_difference: int,
    width: int,
    cipher: ReducedRoundCipher,
    *,
    beam_width: int,
    depth: int,
) -> tuple[int, ...]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_beam_statistics_words requires a 4-bit cell block size")
    if beam_width < 1:
        raise ValueError("beam_width must be >= 1")
    if depth < 1:
        raise ValueError("depth must be >= 1")
    beams: list[tuple[int, int]] = [(aligned_difference, 0)]
    output_words: list[int] = []
    mask = (1 << width) - 1
    for _layer in range(depth):
        candidates: list[tuple[int, int, int, int, int]] = []
        for current, cumulative_score in beams:
            top_words, confidence_words, margin_words, scores = present_sbox_ddt_topk_words(
                current,
                width,
                top_k=beam_width,
            )
            for word, confidence, margin, score in zip(top_words, confidence_words, margin_words, scores):
                candidates.append((cumulative_score + score, word, confidence, margin, score))
        candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
        selected = candidates[:beam_width]
        while len(selected) < beam_width:
            selected.append((0, 0, 0, 0, 0))

        top_score, top_word, top_confidence, top_margin, _layer_score = selected[0]
        disagreement = 0
        confidence_union = 0
        margin_union = 0
        score_word = 0
        active_word = 0
        cumulative_word = 0
        for index, (cumulative_score, word, confidence, margin, score) in enumerate(selected[:beam_width]):
            disagreement ^= top_word ^ word
            confidence_union |= confidence
            margin_union |= margin
            score_word |= present_sbox_ddt_score_nibble(score, width) << (4 * index)
            cumulative_word |= present_sbox_ddt_score_nibble(cumulative_score, width) << (4 * index)
            active_word |= present_active_nibble_count(word, width) << (4 * index)
        output_words.extend(
            [
                top_word,
                top_confidence,
                top_margin,
                disagreement & mask,
                confidence_union,
                margin_union,
                score_word,
                cumulative_word,
                active_word,
            ]
        )
        beams = [
            (inverse_permutation_difference(word, width, cipher), cumulative_score)
            for cumulative_score, word, _confidence, _margin, _score in selected[:beam_width]
        ]
        if not beams:
            beams = [(top_word, top_score)]
    return tuple(output_words)


def present_sbox_ddt_beam_words(
    aligned_difference: int,
    width: int,
    cipher: ReducedRoundCipher,
    *,
    beam_width: int,
    depth: int,
) -> tuple[int, ...]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_beam_words requires a 4-bit cell block size")
    if beam_width < 1:
        raise ValueError("beam_width must be >= 1")
    if depth < 1:
        raise ValueError("depth must be >= 1")
    beams: list[tuple[int, int]] = [(aligned_difference, 0)]
    output_words: list[int] = []
    mask = (1 << width) - 1
    for _layer in range(depth):
        candidates: list[tuple[int, int, int, int, int, int]] = []
        for current, cumulative_score in beams:
            top_words, confidence_words, margin_words, scores = present_sbox_ddt_topk_words(
                current,
                width,
                top_k=beam_width,
            )
            for word, confidence, margin, score in zip(top_words, confidence_words, margin_words, scores):
                candidates.append((cumulative_score + score, word, confidence, margin, current, score))
        candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
        selected = candidates[:beam_width]
        selected_words = [item[1] for item in selected]
        selected_confidences = [item[2] for item in selected]
        selected_margins = [item[3] for item in selected]
        selected_scores = [item[5] for item in selected]
        while len(selected_words) < beam_width:
            selected_words.append(0)
            selected_confidences.append(0)
            selected_margins.append(0)
            selected_scores.append(0)
        top_word = selected_words[0]
        disagreement = 0
        score_word = 0
        active_word = 0
        for index, word in enumerate(selected_words[:beam_width]):
            disagreement ^= top_word ^ word
            score_word |= present_sbox_ddt_score_nibble(selected_scores[index], width) << (4 * index)
            active_word |= present_active_nibble_count(word, width) << (4 * index)
        output_words.extend(selected_words[:beam_width])
        output_words.extend(selected_confidences[:beam_width])
        output_words.extend(selected_margins[:beam_width])
        output_words.extend([disagreement & mask, score_word, active_word])
        beams = [(inverse_permutation_difference(word, width, cipher), selected[index][0]) for index, word in enumerate(selected_words[:beam_width])]
    return tuple(output_words)


def present_sbox_ddt_topk_words(
    aligned_difference: int,
    width: int,
    *,
    top_k: int,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    if width % 4 != 0:
        raise ValueError("present_sbox_ddt_topk_words requires a 4-bit cell block size")
    if top_k < 1:
        raise ValueError("top_k must be >= 1")
    words = [0 for _ in range(top_k)]
    confidence_words = [0 for _ in range(top_k)]
    margin_words = [0 for _ in range(top_k)]
    scores = [0 for _ in range(top_k)]
    for nibble_index in range(width // 4):
        output_difference = (aligned_difference >> (4 * nibble_index)) & 0xF
        ranked = sorted(
            range(16),
            key=lambda input_difference: (
                PRESENT_SBOX_DDT[input_difference][output_difference],
                -input_difference,
            ),
            reverse=True,
        )
        selected = ranked[:top_k]
        while len(selected) < top_k:
            selected.append(0)
        counts = [PRESENT_SBOX_DDT[input_difference][output_difference] for input_difference in selected]
        for index, (input_difference, count) in enumerate(zip(selected, counts)):
            next_count = counts[index + 1] if index + 1 < len(counts) else 0
            confidence = min(15, round(count * 15 / 16))
            margin = min(15, max(0, count - next_count))
            words[index] |= input_difference << (4 * nibble_index)
            confidence_words[index] |= confidence << (4 * nibble_index)
            margin_words[index] |= margin << (4 * nibble_index)
            scores[index] += count
    return tuple(words), tuple(confidence_words), tuple(margin_words), tuple(scores)


def present_sbox_ddt_score_nibble(score: int, width: int) -> int:
    nibbles = max(1, width // 4)
    return min(15, max(0, round(score * 15 / (16 * nibbles))))


def present_active_nibble_count(word: int, width: int) -> int:
    count = 0
    max_nibbles = min(16, width // 4)
    for nibble_index in range(max_nibbles):
        if ((word >> (4 * nibble_index)) & 0xF) != 0:
            count += 1
    return min(15, count)


def present_sbox_ddt_back2_words(
    aligned_difference: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> tuple[int, int, int, int, int]:
    layer1, confidence1 = present_sbox_ddt_words(aligned_difference, width)
    layer1_paligned = inverse_permutation_difference(layer1, width, cipher)
    layer2, confidence2 = present_sbox_ddt_words(layer1_paligned, width)
    return layer1, confidence1, layer1_paligned, layer2, confidence2


def present_structural_inverse_sbox_difference(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> int:
    inverse_sbox = getattr(cipher, "inverse_sbox_layer", None)
    if inverse_sbox is None or not callable(inverse_sbox):
        raise ValueError(
            "present_pair_xor_paligned_sinv_cell_matrix_bits requires a cipher with "
            "inverse_sbox_layer"
        )
    left_aligned = inverse_permutation_difference(left, width, cipher)
    right_aligned = inverse_permutation_difference(right, width, cipher)
    mask = (1 << width) - 1
    return (int(inverse_sbox(left_aligned)) ^ int(inverse_sbox(right_aligned))) & mask


def present_xor_paligned_cell_matrix_bits(
    left: int,
    right: int,
    width: int,
    cipher: ReducedRoundCipher,
) -> list[int]:
    difference = left ^ right
    aligned_difference = inverse_permutation_difference(difference, width, cipher)
    return words_to_present_cell_matrix_bits(
        [difference, aligned_difference],
        width,
        "present_xor_paligned_cell_matrix_bits",
    )


def words_to_present_cell_matrix_bits(words: list[int], width: int, feature_encoding: str) -> list[int]:
    if width % 4 != 0:
        raise ValueError(f"{feature_encoding} requires a 4-bit cell block size")
    bits = []
    for word in words:
        bits.extend(int_to_bits(word, width))
    cells = [bits[index : index + 4] for index in range(0, len(bits), 4)]
    return [cell[bit_index] for bit_index in range(4) for cell in cells]


def xor_bits(left: int, right: int, width: int) -> list[int]:
    return int_to_bits(left ^ right, width)


def pair_xor_bits(left: int, right: int, width: int) -> tuple[list[int], list[int], list[int]]:
    left_bits = int_to_bits(left, width)
    right_bits = int_to_bits(right, width)
    difference_bits = [left_bit ^ right_bit for left_bit, right_bit in zip(left_bits, right_bits)]
    return left_bits, right_bits, difference_bits


def pair_bits_for_encoding(block_bits: int, feature_encoding: str) -> int:
    if feature_encoding in {"ciphertext_pair_bits", "present_mcnd_cell_matrix_bits"}:
        return block_bits * 2
    if feature_encoding == "present_pair_xor_cell_matrix_bits":
        return block_bits * 3
    if feature_encoding == "present_pair_xor_paligned_cell_matrix_bits":
        return block_bits * 4
    if feature_encoding == "present_pair_xor_paligned_sinv_cell_matrix_bits":
        return block_bits * 5
    if feature_encoding == "present_pair_xor_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits":
        return block_bits * 50
    if feature_encoding == "present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits":
        return block_bits * 48
    if feature_encoding == "present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits":
        return block_bits * 30
    if feature_encoding == "present_pair_xor_paligned_sboxddt_cell_matrix_bits":
        return block_bits * 6
    if feature_encoding == "present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits":
        return block_bits * 8
    if feature_encoding == "present_pair_xor_paligned_sboxddt_back2_cell_matrix_bits":
        return block_bits * 9
    if feature_encoding == "present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits":
        return block_bits * 12
    if feature_encoding == "present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits":
        return block_bits * 49
    if feature_encoding == "present_xor_paligned_cell_matrix_bits":
        return block_bits * 2
    if feature_encoding == "ciphertext_xor_bits":
        return block_bits
    if feature_encoding in {"ciphertext_xor_spn_aligned_bits", "ciphertext_xor_spn_paligned_bits"}:
        return block_bits * 2
    if feature_encoding == "ciphertext_pair_xor_bits":
        return block_bits * 3
    if feature_encoding == "ciphertext_pair_xor_spn_aligned_bits":
        return block_bits * 4
    if feature_encoding == "ciphertext_pair_xor_arx_aligned_bits":
        return block_bits * 4
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_bits":
        return block_bits * 7
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_rx_bits":
        return block_bits * 11
    if feature_encoding == "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits":
        return block_bits * 17
    raise ValueError(f"unsupported feature encoding: {feature_encoding}")
