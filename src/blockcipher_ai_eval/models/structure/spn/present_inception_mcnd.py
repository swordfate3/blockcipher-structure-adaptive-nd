from __future__ import annotations

import torch
from torch import nn

from blockcipher_ai_eval.models.common.components import build_activation, build_norm


def _conv_norm(name: str, channels: int) -> nn.Module:
    key = name.lower()
    if key in {"batchnorm1d", "batchnorm"}:
        return nn.BatchNorm1d(channels)
    if key in {"none", "identity"}:
        return nn.Identity()
    raise ValueError(f"unsupported convolution norm: {name}")


class PresentInceptionMCNDBlock(nn.Module):
    """Inception-style residual block over a set of PRESENT ciphertext pairs."""

    def __init__(
        self,
        channels: int,
        branch_channels: int,
        activation: str = "gelu",
        norm: str = "batchnorm1d",
        dropout: float = 0.0,
        kernel_sizes: tuple[int, ...] = (1, 3, 5),
    ) -> None:
        super().__init__()
        if branch_channels < 1:
            raise ValueError("branch_channels must be >= 1")
        if not kernel_sizes:
            raise ValueError("kernel_sizes must not be empty")
        conv_branches = [
            nn.Sequential(
                nn.Conv1d(channels, branch_channels, kernel_size=kernel_size, padding="same"),
                _conv_norm(norm, branch_channels),
                build_activation(activation),
            )
            for kernel_size in kernel_sizes
        ]
        self.branches = nn.ModuleList(
            [
                *conv_branches,
                nn.Sequential(
                    nn.MaxPool1d(kernel_size=3, stride=1, padding=1),
                    nn.Conv1d(channels, branch_channels, kernel_size=1),
                    _conv_norm(norm, branch_channels),
                    build_activation(activation),
                ),
            ]
        )
        out_channels = branch_channels * len(self.branches)
        self.projection = nn.Conv1d(out_channels, channels, kernel_size=1)
        self.norm = _conv_norm(norm, channels)
        self.activation = build_activation(activation)
        self.dropout = nn.Dropout(dropout)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        hidden = torch.cat([branch(features) for branch in self.branches], dim=1)
        hidden = self.projection(hidden)
        hidden = self.dropout(hidden)
        return self.activation(self.norm(features + hidden))


