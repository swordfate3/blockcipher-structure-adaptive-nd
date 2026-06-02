# 结构适配框架推进记录

日期：2026-06-02

## 目的

将创新一从“单个 SPECK 强模型”推进为完整的结构适配框架：

```text
密码结构特征 -> 输入组织方式 -> 专家选择/路由 -> 统一实验协议
```

本次改动不是性能实验结论，而是让跨结构实验能够统一运行，为后续 SPECK / PRESENT /
SM4 的结构适配矩阵做准备。

## 关键改动

### 1. pairwise DBitNet 自动 pair_bits

此前 `adaptive_dbitnet_pairwise` 在工厂中固定 `pair_bits=96`，只适合 SPECK32/64 的：

```text
ciphertext_pair_xor_bits = C || C' || ΔC = 32 + 32 + 32 = 96 bits
```

现在 runner 会根据 cipher block size 和 feature encoding 推断：

| feature encoding | pair_bits |
|---|---:|
| `ciphertext_pair_bits` | `2 * block_bits` |
| `ciphertext_pair_xor_bits` | `3 * block_bits` |

因此：

| cipher | block bits | `ciphertext_pair_xor_bits` pair_bits |
|---|---:|---:|
| SPECK32/64 | 32 | 96 |
| PRESENT-80 | 64 | 192 |
| SM4 | 128 | 384 |

### 2. MoE v3 专家池

新增模型键：

```text
moe_v3_uniform
moe_v3_hard
moe_v3_soft
```

MoE v3 专家池：

```text
resnet_bitslice
adaptive_dbitnet_pairwise
cnn
mlp
senet_resnext
multiscale_dense_resnet
```

相比 MoE v2，v3 将 `adaptive_dbitnet` 替换为 `adaptive_dbitnet_pairwise`。

### 3. 结构规则选择器

新增实验入口：

```text
selector_rule
```

当前规则：

| structure | condition | selected model |
|---|---|---|
| ARX | `pairs_per_sample > 1` | `adaptive_dbitnet_pairwise` |
| ARX | single pair | `resnet_bitslice` |
| SPN | - | `senet_resnext` |
| Feistel-like | - | `multiscale_dense_resnet` |
| fallback | - | `mlp` |

这不是最终最优路由，而是用于结构适配消融的规则基线。

## Smoke 验证

命令：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 present80 sm4 \
  --models selector_rule moe_v3_hard mlp \
  --rounds 1 \
  --seeds 0 \
  --samples-per-class 64 \
  --pairs-per-sample 2 \
  --epochs 1 \
  --batch-size 32 \
  --hidden-bits 8 \
  --feature-encoding ciphertext_pair_xor_bits \
  --output outputs/innovation_one_structure_adaptation_smoke.jsonl
```

验证点：

- SPECK32/64 自动使用 `pair_bits=96`。
- PRESENT-80 自动使用 `pair_bits=192`。
- SM4 自动使用 `pair_bits=384`。
- `selector_rule` 记录 `selected_model`：
  - SPECK32/64 -> `adaptive_dbitnet_pairwise`
  - PRESENT-80 -> `senet_resnext`
  - SM4 -> `multiscale_dense_resnet`
- `moe_v3_hard` 能在三种结构上统一运行，并记录 `expert_set=v3_pairwise`。

## 后续实验

下一步应跑正式结构适配矩阵，而不是只看 smoke：

```text
ciphers:
  SPECK32/64 r=6
  PRESENT-80 r=5 或文献差分对应轮数
  SM4 r=4 或文献差分对应轮数

models:
  mlp
  adaptive_dbitnet
  adaptive_dbitnet_pairwise
  senet_resnext
  multiscale_dense_resnet
  moe_v2_soft
  moe_v3_soft
  selector_rule
```

评价重点：

- `selector_rule` 是否接近每个结构的最优单专家。
- `moe_v3_*` 是否因混入弱专家而稀释强 pairwise 专家。
- 错误结构路由是否明显下降。
