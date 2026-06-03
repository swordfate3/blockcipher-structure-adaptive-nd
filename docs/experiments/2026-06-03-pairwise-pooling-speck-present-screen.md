# Pairwise Adaptive DBitNet pair 数量与 pooling 消融筛查

日期：2026-06-03

## 目的

本轮服务两个任务：

1. 毕业论文创新一：验证 multi-pair 输入组织如何影响神经网络专家选择。
2. 中文核心小论文子线：验证共享 pair encoder 与跨 pair pooling 是否优于直接拼接多个 pair。

重点问题：

```text
1. pairwise 编码是否优于直接宽输入 adaptive DBitNet？
2. pairs_per_sample 从 1 到 8 是否持续提升？
3. mean、max、mean+max 哪种 pooling 更稳？
```

## 实验设置

计划文件：

- `outputs/innovation_one_pairwise_pooling_speck_present_plan.csv`

输出：

- `outputs/innovation_one_pairwise_pooling_speck_present.jsonl`
- `outputs/innovation_one_pairwise_pooling_speck_present_summary.csv`

统一设置：

```text
feature_encoding = ciphertext_pair_xor_bits
pairs_per_sample = 1, 2, 4, 8
samples_per_class = 8192
epochs = 5
batch_size = 1024
hidden_bits = 32
seeds = 0 1 2
```

密码与差分：

| cipher | structure | rounds | difference profile |
|---|---|---:|---|
| SPECK32/64 | ARX | 6 | `speck32_gohr2019` |
| PRESENT-80 | SPN | 5 | `present_wang_jain2021`, member 0 |

模型：

```text
mlp
adaptive_dbitnet
adaptive_dbitnet_pairwise_mean
adaptive_dbitnet_pairwise_max
adaptive_dbitnet_pairwise_mean_max
```

其中：

- `adaptive_dbitnet` 是直接拼接宽输入的 DBitNet-style encoder。
- `adaptive_dbitnet_pairwise_*` 是共享 pair encoder + pooling 的 multi-pair 变体。
- `adaptive_dbitnet_pairwise_mean_max` 等价于历史默认 `adaptive_dbitnet_pairwise`。

## 结果

指标为 3 个 seed 的 mean。表中格式为：

```text
calibrated accuracy / AUC
```

### SPECK32/64 r=6

| model | p=1 | p=2 | p=4 | p=8 |
|---|---:|---:|---:|---:|
| `mlp` | 0.5739 / 0.5855 | 0.5888 / 0.6150 | 0.6213 / 0.6577 | 0.6531 / 0.7084 |
| `adaptive_dbitnet` | 0.5527 / 0.5640 | 0.5499 / 0.5687 | 0.5774 / 0.6044 | 0.6267 / 0.6727 |
| `pairwise_mean` | 0.5489 / 0.5621 | 0.6334 / 0.6782 | 0.7702 / 0.8486 | 0.8805 / 0.9491 |
| `pairwise_max` | 0.5477 / 0.5615 | 0.6200 / 0.6619 | 0.7602 / 0.8360 | 0.8485 / 0.9240 |
| `pairwise_mean_max` | 0.5474 / 0.5601 | 0.6360 / 0.6844 | 0.7738 / 0.8497 | 0.8662 / 0.9392 |

最佳：

| pairs | best model | calibrated accuracy | AUC |
|---:|---|---:|---:|
| 1 | `mlp` | 0.5739 | 0.5855 |
| 2 | `pairwise_mean_max` | 0.6360 | 0.6844 |
| 4 | `pairwise_mean_max` | 0.7738 | 0.8497 |
| 8 | `pairwise_mean` | 0.8805 | 0.9491 |

观察：

- SPECK6 下 pairwise 编码从 `pairs=2` 开始明显超过 MLP 和直接宽输入 `adaptive_dbitnet`。
- `pairs=4` 时 mean+max 略优；`pairs=8` 时 mean pooling 反而最强。
- 这说明 pairwise 的收益不是简单来自输入 bit 数增加，而是来自保留 pair 边界后的共享编码与聚合。

### PRESENT-80 r=5

| model | p=1 | p=2 | p=4 | p=8 |
|---|---:|---:|---:|---:|
| `mlp` | 0.5483 / 0.5644 | 0.5665 / 0.5889 | 0.5891 / 0.6222 | 0.6315 / 0.6774 |
| `adaptive_dbitnet` | 0.5281 / 0.5289 | 0.5391 / 0.5469 | 0.5621 / 0.5816 | 0.6091 / 0.6462 |
| `pairwise_mean` | 0.5226 / 0.5279 | 0.5551 / 0.5710 | 0.6194 / 0.6620 | 0.7664 / 0.8414 |
| `pairwise_max` | 0.5268 / 0.5309 | 0.5516 / 0.5683 | 0.6154 / 0.6553 | 0.7188 / 0.7878 |
| `pairwise_mean_max` | 0.5218 / 0.5235 | 0.5560 / 0.5768 | 0.6343 / 0.6770 | 0.7117 / 0.7741 |

最佳：

| pairs | best model | calibrated accuracy | AUC |
|---:|---|---:|---:|
| 1 | `mlp` | 0.5483 | 0.5644 |
| 2 | `mlp` | 0.5665 | 0.5889 |
| 4 | `pairwise_mean_max` | 0.6343 | 0.6770 |
| 8 | `pairwise_mean` | 0.7664 | 0.8414 |

观察：

- PRESENT5 下 `pairs=1/2` 仍是 MLP 最强或接近最强，说明 pairwise 专家需要足够多 pair 才能释放优势。
- `pairs=4` 后 pairwise 明显超过 MLP 与直接宽输入 adaptive DBitNet。
- `pairs=8` 时 mean pooling 明显最强，mean+max 方差较大，说明 max 分支可能引入不稳定强响应。

## 结论

本轮支持小论文子线：

```text
multi-pair 输入下，保持 pair 边界并共享 pair encoder 明显优于直接拼接宽输入。
```

同时支持毕业论文创新一：

```text
输入组织方式会改变最优专家选择；当 pairs_per_sample 足够大时，pairwise 专家成为强结构适配模块。
```

关键发现：

1. `adaptive_dbitnet_pairwise_*` 在 SPECK/PRESENT 的 `pairs=4/8` 下显著优于 `adaptive_dbitnet`。
2. pair 数量从 1 到 8 在本轮 SPECK/PRESENT 上整体提升明显，但不能先验假设对所有密码都单调，SM4 仍需单独验证。
3. `mean+max` 在 `pairs=4` 较强；`mean` 在 `pairs=8` 更稳更强。
4. 后续扩大验证应优先比较 `pairwise_mean` 与 `pairwise_mean_max`，`pairwise_max` 作为消融保留即可。

## 后续

下一步：

1. 跑 SM4 r=4/r=5 的 pair 数量消融，建议先降低 batch size 避免 pairs=8 显存峰值。
2. 对 SPECK r=6 和 PRESENT r=5 选择 `pairwise_mean`、`pairwise_mean_max` 做扩大验证：

```text
samples_per_class = 32768
epochs = 10
seeds = 0,1,2,3,4
```

3. 实现参数量统计脚本，补小论文需要的模型复杂度表。
