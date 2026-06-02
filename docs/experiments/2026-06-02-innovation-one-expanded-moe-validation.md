# 创新一扩展专家池 MoE 验证记录

日期：2026-06-02

## 目的

将新增模型纳入 SA-MoE 专家池，验证专家融合是否能在 multi-pair 强基线之上继续带来提升。

扩展后专家池：

- `resnet_bitslice`
- `dbitnet_dilated_cnn`
- `cnn`
- `mlp`
- `senet_resnext`
- `multiscale_dense_resnet`

## 实现变更

`StructureAwareMoEDistinguisher` 从 4 专家扩展为 6 专家。

Hard gate 初始权重：

- ARX: `(0.35, 0.20, 0.05, 0.05, 0.10, 0.25)`
- SPN: `(0.10, 0.30, 0.30, 0.05, 0.20, 0.05)`
- Feistel-like: `(0.20, 0.35, 0.10, 0.05, 0.10, 0.20)`

权重顺序：

`resnet_bitslice`, `dbitnet_dilated_cnn`, `cnn`, `mlp`, `senet_resnext`, `multiscale_dense_resnet`

## 验证配置

- cipher: `speck32`
- rounds: `6`
- difference profile: `speck32_gohr2019`
- feature encoding: `ciphertext_pair_xor_bits`
- pairs per sample: `4`
- models: `mlp`, `moe_uniform`, `moe_soft`
- seeds: `0 1 2`
- samples per class: `8192`
- epochs: `5`
- batch size: `1024`
- hidden bits: `32`

输出：

- `outputs/innovation_one_speck6_expanded_moe_pairs4_validation.jsonl`
- `outputs/innovation_one_speck6_expanded_moe_pairs4_validation_summary.csv`

## 结果

| model | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|
| `mlp` | 3 | 0.6207 | 0.0064 | 0.6567 |
| `moe_soft` | 3 | 0.6198 | 0.0045 | 0.6561 |
| `moe_uniform` | 3 | 0.5934 | 0.0022 | 0.6253 |

`moe_soft` 平均 gate 权重：

| expert | mean weight |
|---|---:|
| `mlp` | 0.5765 |
| `resnet_bitslice` | 0.1054 |
| `multiscale_dense_resnet` | 0.0919 |
| `dbitnet_dilated_cnn` | 0.0850 |
| `cnn` | 0.0751 |
| `senet_resnext` | 0.0661 |

## 结论

- 扩展专家池后，`moe_soft` 与强 MLP 基线基本持平，没有明显超过 MLP。
- `moe_soft` 的 gate 主要集中到 MLP，说明当前收益仍主要来自 multi-pair 输入格式，而不是专家融合本身。
- `moe_uniform` 将强弱专家平均，性能低于 MLP 和 `moe_soft`，可作为消融中“盲目融合会稀释强专家”的证据。
- 论文中应将 MoE 写作结构感知模型选择/融合框架，而不是声称 MoE 自身已经显著提升 SOTA。

