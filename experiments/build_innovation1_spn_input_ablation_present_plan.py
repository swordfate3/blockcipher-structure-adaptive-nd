from __future__ import annotations

import csv
from pathlib import Path


FIELDNAMES = [
    "cipher",
    "structure",
    "network",
    "model_key",
    "family",
    "architecture_rank",
    "score",
    "rounds",
    "seed",
    "samples_per_class",
    "pairs_per_sample",
    "feature_encoding",
    "negative_mode",
    "train_key",
    "validation_key",
    "difference_profile",
    "difference_member",
    "evidence",
    "literature",
]

FEATURE_ENCODINGS = [
    "ciphertext_xor_bits",
    "ciphertext_xor_spn_aligned_bits",
    "ciphertext_pair_xor_bits",
    "ciphertext_pair_xor_spn_aligned_bits",
]


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rounds in [5, 6]:
        for feature_encoding in FEATURE_ENCODINGS:
            for seed in range(3):
                rows.append(
                    {
                        "cipher": "PRESENT-80",
                        "structure": "SPN",
                        "network": "SPN-TokenMixer-PairSet",
                        "model_key": "spn_token_mixer_pairset",
                        "family": "spn_token_mixer",
                        "architecture_rank": 0,
                        "score": 64,
                        "rounds": rounds,
                        "seed": seed,
                        "samples_per_class": 32768,
                        "pairs_per_sample": 4,
                        "feature_encoding": feature_encoding,
                        "negative_mode": "encrypted_random_plaintexts",
                        "train_key": "0x00000000000000000000",
                        "validation_key": "0x11111111111111111111",
                        "difference_profile": "present_wang_jain2021",
                        "difference_member": 0,
                        "evidence": "Input ablation for raw difference, inverse-P aligned difference, and full pair encodings",
                        "literature": "Innovation-one SPN aligned input validation",
                    }
                )
    return rows


def main() -> None:
    output = Path("experiments/plans/innovation1_spn_input_ablation_present.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(build_rows())


if __name__ == "__main__":
    main()
