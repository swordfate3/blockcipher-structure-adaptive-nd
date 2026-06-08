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
    "difference_profile",
    "difference_member",
    "evidence",
    "literature",
]

MODELS = [
    {
        "network": "Pairwise-Adaptive-DBitNet",
        "model_key": "adaptive_dbitnet_pairwise",
        "family": "pairwise_adaptive_dbitnet",
        "architecture_rank": 1,
        "score": 30,
        "evidence": "Strong pairwise adaptive DBitNet baseline",
        "literature": "Multi-pair neural distinguisher / DBitNet-style",
    },
    {
        "network": "SPN-TokenMixer-PairSet",
        "model_key": "spn_token_mixer_pairset",
        "family": "spn_token_mixer",
        "architecture_rank": 2,
        "score": 44,
        "evidence": "SPN token mixer for S-box/P-layer locality",
        "literature": "Innovation-one SPN token mixer pair-set model",
    },
    {
        "network": "MoE-v5-Soft-HPO-Trial20",
        "model_key": "moe_v5_soft_hpo_present_best",
        "family": "structure_expert_moe_hpo_fixed",
        "architecture_rank": 0,
        "score": 50,
        "evidence": "Fixed HPO trial 20 best configuration for PRESENT multi-pair validation",
        "literature": "Innovation-one MoE v5 component HPO",
    },
]

FEATURE_ENCODINGS = [
    "ciphertext_pair_xor_bits",
    "ciphertext_pair_xor_spn_aligned_bits",
]


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for feature_encoding in FEATURE_ENCODINGS:
        for seed in range(5):
            for model in MODELS:
                rows.append(
                    {
                        "cipher": "PRESENT-80",
                        "structure": "SPN",
                        **model,
                        "rounds": 5,
                        "seed": seed,
                        "samples_per_class": 32768,
                        "pairs_per_sample": 4,
                        "feature_encoding": feature_encoding,
                        "difference_profile": "present_wang_jain2021",
                        "difference_member": 0,
                    }
                )
    return rows


def main() -> None:
    output = Path("experiments/plans/innovation1_spn_aligned_present.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(build_rows())


if __name__ == "__main__":
    main()
