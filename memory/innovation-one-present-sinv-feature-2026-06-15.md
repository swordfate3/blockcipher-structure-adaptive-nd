# Innovation 1 PRESENT Public InvP+InvS Feature - 2026-06-15

## Purpose

PRESENT r7/r8 remains near random in completed experiments. The next representation candidate is a public structural partial-inverse feature, inspired by the observation that `InvP(Delta)` helps r5/r6 but may not expose enough last-round nonlinear structure for r7.

This feature does not guess or leak the key. It uses the public PRESENT permutation and S-box tables as a zero-key structural approximation.

## Feature

New encoding:

```text
present_pair_xor_paligned_sinv_cell_matrix_bits
```

For one ciphertext pair `(C, C')`, the per-pair words are:

```text
C || C' || Delta || InvP(Delta) || InvS(InvP(C)) xor InvS(InvP(C'))
```

The words are then arranged in the same PRESENT 4-bit cell-matrix bit-plane order used by the existing matrix features.

PRESENT-64 width:

```text
pair_bits = 5 * 64 = 320
with m=16: input_bits = 5120
```

## Implementation

Files changed:

- `src/blockcipher_ai_eval/ciphers/spn/present.py`
  - added `PRESENT_INV_SBOX` and `Present80.inverse_sbox_layer`.
- `src/blockcipher_ai_eval/features/pair_features.py`
  - added `present_pair_xor_paligned_sinv_cell_matrix_bits`.
- `src/blockcipher_ai_eval/features/registry.py`
  - registered the new feature encoding.
- `experiments/run_innovation_one_matrix.py`
  - allowed the new feature in CLI choices.

Validation:

```text
uv run pytest tests/test_feature_encodings.py tests/test_ciphers.py tests/test_remote_script_generator.py tests/test_experiment_matrix_runner.py::test_plan_rows_can_request_curriculum_pretraining -q
43 passed
```

CPU smoke:

```text
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers present80 \
  --models present_inception_mcnd_matrix \
  --rounds 2 --seeds 0 \
  --samples-per-class 8 --pairs-per-sample 2 \
  --epochs 1 --batch-size 8 --hidden-bits 8 \
  --feature-encoding present_pair_xor_paligned_sinv_cell_matrix_bits \
  --negative-mode encrypted_random_plaintexts \
  --sample-structure zhang_wang_case2_mcnd \
  --difference-profile present_zhang_wang2022_mcnd \
  --loss mse --device cpu
```

The smoke wrote a valid JSONL row with `pair_bits=320` and `input_bits=640` for `m=2`.

## Remote Candidate

Prepared plan:

```text
experiments/innovation1/plans/innovation1_spn_present_sinv_matrix_screen.csv
```

Prepared run:

```text
run_id: innovation1-spn-present-sinv-matrix-screen-gpu0-20260615
expected_rows: 12
rounds: 6, 7
seeds: 0, 1
models: present_inception_mcnd_matrix, present_inception_mcnd_global_matrix, present_inception_mcnd_pair_stack_matrix
samples_per_class: 32768
pairs_per_sample: 16
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
feature: present_pair_xor_paligned_sinv_cell_matrix_bits
```

This is a candidate, not evidence. It must pass result gate and show stable r7 lift before being used as a breakthrough claim.
