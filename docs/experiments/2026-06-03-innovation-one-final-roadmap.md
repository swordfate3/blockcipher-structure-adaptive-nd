# 创新一最终推进路线图

日期：2026-06-03

## 总定位

创新一最终收束为：

```text
面向分组密码结构与输入组织联合适配的神经差分区分器方法。
```

该定位同时服务两个任务：

| 任务 | 定位 | 核心产出 |
|---|---|---|
| 毕业论文 | 结构感知与输入组织联合适配框架 | 创新一完整章节、跨结构主表、高轮边界、消融实验 |
| 中文核心小论文 | 多密文对输入下的共享 pair 编码与聚合方法 | Pairwise Adaptive DBitNet 子线、pair 数量消融、pooling 消融 |

## 不再发散的边界

不把创新一写成：

- MoE 全面优于所有模型。
- Pairwise Adaptive DBitNet 超越所有前沿神经区分器。
- 直接复现 Bellini et al. DBitNet 的原始结构。
- 直接超过 Gohr 2019 SPECK single-pair 协议。

安全表述：

```text
本文在统一 reduced-round 协议下，比较密码结构、输入组织方式和神经网络专家之间的适配关系。
Pairwise Adaptive DBitNet 是本文基于 DBitNet-style 自适应扩张卷积与 multi-pair 输入组织设计的变体。
```

## 毕业论文主轨

毕业论文创新一保留完整框架：

1. 密码结构特征：ARX、SPN、Feistel-like。
2. 输入组织：single-pair / multi-pair，`C || C'` 与 `C || C' || C xor C'`。
3. 专家池：MLP、Gohr/ResNet、SENet、Multiscale Dense ResNet、Adaptive DBitNet、Pairwise Adaptive DBitNet。
4. 融合与路由：MoE v3、`selector_rule`、`selector_rule_v2`。
5. 实验协议：文献差分、统一样本量、统一训练预算、AUC/calibrated accuracy。

主表优先级：

| priority | experiment | purpose |
|---:|---|---|
| 1 | `selector_rule` vs `selector_rule_v2` | 证明输入组织必须进入结构适配 |
| 2 | `adaptive_dbitnet` vs `adaptive_dbitnet_pairwise` | 证明 pairwise 不是简单输入变宽 |
| 3 | single-pair vs multi-pair | 证明输入组织改变最优专家 |
| 4 | SPECK/PRESENT/SM4 跨结构 | 证明不是单密码偶然 |
| 5 | PRESENT r=6、SM4 r=5、SPECK r=7 | 证明方法边界，不只低轮过易 |

## 小论文副轨

小论文只切 pairwise 子线：

```text
多密文对神经差分区分器的共享 Pair 编码与聚合方法。
```

核心对照：

| experiment | models |
|---|---|
| concat vs pairwise | `adaptive_dbitnet`, `adaptive_dbitnet_pairwise` |
| pair 数量消融 | `pairs_per_sample=1,2,4,8` |
| pooling 消融 | mean, max, mean+max |
| 跨密码验证 | SPECK32/64、PRESENT-80、SM4 |
| 边界验证 | SPECK r=7、PRESENT r=6、SM4 r=5 |

已新增 pooling ablation keys：

```text
adaptive_dbitnet_pairwise_mean
adaptive_dbitnet_pairwise_max
adaptive_dbitnet_pairwise_mean_max
```

其中：

- `adaptive_dbitnet_pairwise` 保持为默认 mean+max，兼容历史实验。
- `adaptive_dbitnet_pairwise_mean_max` 是显式消融 key，等价于默认 key。

## 下一组实验

先跑小规模筛查，确认 pair 数量和 pooling 方向：

```text
ciphers:
  SPECK32/64 r=6, speck32_gohr2019
  PRESENT-80 r=5, present_wang_jain2021 member 0
  SM4 r=4, sm4_yu2023_conv_resnet

feature_encoding:
  ciphertext_pair_xor_bits

pairs_per_sample:
  1, 2, 4, 8

models:
  mlp
  adaptive_dbitnet
  adaptive_dbitnet_pairwise_mean
  adaptive_dbitnet_pairwise_max
  adaptive_dbitnet_pairwise_mean_max

training:
  samples_per_class = 8192
  epochs = 5
  batch_size = 1024
  hidden_bits = 32
  seeds = 0, 1, 2
```

实验目的：

1. 比较直接宽输入 `adaptive_dbitnet` 与 pairwise 编码。
2. 判断 mean、max、mean+max 哪种聚合更稳。
3. 判断 `pairs_per_sample` 是否单调提升，或者存在最佳点。
4. 给毕业论文消融表和小论文主表同时提供数据。

## 扩大验证

筛查后选择每个密码最有希望的 1-2 个设置扩大：

```text
samples_per_class = 32768
epochs = 10
seeds = 0,1,2,3,4
```

扩大验证优先级：

1. SPECK32/64 r=6 pairwise vs concat。
2. PRESENT-80 r=5/6 pairwise pooling。
3. SM4 r=5 边界实验。

## 写作编排

毕业论文章节：

```text
方法：结构特征 -> 专家池 -> pairwise 专家 -> 显式路由
实验：跨结构主表 -> pairwise 消融 -> 路由消融 -> 高轮边界
```

小论文：

```text
问题：multi-pair 直接拼接弱化 pair 边界
方法：共享 pair encoder + pooling
实验：concat vs pairwise、pair 数量、pooling、跨密码
```
