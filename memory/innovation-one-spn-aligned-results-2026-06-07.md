# 创新一 SPN 结构对齐结果记忆

更新时间：2026-06-07

## 当前结论

创新一当前最强证据链已从 MoE/HPO 转向：

```text
面向 SPN 分组密码的结构对齐输入表示 + 匹配的 nibble-token mixer 神经差分区分器。
```

核心方法不是简单增加输入维度，也不是声称首次提出 TokenMixer，而是：

```text
PRESENT/SPN 的公开 P-layer 逆置换差分对齐
+ 4-bit nibble token 表示
+ token/channel mixing
+ 多密文对 attention/mean/max 聚合
```

论文中建议称为：

```text
SPN-TokenMixer 多密文对区分器
```

或：

```text
基于 SPN 结构对齐的 Nibble-Token Mixer 神经差分区分器
```

## 方法边界

### 输入表示

raw 输入：

```text
C || C' || ΔC
ΔC = C xor C'
```

SPN aligned 输入：

```text
C || C' || ΔC || P^-1(ΔC)
```

其中 `P^-1` 是 PRESENT 公开置换层的逆变换，不依赖密钥。

### 模型结构

模型 key：

```text
spn_token_mixer_pairset
```

代码类：

```text
SpnTokenMixerPairSetDistinguisher
```

实现位置：

```text
src/blockcipher_ai_eval/models/adaptive_dbitnet.py
```

主要结构：

- 将每个 ciphertext pair 的 bit 表示切成 `4-bit nibble` token。
- 每个 nibble 通过 `Linear(4 -> token_dim)` 编码。
- 加入可学习位置嵌入，保留 PRESENT S-box/P-layer 位置关系。
- 使用 token mixing 建模跨 nibble 位置扩散。
- 使用 channel mixing 建模 token 内特征组合。
- 对多个 ciphertext pairs 使用 attention/mean/max 聚合。

## 正式实验一：PRESENT 5 轮 10 seeds 确认

run id：

```text
innovation1-spn-aligned-confirm-present-gpu1-20260607
```

本地结果目录：

```text
outputs/remote_results/innovation1-spn-aligned-confirm-present-gpu1-20260607/
```

gate：

```text
result_lines=40
expected_rows=40
stderr=empty
```

协议：

- PRESENT-80。
- rounds = 5。
- difference profile = `present_wang_jain2021`。
- `pairs_per_sample=4`。
- `samples_per_class=32768`。
- seeds = `0..9`。
- epochs = 10。
- batch size = 1024。
- optimizer = AdamW。
- device = `cuda:1`。

结果：

| model | input | calibrated acc mean | acc std | AUC mean | AUC std |
|---|---:|---:|---:|---:|---:|
| `moe_v5_soft_hpo_present_best` | raw | 0.781354 | 0.006258 | 0.858458 | 0.005734 |
| `moe_v5_soft_hpo_present_best` | aligned | 0.779996 | 0.007232 | 0.855521 | 0.007771 |
| `spn_token_mixer_pairset` | raw | 0.791647 | 0.011208 | 0.869388 | 0.010827 |
| `spn_token_mixer_pairset` | aligned | 0.809634 | 0.003708 | 0.886577 | 0.003085 |

delta：

| model | aligned - raw acc | aligned - raw AUC |
|---|---:|---:|
| `moe_v5_soft_hpo_present_best` | -0.001358 | -0.002937 |
| `spn_token_mixer_pairset` | +0.017987 | +0.017190 |

SPN-TokenMixer 每个 seed 的 acc 提升：

| seed | aligned - raw acc |
|---:|---:|
| 0 | +0.021545 |
| 1 | +0.020508 |
| 2 | +0.024109 |
| 3 | +0.002258 |
| 4 | +0.007446 |
| 5 | +0.016876 |
| 6 | +0.015198 |
| 7 | +0.033020 |
| 8 | +0.031677 |
| 9 | +0.007233 |

解释：

```text
aligned 输入不是对所有模型都自动有效；
它对 MoE-HPO 略降，但对 SPN-TokenMixer 10 个 seed 全部正提升。
```

这支持“结构对齐输入 + 匹配结构网络”的联合适配结论。

## 正式实验二：PRESENT 4/5/6 轮 round sweep

run id：

```text
innovation1-spn-aligned-round-sweep-present-gpu0-20260607
```

本地结果目录：

```text
outputs/remote_results/innovation1-spn-aligned-round-sweep-present-gpu0-20260607/
```

gate：

```text
result_lines=30
expected_rows=30
stderr=empty
```

协议：

- PRESENT-80。
- rounds = 4, 5, 6。
- model = `spn_token_mixer_pairset`。
- raw vs aligned。
- seeds = `0..4`。
- `pairs_per_sample=4`。
- `samples_per_class=32768`。
- epochs = 10。
- device = `cuda:0`。

结果：

