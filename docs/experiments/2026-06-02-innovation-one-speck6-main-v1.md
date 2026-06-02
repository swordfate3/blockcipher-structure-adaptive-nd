# 创新一 SPECK6 主表 v1 与容量消融

日期：2026-06-02

## 目的

在更稳的中等规模设置下复查 SPECK32/64 6 轮实验，验证此前小规模筛查中观察到的 multi-pair 收益是否稳定，并检查输入宽度增大后是否需要同步增大模型容量。

本记录不作为最终论文 SOTA 数值；它用于确定后续论文主表的实验配置。

## 公共配置

- cipher: `speck32`
- rounds: `6`
- difference profile: `speck32_gohr2019`
- feature encoding: `ciphertext_pair_xor_bits`
- samples per class: `32768`
- epochs: `10`
- batch size: `2048`
- seeds: `0 1 2 3 4`

## 实验 A：pairs=1, hidden=64

输出：

- `outputs/innovation_one_main_v1_speck6_pairs1.jsonl`
- `outputs/innovation_one_main_v1_speck6_pairs1_summary.csv`

| model | pairs | hidden bits | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|---:|---:|
| `mlp` | 1 | 64 | 5 | 0.6767 | 0.0039 | 0.7241 |
| `moe_soft` | 1 | 64 | 5 | 0.6710 | 0.0050 | 0.7198 |
| `dbitnet_dilated_cnn` | 1 | 64 | 5 | 0.5221 | 0.0038 | 0.5280 |
| `resnet_bitslice` | 1 | 64 | 5 | 0.5174 | 0.0040 | 0.5207 |
| `multiscale_dense_resnet` | 1 | 64 | 5 | 0.5142 | 0.0040 | 0.5157 |

观察：

- SPECK6 上强 MLP 仍是最强基线。
- `moe_soft` 接近 MLP，但没有超过 MLP。
- 当前实现中的 ResNet/DBitNet/multiscale 在该配置下没有学到与 MLP 同等强度的区分信号。

## 实验 B：pairs=4, hidden=64

输出：

- `outputs/innovation_one_main_v1_speck6_pairs4.jsonl`
- `outputs/innovation_one_main_v1_speck6_pairs4_summary.csv`

| model | pairs | hidden bits | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|---:|---:|
| `moe_soft` | 4 | 64 | 5 | 0.6495 | 0.0024 | 0.7027 |
| `mlp` | 4 | 64 | 5 | 0.6494 | 0.0031 | 0.7033 |
| `dbitnet_dilated_cnn` | 4 | 64 | 5 | 0.5275 | 0.0024 | 0.5370 |
| `resnet_bitslice` | 4 | 64 | 5 | 0.5273 | 0.0032 | 0.5359 |
| `multiscale_dense_resnet` | 4 | 64 | 5 | 0.5249 | 0.0043 | 0.5327 |

观察：

- 固定 `hidden_bits=64` 时，pairs=4 相比 pairs=1 下降。
- 这说明不能简单声称 `pairs_per_sample=4` 在所有设置下必然提升。
- pairs=4 输入宽度从 96 bits 增加到 384 bits，若模型容量不随之调整，可能出现欠拟合或优化不足。

## 实验 C：pairs=4, MLP hidden=128

输出：

- `outputs/innovation_one_main_v1_speck6_pairs4_mlp_h128_capacity.jsonl`
- `outputs/innovation_one_main_v1_speck6_pairs4_mlp_h128_capacity_summary.csv`

| model | pairs | hidden bits | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|---:|---:|
| `mlp` | 4 | 128 | 5 | 0.6729 | 0.0025 | 0.7349 |

观察：

- 将 MLP hidden bits 从 64 增加到 128 后，pairs=4 的 calibrated accuracy 从 0.6494 恢复到 0.6729。
- pairs=4/h128 的 calibrated accuracy 仍略低于 pairs=1/h64 的 0.6767，但 AUC 从 0.7241 提升到 0.7349。
- 这说明 multi-pair 输入在 SPECK6 上并非无效，而是需要与模型容量配套；AUC 提升也说明排序区分能力增强，但阈值校准仍需处理。

## 工程修正

本轮实验前补了三个实验管线问题：

- `summarize_innovation_one_results.py` 已按 `pairs_per_sample` 分组，避免 single-pair 与 multi-pair 结果混合。
- `run_innovation_one_matrix.py` 已改为每个 task 完成后增量写入 JSONL，并打印 `[i/n]` 进度。
- AUC 计算从正负样本两两比较矩阵改为排序秩统计，避免大验证集下评估开销过高。

## 结论

- SPECK6 的主结论应写为：强 MLP 是当前最可靠基线，MoE-soft 接近但未超过 MLP。
- multi-pair 输入不是无条件提升项；它需要与输入宽度相匹配的模型容量。
- 对 SPECK6，后续论文主表建议同时报告 `pairs=1/h64` 与 `pairs=4/h128`，而不是只比较 `pairs=1/h64` 与 `pairs=4/h64`。
- MoE hidden=128 的单 seed 训练成本过高，本轮未作为默认主表配置继续扩大；MoE 更适合作为结构感知融合消融，而不是 SPECK 主收益来源。

## 下一步

1. 对 PRESENT5 与 SM4 复查同样的问题：multi-pair 增益是否受 hidden bits 影响。
2. SPECK6 可追加 `pairs=4/h128/epochs=20` 或阈值校准实验，判断 AUC 提升能否转化为 calibrated accuracy。
3. 论文创新一表述调整为“结构感知输入组织 + 容量匹配 + 模型池/专家融合消融”，避免把 multi-pair 或 MoE 单独夸大成普适提升。
