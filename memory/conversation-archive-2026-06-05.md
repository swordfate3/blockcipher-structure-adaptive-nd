# Conversation Archive - 2026-06-05

本文件保存截至 2026-06-05 的连续对话上下文，用于后续继续创新一实验、远程 GPU 跑批和毕业论文写作时快速恢复状态。

## 1. 项目状态

当前项目目录：

```text
/home/fate/gitproject/blockcipher-structure-adaptive-nd
```

早期旧目录：

```text
/home/fate/gitproject/thesis_liaoxiyue
```

后续工作以新目录为准。Python 包名仍是：

```text
blockcipher_ai_eval
```

GitHub 仓库：

```text
https://github.com/swordfate3/blockcipher-structure-adaptive-nd
```

当前本地 `main` 曾出现 `ahead 1`，原因是新增远程状态检查脚本的提交因为 GitHub TLS 连接问题未成功 push；核心模型和实验代码已经先前推送过。

## 2. 创新一目标

用户主线目标是完成毕业论文创新一：

```text
面向分组密码结构特性的结构自适应神经差分区分器。
```

核心问题不是单纯堆一个大网络，而是研究：

```text
不同分组密码结构是否需要不同神经网络归纳偏置？
神经区分器能否根据 ARX / SPN / Feistel-like 等结构进行模型或专家适配？
```

潜在小论文副线：

```text
多密文对神经差分区分器的共享 pair encoder 与聚合方法。
```

副线可以从 `adaptive_dbitnet_pairwise` / pairset 聚合实验中拆出，但毕业论文仍是当前主任务。

## 3. 文献调研脉络

前期围绕神经差分区分器和分组密码结构适配调研过多篇论文，主要整理位置：

```text
docs/research/innovation_one_literature_index.md
docs/research/neural_differential_models_survey.md
papers/innovation_one/
```

讨论过的主要模型线索：

- Gohr 2019 SPECK32/64 神经区分器。
- Bellini 等 DBitNet / cipher-agnostic neural training pipeline。
- Multi-pair neural distinguisher。
- SENet / SE-ResNeXt。
- Multiscale Dense ResNet。
- GPD / Generic Partial Decryption。
- RX-neural、related-key、polytopic neural distinguishers。
- PRESENT / GIFT / ASCON 等轻量密码上的神经或统计区分研究。

当前文献边界判断：

```text
不能声称“首次通用神经区分器”或“首次多密文对神经区分器”。
更稳妥的创新表述是：结构感知模型匹配、结构先验输入组织、统一协议下的跨结构评估。
```

## 4. 已实现模型脉络

已经实现并接入实验入口的主要模型包括：

- `mlp`
- `cnn`
- `resnet_bitslice`
- `dbitnet_dilated_cnn`
- `adaptive_dbitnet`
- `adaptive_dbitnet_pairwise`
- `senet_resnext`
- `multiscale_dense_resnet`
- `moe_uniform` / `moe_hard` / `moe_soft`
- `moe_v2_*`
- `moe_v3_*`
- `moe_v4_*`
- `selector_rule`
- `selector_rule_v2`
- `lstm_roundseq`
- `transformer_encoder`
- `gohr_resnet_speck`
- `gohr_resnet_speck_depth10`
- `structure_adaptive_pairset_dbitnet`
- `structure_adaptive_pairset_dbitnet_attention`
- `structure_adaptive_pairset_dbitnet_mean_max`
- `spn_pairset_dbitnet_v2`

关键理解：

```text
adaptive_dbitnet_pairwise
```

是多密文对共享 pair encoder 主力基线。它保留每个密文对边界，再跨 pair 做聚合，比直接 concat 更贴 multi-pair 区分任务。

```text
structure_adaptive_pairset_dbitnet
```

是创新一重要候选之一。它不是 MoE，也不是 Bellini 原版 DBitNet，而是结构条件化 DBitNet dilation + bit-mask prior + pair-set 聚合。

```text
moe_v4_soft
```

是当前结构融合对照中表现稳定的模型，尤其在 PRESENT/SPN 实验中表现最好。但论文主张不应写成“MoE 本身是唯一创新”，而应写成“结构自适应专家融合框架”。

## 5. 密码算法与项目结构

用户明确要求：

```text
密码算法不能全部写在一个 py 文件里。
```

因此项目结构应按架构和算法分类，保证分组密码实现、实验入口、模型定义、远程脚本和测试分离。

讨论中覆盖的密码结构：

- ARX 类：SPECK、SIMON、SIMECK、CHAM、LEA 等。
- SPN 类：PRESENT、GIFT、RECTANGLE 等。
- Feistel-like / 传统结构：SM4、DES 类方向。
- ASCON 曾讨论过，但不作为当前创新一主线结果。

测试原则：

```text
新增密码算法必须有 KAT 或逆变换一致性测试；
新增实验模型必须能被 matrix runner 调用；
新增远程脚本必须有本地脚本测试覆盖。
```

## 6. 本地环境与 uv / PyTorch

项目使用 uv 虚拟环境和 PyTorch。

