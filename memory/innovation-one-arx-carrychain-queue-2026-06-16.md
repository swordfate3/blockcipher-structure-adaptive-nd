# Innovation 1 ARX Carry-Chain Queue - 2026-06-16

## Goal

Continue the ARX/SPECK branch of Innovation 1 with a stronger structure-adaptive feature and model path, while the PRESENT/SPN high-round queue continues remotely.

## New ARX Feature

Added feature encoding:

- `ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits`

For SPECK32/64, it keeps the existing public ciphertext pair, XOR difference, rotation-aligned difference, partial inverse, RX, and carry proxy words, then appends six 32-bit public carry-chain role words:

- `carry_generate_xy_delta`
- `carry_propagate_xy_delta`
- `carry_edge_xy_delta`
- `carry_generate_rot_pre_delta`
- `carry_propagate_rot_pre_delta`
- `carry_edge_rot_pre_delta`

The feature width is:

- `17 * 32 = 544 bits` per ciphertext pair.

All appended values are computed from public ciphertext-pair words and public SPECK round-function relations. No key bits are introduced.

## Model Alignment

`ArxRoundFunctionHybridPairSetDistinguisher` now exposes 17-word role names and groups for this feature:

- raw/difference group: `(0, 1, 2)`
- rotation group: `(2, 3)`
- partial-inverse group: `(4, 5, 6)`
- RX group: `(7, 8)`
- old carry proxy group: `(9, 10)`
- ciphertext-word carry-chain group: `(11, 12, 13)`
- rotated/partial-inverse carry-chain group: `(14, 15, 16)`

This keeps the ARX experiment aligned with the Innovation 1 claim: structure-specific feature encoding plus structure-specific neural fusion.

## Local Verification

Passed:

```text
uv run pytest tests/test_feature_encodings.py \
  tests/test_adaptive_dbitnet_model.py::test_arx_round_function_hybrid_pairset_exposes_carrychain_role_groups \
  tests/test_adaptive_dbitnet_model.py::test_build_model_supports_arx_round_function_hybrid_pairset_key_and_options -q

27 passed
```

Passed:

```text
uv run pytest tests/test_build_plan_config.py tests/test_remote_script_generator.py -q

17 passed
```

Passed:

```text
uv run pytest \
  tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_use_chunked_dataset_cache \
  tests/test_experiment_matrix_runner.py::test_plan_rows_can_override_training_protocol_fields \
  tests/test_experiment_matrix_runner.py::test_plan_rows_can_request_curriculum_pretraining -q

3 passed
```

Tiny CPU smoke also passed with one row written:

```text
experiments/run_innovation_one_matrix.py
plan: /tmp/arx_carrychain_tiny.csv
output: /tmp/arx_carrychain_tiny.jsonl
```

## Remote Queue

Smoke run:

- run id: `innovation1-arx-speck32-carrychain-smoke-gpu1-20260616`
- plan: `experiments/innovation1/plans/innovation1_arx_speck32_carrychain_smoke.csv`
- expected rows: 4
- device: `cuda:1`
- samples/class: 32768
- pairs/sample: 4
- rounds: r6 seeds 0,1 and r7 seeds 0,1
- r7 uses r6 curriculum.

Confirm run:

- run id: `innovation1-arx-speck32-carrychain-r7-confirm-4seed-gpu1-20260616`
- plan: `experiments/innovation1/plans/innovation1_arx_speck32_carrychain_r7_confirm_4seed.csv`
- expected rows: 4
- device: `cuda:1`
- samples/class: 131072
- pairs/sample: 4
- rounds: r7 seeds 0..3
- uses r6 curriculum.

Watchers:

- `scripts/generated/remote/watch_gpu1_then_arx_carrychain_smoke_20260616.ps1`
- `scripts/generated/remote/watch_after_arx_carrychain_smoke_to_r7_confirm_20260616.ps1`

The first watcher waits for GPU1 to become free before launching smoke. The second watcher waits for the smoke results branch before launching r7 confirm.

## Interpretation Plan

Compare the carry-chain r7 confirm against the previous strongest ARX baseline:

- `structure_adaptive_pairset_dbitnet + ciphertext_pair_xor_arx_partial_inverse_bits`
- historical r7 approximate result: calibrated accuracy around `0.7896`, AUC around `0.8692` on 4 seeds.

Carry-chain is meaningful only if it improves or stabilizes this baseline under the same multi-key protocol (`key_rotation_interval=1024`) and separate validation key.
