# Innovation 1 SPN r7 Confirm Queue - 2026-06-16

Trigger evidence:

- Run `innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616` wrote the first formal r7 SPN-aligned row.
- Raw r7 controls under the same protocol were random:
  - raw seed0 AUC `0.504861606284976`, calibrated accuracy `0.506134033203125`
  - raw seed1 AUC `0.5013546906411648`, calibrated accuracy `0.5032958984375`
- SPN-aligned r7 seed0 was non-random:
  - feature `present_pair_xor_paligned_cell_matrix_bits`
  - model `present_inception_mcnd_global_matrix`
  - key rotation interval `1`
  - sample structure `zhang_wang_case2_independent_mcnd`
  - AUC `0.6442790199071169`
  - calibrated accuracy `0.6053466796875`

New confirmation plans:

1. `innovation1_spn_present_protocol_spnaligned_r7_confirm_5seed.csv`
   - purpose: reproduce and stabilize the r7 SPN-aligned signal under the protocol that produced it.
   - rows: raw control + SPN-aligned, seeds 0..4.
   - key rotation: `1`
   - sample structure: `zhang_wang_case2_independent_mcnd`
   - samples/class: `32768`
   - checkpoint metric: `val_loss`

2. `innovation1_spn_present_strict_spnaligned_r7_confirm_5seed.csv`
   - purpose: test whether the same r7 SPN-aligned idea survives a stricter multi-key setting.
   - rows: raw control + SPN-aligned, seeds 0..4.
   - key rotation: `1024`
   - sample structure: `zhang_wang_case2_mcnd`
   - samples/class: `65536`
   - checkpoint metric: `val_auc`

Remote queue:

`innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616`
-> `innovation1-spn-present-protocol-spnaligned-r7-confirm-5seed-gpu0-20260616`
-> `innovation1-spn-present-strict-spnaligned-r7-confirm-5seed-gpu0-20260616`

Interpretation:

- If protocol confirm repeats AUC around `0.62-0.65` across multiple seeds while raw stays random, this becomes strong evidence that the SPN structure-aligned representation is carrying r7 signal.
- If strict confirm also remains non-random, this is the first credible route toward an Innovation 1 r7 result suitable for the thesis.
- If strict confirm collapses, the result remains a protocol-dependent discovery and must be framed as a lead, not a final breakthrough.