class PresentInceptionMCNDDistinguisher(nn.Module):
    """PRESENT-oriented multi-ciphertext neural distinguisher baseline.

    The model is designed for MCND-style inputs where each sample concatenates
    m ciphertext-pair feature vectors.  For PRESENT raw pair inputs, pair_bits is
    typically 128 bits (C0 || C1).  For xor/aligned inputs, pair_bits can be 64 or
    another project-defined width.
    """

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 128,
        base_channels: int = 32,
        branches: int | None = None,
        blocks: int = 3,
        activation: str = "gelu",
        norm: str = "batchnorm1d",
        pooling: str = "attention_mean_max",
        dropout: float = 0.0,
        kernel_sizes: tuple[int, ...] = (1, 3, 5),
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("PresentInceptionMCND input_bits must be a multiple of pair_bits")
        if pair_bits < 1:
            raise ValueError("pair_bits must be >= 1")
        if blocks < 1:
            raise ValueError("blocks must be >= 1")
        if pooling not in {"attention", "attention_mean_max", "mean_max"}:
            raise ValueError(f"unsupported pooling: {pooling}")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.structure = "SPN"
        self.base_channels = base_channels
        self.branch_channels = branches or max(4, base_channels // 4)
        self.blocks = blocks
        self.activation = activation
        self.norm = norm
        self.pooling = pooling
        self.dropout = dropout
        self.kernel_sizes = tuple(kernel_sizes)

        self.pair_bit_encoder = nn.Sequential(
            nn.Conv1d(1, base_channels, kernel_size=7, padding=3),
            _conv_norm(norm, base_channels),
            build_activation(activation),
            nn.Dropout(dropout),
        )
        self.inception_blocks = nn.Sequential(
            *[
                PresentInceptionMCNDBlock(
                    base_channels,
                    branch_channels=self.branch_channels,
                    activation=activation,
                    norm=norm,
                    dropout=dropout,
                    kernel_sizes=self.kernel_sizes,
                )
                for _ in range(blocks)
            ]
        )
        self.pair_projection = nn.Sequential(
            nn.Linear(base_channels * 3, max(64, base_channels * 4)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 4), max(32, base_channels * 2)),
            build_activation(activation),
        )
        self.pair_embedding_bits = max(32, base_channels * 2)
        self.attention = nn.Sequential(
            build_norm("layernorm", self.pair_embedding_bits),
            nn.Linear(self.pair_embedding_bits, max(16, base_channels)),
            build_activation(activation),
            nn.Linear(max(16, base_channels), 1),
        )
        pooling_multiplier = 3 if pooling == "attention_mean_max" else 2 if pooling == "mean_max" else 1
        self.classifier = nn.Sequential(
            build_norm("layernorm", self.pair_embedding_bits * pooling_multiplier),
            nn.Linear(self.pair_embedding_bits * pooling_multiplier, max(64, base_channels * 4)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 4), max(32, base_channels * 2)),
            build_activation(activation),
            nn.Linear(max(32, base_channels * 2), 1),
        )
        self.last_attention_weights: torch.Tensor | None = None

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _encode_pairs(self, pair_features: torch.Tensor) -> torch.Tensor:
        hidden = pair_features.unsqueeze(1).float()
        hidden = self.pair_bit_encoder(hidden)
        hidden = self.inception_blocks(hidden)
        mean_embedding = hidden.mean(dim=2)
        max_embedding = hidden.max(dim=2).values
        edge_embedding = hidden[:, :, -1] - hidden[:, :, 0]
        return self.pair_projection(torch.cat([mean_embedding, max_embedding, edge_embedding], dim=1))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.reshape(features.shape[0] * self.pairs_per_sample, self.pair_bits)
        pair_embeddings = self._encode_pairs(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.pair_embedding_bits,
        )
        attention_logits = self.attention(pair_embeddings).squeeze(-1)
        attention_weights = torch.softmax(attention_logits, dim=1)
        self.last_attention_weights = attention_weights.detach()
        attention_embedding = torch.sum(pair_embeddings * attention_weights.unsqueeze(-1), dim=1)
        if self.pooling == "attention":
            pooled = attention_embedding
        elif self.pooling == "mean_max":
            pooled = torch.cat([pair_embeddings.mean(dim=1), pair_embeddings.max(dim=1).values], dim=1)
        else:
            pooled = torch.cat(
                [
                    attention_embedding,
                    pair_embeddings.mean(dim=1),
                    pair_embeddings.max(dim=1).values,
                ],
                dim=1,
            )
        return self.classifier(pooled)


def _matrix_kernel_size(value: int | tuple[int, int] | list[int]) -> tuple[int, int]:
    if isinstance(value, int):
        return (1, value)
    if len(value) != 2:
        raise ValueError("matrix kernel sizes must be ints or [height, width] pairs")
    return (int(value[0]), int(value[1]))


