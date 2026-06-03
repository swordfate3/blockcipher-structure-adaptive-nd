# 创新一长期记忆

更新时间：2026-06-03

## 当前定位

创新一不应写成“MoE 或 multi-pair 单独显著超过所有前沿模型”。当前更稳的定位是：

> 结构感知输入组织 + 容量匹配 + 自适应/结构化模型池 + 专家融合消融。

论文表述重点应放在：不同分组密码结构、输入组织方式、模型容量和神经网络架构之间存在适配关系；本文在统一实验协议下比较这种适配关系。

## 毕业论文与小论文双轨计划

总原则：

```text
毕业论文是主轨，小论文是从创新一中切出的 pairwise 子线。
```

### 主轨：毕业论文创新一

定位：

```text
面向分组密码结构与输入组织联合适配的神经差分区分器方法。
```

毕业论文必须保留完整框架：

- 密码结构分类：ARX、SPN、Feistel-like。
- 结构特征建模：`CipherProfile` 与轮数特征。
- 专家模型池：MLP、Gohr/ResNet、SENet、Multiscale Dense ResNet、Adaptive DBitNet、Pairwise Adaptive DBitNet、MoE。
- 输入组织：single-pair / multi-pair，`C || C'` 与 `C || C' || C xor C'`。
- 显式路由：`selector_rule` 与 `selector_rule_v2`。
- 融合消融：`moe_v3_*` 不作为唯一创新点，而作为专家融合对照。

毕业论文核心实验：

1. 跨结构主表：SPECK32/64、PRESENT-80、SM4。
2. single-pair / multi-pair 对照。
3. `selector_rule` vs `selector_rule_v2`。
4. `adaptive_dbitnet` vs `adaptive_dbitnet_pairwise`。
5. 高轮边界：SPECK r=7、PRESENT r=6、SM4 r=5。
6. Gohr-style SPECK single-pair 协议单独对齐，不能和 multi-pair 直接混比。

### 副轨：中文核心小论文

定位：

```text
多密文对神经差分区分器的共享 Pair 编码与聚合方法。
```

小论文只切 `adaptive_dbitnet_pairwise` 这条线，不展开完整结构路由框架。核心问题是：

```text
multi-pair 输入下，保留 pair 边界并共享 pair encoder 是否优于直接拼接多个 pair。
```

小论文核心实验：

1. concat vs pairwise：`adaptive_dbitnet` vs `adaptive_dbitnet_pairwise`。
2. pair 数量消融：`pairs_per_sample=1,2,4,8`。
3. pooling 消融：mean、max、mean+max，必要时 attention。
4. 跨密码验证：SPECK/PRESENT/SM4。
5. 高轮边界简表：PRESENT r=6、SM4 r=5、SPECK r=7。
6. 参数量、训练时间、显存占用作为补充，避免被质疑只是模型更大。

### 当前推进顺序

优先级：

1. 固定创新一最终口径，不再无限加模型。
2. 先补 pairwise pooling 消融模型与实验，因为它同时服务毕业论文和小论文。
3. 再跑 pair 数量消融：`1,2,4,8`。
4. 再跑更高轮边界：PRESENT r=6、SM4 r=5、SPECK r=7。
5. 最后整理毕业论文创新一章节，并从其中抽出 pairwise 子线形成小论文初稿。

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
- `adaptive_dbitnet_pairwise`
- `senet_resnext`
- `multiscale_dense_resnet`
- `moe_uniform`
- `moe_hard`
- `moe_soft`
- `moe_v2_uniform`
- `moe_v2_hard`
- `moe_v2_soft`
- `moe_v3_uniform`
- `moe_v3_hard`
- `moe_v3_soft`
- `moe_v4_uniform`
- `moe_v4_hard`
- `moe_v4_soft`
- `selector_rule`
- `lstm_roundseq`
- `transformer_encoder`
- `gohr_resnet_speck_depth10`

