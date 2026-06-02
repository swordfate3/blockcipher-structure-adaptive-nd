# Gohr SPECK 训练日程筛查

日期：2026-06-02

## 目的

在 `gohr_resnet_speck` 实现后，验证 SPECK32/64 文献差分 `speck32_gohr2019`
下的强基线是否能接近 Gohr 2019 报告水平。

当前实验结论需要保守表述：

- 新增的 Gohr-style 4-channel word-aware 模型显著强于项目内旧模型。
- 样本数与 AMSGrad 训练设置能继续提升 SPECK6。
- 当前实现仍未达到 Gohr 2019 SPECK6 约 `0.788`、SPECK7 约 `0.616`
  的文献水平，不能声称已经复现 SOTA。

## 实验 1：小规模横向筛查

命令：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models gohr_resnet_speck resnet_bitslice adaptive_dbitnet mlp \
  --rounds 5 6 7 \
  --seeds 0 1 2 \
  --samples-per-class 8192 \
  --pairs-per-sample 1 \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 32 \
  --feature-encoding ciphertext_pair_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_gohr_speck_repro_screen.jsonl
```

汇总：

| rounds | model | calibrated accuracy mean | AUC mean |
|---:|---|---:|---:|
| 5 | `gohr_resnet_speck` | 0.8527 | 0.9074 |
| 5 | `adaptive_dbitnet` | 0.7977 | 0.8549 |
| 5 | `resnet_bitslice` | 0.6884 | 0.7187 |
| 5 | `mlp` | 0.5492 | 0.5666 |
| 6 | `gohr_resnet_speck` | 0.6675 | 0.7134 |
| 6 | `resnet_bitslice` | 0.5214 | 0.5258 |
| 6 | `adaptive_dbitnet` | 0.5203 | 0.5243 |
| 6 | `mlp` | 0.5082 | 0.5015 |
| 7 | `gohr_resnet_speck` | 0.5095 | 0.5039 |
| 7 | `adaptive_dbitnet` | 0.5088 | 0.5041 |
| 7 | `resnet_bitslice` | 0.5068 | 0.5016 |
| 7 | `mlp` | 0.5066 | 0.4951 |

结论：

- 4-channel word-aware 输入组织是 SPECK/ARX 强基线的关键，目前已经显著超过旧
  `resnet_bitslice`。
- SPECK6 的 `0.6675` 仍明显低于 Gohr 2019 约 `0.788`。

## 实验 2：depth10 + cyclic LR 负结果

为靠近深残差训练路线，新增模型键：

```text
gohr_resnet_speck_depth10
```

训练参数：

- `samples_per_class=8192`
- `epochs=5`
- `optimizer=adamw`
- `amsgrad=True`
- `weight_decay=1e-5`
- `lr_scheduler=cyclic`
- `learning_rate=1e-4`
- `max_learning_rate=3e-3`

结果：

| rounds | model | calibrated accuracy mean | AUC mean |
|---:|---|---:|---:|
| 5 | `gohr_resnet_speck_depth10` | 0.8407 | 0.8986 |
| 6 | `gohr_resnet_speck_depth10` | 0.6304 | 0.6662 |
| 7 | `gohr_resnet_speck_depth10` | 0.5070 | 0.5026 |

结论：

- 在当前预算下，depth10 + 较高峰值 cyclic LR 反而弱于浅层
  `gohr_resnet_speck`。
- 这说明不能简单把“更深网络”写成提升点；需要继续对齐原论文训练日程或做系统调参。

## 实验 3：SPECK6 AMSGrad 大样本专项

命令：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models gohr_resnet_speck \
  --rounds 6 \
  --seeds 0 1 2 \
  --samples-per-class 32768 \
  --pairs-per-sample 1 \
  --epochs 10 \
  --batch-size 4096 \
  --hidden-bits 32 \
  --learning-rate 0.001 \
  --optimizer adam \
  --amsgrad \
  --weight-decay 0.00001 \
  --lr-scheduler none \
  --feature-encoding ciphertext_pair_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_gohr_amsgrad_speck6_screen.jsonl
```

结果：

| rounds | model | samples/class | epochs | calibrated accuracy mean | AUC mean |
|---:|---|---:|---:|---:|---:|
| 6 | `gohr_resnet_speck` | 32768 | 10 | 0.6978 | 0.7535 |

结论：

- 相对实验 1 的 SPECK6 `0.6675 / AUC 0.7134`，AMSGrad + 更大样本 +
  更多 epoch 提升到 `0.6978 / AUC 0.7535`。
- 训练设置方向有效，但仍未达到文献强基线；后续需要优先排查：
  - Gohr 原始 bit ordering 与当前 `(x, y, x', y')` bit ordering 是否完全一致。
  - Conv1d block、dense head、BN/ReLU 顺序与论文/开源实现是否一致。
  - 是否需要更长训练、学习率衰减或更大的训练集。
  - 评估集大小与阈值校准是否和文献可比。

## 对创新一的影响

目前可写成：

> 在统一实验协议下，结构感知输入组织显著改变 SPECK32/64 神经区分器表现；
> SPECK 专用 Gohr-style 4-channel ResNet 在 5/6 轮上明显强于通用 MLP、简化
> ResNet 与 Adaptive DBitNet。进一步的 AMSGrad 大样本训练能提升 6 轮性能，
> 但尚未完全复现 Gohr 2019 的最高报告结果，因此本文后续将其作为强基线校准
> 与结构适配研究对象，而不是宣称已超越前沿。
