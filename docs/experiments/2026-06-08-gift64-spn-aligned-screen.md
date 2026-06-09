# GIFT-64 SPN Aligned Results

Date: 2026-06-08/09

## Purpose

This experiment tests whether the SPN aligned-input effect observed on PRESENT transfers to another lightweight SPN cipher. The compared inputs are:

```text
raw:     C || C' || Delta C
aligned: C || C' || Delta C || P_gift^-1(Delta C)
```

`P_gift^-1` is the public inverse bit permutation of GIFT-64 and does not use key material.

## Screen Run

```text
run_id: innovation1-spn-gift64-aligned-screen-gpu1-20260608
result_dir: outputs/remote_results/innovation1-spn-gift64-aligned-screen-gpu1-20260608
cipher: GIFT-64
model: spn_token_mixer_pairset
result_lines: 24
expected_rows: 24
stderr: 0 bytes
```

Protocol:

- rounds: 4, 5, 6
- seeds: 0, 1, 2, 3
- train key: `0x00000000000000000000000000000000`
- validation key: `0x11111111111111111111111111111111`
- negative mode: `encrypted_random_plaintexts`
- samples per class: 32768
- pairs per sample: 4
- epochs: 8
- difference profile: `gift64_shen2024_spn_screen`

Screen results:

| rounds | feature | runs | calibrated acc | AUC | loss |
|---:|---|---:|---:|---:|---:|
| 4 | raw | 4 | 0.986298 | 0.998864 | 0.048102 |
| 4 | aligned | 4 | 0.998611 | 0.999980 | 0.006919 |
| 5 | raw | 4 | 0.761864 | 0.841192 | 0.493644 |
| 5 | aligned | 4 | 0.867210 | 0.941049 | 0.310727 |
| 6 | raw | 4 | 0.502701 | 0.499632 | 0.693217 |
| 6 | aligned | 4 | 0.520088 | 0.525192 | 0.690538 |

Screen aligned minus raw:

| rounds | calibrated acc delta | AUC delta | positive seeds |
|---:|---:|---:|---:|
| 4 | +0.012314 | +0.001116 | 4/4 |
| 5 | +0.105347 | +0.099857 | 4/4 |
| 6 | +0.017387 | +0.025560 | 4/4 |

Across the 12 paired seed-round comparisons in the screen, aligned input is positive in all 12.

## 10-Seed Confirmation Run

```text
run_id: innovation1-spn-gift64-aligned-confirm-10seed-gpu0-20260608
result_dir: outputs/remote_results/innovation1-spn-gift64-aligned-confirm-10seed-gpu0-20260608
cipher: GIFT-64
model: spn_token_mixer_pairset
result_lines: 40
expected_rows: 40
stderr: 0 bytes
git_revision: 7c59d1798589e0b0654785cb8a44405066e8cb58
```

Protocol:

- rounds: 5, 6
- seeds: 0..9
- train key: `0x00000000000000000000000000000000`
- validation key: `0x11111111111111111111111111111111`
- negative mode: `encrypted_random_plaintexts`
- samples per class: 32768
- pairs per sample: 4
- epochs: 8
- difference profile: `gift64_shen2024_spn_screen`

Confirmation results:

| rounds | feature | runs | accuracy mean | accuracy std | calibrated acc mean | calibrated acc std | AUC mean | AUC std | loss mean |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | raw | 10 | 0.745639 | 0.019430 | 0.750476 | 0.022337 | 0.828513 | 0.024495 | 0.508216 |
| 5 | aligned | 10 | 0.864676 | 0.009080 | 0.867969 | 0.006999 | 0.941747 | 0.004996 | 0.311885 |
| 6 | raw | 10 | 0.500638 | 0.002145 | 0.503983 | 0.001752 | 0.501735 | 0.003385 | 0.693210 |
| 6 | aligned | 10 | 0.508237 | 0.017224 | 0.518094 | 0.017910 | 0.522215 | 0.025784 | 0.692082 |

Confirmation aligned minus raw:

| rounds | calibrated acc delta mean | calibrated acc delta std | AUC delta mean | positive seeds |
|---:|---:|---:|---:|---:|
| 5 | +0.117493 | 0.026484 | +0.113235 | 10/10 |
| 6 | +0.014111 | 0.017478 | +0.020479 | 9/10 |

Per-seed calibrated accuracy deltas:

```text
round 5: +0.142395, +0.077454, +0.138641, +0.125793, +0.110352,
         +0.132629, +0.141052, +0.114044, +0.131836, +0.060730
round 6: +0.013092, +0.008545, +0.000916, +0.001068, -0.001160,
         +0.019775, +0.005493, +0.054443, +0.001373, +0.037567
```

## Interpretation

The 10-seed confirmation strongly supports SPN-family transfer. PRESENT was not just a single-cipher special case: replacing PRESENT's inverse P-layer with GIFT-64's public inverse bit permutation still improves the same SPN TokenMixer pair-set distinguisher.

The strongest evidence is round 5 in the confirmation run:

```text
calibrated accuracy: 0.750476 -> 0.867969, delta +0.117493
AUC:                 0.828513 -> 0.941747, delta +0.113235
positive seeds:      10/10
```

Round 6 remains close to the weak-signal boundary. Raw is essentially random, while aligned remains slightly positive on average with 9/10 seeds positive. This is useful as boundary evidence, but the paper-grade claim should emphasize round 5.

## Claim Boundary

Supported claim:

```text
For lightweight SPN block ciphers, a public inverse-permutation aligned output-difference representation improves a matching SPN TokenMixer neural distinguisher across more than one cipher family member. The effect is confirmed on PRESENT-80 and GIFT-64, with GIFT-64 round-5 showing a 10-seed calibrated-accuracy improvement of +0.117493 under a cross-key encrypted-negative protocol.
```

Do not overclaim:

- this is a GIFT-64 screening/confirmation profile, not a full reproduction of every GIFT-128 or score-distribution protocol in the literature;
- round 6 is only a weak-signal boundary result, not a strong high-round distinguisher;
- the difference profile is fixed to `gift64_shen2024_spn_screen` and should be refined if a literature-exact GIFT differential is later adopted.

## Next Step

Use the GIFT-64 10-seed confirmation as a main SPN transfer table. Next innovation-one work should either:

- expand the same SPN aligned protocol to another SPN cipher if implementation/profiles are ready, or
- improve the ARX/SPECK branch, because ARX currently shows only a small 6-round gain and no 7-round gain.
