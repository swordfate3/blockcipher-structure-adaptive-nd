# 创新一跨结构 multi-pair 筛查记录

日期：2026-06-02

## 目的

验证 `pairs_per_sample` 的收益是否只出现在 SPECK/ARX，还是也能迁移到 SPN/PRESENT 与 Feistel-like/SM4。

本轮为筛查实验，配置较小，不作为论文最终数值。

## 公共配置

- feature encoding: `ciphertext_pair_xor_bits`
- samples per class: `4096`
- epochs: `3`
- batch size: `512`
- hidden bits: `32`
- seed: `0`

## PRESENT-80 筛查

配置：

- cipher: `present80`
- rounds: `4, 5`
- difference profile: `present_wang_jain2021`
- difference member: `0`
- pairs per sample: `1, 2, 4`
- models: `mlp`, `cnn`, `dbitnet_dilated_cnn`, `multiscale_dense_resnet`, `moe_soft`

输出：

- `outputs/innovation_one_present_multipair_p1_screen.jsonl`
- `outputs/innovation_one_present_multipair_p2_screen.jsonl`
- `outputs/innovation_one_present_multipair_p4_screen.jsonl`
- 对应 `_summary.csv`

### PRESENT-80 Round 4

| pairs | best model | best calibrated accuracy | best AUC |
|---:|---|---:|---:|
| 1 | `mlp` | 0.6697 | 0.7214 |
| 2 | `mlp` | 0.7468 | 0.8156 |
| 4 | `mlp` | 0.8220 | 0.8974 |

Round 4 观察：

- multi-pair 对 PRESENT4 有显著提升。
- `mlp` 在 pairs=1/2/4 下均为最强，说明强 MLP baseline 仍必须保留。
- `moe_soft` 在 pairs=4 下达到 0.8079，接近 MLP，但仍未超过。

### PRESENT-80 Round 5

| pairs | best model | best calibrated accuracy | best AUC |
|---:|---|---:|---:|
| 1 | `dbitnet_dilated_cnn` | 0.5457 | 0.5494 |
| 2 | `multiscale_dense_resnet` | 0.5562 | 0.5705 |
| 4 | `moe_soft` | 0.5825 | 0.6097 |

Round 5 观察：

- multi-pair 在更高轮也有提升，但幅度小于 round 4。
- pairs=4 下 `moe_soft` 略优，说明专家融合在弱信号设置可能有价值。
- `mlp` 在 PRESENT5 pairs=4 下不是最强，和 SPECK 的模型偏好不同。

## SM4 筛查

配置：

- cipher: `sm4`
- rounds: `4`
- difference profile: `sm4_yu2023_conv_resnet`
- pairs per sample: `1, 2, 4`
- models: `mlp`, `cnn`, `dbitnet_dilated_cnn`, `multiscale_dense_resnet`, `moe_soft`

输出：

- `outputs/innovation_one_sm4_multipair_p1_screen.jsonl`
- `outputs/innovation_one_sm4_multipair_p2_screen.jsonl`
- `outputs/innovation_one_sm4_multipair_p4_screen.jsonl`
- 对应 `_summary.csv`

| pairs | best model | best calibrated accuracy | best AUC |
|---:|---|---:|---:|
| 1 | `multiscale_dense_resnet` | 0.6545 | 0.7118 |
| 2 | `multiscale_dense_resnet` | 0.6013 | 0.6366 |
| 4 | `multiscale_dense_resnet` | 0.6624 | 0.7192 |

SM4 观察：

- SM4 的最强模型是 `multiscale_dense_resnet`，不是 MLP。
- pairs=4 相比 pairs=1 有小幅提升；pairs=2 下降，说明 multi-pair 不一定单调有效。
- `moe_soft` 在 pairs=4 下达到 0.6453，接近但未超过 `multiscale_dense_resnet`。

## 跨结构初步结论

- SPECK 与 PRESENT 均显示 multi-pair 明显收益，说明该机制不是 SPECK 单点偶然。
- SM4 对 multi-pair 的响应更复杂，模型偏好更偏向 `multiscale_dense_resnet`。
- 当前创新一最稳表述应是：不同密码结构不仅影响网络架构偏好，也影响输入组织方式；`pairs_per_sample` 是一个有效但结构相关的输入格式超参数。
- 仍需多 seed 验证后才能形成论文最终结论。

## 多 seed 验证结果

### PRESENT5

验证配置：

- cipher: `present80`
- rounds: `5`
- difference profile: `present_wang_jain2021`
- difference member: `0`
- models: `mlp`, `dbitnet_dilated_cnn`, `multiscale_dense_resnet`, `moe_soft`
- pairs: `1, 4`
- seeds: `0 1 2`
- samples per class: `8192`
- epochs: `5`
- batch size: `1024`
- hidden bits: `32`