曾出现 `pip show torch` 返回未找到 torch。结论：不要只看裸 `pip`，应使用项目环境命令：

```bash
uv run python -c "import torch; print(torch.__version__)"
```

曾出现 warning：

```text
VIRTUAL_ENV=/home/fate/gitproject/thesis_liaoxiyue/.venv does not match the project environment path .venv
```

含义是 shell 仍激活旧项目 `.venv`，但 `uv run` 会忽略不匹配的 active venv，使用当前项目环境。通常无需重建 `.venv`，先 `deactivate` 再进入新项目目录即可。

## 7. 远程 GPU 流程

远程实验使用技能：

```text
remote-windows-gpu-conda-ssh
```

远程环境：

```text
host: 10.115.39.172
user: 1304Lijinlin
remote root: G:/lxy
project dir: G:/lxy/blockcipher-structure-adaptive-nd
python: F:/Anaconda/envs/DWT/torch310/python.exe
GPU: 2 x NVIDIA RTX A6000
torch: 2.5.1+cu118
CUDA runtime: 11.8
```

安全约束：远程 SSH 密码只用于交互登录，不能写入文档、脚本、commit、日志或最终回复。

通用流程：

1. 本地改代码。
2. 本地测试。
3. commit 并 push 到 GitHub。
4. 远程 `G:/lxy/<project>` 拉取最新代码。
5. 远程使用 `F:/Anaconda/envs/DWT/torch310/python.exe` 跑实验。
6. 长实验用 Windows Task Scheduler 启动。
7. 远程结果推送到 `results/<run_id>` 分支。
8. 本地用 `scripts/monitor_remote_results.py` 或对应 shell monitor 拉回到 `outputs/remote_results/<run_id>/`。

通用 Python 监控脚本：

```text
scripts/monitor_remote_results.py
```

多个 `.sh` 监控脚本可以包装它，只需要传入不同 run id 和 expected rows。

GitHub 偶发 TLS 问题：

```text
gnutls_handshake() failed
```

通常是网络问题，不代表实验没跑完。应优先检查远程 result branch 或本地 `outputs/remote_results/<run_id>`。

## 8. 已完成远程实验：MoE v4 sanity

早期 sanity run：

```text
innovation1-moe-v4-sanity
```

作用是证明远程 SSH / GPU / torch310 / 上传运行 / 结果拉回流程可用。该实验不是论文级结果，因为轮数低、样本小、部分任务过饱和。

## 9. 已完成远程实验：StructureAdaptive PairSet

两个主要 run：

```text
innovation1-structure-pairset-gpu0-20260605
innovation1-structure-pairset-gpu1-20260605
```

本地结果目录：

```text
outputs/remote_results/innovation1-structure-pairset-gpu0-20260605/
outputs/remote_results/innovation1-structure-pairset-gpu1-20260605/
```

完整性：

```text
GPU0: result_lines=72 expected_rows=72
GPU1: result_lines=36 expected_rows=36
stderr: 0 bytes
```

关键结论：`structure_adaptive_pairset_dbitnet` 对 SPECK/ARX 有正向效果。

代表结果：

```text
SPECK32/64 r6 pairs=4:
adaptive_dbitnet_pairwise          0.808899
structure_adaptive_pairset_dbitnet 0.847443
diff +0.038544
```

但它在 PRESENT/SPN 上表现差：

```text
PRESENT-80 r5 pairs=4:
adaptive_dbitnet_pairwise          0.770325
structure_adaptive_pairset_dbitnet 0.619583
diff -0.150742
```

解释：ARX 的 word/rotation/pairset 先验有效；SPN 不能只靠简单 PairSet 和结构 mask，需要更强的 S-box/nibble 局部建模。

## 10. 已完成远程实验：SPN PairSet DBitNet v2

为了修复 PRESENT/SPN 弱点，实现了：

```text
spn_pairset_dbitnet_v2
```

设计：

```text
DBitNet encoder + 显式 4-bit cell encoder + pairset attention/mean/max pooling
```

远程 run：

```text
innovation1-spn-pairset-v2-present-gpu1-20260605
```

实验配置：

```text
cipher: PRESENT-80
rounds: 4, 5
seeds: 0, 1
pairs_per_sample: 1, 2, 4
samples_per_class: 32768
epochs: 10
batch_size: 1024
hidden_bits: 64
optimizer: AdamW
device: cuda:1
expected_rows: 48
```

对比模型：

```text
adaptive_dbitnet_pairwise
structure_adaptive_pairset_dbitnet
spn_pairset_dbitnet_v2
moe_v4_soft
```

结果已经完成并拉回：

```text
outputs/remote_results/innovation1-spn-pairset-v2-present-gpu1-20260605/
```

完整性：

```text
result_lines=48
expected_rows=48
train stderr=0 bytes
summary stderr=0 bytes
```

聚合结论：

```text
moe_v4_soft                    mean=0.795647
adaptive_dbitnet_pairwise      mean=0.789121
structure_adaptive_pairset     mean=0.727336
spn_pairset_dbitnet_v2         mean=0.725334
```

任务胜出次数：