class PresentInceptionMCNDMatrixBlock(nn.Module):
    """2D Inception residual block over PRESENT MCND cell matrices."""

    def __init__(
        self,
        channels: int,
        branch_channels: int,
        activation: str = "gelu",
        norm: str = "batchnorm2d",
        dropout: float = 0.0,
        kernel_sizes: tuple[tuple[int, int], ...] = ((1, 1), (1, 2), (2, 4)),
    ) -> None:
        super().__init__()
        if branch_channels < 1:
            raise ValueError("branch_channels must be >= 1")
        self.branches = nn.ModuleList()
        for kernel_size in kernel_sizes:
            padding = (kernel_size[0] // 2, kernel_size[1] // 2)
            self.branches.append(
                nn.Sequential(
                    nn.Conv2d(channels, branch_channels, kernel_size=kernel_size, padding=padding),
                    nn.BatchNorm2d(branch_channels) if norm.lower() not in {"none", "identity"} else nn.Identity(),
                    build_activation(activation),
                )
            )
        self.branches.append(
            nn.Sequential(
                nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
                nn.Conv2d(channels, branch_channels, kernel_size=1),
                nn.BatchNorm2d(branch_channels) if norm.lower() not in {"none", "identity"} else nn.Identity(),
                build_activation(activation),
            )
        )
        self.projection = nn.Conv2d(branch_channels * len(self.branches), channels, kernel_size=1)
        self.norm = nn.BatchNorm2d(channels) if norm.lower() not in {"none", "identity"} else nn.Identity()
        self.activation = build_activation(activation)
        self.dropout = nn.Dropout2d(dropout)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        target_height, target_width = features.shape[-2:]
        branch_outputs = []
        for branch in self.branches:
            branch_output = branch(features)
            branch_outputs.append(branch_output[..., :target_height, :target_width])
        hidden = torch.cat(branch_outputs, dim=1)
        hidden = self.projection(hidden)
        hidden = self.dropout(hidden)
        return self.activation(self.norm(features + hidden))


class PresentInceptionMCNDMatrixDistinguisher(nn.Module):
    """Zhang/Wang-style PRESENT MCND model over m x 4 x 32 cell matrices."""

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 128,
        base_channels: int = 32,
        branches: int | None = None,
        blocks: int = 3,
        activation: str = "gelu",
        norm: str = "batchnorm2d",
        pooling: str = "attention_mean_max",
        dropout: float = 0.0,
        kernel_sizes: tuple[tuple[int, int], ...] = ((1, 1), (1, 2), (2, 4)),
        cell_bits: int = 4,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("PresentInceptionMCNDMatrix input_bits must be a multiple of pair_bits")
        if pair_bits % cell_bits != 0:
            raise ValueError("pair_bits must be divisible by cell_bits")
        if pooling not in {"attention", "attention_mean_max", "mean_max"}:
            raise ValueError(f"unsupported pooling: {pooling}")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.cell_bits = cell_bits
        self.cell_width = pair_bits // cell_bits
        self.structure = "SPN"
        self.base_channels = base_channels
        self.branch_channels = branches or max(4, base_channels // 4)
        self.blocks = blocks
        self.activation = activation
        self.norm = norm
        self.pooling = pooling
        self.dropout = dropout
        self.kernel_sizes = tuple(kernel_sizes)

        self.stem = nn.Sequential(
            nn.Conv2d(1, base_channels, kernel_size=(2, 3), padding=(1, 1)),
            nn.BatchNorm2d(base_channels) if norm.lower() not in {"none", "identity"} else nn.Identity(),
            build_activation(activation),
            nn.Dropout2d(dropout),
        )
        self.blocks_layer = nn.Sequential(
            *[
                PresentInceptionMCNDMatrixBlock(
                    base_channels,
                    branch_channels=self.branch_channels,
                    activation=activation,
                    norm=norm,
                    dropout=dropout,
                    kernel_sizes=self.kernel_sizes,
                )
                for _ in range(blocks)
            ]
        )
        self.pair_embedding_bits = max(32, base_channels * 2)
        self.pair_projection = nn.Sequential(
            nn.Linear(base_channels * 3, max(64, base_channels * 4)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 4), self.pair_embedding_bits),
            build_activation(activation),
        )
        self.attention = nn.Sequential(
            build_norm("layernorm", self.pair_embedding_bits),
            nn.Linear(self.pair_embedding_bits, max(16, base_channels)),
            build_activation(activation),
            nn.Linear(max(16, base_channels), 1),
        )
        pooling_multiplier = 3 if pooling == "attention_mean_max" else 2 if pooling == "mean_max" else 1
        self.classifier = nn.Sequential(
            build_norm("layernorm", self.pair_embedding_bits * pooling_multiplier),
            nn.Linear(self.pair_embedding_bits * pooling_multiplier, max(64, base_channels * 4)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 4), max(32, base_channels * 2)),
            build_activation(activation),
            nn.Linear(max(32, base_channels * 2), 1),
        )
        self.last_attention_weights: torch.Tensor | None = None

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def _encode_pair_matrices(self, pair_features: torch.Tensor) -> torch.Tensor:
        matrices = pair_features.float().reshape(pair_features.shape[0], 1, self.cell_bits, self.cell_width)
        hidden = self.stem(matrices)
        hidden = self.blocks_layer(hidden)
        mean_embedding = hidden.mean(dim=(2, 3))
        max_embedding = hidden.amax(dim=(2, 3))
        width_edge = hidden[:, :, :, -1].mean(dim=2) - hidden[:, :, :, 0].mean(dim=2)
        return self.pair_projection(torch.cat([mean_embedding, max_embedding, width_edge], dim=1))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        pair_features = features.reshape(features.shape[0] * self.pairs_per_sample, self.pair_bits)
        pair_embeddings = self._encode_pair_matrices(pair_features).reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.pair_embedding_bits,
        )
        attention_logits = self.attention(pair_embeddings).squeeze(-1)
        attention_weights = torch.softmax(attention_logits, dim=1)
        self.last_attention_weights = attention_weights.detach()
        attention_embedding = torch.sum(pair_embeddings * attention_weights.unsqueeze(-1), dim=1)
        if self.pooling == "attention":
            pooled = attention_embedding
        elif self.pooling == "mean_max":
            pooled = torch.cat([pair_embeddings.mean(dim=1), pair_embeddings.max(dim=1).values], dim=1)
        else:
            pooled = torch.cat(
                [
                    attention_embedding,
                    pair_embeddings.mean(dim=1),
                    pair_embeddings.max(dim=1).values,
                ],
                dim=1,
            )
        return self.classifier(pooled)


