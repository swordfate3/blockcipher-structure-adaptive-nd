# Zhang/Wang 2022 PRESENT MCND Reproduction Track

This note records the project-local reproduction scaffold for Zhang/Wang 2022,
`Improving Differential-Neural Distinguisher Model For DES, Chaskey, and PRESENT`
(arXiv:2204.06341). The aim is to separate a literature reproduction baseline
from innovation-one structure-adaptive experiments.

## Literature Target

The paper reports improved differential-neural distinguishers for 6-7 round
PRESENT. The PRESENT input difference is represented as four 16-bit words:

```text
(0, 0, 0, 0x9)
```

In this project this is encoded as the 64-bit xor difference:

```text
0x0000000000000009
```

The reproduction scaffold uses the model family:

```text
present_inception_mcnd
```

with configurable Inception branch kernel sizes. For the Zhang/Wang track, the
plan passes:

```json
{"kernel_sizes": [1, 2, 4], "blocks": 3, "dropout": 0.0, "pooling": "attention_mean_max"}
```

## Project Protocol

New difference profile:

```text
present_zhang_wang2022_mcnd -> 0x0000000000000009
```

New sample structure:

```text
zhang_wang_case2_mcnd
```

This sample structure creates one MCND sample from `m = pairs_per_sample`
ciphertext pairs. The pairs share one random base plaintext and use random public
plaintext masks before applying the fixed input difference. This is intended to
move away from fully independent pair-set generation toward the grouped MCND
Case-2 style used by the literature.

Current caveat: this is still a reproduction scaffold, not a confirmed exact
line-by-line reproduction. The next validation criterion is empirical: 6-round
PRESENT should separate clearly before spending large GPU time on 7-round or
8-round experiments.

## Plans

Smoke plan:

```text
experiments/innovation1/plans/innovation1_spn_present_zhang_wang2022_mcnd_smoke.csv
```

Medium plan:

```text
experiments/innovation1/plans/innovation1_spn_present_zhang_wang2022_mcnd_medium.csv
```

Medium run protocol:

```text
rounds: 6, 7
seeds: 0, 1, 2
samples_per_class: 8192
pairs_per_sample: 16
feature_encoding: ciphertext_pair_bits
negative_mode: encrypted_random_plaintexts
sample_structure: zhang_wang_case2_mcnd
key_rotation_interval: 1024
```

## Interpretation Rules

- If 6-round remains near random, do not claim a Zhang/Wang reproduction.
- If 6-round becomes strong but 7-round remains weak, increase training scale
  and check exact Case-1/Case-2 details.
- Only after a credible 7-round baseline should innovation-one aligned inputs or
  P-aligned/integral variants be attached to this reproduction baseline.
