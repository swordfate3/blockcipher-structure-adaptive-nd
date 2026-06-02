# Gohr ResNet SPECK 实现记录

日期：2026-06-02

## 目的

当前 `resnet_bitslice` 是简化版 Gohr-style 模型，使用 `2 × sequence_bits` reshape，不是 Gohr 原始 SPECK32/64 区分器的 4-channel word-aware 输入结构。

为复现 Gohr SPECK32/64 神经区分器，需要新增 SPECK 专用模型：

- 输入只接受 64-bit `C || C'` ciphertext pair。
- reshape 为 `4 channels × 16 bit positions`，对应 `(x, y, x', y')`。
- 使用 `Conv1d(kernel_size=1)` slicing stem。
- 使用 residual Conv1d blocks。
- 使用 dense prediction head，而不是全局池化后单层线性。

## 新增模型

新增模型 key：

```text
gohr_resnet_speck
```

新增文件：

- `src/blockcipher_ai_eval/models/gohr_speck.py`
- `tests/test_gohr_speck_model.py`

当前结构：

```text
64-bit C||C'
  -> reshape(batch, 4, 16)
  -> Conv1d(4, filters, kernel_size=1)
  -> residual Conv1d blocks
  -> Flatten
  -> Linear(filters * 16, 64)
  -> Linear(64, 64)
  -> Linear(64, 1)
```

默认参数：

- filters: experiment `hidden_bits`
- residual blocks: `1`

## 输入限制

`gohr_resnet_speck` 是 SPECK32/64 原始 pair 输入专用模型，只支持：

```text
input_bits = 64
feature_encoding = ciphertext_pair_bits
pairs_per_sample = 1
```

它不直接支持 `ciphertext_pair_xor_bits` 或 `pairs_per_sample=4` 的 96/384-bit 宽输入；后续如果需要，应单独设计 adapter，而不是把 Gohr 原版模型语义混到宽输入里。

## Smoke 验证

命令：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models gohr_resnet_speck \
  --rounds 1 \
  --seeds 0 \
  --samples-per-class 8 \
  --pairs-per-sample 1 \
  --epochs 1 \
  --batch-size 8 \
  --hidden-bits 8 \
  --feature-encoding ciphertext_pair_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/gohr_resnet_speck_smoke.jsonl
```

结果：

```text
[1/1] SPECK32/64 r=1 model=gohr_resnet_speck seed=0 pairs=1
wrote 1 rows to outputs/gohr_resnet_speck_smoke.jsonl
```

## 下一步

后续训练日程筛查记录见：

- `docs/experiments/2026-06-02-gohr-speck-training-schedule-screen.md`

已完成结果：

- 小规模 `8192/class, 5 epochs` 下，`gohr_resnet_speck` 达到：
  - SPECK5 calibrated accuracy `0.8527`, AUC `0.9074`
  - SPECK6 calibrated accuracy `0.6675`, AUC `0.7134`
  - SPECK7 接近随机
- 新增 `gohr_resnet_speck_depth10`，但当前 cyclic LR 小规模筛查没有超过浅层模型。
- SPECK6 使用 AMSGrad + `32768/class` + `10 epochs` 后提升到 calibrated accuracy
  `0.6978`, AUC `0.7535`。

仍需继续校准：

1. Gohr 原始 bit ordering 与当前 `(x, y, x', y')` bit ordering 是否完全一致。
2. residual block、BN/ReLU 顺序和 dense head 是否与论文/开源实现一致。
3. 是否需要更大训练集、更长训练或更接近论文的学习率衰减策略。
