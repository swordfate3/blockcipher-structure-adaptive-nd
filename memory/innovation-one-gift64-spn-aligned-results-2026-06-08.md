# Memory: GIFT-64 SPN Aligned Screen Results

Date: 2026-06-08

## Run

```text
run_id: innovation1-spn-gift64-aligned-screen-gpu1-20260608
result_dir: outputs/remote_results/innovation1-spn-gift64-aligned-screen-gpu1-20260608
cipher: GIFT-64
model: spn_token_mixer_pairset
```

Gate:

```text
result_lines=24
expected_rows=24
stderr=0 bytes
```

## Purpose

This run tests whether the SPN aligned-input effect observed on PRESENT transfers to another lightweight SPN cipher.  The compared inputs are:

```text
raw:     C || C' || Delta C
aligned: C || C' || Delta C || P_gift^-1(Delta C)
```

`P_gift^-1` is the public inverse bit permutation of GIFT-64 and does not use key material.

## Protocol

- cipher: GIFT-64
- model: `spn_token_mixer_pairset`
- rounds: 4, 5, 6
- seeds: 0, 1, 2, 3
- train key: `0x00000000000000000000000000000000`
- validation key: `0x11111111111111111111111111111111`
- negative mode: `encrypted_random_plaintexts`
- samples per class: 32768
- pairs per sample: 4
- epochs: 8
- difference profile: `gift64_shen2024_spn_screen`

## Raw vs Aligned Results

| rounds | feature | runs | calibrated acc | AUC | loss |
|---:|---|---:|---:|---:|---:|
| 4 | raw | 4 | 0.986298 | 0.998864 | 0.048102 |
| 4 | aligned | 4 | 0.998611 | 0.999980 | 0.006919 |
| 5 | raw | 4 | 0.761864 | 0.841192 | 0.493644 |
| 5 | aligned | 4 | 0.867210 | 0.941049 | 0.310727 |
| 6 | raw | 4 | 0.502701 | 0.499632 | 0.693217 |
| 6 | aligned | 4 | 0.520088 | 0.525192 | 0.690538 |

Aligned minus raw:

| rounds | calibrated acc delta | AUC delta | loss delta |
|---:|---:|---:|---:|
| 4 | +0.012314 | +0.001116 | -0.041183 |
| 5 | +0.105347 | +0.099857 | -0.182916 |
| 6 | +0.017387 | +0.025560 | -0.002680 |

Paired seed deltas:

| rounds | calibrated acc deltas | positive | AUC deltas | positive |
|---:|---|---:|---|---:|
| 4 | +0.014008, +0.011139, +0.011871, +0.012238 | 4/4 | +0.001326, +0.000858, +0.001106, +0.001173 | 4/4 |
| 5 | +0.079498, +0.077454, +0.138641, +0.125793 | 4/4 | +0.073581, +0.071689, +0.131156, +0.123001 | 4/4 |
| 6 | +0.059021, +0.008545, +0.000916, +0.001068 | 4/4 | +0.084924, +0.012936, +0.001882, +0.002498 | 4/4 |

Across the 12 paired seed-round comparisons, aligned input is positive in all 12.

## Interpretation

The GIFT-64 screen strongly supports SPN-family transfer.  PRESENT was not just a single-cipher special case: replacing PRESENT's inverse P-layer with GIFT-64's public inverse bit permutation still improves the same SPN TokenMixer pair-set distinguisher.

The strongest evidence is round 5:

```text
calibrated accuracy: 0.761864 -> 0.867210, delta +0.105347
AUC:                 0.841192 -> 0.941049, delta +0.099857
```

Round 4 is already easy, so the improvement is small but consistent.  Round 6 is near the current boundary; raw is essentially random, while aligned remains slightly positive across all seeds.

## Claim Boundary

Supported claim:

```text
For lightweight SPN block ciphers, a public inverse-permutation aligned output-difference representation can improve a matching SPN TokenMixer neural distinguisher across more than one cipher family member: PRESENT-80 and GIFT-64.
```

Do not overclaim:

- this is a GIFT-64 screening profile, not a full reproduction of every GIFT-128 / score-distribution protocol in the literature;
- seeds are 0..3, so a 10-seed confirmation should be run before using this as a final paper-grade main table;
- round 6 remains close to the weak-signal boundary.

## Next Step

Run a focused confirmation:

```text
GIFT-64 rounds 5 and 6
raw vs aligned
seeds 0..9
same cross-key encrypted-negative protocol
expected rows = 40
```
