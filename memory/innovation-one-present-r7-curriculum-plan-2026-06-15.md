# Innovation 1 PRESENT r7 Curriculum Push - 2026-06-15

## Context

The strongest verified PRESENT/SPN evidence remains r6, not r7/r8. Completed local result audit found no trustworthy PRESENT r7/r8 breakthrough yet. The best completed PRESENT r6 matrix result is `innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615` with `present_pair_xor_paligned_cell_matrix_bits`, `present_inception_mcnd_matrix`, `pairs_per_sample=16`, `samples_per_class=32768`, `key_rotation_interval=1024`, and about `cal_acc=0.8839`, `AUC=0.9519` over 3 seeds. This is strong but still needs 10-seed controls.

The literature/method audit says the next r7 attempts should focus on representation/transfer rather than simply enlarging ordinary networks:

- complete current r7 matrix layout screen;
- run delta-only `Delta || InvP(Delta)` matrix screen;
- test r6 -> r7 curriculum/warm-start;
- if still random, implement PRESENT partial inverse / GPD-style structural features.

## Code Added

`experiments/run_innovation_one_matrix.py` now supports optional curriculum pretraining:

- CLI: `--pretrain-rounds <int>` and `--pretrain-epochs <int>`.
- CSV plan columns: `pretrain_rounds`, `pretrain_epochs`.
- For each target row, the runner can train the same model first on a lower-round dataset, then fine-tune on the target row.
- Result JSON records `training.pretraining.enabled`, pretraining metrics, epochs, best epoch, and selected checkpoint.
- Progress JSONL emits `pretrain_cache_ready` and training events with `stage=pretraining` before target `stage=training`.

Small CPU smoke passed:

```text
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers present80 --models present_inception_mcnd_matrix \
  --rounds 2 --pretrain-rounds 1 --pretrain-epochs 1 \
  --samples-per-class 8 --pairs-per-sample 2 --epochs 1 \
  --feature-encoding present_pair_xor_paligned_cell_matrix_bits \
  --negative-mode encrypted_random_plaintexts \
  --sample-structure zhang_wang_case2_mcnd \
  --difference-profile present_zhang_wang2022_mcnd \
  --loss mse --device cpu
```

Relevant tests passed:

```text
uv run pytest tests/test_experiment_matrix_runner.py::test_plan_rows_can_request_curriculum_pretraining \
  tests/test_remote_script_generator.py \
  tests/test_feature_encodings.py \
  tests/test_present_inception_mcnd_model.py -q
26 passed
```

## New Remote Candidate

New r7 curriculum screen:

```text
run_id: innovation1-spn-present-spnaligned-r7-curriculum-screen-gpu0-20260615
plan: experiments/innovation1/plans/innovation1_spn_present_spnaligned_r7_curriculum_screen.csv
expected_rows: 6
target: PRESENT r7
pretrain: PRESENT r6 for 8 epochs
target training: 16 epochs
feature: present_pair_xor_paligned_cell_matrix_bits = C || C' || Delta || InvP(Delta)
models: present_inception_mcnd_matrix, present_inception_mcnd_global_matrix, present_inception_mcnd_pair_stack_matrix
seeds: 0, 1
samples_per_class: 32768
pairs_per_sample: 16
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
loss/optimizer: MSE + Adam + cyclic LR from plan
```

Purpose: test whether the strong r6 SPN-aligned matrix signal provides a useful initialization for r7. This must not be claimed as successful until the result gate passes and r7 metrics are above random across seeds.

Delta-only matrix screen remains prepared and regenerated with current remote script generator:

```text
run_id: innovation1-spn-present-delta-paligned-matrix-screen-gpu0-20260615
feature: present_xor_paligned_cell_matrix_bits = Delta || InvP(Delta)
expected_rows: 18
```

Purpose: test whether removing raw ciphertext words reduces noise at r7 while keeping public SPN-aligned difference signal.

## Caution

Do not overclaim r7/r8. Current completed r7/r8 results are near random. The curriculum and delta-only runs are candidate experiments, not evidence until complete.
