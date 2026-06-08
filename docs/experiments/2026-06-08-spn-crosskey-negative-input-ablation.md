# Innovation One SPN Protocol Stress Results

Date: 2026-06-08

## Runs

- `innovation1-spn-crosskey-negative-present-gpu0-20260607`
- `innovation1-spn-input-ablation-present-gpu1-20260607`

Local result paths:

```text
outputs/remote_results/innovation1-spn-crosskey-negative-present-gpu0-20260607/
outputs/remote_results/innovation1-spn-input-ablation-present-gpu1-20260607/
```

Gate:

```text
innovation1-spn-crosskey-negative-present-gpu0-20260607: 48 / 48 rows, stderr 0 bytes
innovation1-spn-input-ablation-present-gpu1-20260607: 24 / 24 rows, stderr 0 bytes
```

## Purpose

This experiment validates whether the previous PRESENT/SPN aligned-input gain is robust to common protocol concerns:

- fixed-key overfitting,
- overly easy random-ciphertext negative samples,
- apparent improvement caused only by adding more input bits.

The tested method is the SPN-TokenMixer pair-set distinguisher with a public inverse-P-layer aligned representation:

```text
raw full pair:      C || C' || Delta C
aligned full pair:  C || C' || Delta C || P^-1(Delta C)
delta only:         Delta C
aligned delta only: Delta C || P^-1(Delta C)
```

`P^-1` is PRESENT's public inverse permutation layer and does not use key material.

## Cross-Key And Negative-Sample Stress Test

Protocol:

- cipher: PRESENT-80
- model: `spn_token_mixer_pairset`
- rounds: 5 and 6
- seeds: 0, 1, 2
- train key: `0x00000000000000000000`
- validation keys: same all-zero key and unseen `0x11111111111111111111`
- negative modes: `random_ciphertext` and `encrypted_random_plaintexts`
- samples per class: 32768
- pairs per sample: 4
- epochs: 10

| rounds | feature | negative | validation key | n | acc mean | acc std | AUC mean | AUC std |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 5 | raw | `encrypted_random_plaintexts` | same | 3 | 0.797831 | 0.004971 | 0.875394 | 0.004552 |
| 5 | raw | `encrypted_random_plaintexts` | unseen 0x111... | 3 | 0.787679 | 0.003201 | 0.864653 | 0.003121 |
| 5 | raw | `random_ciphertext` | same | 3 | 0.791117 | 0.005701 | 0.869812 | 0.007791 |
| 5 | raw | `random_ciphertext` | unseen 0x111... | 3 | 0.783834 | 0.002204 | 0.861593 | 0.001873 |
| 5 | aligned | `encrypted_random_plaintexts` | same | 3 | 0.807882 | 0.000593 | 0.886152 | 0.001056 |
| 5 | aligned | `encrypted_random_plaintexts` | unseen 0x111... | 3 | 0.806376 | 0.001753 | 0.882153 | 0.000521 |
| 5 | aligned | `random_ciphertext` | same | 3 | 0.809601 | 0.001245 | 0.886802 | 0.000569 |
| 5 | aligned | `random_ciphertext` | unseen 0x111... | 3 | 0.805868 | 0.002642 | 0.882139 | 0.001149 |
| 6 | raw | `encrypted_random_plaintexts` | same | 3 | 0.520874 | 0.018960 | 0.525979 | 0.026199 |
| 6 | raw | `encrypted_random_plaintexts` | unseen 0x111... | 3 | 0.520976 | 0.018495 | 0.525256 | 0.025193 |
| 6 | raw | `random_ciphertext` | same | 3 | 0.515055 | 0.012025 | 0.518365 | 0.017201 |
| 6 | raw | `random_ciphertext` | unseen 0x111... | 3 | 0.516144 | 0.011875 | 0.519816 | 0.018936 |
| 6 | aligned | `encrypted_random_plaintexts` | same | 3 | 0.583689 | 0.004301 | 0.617081 | 0.004544 |
| 6 | aligned | `encrypted_random_plaintexts` | unseen 0x111... | 3 | 0.585388 | 0.003793 | 0.617820 | 0.006002 |
| 6 | aligned | `random_ciphertext` | same | 3 | 0.585561 | 0.001433 | 0.618343 | 0.001699 |
| 6 | aligned | `random_ciphertext` | unseen 0x111... | 3 | 0.585602 | 0.000271 | 0.618968 | 0.000615 |

Aligned minus raw deltas:

| rounds | negative | validation key | seeds | acc delta | AUC delta |
|---:|---|---:|---:|---:|---:|
| 5 | `encrypted_random_plaintexts` | same | 3 | +0.010050 | +0.010759 |
| 5 | `encrypted_random_plaintexts` | unseen 0x111... | 3 | +0.018697 | +0.017500 |
| 5 | `random_ciphertext` | same | 3 | +0.018483 | +0.016990 |
| 5 | `random_ciphertext` | unseen 0x111... | 3 | +0.022034 | +0.020546 |
| 6 | `encrypted_random_plaintexts` | same | 3 | +0.062815 | +0.091101 |
| 6 | `encrypted_random_plaintexts` | unseen 0x111... | 3 | +0.064412 | +0.092564 |
| 6 | `random_ciphertext` | same | 3 | +0.070506 | +0.099978 |
| 6 | `random_ciphertext` | unseen 0x111... | 3 | +0.069458 | +0.099152 |

