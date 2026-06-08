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
    def gift64() -> "CipherProfile":
        return CipherProfile(
            name="GIFT-64",
            structure="SPN",
            block_bits=64,
            key_bits=128,
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
                name="StructureAdaptive-PairSet-DBitNet",
                family="pairset_dilated_cnn",
                strengths=(
                    "modular_addition",
                    "xor",
                    "rotation",
                    "carry_propagation",
                    "word_parallelism",
                    "sbox_layer",
                    "sbox_locality",
                    "permutation_layer",
                    "bit_permutation",
                    "linear_diffusion",
                    "unbalanced_round_update",
                    "wide_receptive_field",
                    "multi_pair_statistics",
                    "structure_conditioning",
                ),
                compute_cost="medium",
                notes="Innovation-one pair-set DBitNet with structure-conditioned dilation, bit mask priors, and attention pooling.",
            ),
            NetworkProfile(
                name="SENet-ResNeXt",
                family="se_resnext",
                strengths=(
                    "xor",
                    "rotation",
                    "bit_permutation",
                    "sbox_locality",
                    "wide_receptive_field",
                    "deep_feature_reuse",
                ),
                compute_cost="medium",
                notes="Squeeze-and-excitation grouped residual CNN for stronger long-round neural distinguishers.",
            ),
            NetworkProfile(
                name="MultiScale-DenseResNet",
                family="multiscale_dense_residual",
                strengths=(
                    "modular_addition",
                    "carry_propagation",
                    "word_parallelism",
                    "sbox_locality",
                    "wide_receptive_field",
                    "deep_feature_reuse",
                ),
                compute_cost="medium",
                notes="Multi-scale convolutional residual candidate for multi-pair and engineered data formats.",
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
class LiteratureRule:
    """Literature-derived evidence that links cipher structure to architectures."""

    source_id: str
    citation: str
    cipher_structures: tuple[str, ...]
    cipher_traits: tuple[str, ...]
    network_families: tuple[str, ...]
    network_names: tuple[str, ...]
    evidence: tuple[str, ...]
    weight: int


@dataclass(frozen=True)
class RankedArchitecture:
    name: str
    family: str
    score: int
    compute_cost: str
    evidence: tuple[str, ...]
    literature: tuple[str, ...]
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
    "multi_pair_statistics": "multi-ciphertext-pair statistical aggregation",
    "structure_conditioning": "structure-conditioned bit-interaction priors",
}

COMPUTE_PENALTY = {"low": 0, "medium": 1, "high": 3}
LITERATURE_WEIGHT_MULTIPLIER = 2
MODEL_KEYS = {
    "ResNet-BitSlice": "resnet_bitslice",
    "DBitNet-DilatedCNN": "dbitnet_dilated_cnn",
    "StructureAdaptive-PairSet-DBitNet": "structure_adaptive_pairset_dbitnet",
    "SENet-ResNeXt": "senet_resnext",
    "MultiScale-DenseResNet": "multiscale_dense_resnet",
    "CNN-SBoxLocal": "cnn",
    "RNN-LSTM-RoundSeq": "lstm_roundseq",
    "Transformer-Encoder": "transformer_encoder",
    "MLP-Baseline": "mlp",
}
LITERATURE_DIFFERENCE_PROFILES = {
    "SPECK32/64": ("speck32_gohr2019", 0),
    "PRESENT-80": ("present_wang_jain2021", 0),
    "SM4": ("sm4_yu2023_conv_resnet", 0),
}


