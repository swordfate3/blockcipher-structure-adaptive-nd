# 神经网络差分区分器模型调研补充

调研日期：2026-06-02

## 结论先行

目前本项目已经收集并抽取了 30 篇创新一相关论文，覆盖了神经差分区分器的核心模型线：Gohr ResNet、DBitNet/AutoND、SENet/SE-ResNeXt、多密文对、bit selection、NNBits ensemble、PRESENT/SPN、SM4 卷积残差网络、GPD、RX-neural、polytopic neural distinguisher、GIFT/ASCON score-distribution MLP test 和评估综述。

前一轮登记为 `pending_download` 的 3 篇近年论文已经补齐并抽取文本：

- 双差分 / related-key neural distinguisher。
- GIFT-128 / ASCON 的 score-distribution + MLP test 模型。
- Enhanced related-key SIMON/SIMECK。

这不表示整个领域永远“找齐”，但对当前创新一的核心清单来说，本地已有完整 PDF/text 证据链。这些新工作不一定都需要完整实现，但至少要在论文相关工作和创新边界里说明；其中 GPD、多输入/多差分、多密文对数据格式、SENet/SE-ResNeXt、score-distribution/MLP test 最值得作为创新一后续实验扩展。

## 已覆盖模型谱系

| 模型 / 方法 | 代表论文 | 本项目状态 | 对创新一的意义 |
|---|---|---|---|
| Gohr-style ResNet-BitSlice | Gohr 2019, SPECK32/64 | 已下载；已实现 `resnet_bitslice` | ARX/SPECK 强基线，所有新模型必须和它比较 |
| MLP / CNN 基线 | Baksi 2020; PRESENT 2020/2021; 多篇比较论文 | 已下载；已实现 `mlp`, `cnn` | 轻量但不能忽视，SPECK6 扩大验证中 MLP 已成强基线 |
| DBitNet / AutoND | Bellini et al., cipher-agnostic pipeline | 已下载；已实现 `dbitnet_dilated_cnn` | 通用管线边界论文，创新一不能声称“首次通用”，应强调结构感知匹配 |
| SENet / SE-ResNeXt | Bao et al. 2022, Simon32/64 | 已下载；未实现 | AND-RX/SIMON/SIMECK 分支重要候选模型，适合补入模型池 |
| 多密文对输入 | Chen et al. 2021; Lu et al. 2022/2024 | 已下载；未系统实现 | 说明输入表示本身是模型能力的一部分，适合扩展 `multi_pair_*` |
| bit selection / partial ML | Ebrahimi et al. 2022 | 已下载；未实现 | 可做低成本特征选择或输入 mask 消融 |
| NNBits ensemble | NNBits 2023 | 已下载；未实现 | 与 MoE/ensemble 接近，但目标是 bit profiling，不是结构路由 |
| SM4 Conv-ResNet | 余玥琳等 2023 | 已下载；已有 SM4 分支和差分配置 | 支撑 SM4 不能只当普通 SPN 处理 |
| SPN-specific framework | Liu 2026, IoT-friendly lightweight SPN | 已下载；未实现专门 SPN 模型 | 支撑 PRESENT/GIFT 类结构需要数据格式与网络结构优化 |
| SoK / Assessment | GLN 2022; SoK 2024/2025 | 已下载 | 支撑统一协议、多种子、可比较性和谨慎表述 |

## 近年需要补齐的模型线

### 1. 双差分 / related-key neural distinguisher

代表论文：

- Gao Wang, Gaoli Wang, Siwei Sun, *A New (Related-Key) Neural Distinguisher Using Two Differences for Differential Cryptanalysis*, IET Information Security, 2024. DOI: `10.1049/2024/4097586`.

核心思想：

- 不再只用一个固定输入差分生成正样本，而是使用两个不同差分生成的 ciphertext pairs。
- 目标是增强 related-key 或 differential neural distinguisher 对非线性结构的捕获能力。
- 论文提出自动训练框架，包括 difference selection、sample generation、training pipeline、evaluation scheme。

对创新一影响：

- 这条线和我们当前 MoE 的“专家融合”不同，它是在数据生成/差分输入层面做融合。
- 后续可以新增 `difference_profile` 的 `members > 1` 模式，训练时同一样本接收多差分来源，作为 `multi_difference` 消融。
- 如果论文里写创新一，要避免说“第一次融合多个差分信号”；更准确说法是“结构感知地选择/融合网络专家，并在统一协议下评估不同结构和输入差分配置”。

### 2. Enhanced related-key SIMON/SIMECK

代表论文：

- *Enhanced related-key differential neural distinguishers for SIMON and SIMECK block ciphers*, PeerJ Computer Science, 2024.

