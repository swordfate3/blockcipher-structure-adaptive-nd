from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from blockcipher_ai_eval.innovation_one import (
    CipherProfile,
    ExperimentPlan,
    NetworkProfile,
    build_experiment_matrix,
    rank_architectures,
    summarize_recommendation,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the experiment matrix for innovation point 1."
    )
    parser.add_argument(
        "--output",
        default="outputs/innovation_one_experiment_matrix.csv",
        help="CSV path for the crossed cipher/network/round/seed matrix.",
    )
    parser.add_argument(
        "--samples-per-class",
        type=int,
        default=1048576,
        help="Number of positive and negative samples for each experiment.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        nargs="+",
        default=[3, 4, 5, 6, 7],
        help="Reduced-round settings to evaluate.",
    )
    parser.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=[0, 1, 2, 3, 4],
        help="Random seeds for repeated trials.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ciphers = [CipherProfile.speck32_64(), CipherProfile.present80(), CipherProfile.sm4()]
    networks = NetworkProfile.default_candidates()
    plan = ExperimentPlan(
        ciphers=ciphers,
        networks=networks,
        rounds=args.rounds,
        seeds=args.seeds,
        samples_per_class=args.samples_per_class,
    )

    rows = build_experiment_matrix(plan)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} experiment rows to {output}")
    for cipher in ciphers:
        ranked = rank_architectures(cipher, networks)
        print(summarize_recommendation(cipher, ranked[:3]))


if __name__ == "__main__":
    main()
