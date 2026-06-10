# Memory: SPECK32/64 ARX v2 Scale Results (2026-06-10)

## Run Context

Medium-scale ARX scale ablation completed on the remote Windows A6000 workstation.

```text
run_id: innovation1-arx-speck32-v2-scale-m-gpu0-20260609
result_dir: outputs/remote_results/innovation1-arx-speck32-v2-scale-m-gpu0-20260609/
cipher: SPECK32/64
rounds: 7
model: structure_adaptive_pairset_dbitnet
samples_per_class: 131072
validation_samples_per_class: 65536
pairs_per_sample: 4
epochs: 16
batch_size: 1024
optimizer: adamw
weight_decay: 0.0001
train_key: 0x1918111009080100
validation_key: 0x0f0e0d0c0b0a0908
difference_profile: speck32_gohr2019
negative_mode: encrypted_random_plaintexts
seeds: 0,1,2,3
```

The large-scale run `innovation1-arx-speck32-v2-scale-l-gpu1-20260609` produced only 1/8 rows before stopping, so it is not used as a paired feature comparison. Its first raw row reached calibrated accuracy `0.659544` and AUC `0.717728`, which suggests scale helps the raw signal, but it is incomplete.

## Medium-Scale Result

Feature comparison:

```text
raw feature: ciphertext_pair_xor_bits
ARX v2 feature: ciphertext_pair_xor_arx_partial_inverse_bits
```

Summary over 4 seeds:

| Feature | Mean calibrated accuracy | Mean AUC |
|---|---:|---:|
| raw | 0.543276 | 0.560338 |
| ARX v2 partial inverse | 0.789639 | 0.869151 |
| delta | +0.246363 | +0.308813 |

Per-seed paired comparison:

| seed | raw cal_acc | v2 cal_acc | delta cal_acc | raw AUC | v2 AUC | delta AUC |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.568916 | 0.796089 | +0.227173 | 0.595679 | 0.875474 | +0.279795 |
| 1 | 0.535156 | 0.776558 | +0.241402 | 0.549477 | 0.855342 | +0.305865 |
| 2 | 0.556122 | 0.797379 | +0.241257 | 0.578808 | 0.876711 | +0.297903 |
| 3 | 0.512909 | 0.788528 | +0.275620 | 0.517387 | 0.869077 | +0.351691 |

Stability:

```text
positive calibrated-accuracy seeds: 4/4
positive AUC seeds: 4/4
```

## Interpretation

This is the strongest ARX evidence so far. The keyless public partial-inverse feature is no longer just a weak improvement over raw input; under the same model, keys, input difference, negative mode, multi-pair setting, and training scale, it produces a large and consistent gain.

Safe thesis wording:

```text
For SPECK32/64 7-round neural distinguishing, the proposed ARX keyless partial-inverse representation significantly improves over raw ciphertext-pair-xor input under the same StructureAdaptive-PairSet-DBitNet protocol. At medium scale, calibrated accuracy improves from 0.5433 to 0.7896 and AUC from 0.5603 to 0.8692 across seeds 0..3.
```

Do not overclaim this as a direct universal SOTA result because the protocol differs from Gohr-style and later SPECK neural distinguisher settings. It is strong structure-adaptation evidence, not yet a full literature-frontier comparison.

## Engineering Note

The remote training finished with `result_lines=8` and `expected_rows=8`, but automatic result-branch push failed at summary generation because the run clone could not find:

```text
experiments/summarize_innovation_one_results.py
```

The generator was fixed afterward to create a minimal fallback summary when the summarizer is missing, so future successful training runs should still archive and push results. The M result was manually retrieved to local `outputs/remote_results/`.
