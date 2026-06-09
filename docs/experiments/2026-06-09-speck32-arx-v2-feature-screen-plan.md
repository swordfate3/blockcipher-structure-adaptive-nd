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
plan: experiments/plans/innovation1_arx_speck32_v2_feature_screen.csv
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
