# Innovation 1 PRESENT/SPN Push - 2026-06-15

## Context

User goal: continue innovation 1 without stopping after partial runs, compare local papers and current literature, and push PRESENT/SPN neural differential distinguisher round count as far as possible. Main branch: `refactor/model-project-structure`. Remote GPU host: `lxy-a6000`, project root `G:/lxy/blockcipher-structure-adaptive-nd`, run root `G:/lxy/blockcipher-structure-adaptive-nd-runs`.

## Literature Anchors

- Zhang/Wang 2022 PRESENT MCND is the stable differential baseline: input diff `0x0000000000000009`, `m=16`, Case2, MSE + L2 `1e-5`, Adam cyclic LR `1e-4 -> 2e-3`, 20 epochs. Reported 6r Case2 `0.9699`, 7r Case2 `0.7205`.
- AutoND/DBitNet high-round PRESENT uses diff `0x000000000D000000`; 9r claim is weak/near random, useful as search seed not strong baseline.
- 2024 integral PRESENT reaches 8r `57.32%`, but protocol is integral multiset, not direct pair differential ND.
- 2026 entropy-based PRESENT ND uses Gohr-style diff `0x0000000000D00000`; selects low-entropy output-difference bits from 50k pairs, trains compact bit-reduced distinguishers. Important nuance: entropy is computed on output difference bits, but training input is selected positions from both ciphertexts (`C_selected || C'_selected`).

## Implemented Commits

- `842cf28 feat(innovation1): add oom-safe PRESENT aligned matrix run`
  - Added `innovation1_spn_present_zw2022_matrix_spnaligned_scale_s.csv` and remote GPU1 config/scripts.
  - Purpose: rerun `C || C' || Delta || P^-1(Delta)` cell-matrix feature with safe memory settings after scale-m OOM.
  - Config: r6/r7/r8, seeds 0/1/2, samples_per_class 32768, pairs_per_sample 16, batch 128, hidden_bits 32, matrix blocks 2, kernels `[[1,1],[1,2],[2,4]]`.

- `940f646 feat(innovation1): add PRESENT entropy bit selection`
  - Added `selected_bit_indices` support through dataset config, dataset cache metadata, runner plan parsing, and training metadata.
  - Added `present_entropy2026_gohr` difference profile: `0x0000000000D00000`.
  - Added `experiments/select_entropy_bits.py` to estimate low-entropy triplets and output both `selected_bit_indices` and `pair_selected_bit_indices`.
  - Added `innovation1_spn_present_entropy_selected_scale_s.csv` and remote GPU1 scripts.
  - Local 50k r6 entropy selection produced 28 output-difference bits and 56 pair-input indices. Plan uses `ciphertext_pair_bits` + 56 selected pair indices.

## Verification

- Related test batch passed after entropy commit: `71 passed`.
- Local smoke passed for `experiments/select_entropy_bits.py` and for selected-bit training via `experiments/run_innovation_one_matrix.py` on a one-row temp plan.
- Remote main project fast-forwarded to `940f646`.

## Remote Run Status

Do not stop current remote runs.

### GPU0 Raw Matrix

Run id: `innovation1-spn-present-zw2022-matrix-scale-m-gpu0-20260615`

- Feature: `present_mcnd_cell_matrix_bits` (`C || C'` cell matrix), Zhang/Wang Case2 MCND.
- Current observed result lines: 2/9.
- Earlier r5 seed0: accuracy about `0.8867`, AUC about `0.9446`.
- Latest check showed GPU0 memory still occupied; output has two rows.

### GPU1 SPN-Aligned Scale-S

Run id: `innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615`

- Fixes previous scale-m CUDA OOM.
- Feature: `present_pair_xor_paligned_cell_matrix_bits` (`C || C' || Delta || P^-1(Delta)` cell matrix).
- Current status: running, no stderr error, result lines 0/9 because first row has not completed.
- OOM fixed: training uses about 2.7GB on GPU1 instead of ~45GB.
- Latest observed first row r6 seed0: epoch 2/20 ended with `val_accuracy=0.834442138671875`, `val_auc=0.912818655371666`, `val_loss=0.3708669961197302`; epoch 3 training started.

