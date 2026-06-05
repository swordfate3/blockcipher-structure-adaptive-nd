# SPN PairSet DBitNet v2 PRESENT Analysis - 2026-06-05

## Run

```text
run_id: innovation1-spn-pairset-v2-present-gpu1-20260605
result_dir: outputs/remote_results/innovation1-spn-pairset-v2-present-gpu1-20260605
cipher: PRESENT-80
structure: SPN
rounds: 4, 5
seeds: 0, 1
pairs_per_sample: 1, 2, 4
samples_per_class: 32768
epochs: 10
batch_size: 1024
hidden_bits: 64
optimizer: AdamW
weight_decay: 0.0001
device: cuda:1
expected_rows: 48
```

Completeness gate:

```text
result_lines=48
expected_rows=48
train_stderr=0 bytes
summary_stderr=0 bytes
```

## Compared Models

- `adaptive_dbitnet_pairwise`
- `structure_adaptive_pairset_dbitnet`
- `spn_pairset_dbitnet_v2`
- `moe_v4_soft`

`spn_pairset_dbitnet_v2` adds an explicit 4-bit cell encoder to the structure-conditioned DBitNet pair encoder, then aggregates pair embeddings with attention, mean, and max pooling.

## Aggregate Result

Mean calibrated accuracy over PRESENT r4/r5 and pairs 1/2/4:

```text
moe_v4_soft                    0.795647
adaptive_dbitnet_pairwise      0.789121
structure_adaptive_pairset     0.727336
spn_pairset_dbitnet_v2         0.725334
```

Best-by-task counts:

```text
moe_v4_soft                5 / 6
adaptive_dbitnet_pairwise  1 / 6
spn_pairset_dbitnet_v2     0 / 6
```

## Interpretation

The v2 SPN cell prior did not improve PRESENT under this protocol.  The explicit 4-bit cell encoder is not enough because it pools the cell sequence too early with mean/max statistics.  PRESENT's S-box layer and bit permutation make the relative position and propagation path of nibbles important; early global pooling removes that information before the classifier can use it.

This is a useful negative ablation.  It supports the innovation-one thesis that structure adaptation must match the actual propagation mechanism of the cipher, not merely add a structure label or a coarse cell mask.

## Decision

Do not continue scaling `spn_pairset_dbitnet_v2` as the main SPN model.

Next SPN expert:

```text
spn_nibble_conv_pairset
```

Design intent:

```text
pair bits -> 4-bit nibble sequence -> residual 1D conv over nibble positions
-> pair embedding -> attention/mean/max pair-set aggregation -> classifier
```

This keeps nibble order before pair pooling and is a better fit for PRESENT/GIFT/RECTANGLE-like SPN structures.

## Next Experiment

Run a PRESENT r4/r5 comparison using the same protocol:

```text
adaptive_dbitnet_pairwise
structure_adaptive_pairset_dbitnet
spn_pairset_dbitnet_v2
spn_nibble_conv_pairset
moe_v4_soft
```

Before the full comparison, run a small HPO search on `spn_nibble_conv_pairset` to select activation, norm, pooling, learning rate, and weight decay using validation metrics only.
