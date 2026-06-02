# Adaptive DBitNet 实现记录

日期：2026-06-02

## 背景

Bellini et al. 2023 的 cipher-agnostic neural training pipeline 提出 DBitNet，用自适应 dilation 的 1D 卷积替代 Gohr ResNet 中依赖密码 word reshape 的手工输入结构。

论文中的关键点：

- dilation rates 根据输入宽度自动生成。
- 64-bit input 对应 `[31, 15, 7, 3]`。
- 128-bit input 对应 `[63, 31, 15, 7, 3]`。
- 256-bit input 对应 `[127, 63, 31, 15, 7, 3]`。
- prediction head 使用固定强头：`256 -> 256 -> 64 -> 1`。

当前项目旧模型 `dbitnet_dilated_cnn` 只是轻量近似，固定 dilation 为 `1, 2, 4`，且用 `AdaptiveAvgPool1d(1)` 后接单层线性头，不能代表文献里的自适应输入宽度 DBitNet。

## 新增模型

新增模型 key：

- `adaptive_dbitnet`

新增实现：

- `src/blockcipher_ai_eval/models/adaptive_dbitnet.py`

核心行为：

| input bits | adaptive dilations |
|---:|---|
| 64 | `[31, 15, 7, 3]` |
| 96 | `[47, 23, 11, 5]` |
| 128 | `[63, 31, 15, 7, 3]` |
| 384 | `[191, 95, 47, 23, 11, 5]` |

每个 dilated block 使用：

- `Conv1d(kernel_size=2, dilation=d)`
- `BatchNorm1d`
- `ReLU`
- `Conv1d(kernel_size=3, padding=1)`
- `BatchNorm1d`
- `ReLU`

通道数随层数增长：

```text
base_channels, base_channels + 16, base_channels + 32, ...
```

分类头：

```text
Flatten -> Linear(256) -> ReLU -> Linear(256) -> ReLU -> Linear(64) -> ReLU -> Linear(1)
```

## Smoke 验证

命令：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models adaptive_dbitnet \
  --rounds 1 \
  --seeds 0 \
  --samples-per-class 8 \
  --epochs 1 \
  --batch-size 8 \
  --hidden-bits 8 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/adaptive_dbitnet_smoke.jsonl
```

结果：

```text
[1/1] SPECK32/64 r=1 model=adaptive_dbitnet seed=0 pairs=1
wrote 1 rows to outputs/adaptive_dbitnet_smoke.jsonl
```

## 后续实验建议

优先用 `adaptive_dbitnet` 复查 SPECK6：

1. `ciphertext_pair_bits`，对齐 Gohr/DBitNet 原始 64-bit pair 输入。
2. `ciphertext_pair_xor_bits`，对齐当前项目的增强输入。
3. `pairs_per_sample=1,4`，观察输入宽度增大后自适应 dilation 是否优于 MLP。
4. `hidden_bits=32,64`，避免直接使用过重配置。

如果 `adaptive_dbitnet` 在 SPECK6/SPECK7 上仍显著弱于文献，则下一步应补 Gohr 原版 4-channel word-aware ResNet，而不是继续扩大 MoE。
