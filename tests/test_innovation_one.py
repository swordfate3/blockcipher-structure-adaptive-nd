from blockcipher_ai_eval.innovation_one import (
    CipherProfile,
    ExperimentPlan,
    LiteratureRule,
    NetworkProfile,
    build_experiment_matrix,
    default_literature_rules,
    rank_architectures,
    recommended_model_key,
    recommend_experiment_configs,
    summarize_recommendation,
)


def test_rank_architectures_prefers_resnet_for_arx_cipher():
    cipher = CipherProfile.speck32_64()
    networks = NetworkProfile.default_candidates()

    ranked = rank_architectures(cipher, networks)

    assert ranked[0].name == "ResNet-BitSlice"
    assert ranked[0].score > ranked[-1].score
    assert "modular addition carry propagation" in ranked[0].evidence
    assert any("Gohr 2019" in source for source in ranked[0].literature)


def test_rank_architectures_prefers_cnn_or_dbitnet_for_spn_cipher():
    cipher = CipherProfile.present80()
    networks = NetworkProfile.default_candidates()

    ranked = rank_architectures(cipher, networks)
    top_names = {ranked[0].name, ranked[1].name}

    assert "DBitNet-DilatedCNN" in top_names
    assert "CNN-SBoxLocal" in top_names
    assert any("sbox locality" in item.evidence for item in ranked[:2])
    assert any("PRESENT" in source or "SPN" in source for item in ranked[:2] for source in item.literature)


def test_rank_architectures_keeps_transformer_as_high_cost_candidate():
    cipher = CipherProfile.sm4()
    networks = NetworkProfile.default_candidates()

    ranked = rank_architectures(cipher, networks)
    transformer = next(item for item in ranked if item.name == "Transformer-Encoder")

    assert transformer.compute_cost == "high"
    assert transformer.score < ranked[0].score


def test_default_literature_rules_cover_core_cipher_structures():
    rules = default_literature_rules()

    assert any(rule.source_id == "gohr2019_speck_resnet" for rule in rules)
    assert any(rule.source_id == "dbitnet2023_cipher_agnostic" for rule in rules)
    assert any(rule.source_id == "yu2023_sm4_conv_resnet" for rule in rules)

    speck_rules = [
        rule
        for rule in rules
        if "ARX" in rule.cipher_structures and "ResNet-BitSlice" in rule.network_names
    ]
    assert speck_rules
    assert speck_rules[0].weight >= 3


def test_custom_literature_rules_can_shift_architecture_ranking():
    cipher = CipherProfile.speck32_64()
    networks = NetworkProfile.default_candidates()
    custom_rules = [
        LiteratureRule(
            source_id="ablation2026_arx_transformer",
            citation="Ablation 2026",
            cipher_structures=("ARX",),
            cipher_traits=("rotation",),
            network_families=("attention",),
            network_names=("Transformer-Encoder",),
            evidence=("global attention ablation for rotation patterns",),
            weight=12,
        )
    ]

    ranked = rank_architectures(cipher, networks, literature_rules=custom_rules)

    assert ranked[0].name == "Transformer-Encoder"
    assert "Ablation 2026" in ranked[0].literature
    assert "global attention ablation for rotation patterns" in ranked[0].evidence


def test_build_experiment_matrix_crosses_ciphers_networks_rounds_and_seeds():
    plan = ExperimentPlan(
        ciphers=[CipherProfile.speck32_64(), CipherProfile.present80()],
        networks=NetworkProfile.default_candidates()[:2],
        rounds=[3, 4],
        seeds=[0, 1],
        samples_per_class=1024,
    )

    matrix = build_experiment_matrix(plan)

    assert len(matrix) == 16
    assert matrix[0]["cipher"] == "SPECK32/64"
    assert matrix[0]["structure"] == "ARX"
    assert matrix[0]["rounds"] == 3
    assert matrix[0]["samples_per_class"] == 1024
    assert matrix[-1]["seed"] == 1


def test_recommend_experiment_configs_keeps_ranked_literature_metadata():
    configs = recommend_experiment_configs(
        ciphers=[CipherProfile.speck32_64()],
        networks=NetworkProfile.default_candidates(),
        top_k=2,
        rounds=[3],
        seeds=[0],
        samples_per_class=1024,
    )

    assert len(configs) == 2
    assert configs[0]["architecture_rank"] == 1
    assert configs[0]["network"] == "ResNet-BitSlice"
    assert "Gohr 2019" in configs[0]["literature"]
    assert "modular addition carry propagation" in configs[0]["evidence"]
    assert configs[0]["rounds"] == 3
    assert configs[0]["seed"] == 0
    assert configs[0]["model_key"] == "resnet_bitslice"


def test_recommended_model_key_maps_paper_architecture_to_runnable_model():
    assert recommended_model_key("ResNet-BitSlice") == "resnet_bitslice"
    assert recommended_model_key("CNN-SBoxLocal") == "cnn"
    assert recommended_model_key("MLP-Baseline") == "mlp"


def test_summarize_recommendation_returns_thesis_ready_claim():
    cipher = CipherProfile.speck32_64()
    ranked = rank_architectures(cipher, NetworkProfile.default_candidates())

    summary = summarize_recommendation(cipher, ranked[:3])

    assert "SPECK32/64" in summary
    assert "ResNet-BitSlice" in summary
    assert "empirical architecture matching" in summary