重要说明：

- 当前 `resnet_bitslice` 只是 Gohr-style 简化版，不是 Gohr 原版 4-channel word-aware ResNet。
- 当前 `dbitnet_dilated_cnn` 是旧的固定 dilation 轻量版，不代表文献完整 DBitNet。
- 新增 `adaptive_dbitnet` 才开始按输入 bit 宽度生成 DBitNet-style dilation rates。
- 新增 `adaptive_dbitnet_pairwise` 按 ciphertext pair 共享编码，再跨 pair mean/max pooling，是当前 SPECK6 multi-pair 最强模型。
- 新增 `gohr_resnet_speck` 是 SPECK32/64 专用 4-channel word-aware Gohr-style 模型，只支持 64-bit `C || C'` 原始 pair 输入。
- 新增 `gohr_resnet_speck_depth10` 用于筛查深残差 Gohr-style 变体，但当前一次小规模实验没有超过浅层 Gohr 模型。
- 新增 `moe_v2_*` 保持 6 专家结构，但将旧 `dbitnet_dilated_cnn` 专家替换为 `adaptive_dbitnet`。
- 新增 `moe_v3_*` 保持 6 专家结构，但将 `adaptive_dbitnet` 专家替换为 `adaptive_dbitnet_pairwise`。
- 新增 `moe_v4_*` 在 v3 专家池前加入结构 adapter：ARX -> `arx_word_mix`，SPN -> `spn_cell_mix`，Feistel-like -> `feistel_branch_mix`。这是结构专用输入路径第一版，不代表 GPD/RX/polytopic/score-distribution 已完整实现。
- 新增 `selector_rule` 作为结构规则选择器：ARX multi-pair -> `adaptive_dbitnet_pairwise`，SPN -> `senet_resnext`，Feistel-like -> `multiscale_dense_resnet`。
- 新增 `selector_rule_v2`：multi-pair 一律选 `adaptive_dbitnet_pairwise`，single-pair 再按结构选择专家。

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

## Gohr ResNet SPECK

新增模型 key：

```text
gohr_resnet_speck
gohr_resnet_speck_depth10
```

对应文件：

- `src/blockcipher_ai_eval/models/gohr_speck.py`
- `tests/test_gohr_speck_model.py`
- `docs/experiments/2026-06-02-gohr-resnet-speck-implementation.md`

当前限制：

```text
input_bits = 64
feature_encoding = ciphertext_pair_bits
pairs_per_sample = 1
```

该模型用于复现 Gohr SPECK32/64 原始 pair 输入设置，不直接用于 `ciphertext_pair_xor_bits` 或 multi-pair 宽输入。

## 已跑关键实验

### 结构适配主矩阵

记录文件：

- `docs/experiments/2026-06-02-structure-adaptation-main-matrix.md`

设置：

- SPECK32/64 r=6, `speck32_gohr2019`
- PRESENT-80 r=5, `present_wang_jain2021`
- SM4 r=4, `sm4_yu2023_conv_resnet`
- `ciphertext_pair_xor_bits`, `pairs_per_sample=4`
- `8192/class`, `5 epochs`, `seeds=0 1 2`, `hidden_bits=32`

各结构最强结果：

| cipher | best model | calibrated accuracy mean | AUC mean |
|---|---|---:|---:|
| SPECK32/64 | `adaptive_dbitnet_pairwise` | 0.7728 | 0.8470 |
| PRESENT-80 | `adaptive_dbitnet_pairwise` | 0.6407 | 0.6826 |
| SM4 | `adaptive_dbitnet_pairwise` | 0.9999 | 1.0000 |

关键结论：

- multi-pair 输入下，`adaptive_dbitnet_pairwise` 同时成为 ARX/SPN/Feistel-like 三类结构最强专家。
- 旧 `selector_rule` 只在 SPECK/ARX 上选对，在 PRESENT/SM4 上低于 pairwise 专家。
- `moe_v3_soft` 在 SPECK/SM4 接近最强专家，但 PRESENT 上仍有稀释。
- 因此结构适配规则必须同时考虑密码结构与输入组织；新增 `selector_rule_v2` 作为修正规则。

