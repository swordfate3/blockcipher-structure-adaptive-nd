# 创新一长期记忆

更新时间：2026-06-02

## 当前定位

创新一不应写成“MoE 或 multi-pair 单独显著超过所有前沿模型”。当前更稳的定位是：

> 结构感知输入组织 + 容量匹配 + 自适应/结构化模型池 + 专家融合消融。

论文表述重点应放在：不同分组密码结构、输入组织方式、模型容量和神经网络架构之间存在适配关系；本文在统一实验协议下比较这种适配关系。

## 文献边界

本地 `papers/innovation_one/` 已整理 30 篇相关论文，核心模型线包括：

- Gohr 2019 SPECK32/64 ResNet neural distinguisher。
- Bellini et al. 2023 DBitNet / cipher-agnostic neural training pipeline。
- 多密文对 / multi-pair neural distinguishers。
- SENet / SE-ResNeXt。
- Generic Partial Decryption, GPD。
- RX-neural / related-key / polytopic neural distinguishers。
- PRESENT entropy-based distinguisher。
- GIFT/ASCON score-distribution MLP test。

不能声称“首次通用神经区分器”或“首次多密文对输入”。安全表述是：结构感知匹配与统一协议评估。

## 当前实现状态

已实现并接入实验入口的模型：

- `mlp`
- `cnn`
- `resnet_bitslice`
- `dbitnet_dilated_cnn`
- `adaptive_dbitnet`
- `senet_resnext`
- `multiscale_dense_resnet`
- `moe_uniform`
- `moe_hard`
- `moe_soft`
- `lstm_roundseq`
- `transformer_encoder`

重要说明：

- 当前 `resnet_bitslice` 只是 Gohr-style 简化版，不是 Gohr 原版 4-channel word-aware ResNet。
- 当前 `dbitnet_dilated_cnn` 是旧的固定 dilation 轻量版，不代表文献完整 DBitNet。
- 新增 `adaptive_dbitnet` 才开始按输入 bit 宽度生成 DBitNet-style dilation rates。

## Adaptive DBitNet

新增模型 key：

```text
adaptive_dbitnet
```

对应文件：

- `src/blockcipher_ai_eval/models/adaptive_dbitnet.py`
- `tests/test_adaptive_dbitnet_model.py`
- `docs/experiments/2026-06-02-adaptive-dbitnet-implementation.md`

自适应 dilation 行为：

| input bits | dilation rates |
|---:|---|
| 64 | `[31, 15, 7, 3]` |
| 96 | `[47, 23, 11, 5]` |
| 128 | `[63, 31, 15, 7, 3]` |
| 384 | `[191, 95, 47, 23, 11, 5]` |

分类头：

```text
Flatten -> Linear(256) -> ReLU -> Linear(256) -> ReLU -> Linear(64) -> ReLU -> Linear(1)
```

## 已跑关键实验

### SPECK6 主表 v1 与容量消融

记录文件：

- `docs/experiments/2026-06-02-innovation-one-speck6-main-v1.md`

关键结果：

| 配置 | 模型 | calibrated accuracy mean | AUC mean |
|---|---|---:|---:|
| pairs=1, hidden=64 | `mlp` | 0.6767 | 0.7241 |
| pairs=1, hidden=64 | `moe_soft` | 0.6710 | 0.7198 |
| pairs=4, hidden=64 | `mlp` | 0.6494 | 0.7033 |
| pairs=4, hidden=64 | `moe_soft` | 0.6495 | 0.7027 |
| pairs=4, hidden=128 | `mlp` | 0.6729 | 0.7349 |

结论：

- 当前 MLP 只是项目内部强 baseline，还没达到 Gohr SPECK6 约 0.78 的文献水平。
- multi-pair 不是无条件提升；输入变宽后需要容量匹配。
- MoE-soft 接近 MLP，但没有在 SPECK6 上超过强 MLP。

### Adaptive DBitNet SPECK6 筛查

记录文件：

- `docs/experiments/2026-06-02-adaptive-dbitnet-speck6-screen.md`

Gohr 可比输入 `ciphertext_pair_bits`, pairs=1：

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `resnet_bitslice` | 0.5229 | 0.5261 |
| `dbitnet_dilated_cnn` | 0.5226 | 0.5232 |
| `adaptive_dbitnet` | 0.5187 | 0.5204 |
| `mlp` | 0.5115 | 0.5039 |

当前宽输入 `ciphertext_pair_xor_bits`, pairs=4：

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `mlp` | 0.6241 | 0.6611 |
| `adaptive_dbitnet` | 0.5754 | 0.6032 |
| `dbitnet_dilated_cnn` | 0.5266 | 0.5332 |
| `resnet_bitslice` | 0.5219 | 0.5230 |

结论：

- `adaptive_dbitnet` 在宽输入下明显强于旧固定 dilation DBitNet 和简化 ResNet。
- `adaptive_dbitnet` 仍低于 MLP，说明需要继续调训练 schedule、容量或输入格式。
- 在 `C || C'` 可比输入下所有模型都弱，说明还没有复现 Gohr/DBitNet 文献级结果。

## 下一步优先级

优先级 1：

- 实现 `gohr_resnet_speck`，使用 SPECK32/64 的 4 channels × 16 bit positions 输入 reshape。
- 目标是复现 Gohr SPECK6 接近 0.78、SPECK7 接近 0.61 的文献水平。

优先级 2：

- 对 `adaptive_dbitnet` 做小扩展：
  - SPECK6
  - `feature_encoding=ciphertext_pair_xor_bits`
  - `pairs_per_sample=4`
  - `hidden_bits=64`
  - `epochs=10`
  - `samples_per_class=8192` 或 `16384`
  - `seeds=0 1 2`

优先级 3：

- PRESENT5 与 SM4 检查容量匹配问题。
- 不要继续盲目扩大 MoE；先保证专家池里 SPECK/ARX 专家真正强。

## 运行注意事项

每次启动 GPU 长实验前后都要运行：

```bash
nvidia-smi
```

确认没有残留：

```text
run_innovation_one_matrix.py
python3 experiments/run_innovation_one_matrix.py
```

之前发生过一次 hidden=128 MoE 容量消融进程在沙盒外残留并占满显存的问题。后续长实验必须确认进程退出和显存释放。

