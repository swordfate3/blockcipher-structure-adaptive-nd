from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.experiments import build_cipher, difference_for_profile
from blockcipher_ai_eval.features.registry import pair_bits_for_encoding
from blockcipher_ai_eval.models.structure.arx.round_stats_hybrid import arx_round_relation_groups
from blockcipher_ai_eval.training.binary import _binary_auc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit ARX feature-level positive/negative separation before expensive training."
    )
    parser.add_argument("--cipher", default="speck32")
    parser.add_argument("--rounds", type=int, nargs="+", default=[7, 8])
    parser.add_argument("--seeds", type=int, nargs="+", default=[0])
    parser.add_argument("--samples-per-class", type=int, default=2048)
    parser.add_argument("--pairs-per-sample", type=int, default=4)
    parser.add_argument(
        "--feature-encodings",
        nargs="+",
        default=[
            "ciphertext_pair_xor_arx_partial_inverse_bits",
            "ciphertext_pair_xor_arx_partial_inverse_rx_bits",
            "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits",
            "ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_plus_bits",
        ],
    )
    parser.add_argument("--difference-profile", default="speck32_gohr2019")
    parser.add_argument("--difference-member", type=int, default=0)
    parser.add_argument("--negative-mode", default="encrypted_random_plaintexts")
    parser.add_argument("--key-rotation-interval", type=int, default=1024)
    parser.add_argument("--sample-structure", default="independent_pairs")
    parser.add_argument("--train-key", type=lambda value: int(value, 0), default=None)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--output", default="outputs/innovation1/arx_feature_separation_audit.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = run_audit(args)
    payload = {
        "kind": "arx_feature_separation_audit",
        "config": {
            "cipher": args.cipher,
            "rounds": args.rounds,
            "seeds": args.seeds,
            "samples_per_class": args.samples_per_class,
            "pairs_per_sample": args.pairs_per_sample,
            "feature_encodings": args.feature_encodings,
            "difference_profile": args.difference_profile,
            "difference_member": args.difference_member,
            "negative_mode": args.negative_mode,
            "key_rotation_interval": args.key_rotation_interval,
            "sample_structure": args.sample_structure,
            "train_key": args.train_key,
            "top_k": args.top_k,
        },
        "rows": rows,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} audit rows to {output}")


