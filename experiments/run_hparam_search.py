from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.datasets import DifferentialDatasetConfig, make_differential_dataset
from blockcipher_ai_eval.experiments import build_cipher, build_model, default_difference
from blockcipher_ai_eval.hpo import select_trials
from blockcipher_ai_eval.training import TrainingConfig, train_binary_classifier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run lightweight hyperparameter search trials.")
    parser.add_argument("--space", required=True, help="JSON search-space file.")
    parser.add_argument("--mode", choices=["grid", "random"], default="random")
    parser.add_argument("--max-trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
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
            print(
                "[{index}/{total}] trial={trial} cipher={cipher} model={model} score={score:.6f}".format(
                    index=trial_id + 1,
                    total=len(trials),
                    trial=trial_id,
                    cipher=row["cipher"],
                    model=row["config"]["model"],
                    score=row["metrics"]["calibrated_accuracy"],
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
        return value.strip('"\'')


def _run_trial(trial_id: int, config: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    cipher_key = str(config.get("cipher", "present80"))
    model_key = str(config.get("model", "spn_nibble_conv_pairset"))
    rounds = int(config.get("rounds", 1))
    pairs_per_sample = int(config.get("pairs_per_sample", 1))
    seed = int(config.get("seed", args.seed + trial_id))
    feature_encoding = str(config.get("feature_encoding", args.feature_encoding))
    samples_per_class = int(config.get("samples_per_class", args.samples_per_class))
    cipher = build_cipher(cipher_key, rounds)
    input_difference = int(config.get("input_difference", default_difference(cipher_key)))
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
        "input_bits": int(train_dataset.features.shape[1]),
        "pair_bits": int(pair_bits),
        "config": config,
        "model_options": model_options,
        "metrics": result.final_metrics,
        "history": result.history,
        "training": result.metadata,
    }



def _model_options_from_config(config: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "activation",
        "norm",
        "pooling",
        "nibble_embed_dim",
        "conv_depth",
        "kernel_size",
        "dropout",
    }
    return {key: config[key] for key in keys if key in config}


if __name__ == "__main__":
    main()