class PresentInceptionMCNDGlobalMatrixDistinguisher(nn.Module):
    """Protocol-reproduction PRESENT MCND model over the full m x cell matrix.

    Unlike PresentInceptionMCNDMatrixDistinguisher, this model keeps all m
    ciphertext pairs in one 2D convolutional field so kernels can learn across
    the group dimension before global pooling, closer to the Zhang/Wang MCND
    input module.
    """

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 128,
        base_channels: int = 32,
        branches: int | None = None,
        blocks: int = 3,
        activation: str = "gelu",
        norm: str = "batchnorm2d",
        dropout: float = 0.0,
        kernel_sizes: tuple[tuple[int, int], ...] = ((1, 1), (1, 2), (2, 4)),
        cell_bits: int = 4,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("PresentInceptionMCNDGlobalMatrix input_bits must be a multiple of pair_bits")
        if pair_bits % cell_bits != 0:
            raise ValueError("pair_bits must be divisible by cell_bits")
        if blocks < 1:
            raise ValueError("blocks must be >= 1")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.cell_bits = cell_bits
        self.cell_width = pair_bits // cell_bits
        self.structure = "SPN"
        self.base_channels = base_channels
        self.branch_channels = branches or max(4, base_channels // 4)
        self.blocks = blocks
        self.activation = activation
        self.norm = norm
        self.dropout = dropout
        self.kernel_sizes = tuple(kernel_sizes)

        self.stem = nn.Sequential(
            nn.Conv2d(1, base_channels, kernel_size=(1, 3), padding=(0, 1)),
            nn.BatchNorm2d(base_channels) if norm.lower() not in {"none", "identity"} else nn.Identity(),
            build_activation(activation),
            nn.Dropout2d(dropout),
        )
        self.blocks_layer = nn.Sequential(
            *[
                PresentInceptionMCNDMatrixBlock(
                    base_channels,
                    branch_channels=self.branch_channels,
                    activation=activation,
                    norm=norm,
                    dropout=dropout,
                    kernel_sizes=self.kernel_sizes,
                )
                for _ in range(blocks)
            ]
        )
        self.classifier = nn.Sequential(
            nn.Linear(base_channels * 3, max(64, base_channels * 4)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 4), max(32, base_channels * 2)),
            build_activation(activation),
            nn.Linear(max(32, base_channels * 2), 1),
        )

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        matrices = features.float().reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.cell_bits,
            self.cell_width,
        )
        global_matrix = matrices.permute(0, 2, 1, 3).reshape(
            features.shape[0],
            1,
            self.cell_bits,
            self.pairs_per_sample * self.cell_width,
        )
        hidden = self.stem(global_matrix)
        hidden = self.blocks_layer(hidden)
        mean_embedding = hidden.mean(dim=(2, 3))
        max_embedding = hidden.amax(dim=(2, 3))
        width_edge = hidden[:, :, :, -1].mean(dim=2) - hidden[:, :, :, 0].mean(dim=2)
        return self.classifier(torch.cat([mean_embedding, max_embedding, width_edge], dim=1))

