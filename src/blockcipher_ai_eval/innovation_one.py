from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CipherProfile:
    """Structure-level description used by the architecture matcher."""

    name: str
    structure: str
    block_bits: int
    key_bits: int
    traits: tuple[str, ...]

    @staticmethod
    def speck32_64() -> "CipherProfile":
        return CipherProfile(
            name="SPECK32/64",
            structure="ARX",
            block_bits=32,
            key_bits=64,
            traits=(
                "modular_addition",
                "xor",
                "rotation",
                "carry_propagation",
                "word_parallelism",
            ),
        )

    @staticmethod
    def present80() -> "CipherProfile":
        return CipherProfile(
            name="PRESENT-80",
            structure="SPN",
            block_bits=64,
            key_bits=80,
            traits=(
                "sbox_layer",
                "permutation_layer",
                "sbox_locality",
                "bit_permutation",
                "lightweight_spn",
            ),
        )

    @staticmethod
    def sm4() -> "CipherProfile":
        return CipherProfile(
            name="SM4",
            structure="Feistel-like",
            block_bits=128,
            key_bits=128,
            traits=(
                "unbalanced_round_update",
                "sbox_layer",
                "linear_diffusion",
                "word_parallelism",
                "round_recurrence",
            ),
        )


@dataclass(frozen=True)
class NetworkProfile:
    """Candidate neural architecture and the cipher traits it can exploit."""

    name: str
    family: str
    strengths: tuple[str, ...]
    compute_cost: str
    notes: str

    @staticmethod
    def default_candidates() -> list["NetworkProfile"]:
        return [
            NetworkProfile(
                name="ResNet-BitSlice",
                family="residual_cnn",
                strengths=(
                    "modular_addition",
                    "xor",
                    "rotation",
                    "carry_propagation",
                    "word_parallelism",
                    "deep_feature_reuse",
                ),
                compute_cost="medium",
                notes="Gohr-style residual convolutional distinguisher baseline for ARX ciphers.",
            ),
            NetworkProfile(
                name="DBitNet-DilatedCNN",
                family="dilated_cnn",
                strengths=(
                    "bit_permutation",
                    "sbox_locality",
                    "linear_diffusion",
                    "cipher_agnostic_input",
                    "wide_receptive_field",
                ),
                compute_cost="medium",
                notes="Cipher-agnostic dilated convolution baseline for unified comparisons.",
            ),
            NetworkProfile(
                name="CNN-SBoxLocal",
                family="cnn",
                strengths=(
                    "sbox_layer",
                    "sbox_locality",
                    "permutation_layer",
                    "local_nonlinearity",
                    "lightweight_spn",
                ),
                compute_cost="low",
                notes="Compact convolutional baseline for local S-box and permutation patterns.",
            ),
            NetworkProfile(
                name="RNN-LSTM-RoundSeq",
                family="sequence",
                strengths=(
                    "round_recurrence",
                    "unbalanced_round_update",
                    "iterative_dependency",
                    "state_transition",
                ),
                compute_cost="medium",
                notes="Sequence model for round-wise traces and Feistel-like state updates.",
            ),
            NetworkProfile(
                name="Transformer-Encoder",
                family="attention",
                strengths=(
                    "global_dependency",
                    "long_range_diffusion",
                    "state_transition",
                    "wide_receptive_field",
                ),
                compute_cost="high",
                notes="High-cost global attention baseline; useful as an ablation rather than first choice.",
            ),
            NetworkProfile(
                name="MLP-Baseline",
                family="mlp",
                strengths=("dense_mixing", "control_baseline"),
                compute_cost="low",
                notes="Simple fully connected baseline for checking whether structure-aware models matter.",
            ),
        ]


@dataclass(frozen=True)
class RankedArchitecture:
    name: str
    family: str
    score: int
    compute_cost: str
    evidence: tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class ExperimentPlan:
    ciphers: list[CipherProfile]
    networks: list[NetworkProfile]
    rounds: list[int]
    seeds: list[int]
    samples_per_class: int


TRAIT_EVIDENCE = {
    "modular_addition": "modular addition carry propagation",
    "carry_propagation": "modular addition carry propagation",
    "xor": "xor and rotation feature mixing",
    "rotation": "xor and rotation feature mixing",
    "word_parallelism": "word-level parallel feature reuse",
    "sbox_layer": "sbox locality",
    "sbox_locality": "sbox locality",
    "permutation_layer": "permutation-layer local-to-global diffusion",
    "bit_permutation": "permutation-layer local-to-global diffusion",
    "linear_diffusion": "linear diffusion across state words",
    "round_recurrence": "round-wise recurrent dependency",
    "unbalanced_round_update": "Feistel-like unbalanced state update",
    "state_transition": "explicit state-transition modelling",
    "wide_receptive_field": "wide receptive field for multi-round diffusion",
}

COMPUTE_PENALTY = {"low": 0, "medium": 1, "high": 3}


def rank_architectures(
    cipher: CipherProfile, networks: Iterable[NetworkProfile]
) -> list[RankedArchitecture]:
    """Rank networks by structure-trait overlap with a small cost penalty."""

    ranked = []
    cipher_traits = set(cipher.traits)
    for network in networks:
        matched = cipher_traits.intersection(network.strengths)
        evidence = tuple(
            dict.fromkeys(TRAIT_EVIDENCE.get(trait, trait) for trait in sorted(matched))
        )
        score = 3 * len(matched) - COMPUTE_PENALTY[network.compute_cost]
        ranked.append(
            RankedArchitecture(
                name=network.name,
                family=network.family,
                score=score,
                compute_cost=network.compute_cost,
                evidence=evidence,
                notes=network.notes,
            )
        )
    return sorted(ranked, key=lambda item: (-item.score, item.compute_cost, item.name))


def build_experiment_matrix(plan: ExperimentPlan) -> list[dict[str, int | str]]:
    """Create the crossed experiment grid for reproducible architecture matching."""

    rows: list[dict[str, int | str]] = []
    for cipher in plan.ciphers:
        for network in plan.networks:
            for rounds in plan.rounds:
                for seed in plan.seeds:
                    rows.append(
                        {
                            "cipher": cipher.name,
                            "structure": cipher.structure,
                            "network": network.name,
                            "rounds": rounds,
                            "seed": seed,
                            "samples_per_class": plan.samples_per_class,
                        }
                    )
    return rows


def summarize_recommendation(
    cipher: CipherProfile, ranked: list[RankedArchitecture]
) -> str:
    """Return a thesis-ready sentence for the top architecture candidates."""

    top = ranked[0]
    runner_up = ", ".join(item.name for item in ranked[1:]) or "no runner-up"
    evidence = "; ".join(top.evidence) if top.evidence else "control-baseline behavior"
    return (
        f"For {cipher.name} ({cipher.structure}), {top.name} is the first candidate "
        f"for empirical architecture matching because it aligns with {evidence}. "
        f"Secondary candidates for ablation are {runner_up}."
    )
