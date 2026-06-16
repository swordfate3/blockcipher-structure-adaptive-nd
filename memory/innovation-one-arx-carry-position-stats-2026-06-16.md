# Innovation 1 ARX Carry-Position Stats - 2026-06-16

## Why This Was Added

ARX/SPECK32 remains a parallel Innovation 1 line. Current evidence indicates the
strongest strict direction is still public, keyless SPECK partial-inverse
structure, but density-only ARX statistics may wash out the bit-position signal
that matters near r7/r8.

The new direction keeps the existing public feature encoding:

```text
ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_plus_bits
```

It does not add secret-key information. It computes statistics from ciphertext
pairs and the public SPECK round-function relations already encoded by the
feature pipeline.

## Model Added

```text
model key: arx_carry_position_stats_pairset
class: ArxCarryPositionStatsPairSetDistinguisher
file: src/blockcipher_ai_eval/models/structure/arx/carry_position_stats.py
```

The model reshapes each sample as:

```text
[batch, pairs_per_sample, feature_words_per_pair=23, side=2, word_bits=16]
```

It keeps:

```text
- per-role/per-side/per-bit mean and variance across pairs
- carrychain-plus role position mean/variance/max
- low/mid/high bit-band statistics
- carry run-length buckets: length 1, 2, 3, 4+
- SPECK-style rotation-aligned correlations for selected carry/addition roles
```

## Experiment Added

Plan:

```text
experiments/innovation1/plans/innovation1_arx_speck32_carry_position_stats_r7r8_screen.csv
```

Remote config:

```text
experiments/innovation1/configs/remote/innovation1_arx_speck32_carry_position_stats_r7r8_screen_gpu1_20260616.json
```

Generated scripts:

```text
scripts/generated/remote/run_innovation1-arx-speck32-carry-position-stats-r7r8-screen-gpu1-20260616_and_push.cmd
scripts/generated/remote/launch_innovation1-arx-speck32-carry-position-stats-r7r8-screen-gpu1-20260616.cmd
scripts/generated/remote/schedule_innovation1_arx_speck32_carry_position_stats_r7r8_screen_gpu1_20260616.cmd
scripts/generated/monitors/monitor_innovation1_arx_speck32_carry_position_stats_r7r8_screen_gpu1_results.sh
```

The plan has 8 rows:

```text
r6 seed0 sanity:
  arx_round_stats_pairset control
  arx_carry_position_stats_pairset

r7 seeds 0,1:
  arx_round_stats_pairset control
  arx_carry_position_stats_pairset

r8 seed0 boundary:
  arx_round_stats_pairset control
  arx_carry_position_stats_pairset
```

Common protocol:

```text
cipher=SPECK32/64
difference_profile=speck32_gohr2019
feature=ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_plus_bits
pairs_per_sample=4
key_rotation_interval=1024
sample_structure=independent_pairs
negative_mode=encrypted_random_plaintexts
loss=mse
checkpoint_metric=val_auc
```

## Verification

Tests:

```text
uv run pytest tests/test_adaptive_dbitnet_model.py::test_arx_carry_position_stats_pairset_preserves_bit_position_evidence tests/test_adaptive_dbitnet_model.py::test_build_model_supports_arx_carry_position_stats_pairset_key_and_options -q
-> 2 passed

uv run pytest tests/test_build_plan_config.py::test_speck32_arx_carry_position_stats_r7r8_screen_plan_shape -q
-> 1 passed

uv run pytest tests/test_adaptive_dbitnet_model.py tests/test_build_plan_config.py::test_speck32_arx_carry_position_stats_r7r8_screen_plan_shape tests/test_remote_script_generator.py -q
-> 76 passed
```

Tiny local training smoke:

```text
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models arx_carry_position_stats_pairset \
  --rounds 2 \
  --seeds 0 \
  --samples-per-class 8 \
  --pairs-per-sample 2 \
  --feature-encoding ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_plus_bits \
  --negative-mode encrypted_random_plaintexts \
  --difference-profile speck32_gohr2019 \
  --key-rotation-interval 4 \
  --sample-structure independent_pairs \
  --epochs 1 \
  --batch-size 4 \
  --hidden-bits 4 \
  --checkpoint-metric val_auc \
  --output /tmp/arx_carry_position_smoke.jsonl
```

Result:

```text
wrote 1 rows to /tmp/arx_carry_position_smoke.jsonl
```

## Remote State When Added

Remote A6000 still had these active jobs:

```text
innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616
innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616
innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
```

The strict ARX partial-inverse confirm had not started yet:

```text
innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616 -> missing
```

Do not start the carry-position stats run until the current GPU1 queue has
room, unless the user explicitly asks to reprioritize.
