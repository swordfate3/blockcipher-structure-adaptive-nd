from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import torch

from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import random_int
from blockcipher_ai_eval.experiments.difference_profiles import difference_for_profile
from blockcipher_ai_eval.experiments.factories import build_cipher
from blockcipher_ai_eval.features.spn_candidate_evidence import (
    present_pairset_candidate_evidence_features,
)


DEFAULT_DIFFERENCE_PROFILE = "present_zhang_wang2022_mcnd"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=7)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--samples-per-class", type=int, default=4096)
    parser.add_argument("--pairs-per-sample", type=int, default=16)
    parser.add_argument("--negative-mode", default="encrypted_random_plaintexts")
    parser.add_argument("--sample-structure", default="zhang_wang_case2_mcnd")
    parser.add_argument("--difference-profile", default=DEFAULT_DIFFERENCE_PROFILE)
    parser.add_argument("--difference-member", type=int, default=0)
    parser.add_argument("--train-key", type=lambda value: int(value, 0), default=0)
    parser.add_argument("--validation-key", type=lambda value: int(value, 0), default=(1 << 80) - 1)
    parser.add_argument("--key-rotation-interval", type=int, default=1024)
    parser.add_argument("--beam-width", type=int, default=4)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--learning-rate", type=float, default=1e-2)
    parser.add_argument("--model", choices=["linear", "mlp"], default="linear")
    parser.add_argument("--device", default="cpu")
    return parser.parse_args()


def make_candidate_dataset(
    *,
    rounds: int,
    key: int,
    input_difference: int,
    seed: int,
    samples_per_class: int,
    pairs_per_sample: int,
    negative_mode: str,
    sample_structure: str,
    key_rotation_interval: int,
    beam_width: int,
    depth: int,
) -> tuple[np.ndarray, np.ndarray]:
    cipher = build_cipher("present80", rounds, key=key)
    config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=input_difference,
        samples_per_class=samples_per_class,
        seed=seed,
        pairs_per_sample=pairs_per_sample,
        negative_mode=negative_mode,
        key_rotation_interval=key_rotation_interval,
        sample_structure=sample_structure,
    )
    rng = np.random.default_rng(seed)
    features: list[np.ndarray] = []
    labels: list[int] = []
    mask = (1 << cipher.block_bits) - 1
    for row_index in range(samples_per_class):
        row_cipher = _cipher_for_row(config, rng, row_index)
        pairs = _positive_pairs(config, rng, row_cipher, mask)
        features.append(
            present_pairset_candidate_evidence_features(
                pairs,
                width=cipher.block_bits,
                cipher=row_cipher,
                beam_width=beam_width,
                depth=depth,
            )
        )
        labels.append(1)
    for row_index in range(samples_per_class):
        row_cipher = _cipher_for_row(config, rng, row_index)
        pairs = _negative_pairs(config, rng, row_cipher, mask)
        features.append(
            present_pairset_candidate_evidence_features(
                pairs,
                width=cipher.block_bits,
                cipher=row_cipher,
                beam_width=beam_width,
                depth=depth,
            )
        )
        labels.append(0)
    feature_array = np.stack(features, axis=0).astype(np.float32)
    label_array = np.array(labels, dtype=np.uint8)
    order = rng.permutation(label_array.size)
    return feature_array[order], label_array[order]


def _positive_pairs(config: DifferentialDatasetConfig, rng: np.random.Generator, cipher, mask: int) -> list[tuple[int, int]]:
    base = random_int(rng, cipher.block_bits)
    pairs = []
    for mask_delta in _plaintext_masks(config, rng):
        plaintext = (base ^ mask_delta) & mask
        paired = (plaintext ^ config.input_difference) & mask
        pairs.append((cipher.encrypt(plaintext), cipher.encrypt(paired)))
    return pairs


def _negative_pairs(config: DifferentialDatasetConfig, rng: np.random.Generator, cipher, mask: int) -> list[tuple[int, int]]:
    base = random_int(rng, cipher.block_bits)
    pairs = []
    for mask_delta in _plaintext_masks(config, rng):
        if config.negative_mode == "random_ciphertext":
            pairs.append((random_int(rng, cipher.block_bits), random_int(rng, cipher.block_bits)))
        else:
            plaintext_a = (base ^ mask_delta) & mask
            plaintext_b = random_int(rng, cipher.block_bits)
            pairs.append((cipher.encrypt(plaintext_a), cipher.encrypt(plaintext_b)))
    return pairs


def _plaintext_masks(config: DifferentialDatasetConfig, rng: np.random.Generator) -> list[int]:
    if config.sample_structure == "independent_pairs":
        return [random_int(rng, config.cipher.block_bits) for _ in range(config.pairs_per_sample)]
    if config.sample_structure != "zhang_wang_case2_mcnd":
        raise ValueError(f"unsupported sample_structure for candidate evidence: {config.sample_structure}")
    masks = {0}
    while len(masks) < config.pairs_per_sample:
        masks.add(random_int(rng, config.cipher.block_bits))
    return list(masks)


