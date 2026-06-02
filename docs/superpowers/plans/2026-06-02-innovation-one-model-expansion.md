# 创新一模型与数据格式扩展计划

日期：2026-06-02

## 目标

在现有 `mlp`、`cnn`、`resnet_bitslice`、`dbitnet_dilated_cnn`、`lstm_roundseq`、`transformer_encoder` 和 SA-MoE 基础上，补齐近年神经差分区分器中最影响创新一可信度的模型与输入格式：

1. `senet_resnext`：SENet / SE-ResNeXt 风格专家。
2. `multiscale_dense_resnet`：多尺度卷积 + dense residual 轻量实现。
3. `multi_pair` 数据管线：每个样本由多个 ciphertext pairs 组成。
4. `difference_kind` schema：为 XOR / RX / related-key / polytope 预留配置。
5. `entropy_bit_selection`：先实现为输入 mask/特征选择模块，不立刻做完整 PRESENT key recovery。

## 文献依据

- Bao et al. 2022：SENet/SE-ResNeXt 在 Simon32/64 长轮区分上优于普通 ResNet/DenseNet。
- Hou et al. 2025：多尺度卷积、dense residual 和多密文对数据格式能提升 Speck/Simon 神经区分器准确率。
- Bellini et al. 2025 GPD：结构化 partial decryption feature 是通用管线和手工特征工程之间的关键折中。
- Liu et al. 2025 RX-neural：ARX/AND-RX 不应只使用 XOR difference，还要支持 rotational-XOR difference。
- Mirzaali et al. 2026 PDND：polytope / ciphertext quadruples 是多输入差分区分的重要路线。
- Martínez et al. 2026 PRESENT entropy：PRESENT/SPN 可通过 entropy-based bit selection 降低输入维度并保留接近 SOTA 的准确率。

## 实施步骤

### 1. 模型池扩展

- 新增 `src/blockcipher_ai_eval/models/senet_resnext.py`。
- 新增 `src/blockcipher_ai_eval/models/multiscale_dense_resnet.py`。
- 更新 `src/blockcipher_ai_eval/models/__init__.py` 和 `experiments/factories.py`。
- 更新 `innovation_one.py` 的 `NetworkProfile`、`MODEL_KEYS` 和结构匹配规则。
- 为两个模型补最小单元测试：输入 shape、输出 shape、非法 input bits。

### 2. 数据格式扩展

- 在数据生成或实验 runner 中加入 `pairs_per_sample`，默认 `1` 保持兼容。
- 单 pair 时维持当前输入。
- 多 pair 时将多个 pair 的 bit features 拼接为 `pairs_per_sample * feature_bits`，先不改 label 逻辑。
- 实验 runner 记录 `pairs_per_sample` 到 CSV。

### 3. 差分配置 schema 扩展

- 在 `DifferenceProfile` 中增加可选字段：
  - `difference_kind`: `xor` 默认。
  - `pairs_per_sample`: 默认 `1`。
  - `related_key_difference`: 可选。
  - `polytope_size`: 默认 `2`，普通 pair；PDND 可设 `4`。
- 当前先不完整实现 RX/polytope 生成，只做 schema 和报错保护。

### 4. Entropy Bit Selection

- 新增一个轻量输入 mask 工具：
  - 支持显式 bit index 列表。
  - 支持从差分样本统计单 bit 或 bit tuple 熵的接口占位。
- 先在 PRESENT 文献差分上做 mask 消融，不做完整 key recovery。

### 5. 实验顺序

1. SPECK32/64 5/6 轮：
   - `mlp`
   - `resnet_bitslice`
   - `dbitnet_dilated_cnn`
   - `senet_resnext`
   - `multiscale_dense_resnet`
   - `moe_uniform`
   - `moe_soft`
2. PRESENT 4/5 轮：
   - 加 `entropy_bit_selection` 消融。
3. SM4 4 轮：
   - 验证新模型是否只是增加参数，还是确有结构适配。
4. 多 pair 小规模筛查：
   - `pairs_per_sample = 2, 4, 8`
   - 先跑 SPECK5/PRESENT4，确认管线可用。

## 论文写作边界

可以主张：

- 当前工作系统化比较“密码结构、输入格式、网络架构”三者的适配关系。
- MoE 是结构感知专家融合的一种实现，但不是唯一创新点。
- 新增模型/数据格式用于与近年强基线对齐，避免只和 Gohr/DBitNet 的早期设置比较。

不能主张：

- 首次提出多差分或多密文对神经区分器。
- 首次提出结构化特征工程。
- MoE 必然学到密码结构语义路由；需要 gate 消融和强 MLP/强 CNN 基线支撑。