Strictest condition: unseen validation key + `encrypted_random_plaintexts` negative samples.

| rounds | seed | acc delta | AUC delta |
|---:|---:|---:|---:|
| 5 | 0 | +0.020477 | +0.017034 |
| 5 | 1 | +0.022461 | +0.020318 |
| 5 | 2 | +0.013153 | +0.015147 |
| 6 | 0 | +0.072510 | +0.100999 |
| 6 | 1 | +0.081238 | +0.118483 |
| 6 | 2 | +0.039490 | +0.058210 |

### Interpretation

The aligned representation remains positive in every tested cross-key and negative-sample condition. Under the stricter unseen-key encrypted-random-plaintext protocol, aligned input improves:

- round 5 accuracy from `0.787679` to `0.806376`, delta `+0.018697`;
- round 6 accuracy from `0.520976` to `0.585388`, delta `+0.064412`;
- round 6 AUC from `0.525256` to `0.617820`, delta `+0.092564`.

The six strict per-seed deltas are all positive, so the effect is not driven by a single lucky seed.

## Input Ablation

Protocol:

- cipher: PRESENT-80
- model: `spn_token_mixer_pairset`
- rounds: 5 and 6
- seeds: 0, 1, 2
- train key: `0x00000000000000000000`
- validation key: unseen `0x11111111111111111111`
- negative mode: `encrypted_random_plaintexts`

| rounds | feature | n | acc mean | acc std | AUC mean | AUC std |
|---:|---|---:|---:|---:|---:|---:|
| 5 | `C || C' || Delta C` | 3 | 0.787679 | 0.003201 | 0.864653 | 0.003121 |
| 5 | `C || C' || Delta C || P^-1(Delta C)` | 3 | 0.806376 | 0.001753 | 0.882153 | 0.000521 |
| 5 | `Delta C` only | 3 | 0.789591 | 0.004732 | 0.867515 | 0.003139 |
| 5 | `Delta C || P^-1(Delta C)` | 3 | 0.809784 | 0.001510 | 0.885429 | 0.002296 |
| 6 | `C || C' || Delta C` | 3 | 0.520976 | 0.018495 | 0.525256 | 0.025193 |
| 6 | `C || C' || Delta C || P^-1(Delta C)` | 3 | 0.585388 | 0.003793 | 0.617820 | 0.006002 |
| 6 | `Delta C` only | 3 | 0.547089 | 0.004737 | 0.565358 | 0.004877 |
| 6 | `Delta C || P^-1(Delta C)` | 3 | 0.589895 | 0.001102 | 0.624002 | 0.000708 |

Aligned minus raw deltas:

| rounds | comparison | seeds | acc delta | AUC delta |
|---:|---|---:|---:|---:|
| 5 | full pair aligned - raw | 3 | +0.018697 | +0.017500 |
| 5 | delta-only aligned - raw | 3 | +0.020192 | +0.017914 |
| 6 | full pair aligned - raw | 3 | +0.064412 | +0.092564 |
| 6 | delta-only aligned - raw | 3 | +0.042806 | +0.058644 |

### Interpretation

`Delta C || P^-1(Delta C)` improves over `Delta C` alone, even without raw `C` and `C'` bits. This supports the claim that `P^-1(Delta C)` itself contributes SPN structural information, rather than merely increasing the input size.

The delta-only aligned feature is especially interesting:

- round 5: `0.809784` acc, slightly above full aligned pair `0.806376`;
- round 6: `0.589895` acc, slightly above full aligned pair `0.585388`.

This suggests that under cross-key validation, raw ciphertext bits may add some key/randomness noise, while output-difference structure and inverse-P alignment are the most stable signal.

## Current Claim Boundary

Supported claim:

```text
For PRESENT/SPN reduced-round neural differential distinguishing, public inverse-P-layer aligned output-difference features improve a matching nibble-token mixer under same-key, cross-key, random-ciphertext negative, and encrypted-random-plaintext negative protocols.
```

Do not overclaim:

- not a full key-recovery attack;
- not yet universal across all SPN ciphers;
- current strict protocol uses 3 seeds and should be expanded to 10 seeds for final paper-grade statistics.

## Next Experiment

Run 10 seeds under the strictest and most paper-relevant protocol:

- PRESENT-80 rounds 5 and 6;
- `spn_token_mixer_pairset`;
- raw full pair vs aligned full pair;
- train key all zero;
- validation key `0x11111111111111111111`;
- negative mode `encrypted_random_plaintexts`;
- seeds 0..9.

Expected rows: `2 rounds * 2 encodings * 10 seeds = 40`.
