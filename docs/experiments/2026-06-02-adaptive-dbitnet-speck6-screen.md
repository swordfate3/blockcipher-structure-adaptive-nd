# Adaptive DBitNet SPECK6 筛查记录

日期：2026-06-02

## 目的

验证新增 `adaptive_dbitnet` 是否能解决旧 `dbitnet_dilated_cnn` 固定 dilation 在不同输入宽度下表现偏弱的问题，并与当前项目内部强基线 MLP、简化 ResNet-BitSlice 比较。

本轮是可控筛查，不作为最终论文主表。

## 公共配置

- cipher: `speck32`
- rounds: `6`
- difference profile: `speck32_gohr2019`
- models: `mlp`, `adaptive_dbitnet`, `dbitnet_dilated_cnn`, `resnet_bitslice`
- seeds: `0 1 2`
- samples per class: `8192`
- epochs: `5`
- batch size: `1024`
- hidden bits / base channels: `32`

## 实验 A：Gohr 可比输入

配置：

- feature encoding: `ciphertext_pair_bits`
- pairs per sample: `1`

输出：

- `outputs/innovation_one_adaptive_dbitnet_speck6_pairbits_p1_screen.jsonl`
- `outputs/innovation_one_adaptive_dbitnet_speck6_pairbits_p1_screen_summary.csv`

| model | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|
| `resnet_bitslice` | 3 | 0.5229 | 0.0017 | 0.5261 |
| `dbitnet_dilated_cnn` | 3 | 0.5226 | 0.0036 | 0.5232 |
| `adaptive_dbitnet` | 3 | 0.5187 | 0.0022 | 0.5204 |
| `mlp` | 3 | 0.5115 | 0.0056 | 0.5039 |

观察：

- 在 `C || C'` 原始 pair 输入下，所有模型都远低于 Gohr 文献中的 SPECK6 约 0.78。
- 这说明当前训练预算和模型实现仍不是 Gohr/DBitNet 文献级复现。
- `adaptive_dbitnet` 没有在该低预算设置下超过旧 DBitNet/ResNet。

## 实验 B：当前项目宽输入

配置：

- feature encoding: `ciphertext_pair_xor_bits`
- pairs per sample: `4`

输出：

- `outputs/innovation_one_adaptive_dbitnet_speck6_xorbits_p4_screen.jsonl`
- `outputs/innovation_one_adaptive_dbitnet_speck6_xorbits_p4_screen_summary.csv`

| model | runs | calibrated accuracy mean | calibrated accuracy std | AUC mean |
|---|---:|---:|---:|---:|
| `mlp` | 3 | 0.6241 | 0.0020 | 0.6611 |
| `adaptive_dbitnet` | 3 | 0.5754 | 0.0021 | 0.6032 |
| `dbitnet_dilated_cnn` | 3 | 0.5266 | 0.0008 | 0.5332 |
| `resnet_bitslice` | 3 | 0.5219 | 0.0074 | 0.5230 |

观察：

- 在 `pairs_per_sample=4`、输入宽度 384 bits 下，`adaptive_dbitnet` 明显超过旧 `dbitnet_dilated_cnn` 与简化 `resnet_bitslice`。
- 这验证了输入宽度自适应 dilation 是有价值的，不应继续用旧固定 dilation DBitNet 代表文献 DBitNet。
- `adaptive_dbitnet` 仍低于 MLP，说明其 head/training schedule 或特征格式还需要继续调优。

## 判断

- `adaptive_dbitnet` 解决了一部分“输入宽度增大后旧卷积模型不适配”的问题。
- 但当前实现还没有达到 Gohr/DBitNet 文献水平，尤其在 `C || C'` 可比输入下表现仍弱。
- 后续若要证明创新一，需要继续补两个强基线：
  1. Gohr 原版 4-channel word-aware ResNet。
  2. DBitNet 文献训练设置，如 AMSGrad、更多 epochs、更接近原始 input format 的实验。

## 下一步

1. 对 `adaptive_dbitnet` 跑 `pairs=4/h64/epochs=10` 小扩展，看是否进一步靠近 MLP。
2. 实现 `gohr_resnet_speck`，使用 4 channels × 16 bit positions 的 SPECK 专用 reshape。
3. 暂不扩大 MoE；先保证专家池里的 SPECK/ARX 专家真正强。
