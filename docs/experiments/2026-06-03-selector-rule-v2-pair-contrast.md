# Selector Rule v2 单对/多对路由对照实验

日期：2026-06-03

## 目的

上一轮结构适配主矩阵显示：

```text
multi-pair 输入下，adaptive_dbitnet_pairwise 往往比单纯按密码结构选择专家更强。
```

因此本轮验证修正规则 `selector_rule_v2`：

| condition | selected model |
|---|---|
| `pairs_per_sample > 1` | `adaptive_dbitnet_pairwise` |
| ARX single pair | `resnet_bitslice` |
| SPN single pair | `senet_resnext` |
| Feistel-like single pair | `multiscale_dense_resnet` |
| fallback | `mlp` |

实验问题：

```text
1. v2 是否按预期在 single-pair 和 multi-pair 间切换？
2. multi-pair 下输入组织优先的路由是否比旧结构路由更好？
3. MoE v3 与强单专家相比是否仍存在稀释或不稳定？
```

## 实验设置

计划文件：

- `outputs/innovation_one_selector_rule_v2_pair_contrast_plan.csv`

输出：

- `outputs/innovation_one_selector_rule_v2_pair_contrast.jsonl`
- `outputs/innovation_one_selector_rule_v2_pair_contrast_summary.csv`

统一设置：

```text
feature_encoding = ciphertext_pair_xor_bits
pairs_per_sample = 1, 4
samples_per_class = 8192
epochs = 5
batch_size = 1024
hidden_bits = 32
seeds = 0 1 2
```

结构与差分：

| cipher | structure | rounds | difference profile |
|---|---|---:|---|
| SPECK32/64 | ARX | 6 | `speck32_gohr2019` |
| PRESENT-80 | SPN | 5 | `present_wang_jain2021`, member 0 |
| SM4 | Feistel-like | 4 | `sm4_yu2023_conv_resnet` |

模型：

```text
mlp
adaptive_dbitnet_pairwise
moe_v3_soft
selector_rule
selector_rule_v2
```

## 路由检查

`selector_rule` 与 `selector_rule_v2` 的实际 `selected_model` 如下：

| cipher | pairs | selector_rule | selector_rule_v2 |
|---|---:|---|---|
| SPECK32/64 | 1 | `resnet_bitslice` | `resnet_bitslice` |
| SPECK32/64 | 4 | `adaptive_dbitnet_pairwise` | `adaptive_dbitnet_pairwise` |
| PRESENT-80 | 1 | `senet_resnext` | `senet_resnext` |
| PRESENT-80 | 4 | `senet_resnext` | `adaptive_dbitnet_pairwise` |
| SM4 | 1 | `multiscale_dense_resnet` | `multiscale_dense_resnet` |
| SM4 | 4 | `multiscale_dense_resnet` | `adaptive_dbitnet_pairwise` |

结论：v2 的切换逻辑正确。它只在 multi-pair 下覆盖旧结构专家；single-pair 下仍保留结构适配。

## 结果

指标为 3 个 seed 的 mean/std。主表使用 calibrated accuracy；AUC 保持原始阈值无关指标。

### SPECK32/64 r=6

| pairs | model | calibrated acc mean | calibrated acc std | AUC mean |
|---:|---|---:|---:|---:|
| 1 | `mlp` | 0.5722 | 0.0027 | 0.5835 |
| 1 | `moe_v3_soft` | 0.5544 | 0.0069 | 0.5704 |
| 1 | `adaptive_dbitnet_pairwise` | 0.5492 | 0.0084 | 0.5633 |
| 1 | `selector_rule_v2` | 0.5216 | 0.0060 | 0.5249 |
| 1 | `selector_rule` | 0.5200 | 0.0054 | 0.5233 |
| 4 | `adaptive_dbitnet_pairwise` | 0.7751 | 0.0072 | 0.8488 |
| 4 | `selector_rule` | 0.7734 | 0.0112 | 0.8487 |
| 4 | `selector_rule_v2` | 0.7732 | 0.0129 | 0.8472 |
| 4 | `moe_v3_soft` | 0.7722 | 0.0039 | 0.8476 |
| 4 | `mlp` | 0.6213 | 0.0055 | 0.6577 |

观察：

- SPECK6 在 `pairs=4` 下，pairwise 专家、v1、v2 和 MoE v3 都接近；v1 和 v2 都路由到 `adaptive_dbitnet_pairwise`。
- SPECK6 在 `pairs=1` 下，当前 `resnet_bitslice` 不是强单对基线，反而低于 MLP。该单对结果不代表 Gohr-style 专用模型水平；Gohr 专用模型应单独使用 `gohr_resnet_speck` + `ciphertext_pair_bits` 协议评估。