def _cipher_for_row(config: DifferentialDatasetConfig, rng: np.random.Generator, row_index: int):
    if config.key_rotation_interval == 0:
        return config.cipher
    key_block_index = row_index // config.key_rotation_interval
    key_rng = np.random.default_rng(config.seed + 1_000_003 * (key_block_index + 1))
    key = random_int(key_rng, int(config.cipher.key_bits))
    return replace(config.cipher, key=key)


def build_baseline(input_dim: int, model: str) -> torch.nn.Module:
    if model == "linear":
        return torch.nn.Linear(input_dim, 1)
    return torch.nn.Sequential(
        torch.nn.LayerNorm(input_dim),
        torch.nn.Linear(input_dim, 128),
        torch.nn.GELU(),
        torch.nn.Linear(128, 64),
        torch.nn.GELU(),
        torch.nn.Linear(64, 1),
    )


def train_model(
    features: np.ndarray,
    labels: np.ndarray,
    *,
    model_name: str,
    epochs: int,
    learning_rate: float,
    device: torch.device,
) -> torch.nn.Module:
    torch.manual_seed(0)
    x = torch.from_numpy(features.astype(np.float32)).to(device)
    y = torch.from_numpy(labels.astype(np.float32)).reshape(-1, 1).to(device)
    model = build_baseline(features.shape[1], model_name).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    for _epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
    return model


def binary_accuracy(labels: np.ndarray, probabilities: np.ndarray, *, threshold: float = 0.5) -> float:
    predictions = (probabilities >= threshold).astype(np.uint8)
    return float((predictions == labels.astype(np.uint8)).mean())


def binary_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    label_array = labels.astype(np.uint8)
    positive_count = int(label_array.sum())
    negative_count = int(label_array.size - positive_count)
    if positive_count == 0 or negative_count == 0:
        return 0.5
    order = np.argsort(scores, kind="mergesort")
    sorted_scores = scores[order]
    ranks = np.empty_like(sorted_scores, dtype=np.float64)
    start = 0
    while start < sorted_scores.size:
        end = start + 1
        while end < sorted_scores.size and sorted_scores[end] == sorted_scores[start]:
            end += 1
        ranks[start:end] = (start + 1 + end) / 2.0
        start = end
    original_ranks = np.empty_like(ranks)
    original_ranks[order] = ranks
    positive_rank_sum = float(original_ranks[label_array == 1].sum())
    return (positive_rank_sum - positive_count * (positive_count + 1) / 2.0) / (
        positive_count * negative_count
    )


def main() -> None:
    args = parse_args()
    input_difference = difference_for_profile(args.difference_profile, args.difference_member)
    train_features, train_labels = make_candidate_dataset(
        rounds=args.rounds,
        key=args.train_key,
        input_difference=input_difference,
        seed=args.seed,
        samples_per_class=args.samples_per_class,
        pairs_per_sample=args.pairs_per_sample,
        negative_mode=args.negative_mode,
        sample_structure=args.sample_structure,
        key_rotation_interval=args.key_rotation_interval,
        beam_width=args.beam_width,
        depth=args.depth,
    )
    validation_features, validation_labels = make_candidate_dataset(
        rounds=args.rounds,
        key=args.validation_key,
        input_difference=input_difference,
        seed=args.seed + 10_000,
        samples_per_class=max(1024, args.samples_per_class // 4),
        pairs_per_sample=args.pairs_per_sample,
        negative_mode=args.negative_mode,
        sample_structure=args.sample_structure,
        key_rotation_interval=args.key_rotation_interval,
        beam_width=args.beam_width,
        depth=args.depth,
    )
    device = torch.device(args.device)
    model = train_model(
        train_features,
        train_labels,
        model_name=args.model,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        device=device,
    )
    with torch.no_grad():
        logits = (
            model(torch.from_numpy(validation_features.astype(np.float32)).to(device))
            .detach()
            .cpu()
            .numpy()
            .reshape(-1)
        )
    probabilities = 1.0 / (1.0 + np.exp(-logits))
    result = {
        "route": "spn_candidate_evidence_baseline",
        "rounds": args.rounds,
        "seed": args.seed,
        "samples_per_class": args.samples_per_class,
        "validation_samples_per_class": max(1024, args.samples_per_class // 4),
        "pairs_per_sample": args.pairs_per_sample,
        "negative_mode": args.negative_mode,
        "sample_structure": args.sample_structure,
        "difference_profile": args.difference_profile,
        "difference_member": args.difference_member,
        "input_difference": input_difference,
        "key_rotation_interval": args.key_rotation_interval,
        "beam_width": args.beam_width,
        "depth": args.depth,
        "model": args.model,
        "device": args.device,
        "feature_dim": int(train_features.shape[1]),
        "val_accuracy": binary_accuracy(validation_labels, probabilities),
        "val_auc": binary_auc(validation_labels, probabilities),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
