from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.datasets import DifferentialDatasetConfig, make_differential_dataset
from blockcipher_ai_eval.experiments import (
    build_cipher,
    build_model,
    default_difference,
    difference_for_profile,
    literature_difference_profiles,
)
from blockcipher_ai_eval.hpo import select_trials
from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.features import structure_feature_vector
from blockcipher_ai_eval.training import TrainingConfig, train_binary_classifier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run lightweight hyperparameter search trials.")
    parser.add_argument("--space", required=True, help="JSON search-space file.")
    parser.add_argument("--mode", choices=["grid", "random"], default="random")
    parser.add_argument("--max-trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--trial-seeds",
        type=int,
        nargs="+",
        default=None,
        help="Optional seed list evaluated inside each trial; metrics are averaged per trial.",
    )
    parser.add_argument("--samples-per-class", type=int, default=8192)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--hidden-bits", type=int, default=64)
    parser.add_argument("--feature-encoding", default="ciphertext_pair_xor_bits")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--output", default="outputs/hparam_search/trials.jsonl")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    space = _load_space(Path(args.space))
    trials = select_trials(space, mode=args.mode, max_trials=args.max_trials, seed=args.seed)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as handle:
        for trial_id, config in enumerate(trials):
            row = _run_trial(trial_id, config, args)
            handle.write(json.dumps(row, sort_keys=True) + "\n")
            handle.flush()
            seed_note = ""
            if row.get("trial_seeds"):
                seed_note = " seeds=" + ",".join(str(seed) for seed in row["trial_seeds"])
            print(
                "[{index}/{total}] trial={trial} cipher={cipher} model={model} score={score:.6f}{seed_note}".format(
                    index=trial_id + 1,
                    total=len(trials),
                    trial=trial_id,
                    cipher=row["cipher"],
                    model=row["config"]["model"],
                    score=row["metrics"]["calibrated_accuracy"],
                    seed_note=seed_note,
                ),
                flush=True,
            )
    print(f"wrote {len(trials)} HPO rows to {output}")