class PresentInceptionMCNDPairStackMatrixDistinguisher(nn.Module):
    """PRESENT MCND model over a pair-stacked m*cell_bits x cell_width matrix.

    The Zhang/Wang input module treats MCND samples as an m-by-omega matrix-like
    object.  This variant keeps the pair dimension as a spatial axis instead of
    flattening all pairs into one long row, letting 2D kernels span neighboring
    pair rows and local PRESENT cell columns before global pooling.
    """

    def __init__(
        self,
        input_bits: int,
        pair_bits: int = 128,
        base_channels: int = 32,
        branches: int | None = None,
        blocks: int = 3,
        activation: str = "gelu",
        norm: str = "batchnorm2d",
        dropout: float = 0.0,
        kernel_sizes: tuple[tuple[int, int], ...] = ((1, 1), (1, 2), (2, 4), (4, 4)),
        cell_bits: int = 4,
    ) -> None:
        super().__init__()
        if input_bits % pair_bits != 0:
            raise ValueError("PresentInceptionMCNDPairStackMatrix input_bits must be a multiple of pair_bits")
        if pair_bits % cell_bits != 0:
            raise ValueError("pair_bits must be divisible by cell_bits")
        if blocks < 1:
            raise ValueError("blocks must be >= 1")
        self.input_bits = input_bits
        self.pair_bits = pair_bits
        self.pairs_per_sample = input_bits // pair_bits
        self.cell_bits = cell_bits
        self.cell_width = pair_bits // cell_bits
        self.matrix_height = self.pairs_per_sample * cell_bits
        self.structure = "SPN"
        self.base_channels = base_channels
        self.branch_channels = branches or max(4, base_channels // 4)
        self.blocks = blocks
        self.activation = activation
        self.norm = norm
        self.dropout = dropout
        self.kernel_sizes = tuple(kernel_sizes)

        self.stem = nn.Sequential(
            nn.Conv2d(1, base_channels, kernel_size=(3, 3), padding=(1, 1)),
            nn.BatchNorm2d(base_channels) if norm.lower() not in {"none", "identity"} else nn.Identity(),
            build_activation(activation),
            nn.Dropout2d(dropout),
        )
        self.blocks_layer = nn.Sequential(
            *[
                PresentInceptionMCNDMatrixBlock(
                    base_channels,
                    branch_channels=self.branch_channels,
                    activation=activation,
                    norm=norm,
                    dropout=dropout,
                    kernel_sizes=self.kernel_sizes,
                )
                for _ in range(blocks)
            ]
        )
        self.classifier = nn.Sequential(
            nn.Linear(base_channels * 4, max(64, base_channels * 4)),
            build_activation(activation),
            nn.Dropout(dropout),
            nn.Linear(max(64, base_channels * 4), max(32, base_channels * 2)),
            build_activation(activation),
            nn.Linear(max(32, base_channels * 2), 1),
        )

    def set_cipher_structure(self, structure: str) -> None:
        return None

    def set_structure_features(self, features: torch.Tensor) -> None:
        return None

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        if features.ndim != 2 or features.shape[1] != self.input_bits:
            raise ValueError(f"expected {self.input_bits} input bits, got {tuple(features.shape)}")
        matrices = features.float().reshape(
            features.shape[0],
            self.pairs_per_sample,
            self.cell_bits,
            self.cell_width,
        )
        pair_stack = matrices.reshape(features.shape[0], 1, self.matrix_height, self.cell_width)
        hidden = self.stem(pair_stack)
        hidden = self.blocks_layer(hidden)
        mean_embedding = hidden.mean(dim=(2, 3))
        max_embedding = hidden.amax(dim=(2, 3))
        height_edge = hidden[:, :, -1, :].mean(dim=2) - hidden[:, :, 0, :].mean(dim=2)
        width_edge = hidden[:, :, :, -1].mean(dim=2) - hidden[:, :, :, 0].mean(dim=2)
        return self.classifier(torch.cat([mean_embedding, max_embedding, height_edge, width_edge], dim=1))

