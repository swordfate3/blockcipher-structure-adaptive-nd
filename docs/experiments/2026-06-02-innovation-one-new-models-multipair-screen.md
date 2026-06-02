# 创新一新模型与多密文对筛查记录

日期：2026-06-02

## 目的

验证近年文献补齐后新增的两类实现是否值得进入创新一主实验：

- 新模型：`senet_resnext`、`multiscale_dense_resnet`。
- 新数据格式：`pairs_per_sample > 1` 的 multi-pair 输入。

本轮是筛查实验，不作为论文最终数值。

## 配置

公共配置：

- cipher: `speck32`
- difference profile: `speck32_gohr2019`
- feature encoding: `ciphertext_pair_xor_bits`
- samples per class: `4096`
- epochs: `3`
- batch size: `512`
- hidden bits: `32`
- seed: `0`

输出文件：

- `outputs/innovation_one_speck_new_models_screen.jsonl`
- `outputs/innovation_one_speck_new_models_screen_summary.csv`
- `outputs/innovation_one_speck_multipair_screen.jsonl`
- `outputs/innovation_one_speck_multipair_screen_summary.csv`
- `outputs/innovation_one_speck_multipair4_screen.jsonl`
- `outputs/innovation_one_speck_multipair4_screen_summary.csv`

## 单 pair 新模型结果

| rounds | model | pairs | calibrated accuracy | AUC |
|---:|---|---:|---:|---:|
| 5 | `mlp` | 1 | 0.7170 | 0.7707 |
| 5 | `moe_soft` | 1 | 0.7031 | 0.7503 |
| 5 | `moe_uniform` | 1 | 0.6960 | 0.7450 |
| 5 | `multiscale_dense_resnet` | 1 | 0.6824 | 0.7070 |
| 5 | `resnet_bitslice` | 1 | 0.6501 | 0.6851 |
| 5 | `dbitnet_dilated_cnn` | 1 | 0.6130 | 0.6433 |
| 5 | `senet_resnext` | 1 | 0.5774 | 0.5893 |
| 6 | `mlp` | 1 | 0.5364 | 0.5435 |
| 6 | `multiscale_dense_resnet` | 1 | 0.5344 | 0.5325 |
| 6 | `dbitnet_dilated_cnn` | 1 | 0.5334 | 0.5367 |
| 6 | `moe_uniform` | 1 | 0.5334 | 0.5376 |
| 6 | `moe_soft` | 1 | 0.5298 | 0.5366 |
| 6 | `senet_resnext` | 1 | 0.5254 | 0.5292 |
| 6 | `resnet_bitslice` | 1 | 0.5217 | 0.5265 |

初步观察：

- `mlp` 仍然是强基线，单 pair 下没有被新模型超过。
- `multiscale_dense_resnet` 在 SPECK5 上强于 ResNet/DBitNet，但没有超过 MLP/MoE。
- 当前轻量 `senet_resnext` 表现偏弱，后续不宜直接作为主张重点。

## Multi-pair 结果

| rounds | model | pairs | input bits | calibrated accuracy | AUC |
|---:|---|---:|---:|---:|---:|
| 5 | `mlp` | 1 | 96 | 0.7170 | 0.7707 |
| 5 | `mlp` | 2 | 192 | 0.7617 | 0.8349 |
| 5 | `mlp` | 4 | 384 | 0.8528 | 0.9248 |
| 5 | `multiscale_dense_resnet` | 1 | 96 | 0.6824 | 0.7070 |
| 5 | `multiscale_dense_resnet` | 2 | 192 | 0.7036 | 0.7472 |
| 5 | `multiscale_dense_resnet` | 4 | 384 | 0.7026 | 0.7502 |
| 6 | `mlp` | 1 | 96 | 0.5364 | 0.5435 |
| 6 | `mlp` | 2 | 192 | 0.5508 | 0.5669 |
| 6 | `mlp` | 4 | 384 | 0.5830 | 0.6003 |
| 6 | `multiscale_dense_resnet` | 1 | 96 | 0.5344 | 0.5325 |
| 6 | `multiscale_dense_resnet` | 2 | 192 | 0.5171 | 0.5108 |
| 6 | `multiscale_dense_resnet` | 4 | 384 | 0.5278 | 0.5256 |

初步观察：

- `pairs_per_sample` 对 MLP 有明显正向作用，且从 1 到 4 呈持续提升。
- `multiscale_dense_resnet` 在 SPECK5 上有小幅收益，但在 SPECK6 上不稳定。
- 本轮结果提示：创新一的主线应从“只融合模型专家”扩展为“结构感知输入格式 + 强基线 + 专家融合”的组合。

## 当前判断

下一步不宜直接扩大所有模型，而应优先验证最有信号的组合：

- `mlp`, `pairs_per_sample=4`, SPECK5/SPECK6。
- `moe_soft` 或 `moe_uniform`, `pairs_per_sample=4`, SPECK5/SPECK6。
- `multiscale_dense_resnet`, `pairs_per_sample=1/4`, 作为文献模型对照。

需要多 seed 验证后才能写成论文结论。

## SPECK6 多种子验证

为确认 multi-pair 提升不是单一 seed 偶然，追加运行：

- cipher: `speck32`
- rounds: `6`
- models: `mlp`, `moe_soft`
- seeds: `0 1 2`
- samples per class: `8192`
- epochs: `5`
- batch size: `1024`
- hidden bits: `32`
- difference profile: `speck32_gohr2019`

输出文件：

- `outputs/innovation_one_speck6_pairs1_validation.jsonl`
- `outputs/innovation_one_speck6_pairs1_validation_summary.csv`
- `outputs/innovation_one_speck6_pairs4_validation.jsonl`
- `outputs/innovation_one_speck6_pairs4_validation_summary.csv`

| model | pairs | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|---:|
| `mlp` | 1 | 3 | 0.5698 | 0.0049 | 0.5823 |
| `mlp` | 4 | 3 | 0.6233 | 0.0028 | 0.6600 |
| `moe_soft` | 1 | 3 | 0.5570 | 0.0059 | 0.5689 |
| `moe_soft` | 4 | 3 | 0.6215 | 0.0053 | 0.6596 |

验证结论：

- `pairs_per_sample=4` 对 SPECK6 有稳定提升。
- MLP 与 MoE-soft 在 multi-pair 下非常接近，说明当前主要收益来自输入格式扩展，而不是 MoE gate 本身。
- 论文表述应将这一点写成“结构感知输入格式与模型池联合设计”，不要把提升单独归因于专家融合。

