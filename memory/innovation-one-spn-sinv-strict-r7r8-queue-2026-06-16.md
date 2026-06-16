# Innovation 1 SPN SInv Strict r7/r8 Queue - 2026-06-16

## Evidence Trigger

Remote run `innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616` produced the strongest current SPN/PRESENT strict evidence:

- protocol: `key_rotation_interval=1024`, `sample_structure=zhang_wang_case2_mcnd`
- feature: `present_pair_xor_paligned_sinv_cell_matrix_bits`
- model: `present_inception_mcnd_matrix`
- r7 seed0 result:
  - AUC `0.6836514687165618`
  - calibrated accuracy `0.632110595703125`
  - samples/class `65536`
  - pairs/sample `16`
  - r6 pretrain enabled (`pretrain_rounds=6`, `pretrain_epochs=6`)

This is stronger and more thesis-relevant than the earlier protocol-only `key_rotation_interval=1` SPN-aligned signal.

## New Queue

Added plan:

- `experiments/innovation1/plans/innovation1_spn_present_sinv_strict_r7r8_confirm.csv`
- rows: `14`
- r7 strict confirm: seeds `0..9`, samples/class `65536`
- r8 boundary probe: seeds `0..3`, samples/class `131072`
- feature: `present_pair_xor_paligned_sinv_cell_matrix_bits`
- model: `present_inception_mcnd_matrix`
- protocol: `key_rotation_interval=1024`, `zhang_wang_case2_mcnd`
- checkpoint metric: `val_auc`
- curriculum: r6 pretrain for all rows

Remote spec and generated scripts:

- `experiments/innovation1/configs/remote/innovation1_spn_present_sinv_strict_r7r8_confirm_gpu0_20260616.json`
- `scripts/generated/remote/run_innovation1-spn-present-sinv-strict-r7r8-confirm-gpu0-20260616_and_push.cmd`
- `scripts/generated/remote/launch_innovation1-spn-present-sinv-strict-r7r8-confirm-gpu0-20260616.cmd`
- `scripts/generated/remote/schedule_innovation1_spn_present_sinv_strict_r7r8_confirm_gpu0_20260616.cmd`
- `scripts/generated/monitors/monitor_innovation1_spn_present_sinv_strict_r7r8_confirm_gpu0_results.sh`

Added watcher:

- `scripts/generated/remote/watch_after_spn_strict_spnaligned_to_sinv_strict_r7r8_20260616.ps1`
- `scripts/generated/remote/schedule_watch_after_spn_strict_spnaligned_to_sinv_strict_r7r8_20260616.cmd`
- chain position:
  `sinv_curriculum_r7`
  -> `protocol_spnaligned_r7_confirm_5seed`
  -> `strict_spnaligned_r7_confirm_5seed`
  -> `sinv_strict_r7r8_confirm`

## Current Remote State at Queue Creation

Remote active processes:

- `innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616`
  - result rows: `4/6`
  - still running, currently processing seed1 r7 pretrain cache for row `5/6`
  - stderr empty
- `innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616`
  - result rows: `9/12`
  - still running, currently row `11/12`
  - stderr empty
- `innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`
  - result rows: `3/8`
  - still running, r8 row `4/8`, epoch `18/20`
  - stderr only PyTorch Transformer nested tensor warnings

Queued but not started at this point:

- `innovation1-spn-present-protocol-spnaligned-r7-confirm-5seed-gpu0-20260616`
- `innovation1-spn-present-strict-spnaligned-r7-confirm-5seed-gpu0-20260616`
- `innovation1-spn-present-sinv-strict-r7r8-confirm-gpu0-20260616`
- `innovation1-spn-present-global-stats-only-beamstats8deep4-r7-gpu0-20260616`
- `innovation1-spn-present-trail-position-stats-r7r8-gpu0-20260616`

## Caution

- Do not claim a PRESENT r7/r8 breakthrough from the queue itself.
- The current hard evidence is one completed strict r7 SInv seed plus three r6 sanity rows.
- A thesis-grade claim needs the new 10-seed r7 confirm and ideally a positive r8 boundary result.
- Remote project HEAD observed during monitoring was `4d951b0`; make sure the new queue is committed/pushed/synced before relying on the watcher to launch it remotely.