| rounds | raw calibrated acc | aligned calibrated acc | acc delta |
|---:|---:|---:|---:|
| 4 | 0.974792 | 0.983008 | +0.008215 |
| 5 | 0.793579 | 0.808459 | +0.014880 |
| 6 | 0.518970 | 0.583893 | +0.064923 |

| rounds | raw AUC | aligned AUC | AUC delta |
|---:|---:|---:|---:|
| 4 | 0.995518 | 0.997812 | +0.002294 |
| 5 | 0.870924 | 0.885217 | +0.014294 |
| 6 | 0.524862 | 0.615276 | +0.090414 |

每个 seed 的 acc delta：

| rounds | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 |
|---:|---:|---:|---:|---:|---:|
| 4 | +0.006653 | +0.017487 | +0.006195 | +0.002319 | +0.008423 |
| 5 | +0.020081 | +0.020508 | +0.024109 | +0.002258 | +0.007446 |
| 6 | +0.085876 | +0.078186 | +0.058380 | +0.036377 | +0.065796 |

解释：

```text
4/5/6 轮所有 seed 均为正提升。
6 轮 raw 已接近随机猜测，aligned 仍能拉到 0.583893。
这说明结构对齐在高轮困难场景下更明显。
```

## 创新边界

不能声称：

- 首次提出 TokenMixer。
- 首次提出 PRESENT 神经差分区分器。
- 首次提出多密文对神经区分器。
- 首次提出结构化特征工程。

前人已有相邻工作：

- Jain/Kohli/Mishra：PRESENT/Simeck neural distinguisher。
- Chen et al.：multiple ciphertext pairs neural distinguisher。
- Tolstikhin et al.：MLP-Mixer / token-channel mixing。
- Bellini et al.：DBitNet / AutoND / GPD 等通用或结构化特征工程。
- Hou et al.：Speck/Simon multi-pair + multi-scale convolution / dense residual。

可以主张：

```text
本文提出一种面向 SPN 型分组密码的结构对齐神经差分区分方法：
使用公开逆置换层构造 P^-1(ΔC) 对齐特征，
以 4-bit nibble 作为 token 设计 SPN-TokenMixer，
并在多密文对设置下验证输入表示与网络结构的联合适配。
```

推荐贡献写法：

1. 提出 SPN 结构对齐差分表示 `C || C' || ΔC || P^-1(ΔC)`。
2. 设计 nibble-level SPN-TokenMixer 多密文对区分器。
3. 在 PRESENT-80 多轮区分任务上证明该输入-模型联合适配稳定提升；同时 MoE-HPO 对 aligned 输入无提升，说明收益不是简单输入维度增加。

## 攻击协议与密钥泄露判断

当前没有明显密钥泄露：

- 网络输入不包含 key、round key 或真实中间状态。
- `P^-1(ΔC)` 只使用 PRESENT 公开 P-layer 的逆置换。
- 攻击者拿到 `C, C'` 后也可公开计算 `ΔC` 和 `P^-1(ΔC)`。

但当前实验是固定密钥区分器协议：

```text
present80 当前工厂 key = 0x00000000000000000000
```

因此论文中应谨慎表述为：

```text
reduced-round fixed-key neural distinguisher setting
```

不能直接声称已经完成实际 key recovery attack。

下一步必须补充的严谨性实验：

1. Cross-key 泛化：
   - train key 固定或多随机 key。
   - test keys 使用未见随机 key。
2. 负样本加密构造消融：
   - 负样本由 `E_K(P), E_K(Q)` 生成，而不是直接 random ciphertext。
3. 输入消融：
   - `ΔC`。
   - `ΔC || P^-1(ΔC)`。
   - `C || C' || ΔC`。
   - `C || C' || ΔC || P^-1(ΔC)`。
4. 模型消融：
   - `adaptive_dbitnet_pairwise` 同协议 raw/aligned。
   - 证明 aligned 需要匹配 SPN 网络结构。

## 推荐论文表述

```text
受 MLP-Mixer 中 token mixing 与 channel mixing 思想启发，本文针对 SPN 型分组密码的 S-box/P-layer 结构，设计了基于 nibble token 的 SPN-TokenMixer 神经差分区分器。不同于已有 PRESENT 神经区分器直接使用密文对或密文差分作为输入，本文进一步引入逆置换层对齐特征 P^-1(ΔC)，使输出差分重新映射到 S-box 局部结构视角，并通过 token mixing 建模 P-layer 引起的跨位置扩散关系。实验表明，该输入-模型联合适配方法在 PRESENT-80 多轮区分任务中稳定提升区分性能。
```

## 下一步优先级

1. 立即补 cross-key / random-key 泛化实验，降低固定密钥过拟合质疑。
2. 补 `adaptive_dbitnet_pairwise` raw/aligned round sweep，形成模型消融。
3. 补 `ΔC only` 与 `ΔC || P^-1(ΔC)` 输入消融，证明提升来自差分结构对齐。
4. 将本结果写入论文创新一章节的实验主表。
