# 2026-06-09 SPECK32/64 ARX v2 Scale Ablation Plan

## Purpose

The 10-seed confirmation showed that `ciphertext_pair_xor_arx_partial_inverse_bits` improves SPECK32/64 round-7 weak distinguishing under the current medium-small training setup. However, the absolute accuracy remains below reported SPECK32/64 7-round neural distinguisher frontiers. This scale ablation tests whether the gap is partly caused by limited training samples and epochs.

The small baseline is already covered by:

```text
run_id: innovation1-arx-speck32-v2-confirm-10seed-gpu1-20260609
samples_per_class: 32768
epochs: 8
features: raw, rotation v1, partial inverse v2
seeds: 0..9
```

This plan adds two larger scales without repeating the small run.

## Scale Runs

Medium scale:

```text
run_id: innovation1-arx-speck32-v2-scale-m-gpu0-20260609
plan: experiments/innovation1/plans/innovation1_arx_speck32_v2_scale_m.csv
expected_rows: 8
device: cuda:0
samples_per_class: 131072
epochs: 16
```

Large scale:

```text
run_id: innovation1-arx-speck32-v2-scale-l-gpu1-20260609
plan: experiments/innovation1/plans/innovation1_arx_speck32_v2_scale_l.csv
expected_rows: 8
device: cuda:1
samples_per_class: 524288
epochs: 24
```

Common protocol:

- cipher: SPECK32/64
- rounds: 7
- model: `structure_adaptive_pairset_dbitnet`
- features: raw and ARX partial-inverse v2
- seeds: 0..3
- pairs per sample: 4
- negative mode: `encrypted_random_plaintexts`
- train key: `0x1918111009080100`
- validation key: `0x0f0e0d0c0b0a0908`
- difference profile: `speck32_gohr2019`

## Decision Rule

If raw and v2 both improve with scale, the current gap to the SPECK32/64 7-round frontier is partly a training-scale issue. If v2 remains clearly above raw but both stay near the 10-seed small-scale values, the next bottleneck is likely model architecture and training schedule.

Target signs:

- v2 paired delta remains positive across most seeds.
- v2 AUC increases with samples/epochs.
- raw should also move above random if the current training scale was suppressing the Gohr-profile signal.

If large-scale v2 approaches `0.58` to `0.60` calibrated accuracy or AUC moves substantially upward, promote ARX work to stronger architecture experiments. If it stays around `0.54`, prioritize `ArxWordMixerPairSet` before further scale increases.


## Medium-Scale Result

The medium-scale run completed on 2026-06-10 and was manually retrieved because the remote archive script failed after training at the summary-generation stage. The training gate itself passed: `result_lines=8`, `expected_rows=8`.

```text
run_id: innovation1-arx-speck32-v2-scale-m-gpu0-20260609
result_dir: outputs/remote_results/innovation1-arx-speck32-v2-scale-m-gpu0-20260609/
rows: 8/8
```

Summary over seeds 0..3:

| Feature | Mean calibrated accuracy | Mean AUC |
|---|---:|---:|
| raw `ciphertext_pair_xor_bits` | 0.543276 | 0.560338 |
| ARX v2 `ciphertext_pair_xor_arx_partial_inverse_bits` | 0.789639 | 0.869151 |
| delta | +0.246363 | +0.308813 |

Per-seed paired comparison:

| seed | raw cal_acc | v2 cal_acc | delta cal_acc | raw AUC | v2 AUC | delta AUC |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.568916 | 0.796089 | +0.227173 | 0.595679 | 0.875474 | +0.279795 |
| 1 | 0.535156 | 0.776558 | +0.241402 | 0.549477 | 0.855342 | +0.305865 |
| 2 | 0.556122 | 0.797379 | +0.241257 | 0.578808 | 0.876711 | +0.297903 |
| 3 | 0.512909 | 0.788528 | +0.275620 | 0.517387 | 0.869077 | +0.351691 |

All four seeds improved in both calibrated accuracy and AUC. This supports the thesis claim that ARX-specific public partial-inverse representation is a strong structure-adaptive input organization for SPECK32/64 under the current multi-pair StructureAdaptive-PairSet-DBitNet protocol.

The large-scale run produced only one raw row before stopping and is not used as a paired comparison.
