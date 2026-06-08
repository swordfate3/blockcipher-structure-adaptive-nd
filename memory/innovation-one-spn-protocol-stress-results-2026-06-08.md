# 创新一 SPN 协议压力测试结果记忆

更新时间：2026-06-08

## 核心结论

2026-06-08 已完成两组 PRESENT/SPN 结构对齐压力测试：

- `innovation1-spn-crosskey-negative-present-gpu0-20260607`：cross-key + negative-mode stress，48/48 rows，stderr 0。
- `innovation1-spn-input-ablation-present-gpu1-20260607`：input ablation，24/24 rows，stderr 0。

结果支持：

```text
P^-1(Delta C) 不是固定 key 偶然，也不是 random-ciphertext 负样本假象；
它在 unseen validation key 和 encrypted_random_plaintexts 负样本下仍然稳定提升 SPN-TokenMixer。
```

## 最严格条件结果

条件：

- PRESENT-80。
- train key = `0x00000000000000000000`。
- validation key = `0x11111111111111111111`。
- negative mode = `encrypted_random_plaintexts`。
- model = `spn_token_mixer_pairset`。
- seeds = 0,1,2。

| rounds | raw acc | aligned acc | acc delta | raw AUC | aligned AUC | AUC delta |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 0.787679 | 0.806376 | +0.018697 | 0.864653 | 0.882153 | +0.017500 |
| 6 | 0.520976 | 0.585388 | +0.064412 | 0.525256 | 0.617820 | +0.092564 |

每个 seed 都是正提升：

| rounds | seed | acc delta | AUC delta |
|---:|---:|---:|---:|
| 5 | 0 | +0.020477 | +0.017034 |
| 5 | 1 | +0.022461 | +0.020318 |
| 5 | 2 | +0.013153 | +0.015147 |
| 6 | 0 | +0.072510 | +0.100999 |
| 6 | 1 | +0.081238 | +0.118483 |
| 6 | 2 | +0.039490 | +0.058210 |

## 输入消融要点

跨 key + encrypted negative 下：

| rounds | feature | acc | AUC |
|---:|---|---:|---:|
| 5 | Delta C only | 0.789591 | 0.867515 |
| 5 | Delta C || P^-1(Delta C) | 0.809784 | 0.885429 |
| 5 | C || C' || Delta C | 0.787679 | 0.864653 |
| 5 | C || C' || Delta C || P^-1(Delta C) | 0.806376 | 0.882153 |
| 6 | Delta C only | 0.547089 | 0.565358 |
| 6 | Delta C || P^-1(Delta C) | 0.589895 | 0.624002 |
| 6 | C || C' || Delta C | 0.520976 | 0.525256 |
| 6 | C || C' || Delta C || P^-1(Delta C) | 0.585388 | 0.617820 |

解释：即使去掉原始密文 `C,C'`，只用 `Delta C || P^-1(Delta C)` 也有提升，说明结构对齐特征本身有效。

## 下一步

已决定推进 10 seeds 严格协议：

```text
rounds = 5,6
feature = ciphertext_pair_xor_bits vs ciphertext_pair_xor_spn_aligned_bits
negative_mode = encrypted_random_plaintexts
train_key = 0x00000000000000000000
validation_key = 0x11111111111111111111
seeds = 0..9
expected_rows = 40
```

若 10 seeds 保持正向提升，可作为毕业论文创新一 SPN 结构适配主结果之一。