核心思想：

- 针对 SIMON/SIMECK 的 related-key 场景继续优化。
- 使用差分选择策略和增强数据格式，进一步扩展可区分轮数。
- 公开了代码和数据记录，可作为 SIMON/SIMECK 后续复现实验入口。

对创新一影响：

- 本项目目前没有 SIMON/SIMECK cipher module，因此 AND-RX 分支仍不完整。
- 如果论文要覆盖“按密码结构匹配”，SIMON/SIMECK 是必须考虑的结构类别之一，因为它们不是 SPECK 那种加法型 ARX，而是 AND-RX/Feistel-like。

### 3. Polytopic / 多输入差分神经区分器

代表论文：

- Iman Mirzaali, Sadegh Sadeghi, Nasour Bagheri, *Improved polytopic differential neural distinguishers for SIMON, SIMECK, and SPECK block ciphers*, Cybersecurity, 2026.

核心思想：

- 使用 polytope / 多输入差分，而不是普通 pairwise differential。
- 输入样本可以是多个相关明密文形成的高阶结构，例如四个 ciphertexts。
- 论文在 SIMON、SIMECK、SPECK 上报告了单钥和相关钥场景结果。

对创新一影响：

- 这是“多密文对”和“多差分”的进一步结构化版本。
- 如果我们只实现单对 ciphertext pair，那么会漏掉近年一个重要趋势。
- 可作为后续 `polytope_encoder` 或 `multi_pair_dbitnet` 的依据。

### 4. Generic Partial Decryption, GPD

代表论文：

- Bellini, Brunelli, Gerault, Hambitzer, Pedicini, *Generic Partial Decryption as Feature Engineering for Neural Distinguishers*, ePrint 2025/1443; LATINCRYPT 2025.

核心思想：

- 在不依赖完整人工密码特化的前提下，对 ciphertext pairs 做若干轮“零密钥或随机轮密钥”的部分逆运算。
- 把得到的 partial differentials 作为神经区分器输入特征。
- 该方法试图在 AutoND 的通用性和专门手工特征工程之间折中。

对创新一影响：

- 对我们很重要，因为创新一强调“结构感知”。GPD 正好说明：完全 cipher-agnostic 未必最强，适度引入密码结构可以显著增强模型。
- 可新增一个特征模式：`ciphertext_pair_xor_bits + partial_decryption_features`。
- 不一定先实现全套 GPD，但论文里应把它作为“近年通用管线向结构化特征回归”的证据。

### 5. GIFT-128 / ASCON score-distribution + MLP test

代表论文：

- Shen, Song, Lu, Long, Tian, *Neural differential distinguishers for GIFT-128 and ASCON*, Journal of Information Security and Applications, 2024.

核心思想：

- 第一阶段先训练区分单个 ciphertext difference 的神经区分器，输出 score。
- 第二阶段不直接分类单个 pair，而是用多个 ciphertext differences 的 score distribution 训练 MLP test。
- 在 GIFT-128 和 ASCON-PERMUTATION 上提升了区分效果。

对创新一影响：

- 这条线不是单纯换网络结构，而是改变判别对象：从 pair-level 到 distribution-level。
- 对 SPN/GIFT 和 permutation/ASCON 很有意义。
- 如果后续加入 GIFT 或 ASCON，应实现 `score_distribution_mlp` 作为单独模型类型。

### 6. RX-neural / rotational-XOR 神经区分器

代表论文：

- Ebrahimi 等，*Deep Learning-Based Rotational-XOR Cryptanalysis*, SAC 2023 preproceedings。
- Liu, Chen, Xiang, Zhang, Zeng, *Enhancing Deep Learning-Based Rotational-XOR Attacks on Lightweight Block Ciphers Simon32/64 and Simeck32/64*, arXiv 2025。

核心思想：

- 样本不再基于普通 XOR difference，而是基于 rotational-XOR, RX, difference。
- 对 AND-RX / ARX-like cipher 更贴合结构特性。
- 近年工作加入 bit sensitivity、数据格式压缩和多密文对，进一步提高轮数。

对创新一影响：

- 这是“结构感知”的强证据：差分定义本身会随密码结构变化。
- 当前项目的 difference profile 只有 XOR 差分，后续如果覆盖 SIMON/SIMECK，应新增 `difference_kind = xor | rx | related_key | polytope`。

### 7. PRESENT entropy-based neural distinguisher

代表论文：

- *Key recovery attack on PRESENT using an entropy-based neural distinguisher*, Neural Computing and Applications, 2026.

核心思想：

- 针对 PRESENT 的 key recovery 设计 entropy-based neural distinguisher。
- 和普通 pair classifier 不完全相同，更接近将神经区分器嵌入攻击流程。

