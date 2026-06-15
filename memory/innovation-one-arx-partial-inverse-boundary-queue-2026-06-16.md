# Innovation 1 ARX Partial-Inverse Boundary Queue - 2026-06-16

## Purpose

ARX/SPECK32 is now being kept as a parallel Innovation 1 evidence line, not a
replacement for the SPN/PRESENT high-round goal.

The current best ARX signal is:

```text
feature: ciphertext_pair_xor_arx_partial_inverse_bits
model: structure_adaptive_pairset_dbitnet
cipher: SPECK32/64
protocol: independent_pairs, key_rotation_interval=1024
pairs_per_sample: 4
```

The partial-inverse feature is public and keyless: it uses the known SPECK round
function relation on ciphertext words to expose one-step inverse/rotation
structure. It should be treated as a structural input encoding, not key leakage.

## Queue Added

Existing watcher chain before this update:

```text
GPU1 current jobs
-> innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616
-> innovation1-arx-speck32-partial-inverse-r7-clean-ablation-10seed-gpu1-20260616
```

Added boundary step:

```text
-> innovation1-arx-speck32-partial-inverse-r8-boundary-10seed-gpu1-20260616
```

The new r8 watcher waits for the r7 clean-ablation result branch:

```text
results/innovation1-arx-speck32-partial-inverse-r7-clean-ablation-10seed-gpu1-20260616
```

Then it waits for GPU1 to be free of matching `run_innovation_one_matrix.py`
training processes and launches the r8 boundary run.

## New Files

Plan:

```text
experiments/innovation1/plans/innovation1_arx_speck32_partial_inverse_r8_boundary_10seed.csv
```

Remote config:

```text
experiments/innovation1/configs/remote/innovation1_arx_speck32_partial_inverse_r8_boundary_10seed_gpu1_20260616.json
```

Generated run scripts:

```text
scripts/generated/remote/run_innovation1-arx-speck32-partial-inverse-r8-boundary-10seed-gpu1-20260616_and_push.cmd
scripts/generated/remote/launch_innovation1-arx-speck32-partial-inverse-r8-boundary-10seed-gpu1-20260616.cmd
scripts/generated/remote/schedule_innovation1_arx_speck32_partial_inverse_r8_boundary_10seed_gpu1_20260616.cmd
scripts/generated/monitors/monitor_innovation1_arx_speck32_partial_inverse_r8_boundary_10seed_gpu1_results.sh
```

Queue watcher:

```text
scripts/generated/remote/watch_after_arx_clean_ablation_to_r8_boundary_20260616.ps1
scripts/generated/remote/schedule_watch_after_arx_clean_ablation_to_r8_boundary_20260616.cmd
```

## R8 Boundary Protocol

Rows:

```text
20 rows = 10 seeds * 2 feature encodings
```

Feature encodings:

```text
ciphertext_pair_xor_bits
ciphertext_pair_xor_arx_partial_inverse_bits
```

Core parameters:

```text
rounds=8
samples_per_class=262144
pairs_per_sample=4
key_rotation_interval=1024
sample_structure=independent_pairs
difference_profile=speck32_gohr2019
epochs=20
batch_size=1024
optimizer=adamw
learning_rate=0.0001
checkpoint_metric=val_auc
restore_best_checkpoint=true
early_stopping_patience=5
```

## Verification

Tests:

```text
uv run pytest tests/test_build_plan_config.py::test_speck32_arx_partial_inverse_r8_boundary_10seed_plan_shape tests/test_remote_script_generator.py tests/test_feature_encodings.py -q
35 passed

uv run pytest tests/test_build_plan_config.py::test_speck32_arx_partial_inverse_r8_boundary_10seed_plan_shape tests/test_build_plan_config.py::test_speck32_arx_partial_inverse_r7_clean_ablation_10seed_plan_shape tests/test_remote_script_generator.py tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_execute_speck_arx_aligned_plan -q
9 passed
```

Tiny local smoke:

```text
uv run python experiments/run_innovation_one_matrix.py --ciphers speck32 --models structure_adaptive_pairset_dbitnet --rounds 2 --seeds 0 --samples-per-class 8 --pairs-per-sample 1 --feature-encoding ciphertext_pair_xor_arx_partial_inverse_bits --negative-mode encrypted_random_plaintexts --difference-profile speck32_gohr2019 --key-rotation-interval 4 --sample-structure independent_pairs --epochs 1 --batch-size 4 --hidden-bits 4 --checkpoint-metric val_auc --output /tmp/arx_partial_inverse_smoke.jsonl
```

Result:

```text
wrote 1 rows to /tmp/arx_partial_inverse_smoke.jsonl
```

## Remote Sync

Local commits:

```text
6805a48 experiment: queue spn and arx followup screens
6024c0b experiment: add arx partial inverse r8 boundary screen
```

Remote GitHub commits after patch-apply:

```text
6443ee1 experiment: queue spn and arx followup screens
b3525d0 experiment: add arx partial inverse r8 boundary screen
```

The remote branch `refactor/model-project-structure` was pushed successfully
from the A6000 workstation because local GitHub access was unavailable.

## Active Watchers

These watcher tasks were launched on the remote node:

```text
innovation1_watch_after_arx_partial_inverse_confirm_to_clean_ablation_20260616
innovation1_watch_after_delta_only_to_spn_parameterized_sboxddt_beam8deep4_20260616
innovation1_watch_after_arx_clean_ablation_to_r8_boundary_20260616
```

Observed watcher logs:

```text
watch_after_innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616_to_innovation1-arx-speck32-partial-inverse-r7-clean-ablation-10seed-gpu1-20260616.log
-> upstream branch not ready, sleeping

watch_after_innovation1-spn-present-delta-only-structural-r7-gpu0-20260616_to_innovation1-spn-present-parameterized-sboxddt-beam8deep4-r7-gpu0-20260616.log
-> upstream branch not ready, sleeping

watch_after_innovation1-arx-speck32-partial-inverse-r7-clean-ablation-10seed-gpu1-20260616_to_innovation1-arx-speck32-partial-inverse-r8-boundary-10seed-gpu1-20260616.log
-> upstream branch not ready, sleeping
```

## Decision Gate

For ARX r7:

```text
partial-inverse must beat raw under the same 10-seed protocol.
Use AUC/calibrated accuracy means and seed variance, not a single seed.
```

For ARX r8:

```text
If partial-inverse r8 is near random and raw is also random, document the ARX
boundary as r7 under this protocol.

If partial-inverse r8 shows repeatable lift over raw, scale r8 with more
samples or test r8 with larger pair count before claiming a round-boundary
improvement.
```

