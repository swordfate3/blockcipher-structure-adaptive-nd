# Innovation 1 PRESENT Delta-Only Structural Queue - 2026-06-16

## Purpose

Continue the PRESENT/SPN high-round push after the latest literature/codebase review concluded:

- r6 structure-adaptive evidence is strong and writeable.
- r7/r8 completed results remain near random.
- The next best diagnostic is to remove raw ciphertext-pair words and test whether public structural delta evidence survives at r7.

## New Experiment Queue

Run id:

- `innovation1-spn-present-delta-only-structural-r7-gpu0-20260616`

Plan:

- `experiments/innovation1/plans/innovation1_spn_present_delta_only_structural_r7_screen.csv`

Remote config:

- `experiments/innovation1/configs/remote/innovation1_spn_present_delta_only_structural_r7_gpu0_20260616.json`

Watcher:

- `scripts/generated/remote/watch_gpu0_then_spn_delta_only_structural_r7_20260616.ps1`

## Matrix

Rows: 12.

Shared protocol:

- cipher: `PRESENT-80`
- difference profile: `present_zhang_wang2022_mcnd`
- sample structure: `zhang_wang_case2_mcnd`
- pairs/sample: `16`
- negative mode: `encrypted_random_plaintexts`
- key rotation interval: `1024`
- train key: `0x00000000000000000000`
- validation key: `0xffffffffffffffffffff`
- loss: `mse`
- optimizer: `adam`
- LR schedule: `cyclic`, max LR `0.002`
- checkpoint metric: `val_auc`

Feature/model groups:

1. Delta-only matrix:
   - feature: `present_xor_paligned_cell_matrix_bits`
   - words: `Delta || InvP(Delta)`
   - model: `present_inception_mcnd_matrix`

2. Delta + structural trail statistics:
   - feature: `present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits`
   - words: `Delta || InvP(Delta) || structural InvS difference || public SBox-DDT beam statistics`
   - model: `present_matrix_trail_hybrid_pairset`

Round/seed setup:

- r6: seeds `0,1,2`, samples/class `32768`
- r7: seeds `0,1,2`, samples/class `65536`, pretrain r6 for 4 epochs

## Verification

Passed:

```text
uv run pytest \
  tests/test_build_plan_config.py::test_present_delta_only_structural_r7_plan_shape \
  tests/test_feature_encodings.py::test_present_xor_paligned_cell_matrix_encoding_keeps_only_difference_planes \
  tests/test_feature_encodings.py::test_present_delta_paligned_sinv_sboxddt_beamstats4deep3_encoding_keeps_compact_trail_statistics -q

3 passed
```

Tiny CPU smoke passed:

```text
experiments/run_innovation_one_matrix.py
plan: /tmp/spn_delta_only_structural_tiny.csv
output: /tmp/spn_delta_only_structural_tiny.jsonl
rows: 2
```

## Decision Rule

This run is diagnostic, not a breakthrough claim by itself.

- r6 should remain clearly above random; otherwise the delta-only/trail-stat input is not preserving the already-known SPN structure signal.
- r7 should be compared against the current completed r7 ceiling around `AUC ~= 0.506`.
- If r7 stays below `AUC 0.53`, do not scale this exact route further.
- If r7 reaches `AUC 0.53+` consistently across seeds, expand to more seeds and larger samples/class before writing any breakthrough claim.