对创新一影响：

- PRESENT 分支不能只停留在 Jain/Kohli/Mishra 2020/2021。
- 若论文实验重点是“区分器”而不是“完整 key recovery”，可先作为相关工作；若扩展到攻击流程，则应补读全文。

### 8. 多密文对 + 多尺度卷积 / dense residual

代表论文：

- Hou, Liu, Han, Ma, Ye, Nie, *Improving deep learning-based neural distinguisher with multiple ciphertext pairs for Speck and Simon*, Scientific Reports, 2025. DOI: `10.1038/s41598-025-98251-1`.

核心思想：

- 重新设计神经网络结构，使用 multi-scale convolutional block 和 dense residual connections。
- 不只使用单个 ciphertext pair，还构造多密文对输入，并组合 ciphertext pairs、ciphertext differences、keys 和 key differences。
- 在 Speck32/64 和 Simon32/64 上报告相对已有模型的准确率提升，并做 key recovery success rate 验证。

对创新一影响：

- 这篇非常贴近我们的“结构感知输入 + 模型匹配”，因为它同时改网络结构和数据格式。
- 它也提醒我们：MoE 如果只融合专家输出，不改输入数据格式，可能会输给更强的 multi-pair / engineered-dataset baseline。
- 后续应新增 `multi_pair` 数据集管线，并在 MoE 消融中比较 `single_pair` 与 `multi_pair`。

## 当前项目实现缺口

| 缺口 | 优先级 | 原因 | 建议动作 |
|---|---:|---|---|
| SENet / SE-ResNeXt | 高 | Simon/SIMECK 文献中表现强，是 ResNet 后的重要模型 | 加入 `senet_resnext`，先在 SPECK/PRESENT/SM4 上做横向，再等 SIMON 模块 |
| 多密文对 / 多差分输入 | 高 | 2021-2026 多篇论文都在强调输入组织方式 | 加 `samples_per_item` 或 `pairs_per_sample` 参数 |
| 多尺度卷积 / dense residual | 高 | 2025 Speck/Simon 多密文对论文显示结构和数据格式共同影响准确率 | 加 `multiscale_dense_resnet` 或先作为 `senet_resnext` 后的第二候选 |
| GPD 部分解密特征 | 高 | 直接支撑结构感知特征工程 | 先设计接口，不急于全密码实现 |
| SIMON/SIMECK cipher module | 高 | AND-RX 类结构目前缺位 | 新增 cipher + 文献差分 + related-key 可选 |
| RX difference | 中高 | ARX/AND-RX 特有差分定义 | 先作为 difference profile schema 扩展 |
| score-distribution MLP test | 中 | GIFT/ASCON 新模型，适合 SPN/permutation | 加入二阶段评估脚本 |
| NNBits-like profiling | 中 | 对解释性有帮助，但工程量较大 | 先不做主实验，作为分析模块 |
| entropy-based PRESENT | 中 | 更偏 key recovery | 区分器论文相关工作先引用，实验后置 |

## 对论文创新一的表述建议

不要写：

> 本文首次提出神经网络融合差分区分器，解决所有分组密码结构。

建议写：

> 近年神经差分密码分析已从 Gohr 式单差分 ResNet，发展出 DBitNet/AutoND、SENet/SE-ResNeXt、多密文对、多差分、GPD 特征工程和 RX-neural 等方向。现有工作多针对单一密码、单一差分设置或单一改进机制展开，实验协议和模型选择依据不完全统一。本文聚焦“密码结构特性与神经区分器架构之间的适配关系”，在统一数据生成、训练预算和评价指标下，构建结构感知模型池与专家融合机制，比较 ARX、SPN、Feistel-like 等结构上的模型偏好，并通过文献差分和消融实验验证结构特征对模型选择的影响。

## 下一步推荐

1. 先实现 `senet_resnext`、`multi_pair` 输入和轻量 `multiscale_dense_resnet`，这是离当前代码最近、也最能提升创新一可信度的三项。
2. 精读新下载的 GPD、RX-neural、polytopic、multi-pair multiscale、PRESENT entropy、two-difference RKND、Enhanced RK SIMON/SIMECK、GIFT/ASCON 八篇，抽取可复现实验参数。
3. 将原先待下载的三篇近年论文纳入实现优先级：two-difference data generation、related-key SIMON/SIMECK、score-distribution MLP test。
4. 扩展 difference profile schema：加入 `difference_kind`、`pairs_per_sample`、`related_key_difference`、`polytope_size`。
5. 若时间允许，再新增 SIMON/SIMECK 模块，作为 AND-RX 结构分支。
