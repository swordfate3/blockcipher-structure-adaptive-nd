#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.experiments import build_cipher, difference_for_profile


def select_entropy_bits_from_matrix(
    differences: np.ndarray,
    *,
    triplet_size: int = 3,
    target_bits: int = 28,
    top_triplets: int | None = None,
) -> list[int]:
    if differences.ndim != 2:
        raise ValueError("differences must be a 2D bit matrix")
    if triplet_size < 1:
        raise ValueError("triplet_size must be positive")
    bit_width = int(differences.shape[1])
    if target_bits < 1 or target_bits > bit_width:
        raise ValueError("target_bits must be in 1..bit_width")
    scores = []
    for combo in itertools.combinations(range(bit_width), triplet_size):
        scores.append((entropy_for_columns(differences, combo), combo))
    scores.sort(key=lambda item: (item[0], item[1]))

    selected: list[int] = []
    seen: set[int] = set()
    limit = top_triplets or len(scores)
    for _entropy, combo in scores[:limit]:
        for bit in combo:
            if bit not in seen:
                selected.append(bit)
                seen.add(bit)
                if len(selected) == target_bits:
                    return sorted(selected)
    for _entropy, combo in scores[limit:]:
        for bit in combo:
            if bit not in seen:
                selected.append(bit)
                seen.add(bit)
                if len(selected) == target_bits:
                    return sorted(selected)
    return sorted(selected)


def entropy_for_columns(bits: np.ndarray, columns: tuple[int, ...]) -> float:
    values = np.zeros(bits.shape[0], dtype=np.uint64)
    for column in columns:
        values = (values << 1) | bits[:, column].astype(np.uint64)
    counts = np.bincount(values, minlength=1 << len(columns)).astype(np.float64)
    probabilities = counts[counts > 0] / counts.sum()
    return float(-(probabilities * np.log2(probabilities)).sum())


def pair_selected_indices(difference_bit_indices: list[int], *, block_bits: int) -> list[int]:
    selected = sorted(difference_bit_indices)
    for index in selected:
        if index < 0 or index >= block_bits:
            raise ValueError("difference bit index is outside the block")
    return selected + [block_bits + index for index in selected]


def build_difference_matrix(
    *,
    cipher_key: str,
    rounds: int,
    input_difference: int,
    samples: int,
    seed: int,
    negative_mode: str,
    train_key: int | None = None,
) -> np.ndarray:
    cipher = build_cipher(cipher_key, rounds, key=train_key)
    dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=cipher,
            input_difference=input_difference,
            samples_per_class=samples,
            seed=seed,
            shuffle=False,
            feature_encoding="ciphertext_xor_bits",
            negative_mode=negative_mode,
        )
    )
    positives = dataset.features[:samples]
    return positives.astype(np.uint8, copy=False)


def write_outputs(output: Path, payload: dict[str, Any]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Select low-entropy output-difference bits for neural distinguishers.")
    parser.add_argument("--cipher", default="present80")
    parser.add_argument("--rounds", type=int, required=True)
    parser.add_argument("--samples", type=int, default=50_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--difference-profile", default="present_entropy2026_gohr")
    parser.add_argument("--difference-member", type=int, default=0)
    parser.add_argument("--negative-mode", default="encrypted_random_plaintexts")
    parser.add_argument("--triplet-size", type=int, default=3)
    parser.add_argument("--target-bits", type=int, default=28)
    parser.add_argument("--top-triplets", type=int, default=None)
    parser.add_argument("--output", type=Path, default=Path("outputs/entropy_bits/selected_bits.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_difference = difference_for_profile(args.difference_profile, args.difference_member)
    matrix = build_difference_matrix(
        cipher_key=args.cipher,
        rounds=args.rounds,
        input_difference=input_difference,
        samples=args.samples,
        seed=args.seed,
        negative_mode=args.negative_mode,
    )
    selected = select_entropy_bits_from_matrix(
        matrix,
        triplet_size=args.triplet_size,
        target_bits=args.target_bits,
        top_triplets=args.top_triplets,
    )
    pair_indices = pair_selected_indices(selected, block_bits=matrix.shape[1])
    payload = {
        "cipher": args.cipher,
        "rounds": args.rounds,
        "samples": args.samples,
        "seed": args.seed,
        "difference_profile": args.difference_profile,
        "difference_member": args.difference_member,
        "input_difference": hex(input_difference),
        "feature_encoding": "ciphertext_xor_bits",
        "base_pair_bits": int(matrix.shape[1]),
        "triplet_size": args.triplet_size,
        "target_bits": args.target_bits,
        "top_triplets": args.top_triplets,
        "selected_bit_indices": selected,
        "pair_selected_bit_indices": pair_indices,
    }
    write_outputs(args.output, payload)
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