def default_literature_rules() -> list[LiteratureRule]:
    """Return the first curated evidence rules for innovation point 1."""

    return [
        LiteratureRule(
            source_id="gohr2019_speck_resnet",
            citation="Gohr 2019 SPECK32/64 neural distinguisher",
            cipher_structures=("ARX",),
            cipher_traits=(
                "modular_addition",
                "xor",
                "rotation",
                "carry_propagation",
                "word_parallelism",
            ),
            network_families=("residual_cnn",),
            network_names=("ResNet-BitSlice",),
            evidence=(
                "Gohr-style residual bit-slice features for SPECK32/64",
                "modular addition carry propagation",
            ),
            weight=4,
        ),
        LiteratureRule(
            source_id="benamira2021_deeper_look",
            citation="Benamira et al. 2021 deeper look at machine learning cryptanalysis",
            cipher_structures=("ARX",),
            cipher_traits=("modular_addition", "carry_propagation", "word_parallelism"),
            network_families=("residual_cnn",),
            network_names=("ResNet-BitSlice",),
            evidence=("feature evidence for Gohr-style ARX distinguishers",),
            weight=2,
        ),
        LiteratureRule(
            source_id="dbitnet2023_cipher_agnostic",
            citation="DBitNet 2023 cipher-agnostic neural training pipeline",
            cipher_structures=("ARX", "SPN", "Feistel-like"),
            cipher_traits=(
                "bit_permutation",
                "sbox_locality",
                "linear_diffusion",
                "wide_receptive_field",
            ),
            network_families=("dilated_cnn",),
            network_names=("DBitNet-DilatedCNN",),
            evidence=("cipher-agnostic dilated convolution comparison baseline",),
            weight=2,
        ),
        LiteratureRule(
            source_id="innovation1_pairset_structure_dbitnet",
            citation="Innovation-one structure-adaptive pair-set DBitNet design",
            cipher_structures=("ARX", "SPN", "Feistel-like"),
            cipher_traits=(
                "modular_addition",
                "rotation",
                "sbox_locality",
                "bit_permutation",
                "linear_diffusion",
                "unbalanced_round_update",
                "wide_receptive_field",
            ),
            network_families=("pairset_dilated_cnn",),
            network_names=("StructureAdaptive-PairSet-DBitNet",),
            evidence=(
                "shared pair encoder with attention/mean/max set aggregation",
                "structure-conditioned dilation and bit-mask priors",
            ),
            weight=5,
        ),
        LiteratureRule(
            source_id="bao2022_senet_simon",
            citation="Bao et al. 2022 SENet/SE-ResNeXt Simon neural distinguisher",
            cipher_structures=("ARX", "Feistel-like"),
            cipher_traits=("xor", "rotation", "bit_permutation", "wide_receptive_field"),
            network_families=("se_resnext",),
            network_names=("SENet-ResNeXt",),
            evidence=("SENet/SE-ResNeXt evidence for longer Simon neural distinguishers",),
            weight=3,
        ),
        LiteratureRule(
            source_id="hou2025_multiscale_dense_speck_simon",
            citation="Hou et al. 2025 multi-pair multi-scale dense residual distinguisher",
            cipher_structures=("ARX", "Feistel-like"),
            cipher_traits=("modular_addition", "carry_propagation", "word_parallelism"),
            network_families=("multiscale_dense_residual",),
            network_names=("MultiScale-DenseResNet",),
            evidence=("multi-scale convolution and dense residual evidence for Speck/Simon",),
            weight=3,
        ),
        LiteratureRule(
            source_id="jain2020_present_neural",
            citation="Jain et al. 2020 PRESENT neural distinguisher",
            cipher_structures=("SPN",),
            cipher_traits=("sbox_layer", "sbox_locality", "permutation_layer"),
            network_families=("cnn",),
            network_names=("CNN-SBoxLocal",),
            evidence=("PRESENT/SPN local S-box neural distinguisher evidence",),
            weight=3,
        ),
        LiteratureRule(
            source_id="liu2026_spn_iot",
            citation="Liu et al. 2026 SPN IoT-friendly neural distinguisher framework",
            cipher_structures=("SPN",),
            cipher_traits=("lightweight_spn", "sbox_locality", "bit_permutation"),
            network_families=("cnn", "dilated_cnn"),
            network_names=("CNN-SBoxLocal", "DBitNet-DilatedCNN"),
            evidence=("SPN-specific lightweight input and architecture design",),
            weight=2,
        ),
        LiteratureRule(
            source_id="yu2023_sm4_conv_resnet",
            citation="Yu/Wu/Zhang 2023 SM4 convolutional residual network analysis",
            cipher_structures=("Feistel-like",),
            cipher_traits=("sbox_layer", "linear_diffusion", "word_parallelism"),
            network_families=("dilated_cnn", "cnn"),
            network_names=("DBitNet-DilatedCNN", "CNN-SBoxLocal"),
            evidence=("SM4 convolutional/residual analysis for Feistel-like structure",),
            weight=4,
        ),
        LiteratureRule(
            source_id="hou2020_des_deep_linear",
            citation="Hou et al. 2020 DES deep learning linear attack",
            cipher_structures=("Feistel-like",),
            cipher_traits=("round_recurrence", "unbalanced_round_update"),
            network_families=("sequence",),
            network_names=("RNN-LSTM-RoundSeq",),
            evidence=("Feistel round-wise dependency ablation for sequence models",),
            weight=1,
        ),
        LiteratureRule(
            source_id="assessment2022_sok2024_protocol",
            citation="Gohr/Leander/Neumann 2022 and SoK 2024 evaluation guidance",
            cipher_structures=("ARX", "SPN", "Feistel-like"),
            cipher_traits=(),
            network_families=("mlp", "attention"),
            network_names=("MLP-Baseline", "Transformer-Encoder"),
            evidence=("controlled baseline and high-cost ablation for comparability",),
            weight=1,
        ),
    ]