输出：

- `outputs/innovation_one_present5_pairs1_validation.jsonl`
- `outputs/innovation_one_present5_pairs1_validation_summary.csv`
- `outputs/innovation_one_present5_pairs4_validation.jsonl`
- `outputs/innovation_one_present5_pairs4_validation_summary.csv`

| model | pairs | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|---:|
| `dbitnet_dilated_cnn` | 1 | 3 | 0.5485 | 0.0033 | 0.5595 |
| `mlp` | 1 | 3 | 0.5484 | 0.0002 | 0.5637 |
| `moe_soft` | 1 | 3 | 0.5482 | 0.0033 | 0.5604 |
| `multiscale_dense_resnet` | 1 | 3 | 0.5378 | 0.0070 | 0.5459 |
| `dbitnet_dilated_cnn` | 4 | 3 | 0.5745 | 0.0058 | 0.5985 |
| `mlp` | 4 | 3 | 0.5908 | 0.0024 | 0.6228 |
| `moe_soft` | 4 | 3 | 0.5999 | 0.0103 | 0.6385 |
| `multiscale_dense_resnet` | 4 | 3 | 0.5736 | 0.0028 | 0.5991 |

PRESENT5 结论：

- `pairs_per_sample=4` 在 PRESENT5 上稳定提升。
- `moe_soft` 在 pairs=4 下超过 MLP 和 DBitNet，说明专家融合在 SPN 弱信号场景有一定价值。
- 单 pair 下各模型差异很小，multi-pair 才拉开模型差距。

### SM4 Round 4

验证配置：

- cipher: `sm4`
- rounds: `4`
- difference profile: `sm4_yu2023_conv_resnet`
- models: `mlp`, `multiscale_dense_resnet`, `moe_soft`
- pairs: `1, 4`
- seeds: `0 1 2`
- samples per class: `8192`
- epochs: `5`
- batch size: `1024`
- hidden bits: `32`

输出：

- `outputs/innovation_one_sm4_pairs1_validation.jsonl`
- `outputs/innovation_one_sm4_pairs1_validation_summary.csv`
- `outputs/innovation_one_sm4_pairs4_validation.jsonl`
- `outputs/innovation_one_sm4_pairs4_validation_summary.csv`

| model | pairs | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|---:|
| `mlp` | 1 | 3 | 0.5759 | 0.0051 | 0.5878 |
| `moe_soft` | 1 | 3 | 0.7783 | 0.0063 | 0.8650 |
| `multiscale_dense_resnet` | 1 | 3 | 0.7955 | 0.0118 | 0.8811 |
| `mlp` | 4 | 3 | 0.6021 | 0.0024 | 0.6237 |
| `moe_soft` | 4 | 3 | 0.8421 | 0.0610 | 0.9097 |
| `multiscale_dense_resnet` | 4 | 3 | 0.8832 | 0.0086 | 0.9542 |

SM4 结论：

- SM4 的结构偏好明显不同于 SPECK/PRESENT：`multiscale_dense_resnet` 是最强模型。
- `pairs_per_sample=4` 对 SM4 也有明显提升，尤其是 `multiscale_dense_resnet` 从 0.7955 提升到 0.8832。
- `moe_soft` 有提升但方差较大，暂时不能作为 SM4 主结论。

## 更新后的跨结构判断

- multi-pair 输入在 SPECK、PRESENT、SM4 三类结构上都能观察到提升，但提升幅度和最优模型不同。
- SPECK：强 MLP + multi-pair 最稳，MoE 近似 MLP。
- PRESENT：multi-pair 后 `moe_soft` 在高轮弱信号下略优。
- SM4：`multiscale_dense_resnet` 明显强于 MLP/MoE，说明结构感知模型池本身有必要。
- 创新一主张可以从“MoE 专家融合”升级为“结构感知输入组织与模型池联合匹配”。

## 下一步

进入论文主表实验前，需要把筛查结论扩大到更稳的配置：

1. SPECK6 / PRESENT5 / SM4 round 4 均使用 `pairs_per_sample=1,4` 对照。
2. 每组至少 `seeds=0 1 2 3 4`。
3. 保留结构代表模型与强基线：`mlp`、`dbitnet_dilated_cnn`、`multiscale_dense_resnet`、`moe_soft`；SPECK 额外保留 `resnet_bitslice`。
4. 汇总表必须按 `pairs_per_sample` 分组，避免把 single-pair 与 multi-pair 结果混合。
