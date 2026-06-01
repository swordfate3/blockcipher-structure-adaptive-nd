from blockcipher_ai_eval.innovation_one import (
    CipherProfile,
    ExperimentPlan,
    NetworkProfile,
    build_experiment_matrix,
    rank_architectures,
    summarize_recommendation,
)


def test_rank_architectures_prefers_resnet_for_arx_cipher():
    cipher = CipherProfile.speck32_64()
    networks = NetworkProfile.default_candidates()

    ranked = rank_architectures(cipher, networks)

    assert ranked[0].name == "ResNet-BitSlice"
    assert ranked[0].score > ranked[-1].score
    assert "modular addition carry propagation" in ranked[0].evidence


def test_rank_architectures_prefers_cnn_or_dbitnet_for_spn_cipher():
    cipher = CipherProfile.present80()
    networks = NetworkProfile.default_candidates()

    ranked = rank_architectures(cipher, networks)
    top_names = {ranked[0].name, ranked[1].name}

    assert "DBitNet-DilatedCNN" in top_names
    assert "CNN-SBoxLocal" in top_names
    assert any("sbox locality" in item.evidence for item in ranked[:2])


def test_rank_architectures_keeps_transformer_as_high_cost_candidate():
    cipher = CipherProfile.sm4()
    networks = NetworkProfile.default_candidates()

    ranked = rank_architectures(cipher, networks)
    transformer = next(item for item in ranked if item.name == "Transformer-Encoder")

    assert transformer.compute_cost == "high"
    assert transformer.score < ranked[0].score


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


def test_summarize_recommendation_returns_thesis_ready_claim():
    cipher = CipherProfile.speck32_64()
    ranked = rank_architectures(cipher, NetworkProfile.default_candidates())

    summary = summarize_recommendation(cipher, ranked[:3])

    assert "SPECK32/64" in summary
    assert "ResNet-BitSlice" in summary
    assert "empirical architecture matching" in summary