### Entropy-Selected Run

Run id prepared but not started: `innovation1-spn-present-entropy-selected-scale-s-gpu1-20260615`

- Do not start while GPU1 SPN-aligned scale-s is running unless explicitly deciding to kill/queue.
- Intended as next route if matrix SPN-aligned stalls or after GPU1 finishes.
- Plan: r6/r7, seeds 0/1/2, samples_per_class 65536, pairs_per_sample 1, MLP hidden_bits 12, MSE, Adam, cyclic LR, selected 56 pair bits from local 50k r6 entropy estimate.

## Next Actions

1. Keep monitoring GPU0 raw and GPU1 SPN-aligned.
2. When GPU1 first row completes, compare r6 aligned vs raw matrix r6/r5 trends; if promising, let all 9 rows finish.
3. Pull result branches only after full gate passes; until then inspect run-dir JSONL/progress by SSH.
4. Start entropy-selected run only after GPU1 is free or if user explicitly wants to queue/replace.
5. If aligned r7 remains below literature, use entropy-selected route and possibly score-distribution second-stage classifier as next implementation.

## 2026-06-15 Independent Case2 Matrix Smoke Result

Pulled remote run `innovation1-spn-present-zw2022-independent-matrix-smoke-gpu1-20260615` into `outputs/remote_results/innovation1-spn-present-zw2022-independent-matrix-smoke-gpu1-20260615`.

Protocol: `present_inception_mcnd_matrix`, `present_mcnd_cell_matrix_bits`, `zhang_wang_case2_independent_mcnd`, `m=16`, `key_rotation_interval=1`, MSE, Adam, weight decay `1e-5`, cyclic LR `1e-4 -> 2e-3`, 20 epochs, `samples_per_class=8192` smoke.

Result: r6 `acc=0.5`, `AUC=0.5067992806`; r7 `acc=0.5`, `AUC=0.5043639243`. This is a negative smoke result, not a r6/r7 reproduction. It suggests the per-pair 2D encoder plus late attention pooling is not sufficient under independent Case2 at this data scale.

Next main route: run `present_inception_mcnd_global_matrix` under the same independent Case2 raw feature protocol so all `m` pairs share one 2D convolutional field before pooling. Use r6 as the gate; do not scale r7/r8 unless r6 recovers strong signal.

## 2026-06-15 Running Queue After Global-Matrix Patch

Committed and pushed:

- `d9610d6 feat(innovation1): add global PRESENT MCND matrix smoke`.
- `be8e105 experiment(innovation1): prepare global matrix basemask smoke`.
- `ff17790 feat(innovation1): add PRESENT pair-stack MCND matrix model`.

Remote running:

- `innovation1-spn-present-zw2022-global-matrix-smoke-gpu1-20260615`: `present_inception_mcnd_global_matrix`, independent Case2, raw `present_mcnd_cell_matrix_bits`, r6/r7, m=16. Early r6/r7 validation AUC stayed near random (~0.505 / ~0.501), but wait for final gate before conclusion.
- `innovation1-spn-present-zw2022-matrix-scale-m-gpu0-20260615`: still running on GPU0, last row pending.

Prepared next runs, not yet launched:

- `innovation1-spn-present-zw2022-pairstack-matrix-smoke-gpu1-20260615`: `present_inception_mcnd_pair_stack_matrix`, independent Case2. This layout reshapes input to `(batch, 1, m*4, 32)` so pair rows participate as a spatial axis; intended to better match the paper's `m x omega x 2L/omega` input-module description than the long-width global matrix.
- `innovation1-spn-present-zw2022-global-matrix-basemask-smoke-gpu1-20260615`: global matrix with legacy `zhang_wang_case2_mcnd` base+mask grouping and key rotation 1024. Use this only as protocol contrast if independent Case2 stays random.

