import pytest
import torch

from blockcipher_ai_eval.models.common.components import (
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