def run_audit(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    input_difference = difference_for_profile(args.difference_profile, args.difference_member)
    for rounds in args.rounds:
        for feature_encoding in args.feature_encodings:
            for seed in args.seeds:
                cipher = build_cipher(args.cipher, rounds, key=args.train_key)
                dataset = make_differential_dataset(
                    DifferentialDatasetConfig(
                        cipher=cipher,
                        input_difference=input_difference,
                        samples_per_class=args.samples_per_class,
                        seed=seed,
                        shuffle=True,
                        feature_encoding=feature_encoding,
                        pairs_per_sample=args.pairs_per_sample,
                        negative_mode=args.negative_mode,
                        key_rotation_interval=args.key_rotation_interval,
                        sample_structure=args.sample_structure,
                    )
                )
                rows.append(
                    audit_dataset(
                        dataset.features.astype(np.float32),
                        dataset.labels.astype(np.uint8),
                        pair_bits=pair_bits_for_encoding(cipher.block_bits, feature_encoding),
                        block_bits=cipher.block_bits,
                        cipher_name=cipher.name,
                        rounds=rounds,
                        seed=seed,
                        feature_encoding=feature_encoding,
                        top_k=args.top_k,
                    )
                )
    return rows


def audit_dataset(
    features: np.ndarray,
    labels: np.ndarray,
    *,
    pair_bits: int,
    block_bits: int,
    cipher_name: str,
    rounds: int,
    seed: int,
    feature_encoding: str,
    top_k: int,
) -> dict[str, Any]:
    if features.ndim != 2:
        raise ValueError("features must be a 2D array")
    if features.shape[1] % pair_bits != 0:
        raise ValueError("feature width must be a multiple of pair_bits")
    if pair_bits % block_bits != 0:
        raise ValueError("ARX audit expects pair_bits to be a multiple of block_bits")

    pairs_per_sample = features.shape[1] // pair_bits
    words_per_pair = pair_bits // block_bits
    word_bits = block_bits // 2
    halves_per_word = 2
    feature_words = features.reshape(features.shape[0], pairs_per_sample, words_per_pair, block_bits)
    half_activity = feature_words.reshape(
        features.shape[0],
        pairs_per_sample,
        words_per_pair,
        halves_per_word,
        word_bits,
    ).mean(axis=4)
    word_activity = feature_words.mean(axis=3)
    pair_activity = features.reshape(features.shape[0], pairs_per_sample, pair_bits).mean(axis=2)
    group_activity = _round_group_activity(word_activity)

    bit_scores = _feature_axis_scores(features, labels)
    half_scores = _feature_axis_scores(half_activity.reshape(features.shape[0], -1), labels)
    word_scores = _feature_axis_scores(word_activity.reshape(features.shape[0], -1), labels)
    pair_scores = _feature_axis_scores(pair_activity, labels)
    group_scores = _feature_axis_scores(group_activity, labels)
    global_scores = _named_scalar_scores(
        {
            "global_bit_density": features.mean(axis=1),
            "pair_activity_mean": pair_activity.mean(axis=1),
            "pair_activity_std": pair_activity.std(axis=1),
            "word_activity_mean": word_activity.mean(axis=(1, 2)),
            "word_activity_std": word_activity.std(axis=(1, 2)),
            "half_activity_mean": half_activity.mean(axis=(1, 2, 3)),
            "half_activity_std": half_activity.std(axis=(1, 2, 3)),
            "first_last_pair_activity_delta": pair_activity[:, -1] - pair_activity[:, 0],
            "base_partial_density_delta": _role_mean(word_activity, 0, 4) - _role_mean(word_activity, 4, 7),
            "rx_partial_density_delta": _role_mean(word_activity, 7, 9) - _role_mean(word_activity, 4, 7),
            "carry_base_density_delta": _role_mean(word_activity, 9, words_per_pair)
            - _role_mean(word_activity, 0, 4),
        },
        labels,
    )

    top_bit_indices = _top_indices(bit_scores["auc_advantage"], top_k)
    top_half_indices = _top_indices(half_scores["auc_advantage"], top_k)
    top_word_indices = _top_indices(word_scores["auc_advantage"], top_k)
    top_group_indices = _top_indices(group_scores["auc_advantage"], top_k)
    return {
        "cipher": cipher_name,
        "rounds": rounds,
        "seed": seed,
        "feature_encoding": feature_encoding,
        "samples": int(features.shape[0]),
        "samples_per_class": int(min((labels == 0).sum(), (labels == 1).sum())),
        "input_bits": int(features.shape[1]),
        "pair_bits": int(pair_bits),
        "pairs_per_sample": int(pairs_per_sample),
        "words_per_pair": int(words_per_pair),
        "best_bit_auc_advantage": _best(bit_scores),
        "best_half_auc_advantage": _best(half_scores),
        "best_word_auc_advantage": _best(word_scores),
        "best_pair_auc_advantage": _best(pair_scores),
        "best_group_auc_advantage": _best(group_scores),
        "global_scores": global_scores,
        "top_bits": _top_feature_rows(bit_scores, top_bit_indices),
        "top_halves": _top_feature_rows(half_scores, top_half_indices),
        "top_words": _top_feature_rows(word_scores, top_word_indices),
        "top_groups": _top_feature_rows(group_scores, top_group_indices),
    }


def _round_group_activity(word_activity: np.ndarray) -> np.ndarray:
    groups = arx_round_relation_groups(word_activity.shape[2])
    values = [word_activity[:, :, group].mean(axis=(1, 2)) for group in groups]
    return np.stack(values, axis=1)


def _role_mean(word_activity: np.ndarray, start: int, stop: int) -> np.ndarray:
    start = min(start, word_activity.shape[2] - 1)
    stop = min(max(stop, start + 1), word_activity.shape[2])
    return word_activity[:, :, start:stop].mean(axis=(1, 2))


def _feature_axis_scores(features: np.ndarray, labels: np.ndarray) -> dict[str, np.ndarray]:
    positive = features[labels == 1]
    negative = features[labels == 0]
    pos_mean = positive.mean(axis=0)
    neg_mean = negative.mean(axis=0)
    pos_var = positive.var(axis=0)
    neg_var = negative.var(axis=0)
    pooled_std = np.sqrt((pos_var + neg_var) / 2.0)
    cohen_d = np.divide(pos_mean - neg_mean, pooled_std, out=np.zeros_like(pos_mean), where=pooled_std > 0)
    auc = np.array([_binary_auc(labels, features[:, index]) for index in range(features.shape[1])], dtype=np.float64)
    return {
        "positive_mean": pos_mean,
        "negative_mean": neg_mean,
        "mean_delta": pos_mean - neg_mean,
        "cohen_d": cohen_d,
        "auc": auc,
        "auc_advantage": np.abs(auc - 0.5),
    }


def _named_scalar_scores(named_scores: dict[str, np.ndarray], labels: np.ndarray) -> dict[str, dict[str, float]]:
    rows = {}
    for name, scores in named_scores.items():
        scores = scores.astype(np.float64)
        positive = scores[labels == 1]
        negative = scores[labels == 0]
        pooled_std = np.sqrt((positive.var() + negative.var()) / 2.0)
        cohen_d = float((positive.mean() - negative.mean()) / pooled_std) if pooled_std > 0 else 0.0
        auc = _binary_auc(labels, scores)
        rows[name] = {
            "positive_mean": float(positive.mean()),
            "negative_mean": float(negative.mean()),
            "mean_delta": float(positive.mean() - negative.mean()),
            "cohen_d": cohen_d,
            "auc": float(auc),
            "auc_advantage": float(abs(auc - 0.5)),
        }
    return rows


def _best(scores: dict[str, np.ndarray]) -> float:
    values = scores["auc_advantage"]
    return float(values.max()) if values.size else 0.0


def _top_indices(scores: np.ndarray, top_k: int) -> list[int]:
    if top_k <= 0 or scores.size == 0:
        return []
    count = min(top_k, scores.size)
    return np.argsort(scores, kind="mergesort")[-count:][::-1].astype(int).tolist()


def _top_feature_rows(scores: dict[str, np.ndarray], indices: list[int]) -> list[dict[str, float | int]]:
    rows = []
    for index in indices:
        rows.append(
            {
                "index": int(index),
                "positive_mean": float(scores["positive_mean"][index]),
                "negative_mean": float(scores["negative_mean"][index]),
                "mean_delta": float(scores["mean_delta"][index]),
                "cohen_d": float(scores["cohen_d"][index]),
                "auc": float(scores["auc"][index]),
                "auc_advantage": float(scores["auc_advantage"][index]),
            }
        )
    return rows


if __name__ == "__main__":
    main()