```text
moe_v4_soft                5 / 6
adaptive_dbitnet_pairwise  1 / 6
spn_pairset_dbitnet_v2     0 / 6
```

结论：

```text
spn_pairset_dbitnet_v2 没有证明有效。
简单 4-bit cell mean/max pooling 会过早丢掉 PRESENT 的 P-layer 位置扩散关系。
这个模型适合作为负向消融，而不是继续作为主线放大。
```

## 11. multi-pair 理解

用户问过 multi-pair 是否是多密文对区分。结论：是。

一个训练样本里包含多个满足同一输入差分的密文对。模型不是判断单个密文对，而是综合多个 pair 判断它们来自真实差分加密还是随机对照。

当前项目中的典型组织方式：

```text
每个 pair: C || C' || C xor C'
多个 pair: [pair_1, pair_2, ..., pair_k]
```

`adaptive_dbitnet_pairwise` 和 pairset 模型会共享 pair encoder，再做 mean/max/attention 聚合。

注意：multi-pair 准确率提升是真实区分证据的一部分，但不能和 single-pair 论文结果直接混比。必须明确 pairs_per_sample、样本生成协议、差分、轮数、训练样本量和评估协议。

## 12. 当前模型路线判断

目前不建议继续把 `spn_pairset_dbitnet_v2` 单独加大作为主线。

更优先的路线：

```text
moe_v5_structure_adaptive + spn_nibble_conv_pairset expert
```

理由：

```text
ARX 上 structure_adaptive_pairset_dbitnet 有提升；
PRESENT/SPN 上 moe_v4_soft 当前最强；
spn v2 的简单 cell pooling 不够；
创新一需要体现“不同结构激活不同专家”，而不是固定单模型包打天下。
```

建议新增 SPN 专家：

```text
spn_nibble_conv_pairset
```

或：

```text
spn_cellconv_pairset_dbitnet
```

核心结构：

```text
输入密文对 bits
-> 按 pair 切分
-> 按 4-bit nibble / S-box cell reshape
-> nibble 内部 MLP 或 small conv
-> nibble 间 1D grouped convolution / residual conv
-> 保留 PRESENT 16 个 nibble 的位置序列
-> PairSet attention 聚合多个密文对
-> classifier
```

与 v2 的区别：v2 太早做 cell mean/max pooling，丢掉位置关系；新 SPN expert 要保留 nibble 序列，并建模 nibble 间传播。

论文叙事建议：

```text
ARX: rotation/word/pairset prior 有效。
SPN: 简单 cell pooling 不足，需要 nibble/S-box 局部专家。
MoE: 用结构路由或软门控融合不同结构专家。
```

## 13. 创新一是否偏移

当前判断：没有偏移，但需要控制表述。

不能写成：

```text
我做了一个 MoE，所以更强。
```

应写成：

```text
面向分组密码结构差异的神经区分器结构适配方法。
通过 ARX / SPN / Feistel-like 的结构先验、输入组织和专家路由，研究不同结构下神经网络归纳偏置的适配效果。
```

负向实验也有价值：SPN v2 失败说明简单 cell pooling 不足，支持“结构适配不是随便加标签，而要匹配结构传播机制”的论点。

## 14. 下一步建议

短期推进：

1. 实现 `spn_nibble_conv_pairset`。
2. 本地 smoke test，确认 matrix runner 可调用。
3. 跑 PRESENT r4/r5 对比：

```text
adaptive_dbitnet_pairwise
structure_adaptive_pairset_dbitnet
spn_pairset_dbitnet_v2
spn_nibble_conv_pairset
moe_v4_soft
```

4. 若 `spn_nibble_conv_pairset` 接近或超过 MoE，则接入 `moe_v5_structure_adaptive`。
5. 若单体 SPN expert 不赢但 MoE v5 赢，则论文表述为专家单体不一定总是最优，但结构路由融合能稳定选择有效归纳偏置。
6. 若 SPN expert 和 MoE v5 都不赢，则 PRESENT/SPN 作为负例，毕业论文主结果聚焦 ARX/SPECK/SIMON，并把 SPN 作为结构适配边界分析。

## 15. 写作提醒

论文中需要避免的风险表述：

- 不要把 multi-pair 结果直接说成超过 single-pair SOTA。
- 不要把 MoE 表述为“当前前沿已证明最强”，除非有同协议对比。
- 不要声称 SPN v2 成功，因为当前结果没有支持。
- 不要把 SM4 低轮饱和结果当作强证据。
- 不要只给准确率，需要同时给 AUC、advantage、轮数、差分、pairs_per_sample、样本量、seed。

推荐表述：

```text
在统一实验协议下，结构条件化 pair-set DBitNet 在 ARX/SPECK 上显示出相对 pairwise baseline 的提升；
而 SPN/PRESENT 上简单 cell pooling 未能提升，提示 SPN 需要保留 S-box/nibble 位置传播的结构专家；
因此后续采用结构路由 MoE，将 ARX word expert、SPN nibble expert 和 Feistel branch expert 统一为结构自适应神经区分器框架。
```
