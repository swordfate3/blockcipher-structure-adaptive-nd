# Structure-Aware MoE Neural Distinguisher Design

## Goal

Build a structure-aware mixture-of-experts neural distinguisher, abbreviated SA-MoE, that fuses the existing ResNet-BitSlice, CNN-SBoxLocal, DBitNet-DilatedCNN, and MLP experts through a gate derived from block-cipher structure features.

The feature upgrades innovation one from "rank and compare architectures" to "dynamically fuse architecture experts according to cipher structure." The first implementation must stay small, reproducible, and compatible with the current single-cipher matrix runner.

## Scope

In scope:

- Add reusable structure-feature encoding from `CipherProfile`.
- Add a MoE model that accepts ciphertext-pair features and a structure feature vector.
- Add hard, uniform, and soft gate modes.
- Add tests that verify gate weights and output shape.
- Add a runner path that can train MoE models for the current single-cipher experiments.
- Record gate mode and mean gate weights in result JSON.

Out of scope for the first implementation:

- Cross-cipher mixed batches with padded inputs.
- Expert checkpoint pretraining and freezing.
- Constrained SM4 Li/Sun difference-family sampling.
- Claims of SOTA or high-round breakthrough.

## Model Design

The first SA-MoE implementation uses the current per-cipher input width. For a run over SPECK32/64, all experts receive the SPECK feature length; for PRESENT and SM4, they receive their own feature length. This avoids padding and keeps the first model compatible with existing dataset generation.

Expert set:

- `resnet_bitslice`
- `cnn`
- `dbitnet_dilated_cnn`
- `mlp`

Each expert maps the same input feature vector `x` to one logit:

```text
z_i = E_i(x)
```

The gate maps a structure vector `s` to expert weights:

```text
alpha = gate(s)
sum(alpha) = 1
alpha_i >= 0
```

The final logit is:

```text
z = sum_i alpha_i * z_i
```

## Gate Modes

### Uniform Gate

All experts receive equal weight. This is the ensemble baseline.

```text
alpha = [0.25, 0.25, 0.25, 0.25]
```

### Hard Structure Gate

Weights are derived from cipher structure:

```text
ARX          -> ResNet 0.55, DBitNet 0.30, CNN 0.10, MLP 0.05
SPN          -> CNN 0.40, DBitNet 0.45, ResNet 0.10, MLP 0.05
Feistel-like -> DBitNet 0.50, ResNet 0.30, CNN 0.15, MLP 0.05
```

The weights are intentionally not one-hot. Keeping secondary experts active makes the hard gate comparable with the soft MoE and avoids brittle behavior.

### Soft Structure Gate

A small MLP maps the structure vector to expert weights:

```text
Linear(structure_bits -> hidden_bits)
ReLU
Linear(hidden_bits -> num_experts)
Softmax
```

The soft gate is trained jointly with experts in the first version. Later work can add pretrained frozen experts.

## Structure Vector

The structure vector is generated from `CipherProfile` and includes:

```text
is_arx
is_spn
is_feistel_like
has_modular_addition
has_xor
has_rotation
has_carry_propagation
has_word_parallelism
has_sbox_layer
has_permutation_layer
has_sbox_locality
has_bit_permutation
has_lightweight_spn
has_unbalanced_round_update
has_linear_diffusion
has_round_recurrence
block_bits / 128
key_bits / 128
rounds / 32
```

The explicit vector is deliberately simple and auditable for thesis writing.

## Runner Integration

`build_model()` gains model keys:

- `moe_uniform`
- `moe_hard`
- `moe_soft`

The matrix runner already knows `cipher_key` and `rounds`; it can construct the matching `CipherProfile` and pass the structure vector into training.

Because existing models accept only `features`, the MoE model will expose:

```python
set_structure_features(structure_features: torch.Tensor) -> None
gate_summary() -> dict[str, float]
```

The training loop can remain unchanged for the first implementation. The MoE stores a per-run structure vector internally and expands it to batch size during `forward(features)`.

## Evaluation

First screening should compare:

- best single expert
- `moe_uniform`
- `moe_hard`
- `moe_soft`

Recommended small commands:

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models resnet_bitslice dbitnet_dilated_cnn moe_uniform moe_hard moe_soft \
  --rounds 5 6 \
  --seeds 0 1 \
  --samples-per-class 8192 \
  --epochs 8 \
  --batch-size 512 \
  --hidden-bits 64 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_speck_moe_screen.jsonl
```

The JSON result should include:

- `model`
- `gate_mode`
- `gate_weights_mean`
- existing metrics

## Success Criteria

The implementation is successful when:

- All existing tests still pass.
- Unit tests verify structure-vector encoding.
- Unit tests verify uniform, hard, and soft gate weights.
- CLI runner can train `moe_uniform`, `moe_hard`, and `moe_soft`.
- Result JSON includes gate metadata.

The research result is considered promising, but not proven, if:

- `moe_hard` or `moe_soft` matches the best single expert within 1-2 percentage points on calibrated accuracy.
- Gate weights align with the expected structure activation pattern.
- The MoE outperforms `moe_uniform` or a no-structure baseline in at least one cipher family.

## Risks

- Soft MoE may overfit with small samples because it trains experts and gate together.
- Uniform MoE can dilute a strong expert with weaker branches.
- Single-cipher runs make gate behavior mostly structure-prior driven; cross-cipher mixed training is needed for stronger claims.
- Different block sizes prevent immediate unified cross-cipher batches without padding or adapters.

## First Implementation Decision

Implement per-cipher SA-MoE first. It is enough to test whether expert fusion is viable under current datasets and training scripts. Cross-cipher padding and pretrained expert checkpoints should be a second design after the first MoE screen produces usable evidence.
