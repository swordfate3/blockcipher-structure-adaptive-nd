# 2026-06-09 SPECK32/64 ARX v2 10-Seed Confirmation Plan

## Purpose

The 4-seed ARX v2 feature screen found that `ciphertext_pair_xor_arx_partial_inverse_bits` is the best SPECK32/64 round-7 feature so far. This run promotes that feature to a 10-seed confirmation against two same-protocol baselines.

## Compared Features

```text
raw:             ciphertext_pair_xor_bits
rotation v1:     ciphertext_pair_xor_arx_aligned_bits
partial inv v2:  ciphertext_pair_xor_arx_partial_inverse_bits
```

v3 RX/carry-inspired features are intentionally excluded from this confirmation because the screen showed that v3 is weaker than v2 on round 7 and hurts round 6.

## Remote Run

```text
run_id: innovation1-arx-speck32-v2-confirm-10seed-gpu1-20260609
plan: experiments/plans/innovation1_arx_speck32_v2_confirm_10seed.csv
expected_rows: 30
device: cuda:1
```

Protocol:

- cipher: SPECK32/64
- structure: ARX
- model: `structure_adaptive_pairset_dbitnet`
- rounds: 7
- seeds: 0..9
- samples per class: 32768
- pairs per sample: 4
- negative mode: `encrypted_random_plaintexts`
- train key: `0x1918111009080100`
- validation key: `0x0f0e0d0c0b0a0908`
- difference profile: `speck32_gohr2019`
- epochs: 8

## Decision Rule

The key check is paired seed-wise delta between v2 and raw. If v2 remains positive on most or all seeds with a mean calibrated-accuracy delta near the 4-seed screen value (`+0.014908`) and AUC delta near `+0.020054`, record v2 as ARX structure-adapted feature evidence.

If the 10-seed result collapses toward raw, stop adding handcrafted ARX views and prioritize an ARX-specific `ArxWordMixerPairSet` model.
