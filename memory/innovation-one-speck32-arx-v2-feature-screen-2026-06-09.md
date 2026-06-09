# Memory: SPECK32/64 ARX v2 Feature Screen Prepared (2026-06-09)

Prepared next ARX innovation-one screen after v1 rotation-only aligned input showed only a small 6-round gain and no 7-round gain.

New feature encodings:

- `ciphertext_pair_xor_arx_partial_inverse_bits`: raw + rotation aligned + keyless partial inverse `pre_y=ROR2(y xor x)`, `pre_y_prime`, and `Delta_pre_y`.
- `ciphertext_pair_xor_arx_partial_inverse_rx_bits`: v2 + RX alpha/beta views + public carry-inspired output-word proxies.

Widths for SPECK32/64 single pair:

- raw: 96 bits
- rotation v1: 128 bits
- partial inverse v2: 224 bits
- partial inverse RX/carry v3: 352 bits

Remote screen:

- run id: `innovation1-arx-speck32-v2-feature-screen-gpu1-20260609`
- expected rows: 32
- rounds: 6, 7
- seeds: 0..3
- features: raw, v1 rotation, v2 partial inverse, v3 partial inverse RX/carry
- samples_per_class: 32768
- pairs_per_sample: 4
- model: `structure_adaptive_pairset_dbitnet`
- device: cuda:1

Validation completed:

- related tests: 39 passed
- full tests: 234 passed
- tiny smoke: all four features trained through `run_innovation_one_matrix.py` and reported expected input/pair widths.

Next: commit, push main, start remote schedule script, and monitor result branch.
