# Innovation 1 SPN/ARX Push Notes - 2026-06-16

## Current Goal

Innovation 1 is still aimed at structure-adaptive neural distinguishers. The SPN/PRESENT line remains the main graduation-paper pressure point: r6 is strong, but r7/r8 are not yet broken. ARX/SPECK32 should continue as a parallel structure-adaptation evidence line, but it must not be allowed to replace the SPN high-round goal.

## Remote State Snapshot

As of 2026-06-16 04:55 CST, remote runs were still active:

- GPU0: `innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615`.
- GPU1: `innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`.
- GPU1: `innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616`.
- Queued watcher: `innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616`, waiting for GPU1.

Do not stack another manual GPU1 training while these are active. Let the GPU guard/watcher launch the partial-inverse 10-seed confirm when GPU1 frees.

## ARX Evidence Pulled Locally

Run pulled locally:

```text
outputs/remote_results/innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616/
```

Files pulled/generated:

- `innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616.jsonl`
- `innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616_progress.jsonl`
- `innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616_stderr.txt`
- `innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616_torch_info.txt`
- `innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616_summary.csv`

The summary was regenerated locally after adding protocol-visible grouping fields to the summarizer.

Key smoke results under `key_rotation_interval=1024`, `sample_structure=independent_pairs`, seed 0, small data:

| Model / feature | r6 AUC | r7 AUC | r7 calibrated acc |
|---|---:|---:|---:|
| Gohr depth10, `ciphertext_pair_bits`, 1 pair | 0.7630 | 0.5147 | 0.5132 |
| PairSet DBitNet raw, `ciphertext_pair_xor_bits`, 4 pairs | 0.9452 | 0.5482 | 0.5389 |
| PairSet DBitNet partial inverse, `ciphertext_pair_xor_arx_partial_inverse_bits`, 4 pairs | 0.9540 | 0.6084 | 0.5767 |
| RoundFunctionHybrid RX, `ciphertext_pair_xor_arx_partial_inverse_rx_bits`, 4 pairs | 0.9125 | 0.5400 | 0.5304 |
| RoundFunctionHybrid CarryChain, `ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits`, 4 pairs | 0.9245 | 0.5336 | 0.5255 |

Interpretation:

- In the same small multi-key protocol, public partial-inverse ARX features give a real r7 lift over Gohr single-pair and raw multi-pair.
- More complex RX/carry role models did not beat the simpler partial-inverse + PairSet DBitNet in this smoke.
- Therefore the next ARX priority is not carrychain scale-up. It is the strict 10-seed multi-key confirm of the current best partial-inverse recipe.

## ARX Next Experiments

Highest priority:

```text
run_id: innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616
plan: experiments/innovation1/plans/innovation1_arx_speck32_partial_inverse_r7_confirm_10seed.csv
config: experiments/innovation1/configs/remote/innovation1_arx_speck32_partial_inverse_r7_confirm_10seed_gpu1_20260616.json
```

Purpose:

- Confirm the strongest historical ARX recipe under strict multi-key rotation.
- Parameters: r7, seeds 0..9, `samples_per_class=131072`, `pairs_per_sample=4`, `feature=ciphertext_pair_xor_arx_partial_inverse_bits`, `key_rotation_interval=1024`, `sample_structure=independent_pairs`.

Secondary ARX route:

- Complete/collect `innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`.
- If its r7 seed-0 result stays near AUC 0.57 and later rows do not improve, do not expand trail/carry models before the partial-inverse 10seed confirm.

## Summary Tool Fix

Changed summary grouping to include:

- `key_rotation_interval`
- `sample_structure`

Files:

- `src/blockcipher_ai_eval/evaluation/summary.py`
- `tests/test_summarize_results.py`

Reason:

- Fixed-key, cross-key, and key-rotating multi-key results must not be averaged into the same summary row.
- This prevents memory/report ambiguity around ARX historical results.

Verification:

```text
uv run pytest tests/test_summarize_results.py -q
4 passed
```

## SPN/PRESENT State

Strongest completed PRESENT evidence so far:

```text
run: innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615
feature: present_pair_xor_paligned_cell_matrix_bits
model: present_inception_mcnd_matrix
protocol: PRESENT-80, Zhang/Wang-style MCND, pairs_per_sample=16
r6: acc_mean ~= 0.8822, AUC_mean ~= 0.9519
r7: acc_mean ~= 0.5000, AUC_mean ~= 0.5060
r8: acc_mean ~= 0.5000, AUC_mean ~= 0.5037
```

Interpretation:

- `C || C' || Delta || InvP(Delta)` is strong at r6.
- Plain SPN-aligned matrix features fail at r7/r8.
- Continue pursuing r7 through public S-box inverse / DDT trail evidence, not generic deeper matrix/global variants.

## SPN Next Experiments

Priority 1: SInv curriculum r7

```text
run_id: innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616
plan: experiments/innovation1/plans/innovation1_spn_present_sinv_curriculum_r7_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_sinv_curriculum_r7_gpu0_20260616.json
feature: present_pair_xor_paligned_sinv_cell_matrix_bits
model: present_inception_mcnd_matrix
key_rotation_interval: 1024
```

Priority 2: delta-only structural r7

```text
run_id: innovation1-spn-present-delta-only-structural-r7-gpu0-20260616
plan: experiments/innovation1/plans/innovation1_spn_present_delta_only_structural_r7_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_delta_only_structural_r7_gpu0_20260616.json
```

Purpose:

- Diagnose whether raw `C,C'` fields are drowning weak r7 structural evidence.

Priority 3: SBox-DDT TrailMixer curriculum highround

```text
run_id: innovation1-spn-present-sboxddt-trailmixer-curriculum-highround-gpu0-20260615
plan: experiments/innovation1/plans/innovation1_spn_present_sboxddt_trailmixer_curriculum_highround_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_sboxddt_trailmixer_curriculum_highround_gpu0_20260615.json
feature family: back2 / beam2 public DDT trail
model: present_trail_mixer_pairset
```

Gate:

- r7 AUC must exceed about 0.53 in a repeatable way before scaling to 10 seeds.
- If SInv and delta-only both fail, implement parameterized DDT beam/stat trail search instead of adding more generic matrix models.
