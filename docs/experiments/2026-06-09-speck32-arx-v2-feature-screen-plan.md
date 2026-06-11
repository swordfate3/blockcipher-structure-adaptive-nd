# 2026-06-09 SPECK32/64 ARX v2 Feature Screen Plan

## Purpose

The first ARX aligned screen only added SPECK public rotation-aligned output differences. It improved round 6 slightly but did not move round 7 away from random. This screen tests richer ARX-specific public features that target keyless partial inverse structure, RX views, and carry-inspired proxies.

## Feature Encodings

Baseline raw:

```text
ciphertext_pair_xor_bits = C || C_prime || Delta_C
```

ARX v1 rotation aligned:

```text
ciphertext_pair_xor_arx_aligned_bits
= C || C_prime || Delta_C || (ROR7(Delta_L) || ROL2(Delta_R))
```

ARX v2 keyless partial inverse:

```text
ciphertext_pair_xor_arx_partial_inverse_bits
= raw || rotation_aligned || pre_y || pre_y_prime || Delta_pre_y
```

For SPECK32/64 ciphertext words `C = x || y` and `C_prime = x_prime || y_prime`:

```text
pre_y       = ROR2(y xor x)
pre_y_prime = ROR2(y_prime xor x_prime)
Delta_pre_y = pre_y xor pre_y_prime
```

This uses the public final SPECK relation `y_out = ROL2(y_in) xor x_out` and does not use the key.

ARX v3 partial inverse + RX/carry-inspired views:

```text
ciphertext_pair_xor_arx_partial_inverse_rx_bits
= v2 || RX_alpha || RX_beta || carry_left_delta || carry_right_delta
```

where alpha=7 and beta=2 are SPECK32/64 public rotation constants. The carry terms are public output-word carry proxies, not claimed as true internal carries.

## Widths

For SPECK32/64 one ciphertext pair:

| feature | pair bits |
| --- | ---: |
| raw | 96 |
| arx_rotation_v1 | 128 |
| arx_partial_inverse_v2 | 224 |
| arx_partial_inverse_rx_v3 | 352 |

With `pairs_per_sample=4`, model input widths are 384, 512, 896, and 1408 bits respectively.

## Remote Screen

```text
run_id: innovation1-arx-speck32-v2-feature-screen-gpu1-20260609
plan: experiments/innovation1/plans/innovation1_arx_speck32_v2_feature_screen.csv
expected_rows: 32
device: cuda:1
```

Protocol:

- cipher: SPECK32/64
- model: `structure_adaptive_pairset_dbitnet`
- rounds: 6, 7
- seeds: 0, 1, 2, 3
- samples per class: 32768
- pairs per sample: 4
- negative mode: `encrypted_random_plaintexts`
- train key: `0x1918111009080100`
- validation key: `0x0f0e0d0c0b0a0908`
- difference profile: `speck32_gohr2019`
- epochs: 8

## Local Verification

```text
uv run pytest tests/test_feature_encodings.py tests/test_build_plan_config.py tests/test_experiment_matrix_runner.py tests/test_remote_script_generator.py -q
39 passed

uv run pytest -q
234 passed
```

Tiny smoke with 2 pairs per sample:

```text
raw                         input_bits=192 pair_bits=96
arx_rotation_v1             input_bits=256 pair_bits=128
arx_partial_inverse_v2      input_bits=448 pair_bits=224
arx_partial_inverse_rx_v3   input_bits=704 pair_bits=352
```

## Decision Rule

If v2 or v3 raises SPECK32/64 round-7 calibrated accuracy meaningfully above the current random-near value (~0.513), promote the best feature to a 10-seed confirmation and then implement an ARX-specific WordMixer PairSet expert. If v2/v3 do not move round 7, prioritize model architecture rather than adding more handcrafted public features.
## Remote Screen Result

```text
run_id: innovation1-arx-speck32-v2-feature-screen-gpu1-20260609
result_dir: outputs/remote_results/innovation1-arx-speck32-v2-feature-screen-gpu1-20260609/
result_lines: 32
expected_rows: 32
stderr: 0 bytes
git_revision: 6324782a712e8d649e1e0e6424bcec64b08d470f
torch: 2.5.1+cu118, CUDA 11.8, NVIDIA RTX A6000
```

Mean metrics over 4 seeds:

| rounds | feature | cal acc | AUC | loss |
| ---: | --- | ---: | ---: | ---: |
| 6 | raw | 0.873116 | 0.939337 | 0.334800 |
| 6 | arx_rotation_v1 | 0.882629 | 0.947729 | 0.326541 |
| 6 | arx_partial_inverse_v2 | 0.880707 | 0.945169 | 0.332285 |
| 6 | arx_partial_inverse_rx_v3 | 0.848808 | 0.919873 | 0.407781 |
| 7 | raw | 0.512062 | 0.514432 | 0.782776 |
| 7 | arx_rotation_v1 | 0.513641 | 0.516397 | 0.732386 |
| 7 | arx_partial_inverse_v2 | 0.526970 | 0.534486 | 0.732185 |
| 7 | arx_partial_inverse_rx_v3 | 0.518944 | 0.524476 | 0.718798 |

Deltas versus raw:

| rounds | feature | cal acc delta | AUC delta | positive seeds |
| ---: | --- | ---: | ---: | ---: |
| 6 | arx_rotation_v1 | +0.009514 | +0.008392 | 4/4 |
| 6 | arx_partial_inverse_v2 | +0.007591 | +0.005831 | 4/4 |
| 6 | arx_partial_inverse_rx_v3 | -0.024307 | -0.019464 | 0/4 |
| 7 | arx_rotation_v1 | +0.001579 | +0.001965 | 2/4 |
| 7 | arx_partial_inverse_v2 | +0.014908 | +0.020054 | 4/4 |
| 7 | arx_partial_inverse_rx_v3 | +0.006882 | +0.010044 | 4/4 |

Interpretation: ARX v2 keyless partial inverse is the best round-7 feature in this screen. It remains a weak distinguisher region, but the improvement is stable over all 4 seeds and larger than the rotation-only v1 feature. The v3 RX/carry-inspired expansion does not help round 6 and is weaker than v2 on round 7, so it is not promoted to the first confirmation run.

## Promotion to 10-Seed Confirmation

The promoted confirmation keeps only round 7 and compares raw, rotation v1, and partial-inverse v2 under the same protocol:

```text
run_id: innovation1-arx-speck32-v2-confirm-10seed-gpu1-20260609
plan: experiments/innovation1/plans/innovation1_arx_speck32_v2_confirm_10seed.csv
expected_rows: 30
rounds: 7
seeds: 0..9
features: raw, arx_rotation_v1, arx_partial_inverse_v2
```

Decision after confirmation: if v2 keeps a positive paired delta over most or all seeds, record it as ARX structure-adapted feature evidence for innovation one. If the 10-seed mean collapses, move ARX work to a dedicated word/rotation/carry-aware model instead of adding more handcrafted public views.
