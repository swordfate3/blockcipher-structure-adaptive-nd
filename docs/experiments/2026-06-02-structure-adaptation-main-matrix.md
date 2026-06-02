# 结构适配主矩阵实验

日期：2026-06-02

## 目的

验证创新一的核心问题：

```text
不同分组密码结构是否需要不同的输入组织和神经网络专家？
结构规则路由是否能接近各结构下的强专家？
MoE 融合是否会稀释强专家？
```

## 实验设置

计划文件：

- `outputs/innovation_one_structure_adaptation_main_plan.csv`

输出：

- `outputs/innovation_one_structure_adaptation_main.jsonl`
- `outputs/innovation_one_structure_adaptation_main_summary.csv`

统一设置：

```text
feature_encoding = ciphertext_pair_xor_bits
pairs_per_sample = 4
samples_per_class = 8192
epochs = 5
batch_size = 1024
hidden_bits = 32
seeds = 0 1 2
```

结构与文献差分：

| cipher | structure | rounds | difference profile |
|---|---|---:|---|
| SPECK32/64 | ARX | 6 | `speck32_gohr2019` |
| PRESENT-80 | SPN | 5 | `present_wang_jain2021`, member 0 |
| SM4 | Feistel-like | 4 | `sm4_yu2023_conv_resnet` |

模型：

```text
mlp
adaptive_dbitnet
adaptive_dbitnet_pairwise
senet_resnext
multiscale_dense_resnet
moe_v2_soft
moe_v3_soft
selector_rule
```

## 结果

### SPECK32/64 r=6

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `adaptive_dbitnet_pairwise` | 0.7728 | 0.8470 |
| `selector_rule` | 0.7727 | 0.8474 |
| `moe_v3_soft` | 0.7716 | 0.8486 |
| `mlp` | 0.6242 | 0.6617 |
| `adaptive_dbitnet` | 0.5754 | 0.6041 |
| `moe_v2_soft` | 0.5732 | 0.5969 |
| `senet_resnext` | 0.5243 | 0.5282 |
| `multiscale_dense_resnet` | 0.5170 | 0.5162 |

结论：

- ARX/SPECK multi-pair 下，pairwise DBitNet 是最强专家。
- `selector_rule` 几乎等于最强专家，说明 ARX multi-pair 路由选对。
- `moe_v3_soft` 接近最强专家，没有明显稀释。

### PRESENT-80 r=5

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `adaptive_dbitnet_pairwise` | 0.6407 | 0.6826 |
| `moe_v3_soft` | 0.6090 | 0.6424 |
| `mlp` | 0.5891 | 0.6222 |
| `multiscale_dense_resnet` | 0.5745 | 0.5998 |
| `senet_resnext` | 0.5710 | 0.5949 |
| `selector_rule` | 0.5707 | 0.5950 |
| `adaptive_dbitnet` | 0.5522 | 0.5674 |
| `moe_v2_soft` | 0.5485 | 0.5638 |

结论：

- 本轮正式矩阵显示，PRESENT5 multi-pair 下 `adaptive_dbitnet_pairwise`
  也强于原本假设的 SPN 专家 `senet_resnext`。
- 旧 `selector_rule` 对 PRESENT 选 `senet_resnext`，因此没有选到最优专家。
- 这说明结构规则需要同时考虑 `pairs_per_sample`：multi-pair 输入组织本身是强结构信号。

### SM4 r=4

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `adaptive_dbitnet_pairwise` | 0.9999 | 1.0000 |
| `moe_v3_soft` | 0.9998 | 1.0000 |
| `selector_rule` | 0.9166 | 0.9741 |
| `multiscale_dense_resnet` | 0.9138 | 0.9736 |
| `mlp` | 0.6010 | 0.6223 |
| `moe_v2_soft` | 0.5773 | 0.6101 |
| `adaptive_dbitnet` | 0.5295 | 0.5336 |
| `senet_resnext` | 0.5186 | 0.5163 |

结论：

- SM4 r=4 multi-pair 下 `adaptive_dbitnet_pairwise` 与 `moe_v3_soft` 几乎满分。
- `selector_rule` 选择 `multiscale_dense_resnet`，明显强于 MLP，但低于 pairwise 专家。
- 对 Feistel-like/SM4，旧结构规则仍有解释力，但 multi-pair pairwise 专家更强。

## 规则路由修正

正式矩阵反馈：旧 `selector_rule` 只在 ARX multi-pair 下选中最强专家；PRESENT 和 SM4
在 multi-pair 设置下也更偏向 `adaptive_dbitnet_pairwise`。

因此新增：

```text
selector_rule_v2
```

规则：

| condition | selected model |
|---|---|
| `pairs_per_sample > 1` | `adaptive_dbitnet_pairwise` |
| ARX single pair | `resnet_bitslice` |
| SPN single pair | `senet_resnext` |
| Feistel-like single pair | `multiscale_dense_resnet` |
| fallback | `mlp` |

## 论文表述建议

可以写：

> 实验表明，结构适配不仅体现在密码结构本身，也体现在输入组织方式上。
> 在 multi-pair 输入下，pairwise DBitNet 通过共享 pair encoder 和跨 pair pooling
> 同时适配 ARX、SPN 与 Feistel-like 三类结构；而在没有 pairwise 路由的 MoE v2 中，
> 专家融合不能充分利用该信号。结构规则路由需要同时考虑密码结构与输入组织。

不能写：

> pairwise DBitNet 全面超越所有前沿方法。

原因：

- 当前是 reduced-round 三类密码的统一协议实验，不是每个密码的 SOTA attack setting。
- SPECK 与 Gohr 单 pair 文献协议不同。
- SM4 r=4 过强，后续需要检查 r=5 或更难差分设置。

## 后续

下一步应跑：

```text
selector_rule_v2
moe_v3_hard
moe_v3_soft
adaptive_dbitnet_pairwise
mlp
```

并在：

```text
pairs_per_sample = 1 和 4
```

上做对照，证明规则从 single-pair 到 multi-pair 的切换是必要的。