### Selector Rule v2 单对/多对路由对照

记录文件：

- `docs/experiments/2026-06-03-selector-rule-v2-pair-contrast.md`

设置：

- SPECK32/64 r=6, `speck32_gohr2019`
- PRESENT-80 r=5, `present_wang_jain2021`
- SM4 r=4, `sm4_yu2023_conv_resnet`
- `ciphertext_pair_xor_bits`, `pairs_per_sample=1,4`
- `8192/class`, `5 epochs`, `seeds=0 1 2`, `hidden_bits=32`

输出：

- `outputs/innovation_one_selector_rule_v2_pair_contrast_plan.csv`
- `outputs/innovation_one_selector_rule_v2_pair_contrast.jsonl`
- `outputs/innovation_one_selector_rule_v2_pair_contrast_summary.csv`

路由验证：

| cipher | pairs | `selector_rule` | `selector_rule_v2` |
|---|---:|---|---|
| SPECK32/64 | 1 | `resnet_bitslice` | `resnet_bitslice` |
| SPECK32/64 | 4 | `adaptive_dbitnet_pairwise` | `adaptive_dbitnet_pairwise` |
| PRESENT-80 | 1 | `senet_resnext` | `senet_resnext` |
| PRESENT-80 | 4 | `senet_resnext` | `adaptive_dbitnet_pairwise` |
| SM4 | 1 | `multiscale_dense_resnet` | `multiscale_dense_resnet` |
| SM4 | 4 | `multiscale_dense_resnet` | `adaptive_dbitnet_pairwise` |

关键 calibrated accuracy / AUC：

| cipher | pairs | best/important model | calibrated accuracy mean | AUC mean |
|---|---:|---|---:|---:|
| SPECK32/64 | 1 | `mlp` | 0.5722 | 0.5835 |
| SPECK32/64 | 4 | `adaptive_dbitnet_pairwise` | 0.7751 | 0.8488 |
| PRESENT-80 | 1 | `mlp` | 0.5483 | 0.5644 |
| PRESENT-80 | 4 | `selector_rule_v2` | 0.6383 | 0.6814 |
| SM4 | 1 | `moe_v3_soft` | 0.9666 | 0.9897 |
| SM4 | 4 | `moe_v3_soft` | 1.0000 | 1.0000 |

v2 证据：

- PRESENT5 multi-pair 下，v2 从旧规则的 `senet_resnext` 切到 `adaptive_dbitnet_pairwise`，calibrated accuracy 从 0.5703 提升到 0.6383。
- SM4 r=4 multi-pair 下，v2 从 `multiscale_dense_resnet` 切到 `adaptive_dbitnet_pairwise`，calibrated accuracy 从 0.9128 提升到 0.9999。
- SPECK multi-pair 下 v1/v2 均选 `adaptive_dbitnet_pairwise`，结果接近最强单专家。
- single-pair 下 v2 不覆盖结构专家，保留 ARX/SPN/Feistel-like 结构路由。

限制：

- SPECK single-pair 当前 `resnet_bitslice` 弱于 MLP，不能代表 Gohr 2019 专用模型水平；Gohr 对齐必须使用 `gohr_resnet_speck` + `ciphertext_pair_bits`。
- SM4 r=4 multi-pair 已接近满分，后续应推进 r=5 或更难差分，避免实验过浅。
- `moe_v3_soft` 在 SM4 上很强，但 PRESENT 上低于 v2/单 pairwise 专家，说明软融合仍存在专家稀释。

### 结构适配框架推进

记录文件：

- `docs/experiments/2026-06-02-structure-adaptation-framework.md`

已完成：