Decision gate:

1. If independent global final r6 is random, launch pair-stack independent next.
2. If pair-stack independent still random, launch base-mask global to test whether the older group-correlated sample construction is the source of the previous r6 signal.
3. Do not claim r7 breakthrough unless final results clearly exceed random and survive at least a seed/control check.

## 2026-06-15 Global Matrix Independent Case2 Smoke Result

Pulled remote run `innovation1-spn-present-zw2022-global-matrix-smoke-gpu1-20260615` into `outputs/remote_results/innovation1-spn-present-zw2022-global-matrix-smoke-gpu1-20260615`.

Protocol: `present_inception_mcnd_global_matrix`, raw `present_mcnd_cell_matrix_bits`, `zhang_wang_case2_independent_mcnd`, `m=16`, key per sample (`key_rotation_interval=1`), MSE, Adam, weight decay `1e-5`, cyclic LR `1e-4 -> 2e-3`, 20 epochs, `samples_per_class=8192` smoke.

Result: r6 `acc=0.5087890625`, `AUC=0.5106733143`; r7 `acc=0.5`, `AUC=0.4997341931`. This is still a negative result. It rules out the first global long-width matrix layout as sufficient under independent Case2 at smoke scale.

Action taken: launched `innovation1-spn-present-zw2022-pairstack-matrix-smoke-gpu1-20260615`, which uses `present_inception_mcnd_pair_stack_matrix` and reshapes input as `(batch, 1, m*4, 32)` so pair rows remain a spatial axis.

## 2026-06-15 Pair-Stack Independent Case2 Smoke Result

Pulled remote run `innovation1-spn-present-zw2022-pairstack-matrix-smoke-gpu1-20260615` into `outputs/remote_results/innovation1-spn-present-zw2022-pairstack-matrix-smoke-gpu1-20260615`.

Protocol: `present_inception_mcnd_pair_stack_matrix`, raw `present_mcnd_cell_matrix_bits`, `zhang_wang_case2_independent_mcnd`, `m=16`, key per sample (`key_rotation_interval=1`), MSE, Adam, weight decay `1e-5`, cyclic LR `1e-4 -> 2e-3`, 20 epochs, `samples_per_class=8192` smoke.

Result: r6 `acc=0.4996337891`, `AUC=0.5028857589`; r7 `acc=0.4991455078`, `AUC=0.4973554909`. This is a negative result. It shows the pair-stack spatial layout alone does not recover the Zhang/Wang r6/r7 signal under independent Case2 at smoke scale.

Configuration correction: the first base-mask launch accidentally used `key_rotation_interval=1` from the CSV plan rows overriding the JSON default. That run was stopped and its remote run directory was removed. Commit `e9b496b` fixes the base-mask CSV rows to `key_rotation_interval=1024`; the corrected remote progress confirms `key_rotation_interval=1024`.

## 2026-06-15 Base-Mask Global Matrix Result and Raw MCND Decision

Pulled corrected base-mask run artifacts into `outputs/remote_results/innovation1-spn-present-zw2022-global-matrix-basemask-smoke-gpu1-20260615` via SCP after the Git result-branch monitor failed to read the branch gate. Remote gate passed (`result_lines=2`, `expected_rows=2`) and stderr was empty.

Protocol: `present_inception_mcnd_global_matrix`, raw `present_mcnd_cell_matrix_bits`, legacy `zhang_wang_case2_mcnd` base+mask grouping, `m=16`, `key_rotation_interval=1024`, MSE, Adam, weight decay `1e-5`, cyclic LR `1e-4 -> 2e-3`, 20 epochs, `samples_per_class=8192` smoke.

Result: r6 `acc=0.5034179688`, `AUC=0.5011024177`; r7 `acc=0.5091552734`, `AUC=0.5078672767`. This is still near random. Together with independent matrix, independent global matrix, and independent pair-stack matrix, raw Zhang/Wang-style MCND is not reproduced in the current implementation/data scale.

