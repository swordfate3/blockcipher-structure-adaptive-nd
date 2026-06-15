# Innovation 1 ARX Carrychain Micro Smoke - 2026-06-16

## Goal

ARX/SPECK must progress alongside the PRESENT/SPN high-round work. The previous ARX trail-mixer scale run was gate-blocked during/near dataset caching with no Python traceback, so the next ARX step is a deliberately smaller carrychain micro-smoke that validates the full remote path before scaling to r7 confirmation.

## Added Run

Run id:

```text
innovation1-arx-speck32-carrychain-micro-smoke-gpu1-20260616
```

Plan:

```text
experiments/innovation1/plans/innovation1_arx_speck32_carrychain_micro_smoke.csv
```

Remote spec:

```text
experiments/innovation1/configs/remote/innovation1_arx_speck32_carrychain_micro_smoke_gpu1_20260616.json
```

Generated scripts:

```text
scripts/generated/remote/run_innovation1-arx-speck32-carrychain-micro-smoke-gpu1-20260616_and_push.cmd
scripts/generated/remote/launch_innovation1-arx-speck32-carrychain-micro-smoke-gpu1-20260616.cmd
scripts/generated/remote/schedule_innovation1_arx_speck32_carrychain_micro_smoke_gpu1_20260616.cmd
scripts/generated/monitors/monitor_innovation1_arx_speck32_carrychain_micro_smoke_gpu1_results.sh
```

## Configuration

```text
cipher: SPECK32/64
profile: speck32_gohr2019
feature: ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits
model: arx_round_function_hybrid_pairset
rounds: 6, 7
seed: 0
samples_per_class: 8192
pairs_per_sample: 4
sample_structure: independent_pairs
negative_mode: encrypted_random_plaintexts
key_rotation_interval: 1024
loss: mse
optimizer: adam
lr_scheduler: cyclic
checkpoint_metric: val_auc
remote epochs: 6
remote batch_size: 128
remote dataset_cache_chunk_size: 512
```

r7 uses a tiny r6 curriculum:

```text
pretrain_rounds: 6
pretrain_epochs: 2
```

## Local Verification

Tests:

```text
uv run pytest \
  tests/test_build_plan_config.py::test_speck32_arx_carrychain_micro_smoke_plan_shape \
  tests/test_adaptive_dbitnet_model.py::test_arx_round_function_hybrid_pairset_exposes_carrychain_role_groups \
  tests/test_feature_encodings.py::test_pair_features_module_encodes_speck_arx_rx_carrychain_pair_features -q
```

Result:

```text
3 passed, 1 warning
```

Local CPU path smoke:

```text
uv run python experiments/run_innovation_one_matrix.py \
  --plan experiments/innovation1/plans/innovation1_arx_speck32_carrychain_micro_smoke.csv \
  --epochs 1 \
  --batch-size 32 \
  --hidden-bits 8 \
  --learning-rate 0.0001 \
  --optimizer adam \
  --weight-decay 1e-05 \
  --key-rotation-interval 1024 \
  --sample-structure independent_pairs \
  --device cpu \
  --dataset-cache-root /tmp/innovation1_arx_carrychain_micro_smoke_cache \
  --dataset-cache-chunk-size 64 \
  --checkpoint-metric val_auc \
  --restore-best-checkpoint \
  --progress-output /tmp/innovation1_arx_carrychain_micro_smoke_progress.jsonl \
  --output /tmp/innovation1_arx_carrychain_micro_smoke.jsonl
```

Result:

```text
wrote 2 rows
r6: AUC ~= 0.7505, calibrated_accuracy ~= 0.6932
r7: AUC ~= 0.5274, calibrated_accuracy ~= 0.5243
r7 pretrain r6: AUC ~= 0.8889
```

These local CPU numbers are not paper evidence, but they show that the carrychain feature/model path is not random at the tiny sanity scale and is worth remote validation.

## Remote State When Queued

The existing GPU jobs were still occupying both GPUs:

```text
GPU0: innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
GPU1: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
```

The existing carrychain watcher was waiting for GPU1:

```text
watch_innovation1-arx-speck32-carrychain-smoke-gpu1-20260616_gpu1.log
```

This micro-smoke should be launched after code is pushed/synced and GPU1 is free, before escalating to the existing `carrychain_smoke` and `carrychain_r7_confirm_4seed` runs if needed.

## Interpretation Gate

Use the micro smoke only as an engineering gate:

- PASS: result branch exists, expected rows = 2, stderr clean, r6 learns clearly above random.
- PROMOTE: if r7 AUC is above about 0.52 under remote 6-epoch training, continue to carrychain smoke/r7 confirm.
- HOLD: if r6 fails, inspect data generation/feature layout before running larger ARX jobs.
