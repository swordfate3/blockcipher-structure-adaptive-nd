# Innovation 1 PRESENT SInv Curriculum r7 - 2026-06-16

## Goal

PRESENT r7 is still near random under the completed `C || C' || Delta || InvP(Delta)` matrix runs. The next SPN push is to test a minimal public S-box-aware structural approximation:

```text
C || C' || Delta || InvP(Delta) || InvS(InvP(C)) xor InvS(InvP(C'))
```

This keeps the Zhang/Wang MCND training skeleton but adds one public inverse-S layer to cross the S-box bottleneck that appears between the strong r6 result and random r7 result.

## Added Plan

```text
experiments/innovation1/plans/innovation1_spn_present_sinv_curriculum_r7_screen.csv
```

Remote spec:

```text
experiments/innovation1/configs/remote/innovation1_spn_present_sinv_curriculum_r7_gpu0_20260616.json
```

Generated scripts:

```text
scripts/generated/remote/run_innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616_and_push.cmd
scripts/generated/remote/launch_innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616.cmd
scripts/generated/remote/schedule_innovation1_spn_present_sinv_curriculum_r7_gpu0_20260616.cmd
scripts/generated/monitors/monitor_innovation1_spn_present_sinv_curriculum_r7_gpu0_results.sh
```

## Configuration

```text
cipher: PRESENT-80
difference_profile: present_zhang_wang2022_mcnd
feature: present_pair_xor_paligned_sinv_cell_matrix_bits
model: present_inception_mcnd_matrix
pairs_per_sample: 16
sample_structure: zhang_wang_case2_mcnd
negative_mode: encrypted_random_plaintexts
key_rotation_interval: 1024
loss: mse
optimizer: adam
lr_scheduler: cyclic
max_lr: 0.002
checkpoint_metric: val_auc
```

Rows:

```text
r6 sanity: seeds 0,1,2; samples_per_class=32768
r7 target: seeds 0,1,2; samples_per_class=65536; pretrain_rounds=6; pretrain_epochs=6
```

Remote:

```text
device: cuda:0
epochs: 16
batch_size: 128
dataset_cache_chunk_size: 1024
expected_rows: 6
```

## Verification

Tests:

```text
uv run pytest \
  tests/test_build_plan_config.py::test_present_sinv_curriculum_r7_plan_shape \
  tests/test_feature_encodings.py::test_present_pair_xor_paligned_sinv_cell_matrix_encoding_includes_public_inverse_sbox_difference \
  tests/test_present_inception_mcnd_model.py -q
```

Result:

```text
8 passed
```

Tiny CPU smoke:

```text
UV_CACHE_DIR=/tmp/uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python experiments/run_innovation_one_matrix.py \
  --plan /tmp/present_sinv_tiny.csv \
  --epochs 1 \
  --batch-size 16 \
  --hidden-bits 8 \
  --learning-rate 0.0001 \
  --optimizer adam \
  --weight-decay 1e-05 \
  --key-rotation-interval 1024 \
  --sample-structure zhang_wang_case2_mcnd \
  --device cpu \
  --checkpoint-metric val_auc \
  --restore-best-checkpoint \
  --progress-output /tmp/present_sinv_tiny_progress.jsonl \
  --output /tmp/present_sinv_tiny.jsonl
```

Result:

```text
wrote 1 row
```

## Interpretation Gate

- If r6 collapses below about AUC 0.85, SInv is destructive and should not be scaled.
- If r6 remains strong and r7 rises above AUC 0.53 across seeds, promote to 10-seed confirmation.
- If r6 remains strong and r7 stays near 0.50, the bottleneck is not solved by one public InvS layer; prioritize compact DDT beamstats or difference/profile search.
