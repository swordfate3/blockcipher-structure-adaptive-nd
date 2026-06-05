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
        "architecture_rank": 0,
        "score": 34,
        "evidence": "Structure-conditioned dilation, bit-mask priors, and attention/mean/max pair-set pooling",
        "literature": "Innovation-one structure-adaptive pair-set DBitNet",
    },
    {
        "network": "MoE-v4-Soft",
        "model_key": "moe_v4_soft",
        "family": "structure_adapter_moe",
        "architecture_rank": 2,
        "score": 20,
        "evidence": "Structure-adapter MoE with soft routing",
        "literature": "Innovation-one structure-aware MoE",
    },
]

GPU0_CIPHERS = [
    {
        "cipher": "SPECK32/64",
        "structure": "ARX",
        "rounds": [5, 6],
        "difference_profile": "speck32_gohr2019",
    },
    {
        "cipher": "PRESENT-80",
        "structure": "SPN",
        "rounds": [4, 5],
        "difference_profile": "present_wang_jain2021",
    },
]

GPU1_CIPHERS = [
    {
        "cipher": "SM4",
        "structure": "Feistel-like",
        "rounds": [3, 4],
        "difference_profile": "sm4_yu2023_conv_resnet",
    },
]


def build_rows(cipher_configs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for cipher_config in cipher_configs:
        for round_count in cipher_config["rounds"]:
            for seed in [0, 1]:
                for pairs_per_sample in [1, 2, 4]:
                    for model in MODELS:
                        rows.append(
                            {
                                "cipher": cipher_config["cipher"],
                                "structure": cipher_config["structure"],
                                **model,
                                "rounds": round_count,
                                "seed": seed,
                                "samples_per_class": 32768,
                                "pairs_per_sample": pairs_per_sample,
                                "feature_encoding": "ciphertext_pair_xor_bits",
                                "difference_profile": cipher_config["difference_profile"],
                                "difference_member": 0,
                            }
                        )
    return rows


def write_plan(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    plan_dir = Path("experiments/plans")
    write_plan(plan_dir / "innovation1_structure_pairset_gpu0.csv", build_rows(GPU0_CIPHERS))
    write_plan(plan_dir / "innovation1_structure_pairset_gpu1.csv", build_rows(GPU1_CIPHERS))


if __name__ == "__main__":
    main()
