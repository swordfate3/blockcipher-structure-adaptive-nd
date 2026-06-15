# Innovation 1 ARX Key Protocol Correction - 2026-06-16

## Why This Matters

The SPECK32/64 ARX line has a strong historical r7 result, but it must not be
reported as a strict multi-key result unless the run uses
`key_rotation_interval > 0`.

## Corrected Interpretation

The strongest historical ARX evidence remains:

```text
run_id: innovation1-arx-speck32-v2-scale-m-gpu0-20260609
cipher: SPECK32/64
rounds: 7
model: structure_adaptive_pairset_dbitnet
feature: ciphertext_pair_xor_arx_partial_inverse_bits
samples_per_class: 131072
pairs_per_sample: 4
seeds: 0,1,2,3
mean calibrated accuracy: about 0.789639
mean AUC: about 0.869151
```

This is strong structure-adaptation evidence, but the original plan/config used
a fixed training key and a fixed validation key. It is better described as:

```text
fixed training key + cross-key validation
```

It is not yet:

```text
key-rotating multi-key confirmation
```

## Code Change

Remote commit:

```text
697cc5e experiment: label innovation key protocols
```

The Innovation 1 summary now includes a `key_protocol` group/output field:

```text
key_rotating_multi_key
fixed_train_cross_key_validation
fixed_key
unspecified
```

Touched files:

```text
src/blockcipher_ai_eval/evaluation/summary.py
tests/test_evaluation_summary.py
```

Local verification:

```text
uv run pytest tests/test_evaluation_summary.py -q
4 passed
```

Remote note:

The remote `torch310` environment does not have `pytest`, so remote pytest was
not run. The patch was applied and pushed from the remote Windows workstation,
and the remote project HEAD is now `697cc5e`.

## Current ARX Queue State

As of the last check:

```text
active: innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
result lines: 2 / 8
device: cuda:1

queued by watcher: innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616
expected rows: 10
protocol: key_rotation_interval=1024, independent_pairs
status: waiting for GPU1 to be free

queued by watcher: innovation1-arx-speck32-round-stats-only-r7-screen-gpu1-20260616
expected rows: 6
status: waiting for GPU1 to be free
```

The partial-inverse 10-seed confirmation is the priority ARX experiment because
it converts the strongest historical fixed/cross-key result into a strict
multi-key confirmation if the signal survives.

## Reporting Rule

For ARX thesis/paper tables:

1. Report the old `0.789639 / 0.869151` result only as fixed-train-key with
   cross-key validation.
2. Use `innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616`
   as the decisive multi-key confirmation.
3. Do not scale carry-chain/carry-chain-plus based on current evidence; their
   r7 smoke results are near random.