def _load_space(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return _load_minimal_yaml(text)


def _load_minimal_yaml(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(":"):
            current_key = line[:-1]
            result[current_key] = []
            continue
        if line.startswith("-") and current_key is not None:
            result[current_key].append(_parse_scalar(line[1:].strip()))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = [_parse_scalar(value.strip())]
            current_key = None
            continue
        raise ValueError(f"unsupported search-space line: {raw_line}")
    return result


def _parse_scalar(value: str) -> Any:
    if value in {"", "null", "None"}:
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        if any(ch in value for ch in [".", "e", "E"]):
            return float(value)
        return int(value)
    except ValueError:
        return value.strip("\"'")


def _run_trial(trial_id: int, config: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    trial_seeds = _trial_seeds(trial_id, config, args)
    if len(trial_seeds) == 1:
        return _run_seed_trial(trial_id, config, args, trial_seeds[0])

    seed_rows = [_run_seed_trial(trial_id, config, args, seed) for seed in trial_seeds]
    return _aggregate_trial_rows(trial_id, config, trial_seeds, seed_rows)


def _trial_seeds(trial_id: int, config: dict[str, Any], args: argparse.Namespace) -> list[int]:
    if args.trial_seeds:
        return [int(seed) for seed in args.trial_seeds]
    return [int(config.get("seed", args.seed + trial_id))]


def _run_seed_trial(
    trial_id: int,
    config: dict[str, Any],
    args: argparse.Namespace,
    seed: int,
) -> dict[str, Any]:
    cipher_key = str(config.get("cipher", "present80"))
    model_key = str(config.get("model", "spn_nibble_conv_pairset"))
    rounds = int(config.get("rounds", 1))
    pairs_per_sample = int(config.get("pairs_per_sample", 1))
    feature_encoding = str(config.get("feature_encoding", args.feature_encoding))
    samples_per_class = int(config.get("samples_per_class", args.samples_per_class))
    difference_profile = str(config.get("difference_profile", "") or "")
    difference_member = int(config.get("difference_member", 0) or 0)

    cipher = build_cipher(cipher_key, rounds)
    input_difference = _input_difference_from_config(
        config,
        cipher_key=cipher_key,
        difference_profile=difference_profile,
        difference_member=difference_member,
    )
    train_dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=cipher,
            input_difference=input_difference,
            samples_per_class=samples_per_class,
            seed=seed,
            feature_encoding=feature_encoding,
            pairs_per_sample=pairs_per_sample,
        )
    )
    validation_dataset = make_differential_dataset(
        DifferentialDatasetConfig(
            cipher=cipher,
            input_difference=input_difference,
            samples_per_class=max(8, samples_per_class // 2),
            seed=seed + 10_000,
            feature_encoding=feature_encoding,
            pairs_per_sample=pairs_per_sample,
        )
    )
    pair_bits = train_dataset.features.shape[1] // pairs_per_sample
    hidden_bits = int(config.get("hidden_bits", args.hidden_bits))
    model_options = _model_options_from_config(config)
    model = build_model(
        model_key,
        input_bits=int(train_dataset.features.shape[1]),
        hidden_bits=hidden_bits,
        pair_bits=pair_bits,
        structure=cipher.structure,
        model_options=model_options,
    )
    _configure_structure_aware_model(model, cipher_key, rounds)
    if hasattr(model, "set_cipher_structure"):
        model.set_cipher_structure(cipher.structure)

    result = train_binary_classifier(
        model,
        train_dataset,
        validation_dataset,
        TrainingConfig(
            epochs=int(config.get("epochs", args.epochs)),
            batch_size=int(config.get("batch_size", args.batch_size)),
            learning_rate=float(config.get("learning_rate", config.get("lr", 1e-3))),
            optimizer=str(config.get("optimizer", "adamw")),
            weight_decay=float(config.get("weight_decay", 0.0)),
            lr_scheduler=str(config.get("lr_scheduler", "none")),
            seed=seed,
            device=args.device,
        ),
    )
    return {
        "trial_id": trial_id,
        "cipher": cipher.name,
        "structure": cipher.structure,
        "rounds": rounds,
        "seed": seed,
        "samples_per_class": samples_per_class,
        "pairs_per_sample": pairs_per_sample,
        "feature_encoding": feature_encoding,
        "input_difference": input_difference,
        "difference_profile": difference_profile,
        "difference_member": difference_member if difference_profile else "",
        "input_bits": int(train_dataset.features.shape[1]),
        "pair_bits": int(pair_bits),
        "config": config,
        "model_options": model_options,
        **_model_metadata(model),
        "metrics": result.final_metrics,
        "history": result.history,
        "training": result.metadata,
    }


def _aggregate_trial_rows(
    trial_id: int,
    config: dict[str, Any],
    trial_seeds: list[int],
    seed_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    first = seed_rows[0]
    metrics = _mean_metrics([row["metrics"] for row in seed_rows])
    metrics_std = _std_metrics([row["metrics"] for row in seed_rows], metrics)
    result = {
        key: value
        for key, value in first.items()
        if key not in {"metrics", "history", "training", "seed"}
    }
    result.update(
        {
            "trial_id": trial_id,
            "seed": ",".join(str(seed) for seed in trial_seeds),
            "trial_seeds": trial_seeds,
            "metrics": metrics,
            "metrics_std": metrics_std,
            "seed_results": [
                {
                    "seed": row["seed"],
                    "metrics": row["metrics"],
                    "history": row["history"],
                    "training": row["training"],
                }
                for row in seed_rows
            ],
        }
    )
    return result


def _mean_metrics(rows: list[dict[str, float]]) -> dict[str, float]:
    keys = sorted(set().union(*(row.keys() for row in rows)))
    return {key: sum(float(row[key]) for row in rows) / len(rows) for key in keys}


def _std_metrics(
    rows: list[dict[str, float]],
    means: dict[str, float],
) -> dict[str, float]:
    if len(rows) < 2:
        return {key: 0.0 for key in means}
    result: dict[str, float] = {}
    for key, mean in means.items():
        variance = sum((float(row[key]) - mean) ** 2 for row in rows) / (len(rows) - 1)
        result[key] = variance ** 0.5
    return result


def _model_options_from_config(config: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "activation",
        "norm",
        "pooling",
        "nibble_embed_dim",
        "conv_depth",
        "kernel_size",
        "dropout",
        "token_dim",
        "mixer_depth",
        "token_mlp_ratio",
        "gate_hidden_bits",
        "gate_activation",
        "gate_dropout",
        "gate_temperature",
        "pairwise_pooling",
        "spn_token_dim",
        "spn_mixer_depth",
        "spn_token_mlp_ratio",
        "expert_activation",
        "expert_norm",
        "spn_pooling",
        "expert_dropout",
    }
    return {key: config[key] for key in keys if key in config}


def _input_difference_from_config(
    config: dict[str, Any],
    cipher_key: str,
    difference_profile: str,
    difference_member: int,
) -> int:
    if "input_difference" in config:
        return int(config["input_difference"])
    if not difference_profile:
        return default_difference(cipher_key)
    profile = literature_difference_profiles()[difference_profile]
    if profile.cipher != cipher_key:
        raise ValueError(
            f"difference profile {difference_profile} is for {profile.cipher}, not {cipher_key}"
        )
    return difference_for_profile(difference_profile, difference_member)


def _configure_structure_aware_model(model: Any, cipher_key: str, rounds: int) -> None:
    if not hasattr(model, "set_structure_features"):
        return
    vector = structure_feature_vector(_cipher_profile(cipher_key), rounds)
    model.set_structure_features(torch.tensor(vector, dtype=torch.float32))


def _model_metadata(model: Any) -> dict[str, Any]:
    if not hasattr(model, "gate_summary"):
        return {}
    summary = model.gate_summary()
    gate_weights = {
        key.removeprefix("gate_weight_"): value
        for key, value in summary.items()
        if key.startswith("gate_weight_")
    }
    component_keys = [
        "gate_hidden_bits",
        "gate_activation",
        "gate_dropout",
        "gate_temperature",
        "pairwise_pooling",
        "spn_token_dim",
        "spn_mixer_depth",
        "spn_token_mlp_ratio",
        "expert_activation",
        "expert_norm",
        "spn_pooling",
        "expert_dropout",
    ]
    return {
        "gate_mode": summary["gate_mode"],
        "expert_set": summary.get("expert_set", "legacy"),
        "gate_weights_mean": gate_weights,
        "moe_components": {key: summary[key] for key in component_keys if key in summary},
    }


def _cipher_profile(cipher_key: str) -> CipherProfile:
    mapping = {
        "speck32": CipherProfile.speck32_64,
        "present80": CipherProfile.present80,
        "sm4": CipherProfile.sm4,
    }
    try:
        return mapping[cipher_key]()
    except KeyError as exc:
        raise ValueError(f"unsupported cipher key for structure features: {cipher_key}") from exc


if __name__ == "__main__":
    main()
