# Innovation 1 progress - SPN r6 controls and ARX stats-only queue (2026-06-16)

## SPN r6 control result recovered locally

Run id: `innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615`

Local archive:

- `outputs/remote_results/innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615/innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615.jsonl`
- `outputs/remote_results/innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615/innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615_summary.csv`

The remote runner wrote all 30 rows and `run_done`, but the legacy generated `.cmd` treated the runner exit as failed before creating result gate/result branch. The generator was fixed in commit `56a6939` so future scripts record `runner_exit_code` and gate primarily on complete result rows.

### 10-seed r6 control metrics

Model: `present_inception_mcnd_matrix`, sample structure `zhang_wang_case2_mcnd`, samples/class 32768, pairs/sample 16.

| feature | mean acc | mean calibrated acc | mean AUC | interpretation |
| --- | ---: | ---: | ---: | --- |
| `present_mcnd_cell_matrix_bits` | 0.500000 | 0.502637 | 0.501616 | no useful signal by itself |
| `present_pair_xor_cell_matrix_bits` | 0.807813 | 0.809177 | 0.890164 | pair-xor signal is strong |
| `present_pair_xor_paligned_cell_matrix_bits` | 0.881830 | 0.882608 | 0.951026 | P-layer aligned structure is strongest |

Conclusion: for PRESENT r6, structure-aligned input is not cosmetic; it produces a large and stable improvement over raw MCND matrix and unaligned pair-xor. This supports Innovation 1's structure-adaptive input-construction claim, but it is still r6. The main target remains r7/high-round improvement.

## ARX progress added

Commit `56a6939 experiment: add arx stats-only r7 screen` adds:

- `arx_round_stats_pairset`: stats-only SPECK pair-set model using public ARX role/carry/RX cross-pair statistics.
- `experiments/innovation1/audit_arx_feature_separation.py`: ARX feature separation audit analogous to SPN audit.
- `innovation1_arx_speck32_round_stats_only_r7_screen.csv`: r7 same-protocol comparison among round-function control, stats-only, and round-stats hybrid.
- Remote config/scripts for `innovation1-arx-speck32-round-stats-only-r7-screen-gpu1-20260616`.

Remote GitHub push from Windows succeeded as remote commit `2126eed` on `refactor/model-project-structure`.

## Remote status

The ARX stats-only run was first scheduled but correctly blocked by GPU guard because GPU1 had two training processes:

- `innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`
- `innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616`

A watcher was uploaded directly to the remote and started:

- `scripts/generated/remote/watch_gpu1_then_arx_round_stats_only_r7_20260616.ps1`
- `scripts/generated/remote/schedule_watch_gpu1_then_arx_round_stats_only_r7_20260616.cmd`

Watcher log:

- `G:/lxy/blockcipher-structure-adaptive-nd-runs/launcher_logs/watch_gpu1_then_innovation1-arx-speck32-round-stats-only-r7-screen-gpu1-20260616.log`

It polls every 600s and will start the ARX stats-only run when GPU1 has no matching `run_innovation_one_matrix.py --device cuda:1` process.

Caveat: the two watcher files are present locally as untracked files because `.git` became read-only in the sandbox after commit `56a6939`; they were copied to remote and started, but need a later local commit when git write access is available.
