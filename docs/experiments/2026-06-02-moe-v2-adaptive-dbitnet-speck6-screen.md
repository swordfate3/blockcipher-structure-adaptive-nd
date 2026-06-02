# MoE v2 Adaptive DBitNet 专家消融

日期：2026-06-02

## 目的

验证将 MoE 专家池中的旧固定 dilation `dbitnet_dilated_cnn` 替换为
`adaptive_dbitnet` 后，是否能改善 SPECK6 多密文对宽输入下的专家融合效果。

## 代码变更

新增 MoE v2 模型键：

```text
moe_v2_uniform
moe_v2_hard
moe_v2_soft
```

旧 MoE 专家池保持不变：

```text
resnet_bitslice
dbitnet_dilated_cnn
cnn
mlp
senet_resnext
multiscale_dense_resnet
```

MoE v2 专家池：

```text
resnet_bitslice
adaptive_dbitnet
cnn
mlp
senet_resnext
multiscale_dense_resnet
```

即本次只替换 DBitNet 专家，保持专家数量和 gate 权重位置不变，方便做公平消融。

## 实验命令

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models mlp adaptive_dbitnet moe_hard moe_v2_hard moe_soft moe_v2_soft \
  --rounds 6 \
  --seeds 0 1 2 \
  --samples-per-class 8192 \
  --pairs-per-sample 4 \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 64 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_moe_v2_adaptive_speck6_screen.jsonl
```

## 结果

| model | gate | calibrated accuracy mean | AUC mean |
|---|---|---:|---:|
| `mlp` | - | 0.6313 | 0.6717 |
| `moe_soft` | soft legacy | 0.6284 | 0.6691 |
| `moe_v2_hard` | hard adaptive | 0.5986 | 0.6313 |
| `adaptive_dbitnet` | - | 0.5964 | 0.6316 |
| `moe_v2_soft` | soft adaptive | 0.5957 | 0.6285 |
| `moe_hard` | hard legacy | 0.5724 | 0.5960 |

## 结论

- 将旧 `dbitnet_dilated_cnn` 替换为 `adaptive_dbitnet` 后，hard gate 从
  `0.5724 / AUC 0.5960` 提升到 `0.5986 / AUC 0.6313`。
- 说明 adaptive DBitNet 作为专家确实比旧固定 dilation DBitNet 更适合作为宽输入专家。
- 但 v2 soft gate 从旧 `moe_soft` 的 `0.6284 / AUC 0.6691` 降到
  `0.5957 / AUC 0.6285`，没有超过 MLP。
- 当前不能写成“MoE v2 超越强 baseline”；只能写成“DBitNet 专家替换改善 hard gate，
  但融合路由与专家容量仍需继续优化”。

## 后续方向

下一步更值得做的是 pairwise DBitNet 专家，而不是继续简单替换：

```text
adaptive_dbitnet_pairwise
```

设计方向：

- 输入按 `pairs_per_sample` 拆成多个 ciphertext-pair 子输入。
- 每个 pair 共享 adaptive DBitNet encoder。
- pair-level embedding 再用 mean/max pooling 或 attention 融合。
- 与 MLP、旧 `adaptive_dbitnet`、`moe_v2_*` 做同预算消融。

这样更贴近多密文对论文中的“每对先提特征，再跨 pair 聚合”的结构，而不是把
384-bit 宽输入直接当作一条长 bit 序列。
