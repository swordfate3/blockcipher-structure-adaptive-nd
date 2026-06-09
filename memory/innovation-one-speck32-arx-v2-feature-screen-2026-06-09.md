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
## Screen Results Retrieved

The remote screen completed and was retrieved locally.

```text
run_id: innovation1-arx-speck32-v2-feature-screen-gpu1-20260609
result_dir: outputs/remote_results/innovation1-arx-speck32-v2-feature-screen-gpu1-20260609/
result_lines: 32
expected_rows: 32
stderr: 0 bytes
git_revision: 6324782a712e8d649e1e0e6424bcec64b08d470f
```

Round-7 key result over 4 seeds:

```text
raw cal_acc:                  0.512062
rotation v1 cal_acc:          0.513641, delta +0.001579, positive seeds 2/4
partial inverse v2 cal_acc:   0.526970, delta +0.014908, positive seeds 4/4
partial inverse v2 AUC:       0.534486, delta +0.020054
partial inverse RX v3 cal_acc:0.518944, delta +0.006882, positive seeds 4/4
```

Interpretation: v2 keyless partial inverse is the best ARX round-7 feature so far. It is still weak-signal evidence, not a high-round breakthrough, but it supports the ARX-specific structure-alignment direction better than rotation-only v1. v3 is not promoted because it is weaker than v2 and hurts round 6.

Next promoted run:

```text
run_id: innovation1-arx-speck32-v2-confirm-10seed-gpu1-20260609
expected_rows: 30
rounds: 7
seeds: 0..9
features: raw, rotation v1, partial inverse v2
```
## Scale Ablation Launched

After 10-seed confirmation, ARX v2 partial inverse improved SPECK32/64 round-7 over raw by `+0.031409` calibrated accuracy and `+0.044881` AUC with 10/10 positive seeds. The absolute value is still below known SPECK32/64 7-round neural distinguisher frontiers, so the next test is a scale ablation.

Small scale is already covered by the 10-seed confirmation:

```text
samples_per_class=32768, epochs=8
```

New remote scale runs:

```text
innovation1-arx-speck32-v2-scale-m-gpu0-20260609
samples_per_class=131072, epochs=16, expected_rows=8

innovation1-arx-speck32-v2-scale-l-gpu1-20260609
samples_per_class=524288, epochs=24, expected_rows=8
```

Both compare only raw versus `ciphertext_pair_xor_arx_partial_inverse_bits` for rounds=7, seeds=0..3, pairs_per_sample=4. These runs test whether data/epoch scale lifts the absolute accuracy/AUC or whether the next bottleneck is ARX-specific model architecture.
