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
plan: experiments/plans/innovation1_arx_speck32_v2_scale_m.csv
expected_rows: 8
device: cuda:0
samples_per_class: 131072
epochs: 16
```

Large scale:

```text
run_id: innovation1-arx-speck32-v2-scale-l-gpu1-20260609
plan: experiments/plans/innovation1_arx_speck32_v2_scale_l.csv
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