def _rule_applies_to_cipher(rule: LiteratureRule, cipher: CipherProfile) -> bool:
    structure_match = cipher.structure in rule.cipher_structures
    trait_match = bool(set(cipher.traits).intersection(rule.cipher_traits))
    return structure_match and (trait_match or not rule.cipher_traits)


def _rule_applies_to_network(rule: LiteratureRule, network: NetworkProfile) -> bool:
    return network.name in rule.network_names or network.family in rule.network_families


def recommended_model_key(architecture_name: str) -> str:
    """Map a thesis architecture label to an experiment model key."""

    try:
        return MODEL_KEYS[architecture_name]
    except KeyError as exc:
        raise ValueError(f"unsupported architecture: {architecture_name}") from exc


def recommended_difference_profile(cipher_name: str) -> tuple[str, int]:
    """Return the literature-backed input-difference profile for a cipher."""

    try:
        return LITERATURE_DIFFERENCE_PROFILES[cipher_name]
    except KeyError as exc:
        raise ValueError(f"unsupported cipher for difference profile: {cipher_name}") from exc


def rank_architectures(
    cipher: CipherProfile,
    networks: Iterable[NetworkProfile],
    literature_rules: Iterable[LiteratureRule] | None = None,
) -> list[RankedArchitecture]:
    """Rank networks by structure-trait overlap with a small cost penalty."""

    ranked = []
    rules = list(default_literature_rules() if literature_rules is None else literature_rules)
    cipher_traits = set(cipher.traits)
    for network in networks:
        matched = cipher_traits.intersection(network.strengths)
        trait_evidence = [
            TRAIT_EVIDENCE.get(trait, trait) for trait in sorted(matched)
        ]
        matched_rules = [
            rule
            for rule in rules
            if _rule_applies_to_cipher(rule, cipher)
            and _rule_applies_to_network(rule, network)
        ]
        literature_score = sum(rule.weight for rule in matched_rules)
        evidence = tuple(
            dict.fromkeys(
                [
                    *trait_evidence,
                    *(
                        evidence_item
                        for rule in matched_rules
                        for evidence_item in rule.evidence
                    ),
                ]
            )
        )
        literature = tuple(
            dict.fromkeys(rule.citation for rule in matched_rules)
        )
        score = (
            3 * len(matched)
            + LITERATURE_WEIGHT_MULTIPLIER * literature_score
            - COMPUTE_PENALTY[network.compute_cost]
        )
        ranked.append(
            RankedArchitecture(
                name=network.name,
                family=network.family,
                score=score,
                compute_cost=network.compute_cost,
                evidence=evidence,
                literature=literature,
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


def recommend_experiment_configs(
    ciphers: Iterable[CipherProfile],
    networks: Iterable[NetworkProfile],
    top_k: int,
    rounds: Iterable[int],
    seeds: Iterable[int],
    samples_per_class: int,
    literature_rules: Iterable[LiteratureRule] | None = None,
) -> list[dict[str, int | str]]:
    """Build a smaller matrix over top-ranked literature-backed candidates."""

    rows: list[dict[str, int | str]] = []
    network_list = list(networks)
    for cipher in ciphers:
        ranked = rank_architectures(
            cipher,
            network_list,
            literature_rules=literature_rules,
        )
        for architecture_rank, architecture in enumerate(ranked[:top_k], start=1):
            difference_profile, difference_member = recommended_difference_profile(
                cipher.name
            )
            for round_count in rounds:
                for seed in seeds:
                    rows.append(
                        {
                            "cipher": cipher.name,
                            "structure": cipher.structure,
                            "network": architecture.name,
                            "model_key": recommended_model_key(architecture.name),
                            "family": architecture.family,
                            "architecture_rank": architecture_rank,
                            "score": architecture.score,
                            "rounds": round_count,
                            "seed": seed,
                            "samples_per_class": samples_per_class,
                            "difference_profile": difference_profile,
                            "difference_member": difference_member,
                            "evidence": "; ".join(architecture.evidence),
                            "literature": "; ".join(architecture.literature),
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
    literature = "; ".join(top.literature) if top.literature else "the baseline rule set"
    return (
        f"For {cipher.name} ({cipher.structure}), {top.name} is the first candidate "
        f"for empirical architecture matching because it aligns with {evidence}. "
        f"Literature support: {literature}. "
        f"Secondary candidates for ablation are {runner_up}."
    )