- `adaptive_dbitnet_pairwise` 的 `pair_bits` 不再固定 96，runner 会按 block size 与 feature encoding 自动推断。
- `ciphertext_pair_xor_bits` 下：
  - SPECK32/64: `pair_bits=96`
  - PRESENT-80: `pair_bits=192`
  - SM4: `pair_bits=384`
- 新增 `moe_v3_uniform/hard/soft`，专家池使用 `adaptive_dbitnet_pairwise`。
- 新增 `selector_rule`，用于结构规则路由。
- 跨 SPECK/PRESENT/SM4 smoke 已通过，不作为性能结论。

下一步：

- 将 `selector_rule_v2` 作为创新一结构适配主基线。
- 推进更高轮/更难设置：
  - SPECK32/64：Gohr-style single-pair 与 pairwise multi-pair 分开比较。
  - PRESENT-80：推进 r=6 或更多差分 member。
  - SM4：推进 r=5，避免 r=4 接近满分。

### Pairwise Adaptive DBitNet SPECK6 筛查

记录文件：

- `docs/experiments/2026-06-02-pairwise-adaptive-dbitnet-speck6-screen.md`

SPECK6, `ciphertext_pair_xor_bits`, `pairs_per_sample=4`, `hidden_bits=64`, `8192/class`, `5 epochs`：

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `adaptive_dbitnet_pairwise` | 0.7861 | 0.8625 |
| `mlp` | 0.6286 | 0.6695 |
| `adaptive_dbitnet` | 0.6001 | 0.6355 |

结论：

- pairwise 共享 encoder + mean/max pooling 显著超过直接 384-bit 长序列 DBitNet。
- 该结果接近 Gohr SPECK6 单 pair 文献准确率约 0.788，但协议不同：这里是 `pairs_per_sample=4` + `ciphertext_pair_xor_bits`。
- 这是创新一目前最强结构优化证据；后续应接入 MoE v3 专家池。

### Pairwise pooling 与 pair 数量消融筛查

记录文件：

- `docs/experiments/2026-06-03-pairwise-pooling-speck-present-screen.md`

设置：

- SPECK32/64 r=6, `speck32_gohr2019`
- PRESENT-80 r=5, `present_wang_jain2021`
- `ciphertext_pair_xor_bits`
- `pairs_per_sample=1,2,4,8`
- `8192/class`, `5 epochs`, `seeds=0 1 2`, `hidden_bits=32`

新增模型 key：

- `adaptive_dbitnet_pairwise_mean`
- `adaptive_dbitnet_pairwise_max`
- `adaptive_dbitnet_pairwise_mean_max`
- 默认 `adaptive_dbitnet_pairwise` 仍等价于 `mean_max`，兼容历史实验。

关键结果：

| cipher | pairs | best model | calibrated accuracy mean | AUC mean |
|---|---:|---|---:|---:|
| SPECK32/64 | 1 | `mlp` | 0.5739 | 0.5855 |
| SPECK32/64 | 2 | `adaptive_dbitnet_pairwise_mean_max` | 0.6360 | 0.6844 |
| SPECK32/64 | 4 | `adaptive_dbitnet_pairwise_mean_max` | 0.7738 | 0.8497 |
| SPECK32/64 | 8 | `adaptive_dbitnet_pairwise_mean` | 0.8805 | 0.9491 |
| PRESENT-80 | 1 | `mlp` | 0.5483 | 0.5644 |
| PRESENT-80 | 2 | `mlp` | 0.5665 | 0.5889 |
| PRESENT-80 | 4 | `adaptive_dbitnet_pairwise_mean_max` | 0.6343 | 0.6770 |
| PRESENT-80 | 8 | `adaptive_dbitnet_pairwise_mean` | 0.7664 | 0.8414 |

结论：