### PRESENT-80 r=5

| pairs | model | calibrated acc mean | calibrated acc std | AUC mean |
|---:|---|---:|---:|---:|
| 1 | `mlp` | 0.5483 | 0.0003 | 0.5644 |
| 1 | `selector_rule` | 0.5476 | 0.0018 | 0.5571 |
| 1 | `selector_rule_v2` | 0.5475 | 0.0023 | 0.5568 |
| 1 | `moe_v3_soft` | 0.5225 | 0.0027 | 0.5233 |
| 1 | `adaptive_dbitnet_pairwise` | 0.5167 | 0.0037 | 0.5174 |
| 4 | `selector_rule_v2` | 0.6383 | 0.0155 | 0.6814 |
| 4 | `adaptive_dbitnet_pairwise` | 0.6311 | 0.0187 | 0.6738 |
| 4 | `moe_v3_soft` | 0.6075 | 0.0326 | 0.6432 |
| 4 | `mlp` | 0.5891 | 0.0039 | 0.6222 |
| 4 | `selector_rule` | 0.5703 | 0.0041 | 0.5949 |

观察：

- PRESENT5 是 v2 修正最清晰的证据：`pairs=4` 时，v2 从旧规则的 `senet_resnext` 切到 `adaptive_dbitnet_pairwise`，calibrated accuracy 从 0.5703 提升到 0.6383。
- `adaptive_dbitnet_pairwise` 单专家本身也明显强于旧结构路由，说明 multi-pair 输入组织对 PRESENT 也有效。
- MoE v3 高于 MLP，但低于 v2/单 pairwise 专家，说明软融合仍会稀释强专家。

### SM4 r=4

| pairs | model | calibrated acc mean | calibrated acc std | AUC mean |
|---:|---|---:|---:|---:|
| 1 | `moe_v3_soft` | 0.9666 | 0.0333 | 0.9897 |
| 1 | `selector_rule` | 0.7851 | 0.0283 | 0.8667 |
| 1 | `selector_rule_v2` | 0.7826 | 0.0312 | 0.8640 |
| 1 | `adaptive_dbitnet_pairwise` | 0.6737 | 0.2086 | 0.6884 |
| 1 | `mlp` | 0.5741 | 0.0064 | 0.5840 |
| 4 | `moe_v3_soft` | 1.0000 | 0.0000 | 1.0000 |
| 4 | `selector_rule_v2` | 0.9999 | 0.0001 | 1.0000 |
| 4 | `adaptive_dbitnet_pairwise` | 0.9998 | 0.0002 | 1.0000 |
| 4 | `selector_rule` | 0.9128 | 0.0144 | 0.9725 |
| 4 | `mlp` | 0.6010 | 0.0016 | 0.6223 |

观察：

- SM4 r=4 对当前差分较容易，`pairs=4` 下 MoE v3、v2、pairwise 单专家几乎满分。
- v2 仍明显高于旧结构路由：0.9999 vs 0.9128。
- `pairs=1` 下 MoE v3 明显强，但方差也不小；后续 SM4 需要推进到 r=5 或更难差分，否则该结果论文价值有限。

## 结论

本轮支持以下论文口径：

1. 结构适配需要同时看密码结构和输入组织。旧规则只按结构选专家，在 PRESENT/SM4 的 multi-pair 设置下会错过 pairwise 输入组织带来的强信号。
2. `selector_rule_v2` 是一个更合理的实验路由基线：single-pair 保留结构专家，multi-pair 优先选择 pairwise 共享编码专家。
3. MoE v3 是有价值的融合模型，但目前不是稳定最优；在 PRESENT 上仍有专家稀释，在 SM4 上则可能受任务过易影响。
4. SPECK single-pair 不应使用当前 `resnet_bitslice` 作为 Gohr 文献水平结论；要对齐 Gohr 2019，仍需使用 `gohr_resnet_speck`、`ciphertext_pair_bits` 和 Gohr-style 训练协议。

## 后续

下一步更适合推进两条线：

```text
1. 将 selector_rule_v2 作为结构适配主基线写入创新一实验设计。
2. 做更高轮/更难设置：
   - SPECK32/64: Gohr-style single-pair 与 pairwise multi-pair 分开比较。
   - PRESENT-80: 继续 r=6 或更多差分 member。
   - SM4: 推进 r=5，避免 r=4 接近满分导致结论过浅。
```