Decision: stop treating raw MCND reproduction as the main breakthrough path for Innovation 1. The current strongest PRESENT/SPN evidence remains the SPN-aligned structure-adaptive route (`present_pair_xor_paligned_cell_matrix_bits` / public inverse P-layer alignment), where previous scale-s r6 reached `acc_mean=0.8822`, `AUC_mean=0.9519`. Next work should scale and harden the SPN-aligned route with seeds and controls, not keep expanding raw MCND variants.



## 2026-06-15 SPN-Aligned R6 Controls and R7 Matrix Screen

Committed and pushed:

- `0804e61 experiment(innovation1): add SPN-aligned PRESENT r6/r7 runs`.
- `d694b47 fix(remote): avoid ambiguous branch pull in generated runs`.
- `4c3dc2b feat(innovation1): add PRESENT delta paligned matrix screen`.

Remote runs launched from revision `0804e6192657840a688502ebfec4baf96ce64d79`:

- `innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615`, expected rows `30`. Purpose: publication-grade r6 control table under Zhang/Wang Case2 MCND scaffold. Rows compare raw `present_mcnd_cell_matrix_bits`, `present_pair_xor_cell_matrix_bits`, and SPN-aligned `present_pair_xor_paligned_cell_matrix_bits` over seeds `0..9`, `samples_per_class=32768`, `pairs_per_sample=16`, `key_rotation_interval=1024`, MSE, Adam, cyclic LR.
- `innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615`, expected rows `24`. Purpose: targeted r7 rescue screen only on SPN-aligned feature `C || Cprime || Delta || InvP(Delta)`, comparing `present_inception_mcnd_matrix`, `present_inception_mcnd_global_matrix`, and `present_inception_mcnd_pair_stack_matrix` at `samples_per_class=32768` and `65536`, seeds `0..2`, `pairs_per_sample=16`, `key_rotation_interval=1024`, MSE, Adam, cyclic LR.

Both runs entered dataset cache generation with empty run stderr. Low GPU memory during this stage is expected because sample generation/cache writing is CPU/disk-bound. Local tmux monitors started:

- `mon_spn_r6_controls` -> monitor expected `30` rows.
- `mon_spn_r7_screen` -> monitor expected `24` rows.

Infrastructure fix: generated remote scripts now use `git fetch origin %BRANCH%` plus `git merge --ff-only FETCH_HEAD` instead of `git pull --ff-only origin %BRANCH%`, avoiding Git for Windows ambiguous multiple-branch stderr when result branches exist. Current already-started runs are not interrupted; this fix applies to future generated-script reruns.

New next-candidate feature prepared but not launched yet:

- Feature encoding: `present_xor_paligned_cell_matrix_bits` = `Delta || InvP(Delta)` in PRESENT 4-bit cell-matrix bit-plane order, `128` bits per pair for PRESENT-64.
- Plan/config/scripts: `innovation1_spn_present_delta_paligned_matrix_screen.csv`, run id `innovation1-spn-present-delta-paligned-matrix-screen-gpu0-20260615`, expected rows `18`.
- Purpose: r6/r7 ablation that removes raw ciphertext words `C,Cprime`, testing whether ciphertext noise is hurting r7 while preserving the public SPN-aligned difference signal.
- Verified locally with `uv run pytest tests/test_feature_encodings.py tests/test_present_inception_mcnd_model.py tests/test_remote_script_generator.py -q` -> `25 passed`.

Decision: the current batch is not a claimed breakthrough. It is the next rigorous push after raw MCND negative evidence: harden the r6 aligned gain and test whether r7 can be rescued by SPN-aligned matrix layout/capacity. The Delta+InvP-only candidate is queued as the next route if full `C,Cprime,Delta,InvP(Delta)` r7 remains near random.