- `pairs=4/8` 下，pairwise 编码显著优于直接宽输入 `adaptive_dbitnet`，支持小论文“共享 pair 编码与聚合”主线。
- `pairs=8` 在 SPECK/PRESENT 上明显增强；但不能预设所有密码单调提升，SM4 需单独验证。
- `mean+max` 在 `pairs=4` 更强，`mean` 在 `pairs=8` 更强且更稳。
- 扩大验证优先选择 `adaptive_dbitnet_pairwise_mean` 与 `adaptive_dbitnet_pairwise_mean_max`，`max` 作为消融保留。

### MoE v2 Adaptive DBitNet 专家消融

记录文件：

- `docs/experiments/2026-06-02-moe-v2-adaptive-dbitnet-speck6-screen.md`

SPECK6, `ciphertext_pair_xor_bits`, `pairs_per_sample=4`, `hidden_bits=64`, `8192/class`, `5 epochs`：

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `mlp` | 0.6313 | 0.6717 |
| `moe_soft` | 0.6284 | 0.6691 |
| `moe_v2_hard` | 0.5986 | 0.6313 |
| `adaptive_dbitnet` | 0.5964 | 0.6316 |
| `moe_v2_soft` | 0.5957 | 0.6285 |
| `moe_hard` | 0.5724 | 0.5960 |

结论：

- 替换为 adaptive DBitNet 后，hard gate 明显改善：`moe_hard` 0.5724 -> `moe_v2_hard` 0.5986。
- 但 `moe_v2_soft` 低于旧 `moe_soft` 和 MLP，说明简单替换专家还不是最终方案。
- 下一步应实现 `adaptive_dbitnet_pairwise`：每个 ciphertext pair 共享 encoder，再跨 pair pooling/attention 融合。

### Gohr ResNet SPECK 训练日程筛查

记录文件：

- `docs/experiments/2026-06-02-gohr-speck-training-schedule-screen.md`

关键结果：

| 配置 | 轮数 | calibrated accuracy mean | AUC mean |
|---|---:|---:|---:|
| `gohr_resnet_speck`, 8192/class, 5 epochs | 5 | 0.8527 | 0.9074 |
| `gohr_resnet_speck`, 8192/class, 5 epochs | 6 | 0.6675 | 0.7134 |
| `gohr_resnet_speck`, 8192/class, 5 epochs | 7 | 0.5095 | 0.5039 |
| `gohr_resnet_speck_depth10`, cyclic LR | 6 | 0.6304 | 0.6662 |
| `gohr_resnet_speck`, AMSGrad, 32768/class, 10 epochs | 6 | 0.6978 | 0.7535 |

结论：

- 真正 SPECK 专用 4-channel Gohr-style reshape 明显强于此前简化 ResNet / DBitNet / MLP。
- AMSGrad + 更大样本 + 更多 epoch 对 SPECK6 有实质提升。
- depth10 + 当前 cyclic LR 设置没有提升，不能把“更深网络”作为创新点硬写。
- 当前最好 SPECK6 仍低于 Gohr 2019 约 0.788，后续需继续校准 bit ordering、网络细节与训练日程。

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

- 已实现 `gohr_resnet_speck` 与 `gohr_resnet_speck_depth10`，使用 SPECK32/64 的 4 channels × 16 bit positions 输入 reshape。
- 当前 SPECK6 最好为 `0.6978 / AUC 0.7535`，相对项目旧模型显著提升，但尚未达到 Gohr 文献水平。
- 下一步应继续排查 Gohr 原始 bit ordering、残差块/BN/ReLU 细节、训练集规模与学习率衰减。

优先级 2：

- 将 `adaptive_dbitnet_pairwise` 接入 MoE v3：
  - 替换 MoE v2 中的 `adaptive_dbitnet` 专家。
  - 对比 `moe_v2_hard/soft`、`moe_v3_hard/soft`、`adaptive_dbitnet_pairwise`、`mlp`。
  - 检查 MoE 是否因为弱专家拖累 pairwise 强专家；必要时设计 ARX 专家专用 gate。

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
