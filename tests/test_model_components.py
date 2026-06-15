import pytest
import torch

from blockcipher_ai_eval.models.common.components import (
    EvidencePooling,
    GatedAttentionPooling,
    build_activation,
    build_norm,
)


@pytest.mark.parametrize("name", ["relu", "gelu", "silu", "mish"])
def test_build_activation_returns_named_activation(name: str):
    activation = build_activation(name)
    output = activation(torch.zeros(2, 3))

    assert output.shape == (2, 3)


def test_build_norm_supports_layernorm_rmsnorm_and_identity():
    batch = torch.zeros(2, 5, 8)

    assert build_norm("layernorm", 8)(batch).shape == (2, 5, 8)
    assert build_norm("rmsnorm", 8)(batch).shape == (2, 5, 8)
    assert build_norm("none", 8)(batch).shape == (2, 5, 8)


def test_gated_attention_pooling_returns_weighted_embedding_and_weights():
    pooling = GatedAttentionPooling(embedding_bits=8, hidden_bits=4)
    embeddings = torch.zeros(3, 5, 8)

    pooled, weights = pooling(embeddings)

    assert pooled.shape == (3, 8)
    assert weights.shape == (3, 5)
    assert torch.allclose(weights.sum(dim=1), torch.ones(3), atol=1e-5)


@pytest.mark.parametrize("mode", ["topk_mean", "logsumexp", "topk_logsumexp"])
def test_evidence_pooling_returns_weighted_embedding_and_weights(mode: str):
    pooling = EvidencePooling(embedding_bits=8, hidden_bits=4, mode=mode, top_k=2)
    embeddings = torch.randn(3, 5, 8)

    pooled, weights = pooling(embeddings)

    assert pooled.shape == (3, 8)
    assert weights.shape == (3, 5)
    assert torch.allclose(weights.sum(dim=1), torch.ones(3), atol=1e-5)
    if mode.startswith("topk"):
        assert torch.count_nonzero(weights, dim=1).tolist() == [2, 2, 2]


def test_evidence_pooling_rejects_invalid_options():
    with pytest.raises(ValueError, match="unsupported evidence pooling mode"):
        EvidencePooling(embedding_bits=8, mode="median")
    with pytest.raises(ValueError, match="top_k"):
        EvidencePooling(embedding_bits=8, top_k=0)
    with pytest.raises(ValueError, match="lse_temperature"):
        EvidencePooling(embedding_bits=8, lse_temperature=0.0)
