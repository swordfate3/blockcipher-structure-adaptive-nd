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
        "evidence": "Shared pair encoder with mean+max pooling baseline",
        "literature": "Multi-pair neural distinguisher / DBitNet-style",
    },
    {
        "network": "StructureAdaptive-PairSet-DBitNet",
        "model_key": "structure_adaptive_pairset_dbitnet",
        "family": "pairset_dilated_cnn",
        "architecture_rank": 2,
        "score": 34,
        "evidence": "Generic structure-conditioned pair-set baseline",
        "literature": "Innovation-one structure-adaptive pair-set DBitNet",
    },
    {
        "network": "SPN-Cell-PairSet-DBitNet-v2",
        "model_key": "spn_pairset_dbitnet_v2",
        "family": "spn_cell_pairset_dbitnet",
        "architecture_rank": 0,
        "score": 36,
        "evidence": "Explicit 4-bit cell encoder for PRESENT/SPN S-box locality",
        "literature": "Innovation-one SPN-specific PairSet DBitNet v2",
    },
    {
        "network": "MoE-v4-Soft",
        "model_key": "moe_v4_soft",
        "family": "structure_adapter_moe",
        "architecture_rank": 3,
        "score": 20,
        "evidence": "Structure-adapter MoE with soft routing",
        "literature": "Innovation-one structure-aware MoE",
    },
]


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for round_count in [4, 5]:
        for seed in [0, 1]:
            for pairs_per_sample in [1, 2, 4]:
                for model in MODELS:
                    rows.append(
                        {
                            "cipher": "PRESENT-80",
                            "structure": "SPN",
                            **model,
                            "rounds": round_count,
                            "seed": seed,
                            "samples_per_class": 32768,
                            "pairs_per_sample": pairs_per_sample,
                            "feature_encoding": "ciphertext_pair_xor_bits",
                            "difference_profile": "present_wang_jain2021",
                            "difference_member": 0,
                        }
                    )
    return rows


def main() -> None:
    output = Path("experiments/plans/innovation1_spn_pairset_v2_present.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(build_rows())


if __name__ == "__main__":
    main()
