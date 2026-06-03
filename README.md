# Block Cipher AI Evaluation

面向毕业论文“创新一”的分组密码神经差分区分器实验项目。

当前创新一主线是：

```text
面向分组密码结构与输入组织联合适配的神经差分区分器方法。
```

也就是说，本项目不是只比较一个神经网络，而是在统一 reduced-round
协议下比较：

- 分组密码结构：ARX、SPN、Feistel-like。
- 输入组织：single-pair / multi-pair，`C || C'` / `C || C' || (C xor C')`。
- 神经网络专家：MLP、ResNet、DBitNet、Pairwise DBitNet、SENet、MoE、selector rule。

## 1. 环境安装

项目使用 `uv` 管理 Python 环境：

```bash
uv sync
```

运行测试：

```bash
uv run pytest -q
```

检查 PyTorch 是否能看到 GPU：

```bash
uv run python -c "import torch; print('cuda_available=', torch.cuda.is_available()); print('device_count=', torch.cuda.device_count()); print('device=', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu')"
```

期望输出类似：

```text
cuda_available= True
device_count= 1
device= NVIDIA GeForce RTX 5080
```

训练时默认 `device=auto`，如果 `torch.cuda.is_available()` 为真，训练会使用 CUDA。

实时看显卡：

```bash
nvidia-smi
```

想持续观察可以开另一个终端：

```bash
watch -n 0.5 nvidia-smi
```

如果系统没有 `watch`，可以用：

```bash
while true; do date; nvidia-smi; sleep 1; done
```

## 2. 目录说明

```text
src/blockcipher_ai_eval/
  ciphers/                 分组密码与 reduced-round 实现
    arx/                   ARX 结构，例如 SPECK
    spn/                   SPN 结构，例如 AES、PRESENT
    feistel/               Feistel-like 结构，例如 DES、SIMON、SM4
  datasets.py              差分数据集生成
  models/                  神经区分器模型
  experiments/             cipher/model 工厂与文献差分
  training/                PyTorch 训练与评估

experiments/
  run_innovation_one_matrix.py          主实验入口
  summarize_innovation_one_results.py   JSONL 汇总为 CSV
  build_innovation_one_matrix.py        生成文献排序实验计划
  run_innovation_one_smoke.py           早期 smoke 入口

docs/experiments/          实验记录
docs/research/             文献调研记录
memory/innovation-one.md   创新一长期记忆
outputs/                   实验输出，不提交 git
```

## 3. 主实验入口

最常用入口是：

```bash
uv run python experiments/run_innovation_one_matrix.py --help
```

核心参数：

| 参数 | 说明 |
|---|---|
| `--ciphers` | 密码：`aes128`, `aes192`, `aes256`, `aria128`, `aria192`, `aria256`, `camellia128`, `camellia192`, `camellia256`, `des`, `3des`, `speck32`, `lea128`, `lea192`, `lea256`, `simon64`, `simeck64`, `present80`, `gift64`, `sm4` |
| `--models` | 模型 key 列表 |
| `--rounds` | reduced-round 轮数 |
| `--seeds` | 随机种子 |
| `--samples-per-class` | 每类样本数，正样本和负样本各这么多 |
| `--pairs-per-sample` | 每个训练样本包含几个 ciphertext pair |
| `--feature-encoding` | 输入编码方式 |
| `--difference-profile` | 文献差分 profile |
| `--difference-member` | 多差分 profile 的 member 编号 |
| `--plan` | 使用 CSV 计划文件批量运行 |
| `--output` | JSONL 输出路径 |

输出是 JSONL，每一行是一组实验结果。

## 4. 支持的密码与文献差分

支持的密码：

| key | cipher | structure |
|---|---|---|
| `aes128` | AES-128 | SPN |
| `aes192` | AES-192 | SPN |
| `aes256` | AES-256 | SPN |
| `aria128` | ARIA-128 | SPN |
| `aria192` | ARIA-192 | SPN |
| `aria256` | ARIA-256 | SPN |
| `camellia128` | Camellia-128 | Feistel-like |
| `camellia192` | Camellia-192 | Feistel-like |
| `camellia256` | Camellia-256 | Feistel-like |
| `des` | DES | Feistel-like |
| `3des` | 3DES | Feistel-like |
| `speck32` | SPECK32/64 | ARX |
| `lea128` | LEA-128 | ARX |
| `lea192` | LEA-192 | ARX |
| `lea256` | LEA-256 | ARX |
| `simon64` | SIMON64/128 | Feistel-like |
| `simeck64` | Simeck64/128 | Feistel-like |
| `present80` | PRESENT-80 | SPN |
| `gift64` | GIFT-64 | SPN |
| `sm4` | SM4 reduced-round | Feistel-like |

当前 curated difference profiles：

| profile | cipher | 说明 |
|---|---|---|
| `speck32_gohr2019` | `speck32` | Gohr 2019 SPECK32/64 input difference |
| `present_wang_jain2021` | `present80` | PRESENT 文献差分，支持 `--difference-member 0..3` |
| `sm4_yu2023_conv_resnet` | `sm4` | Yu/Wu/Zhang 2023 SM4 reduced-round 差分 |
| `sm4_li_sun_2025_19r_family` | `sm4` | 记录为 constrained differential family，当前不作为固定 neural input difference |

常用输入编码：

| encoding | 输入 |
|---|---|
| `ciphertext_pair_bits` | `C || C'` |
| `ciphertext_pair_xor_bits` | `C || C' || (C xor C')` |

## 5. 支持的模型 key

基础模型：

```text
mlp
cnn
resnet_bitslice
dbitnet_dilated_cnn
adaptive_dbitnet
senet_resnext
multiscale_dense_resnet
lstm_roundseq
transformer_encoder
```

SPECK Gohr-style 专用模型：

```text
gohr_resnet_speck
gohr_resnet_speck_depth10
```

注意：

```text
gohr_resnet_speck 只适合 SPECK32/64 的 64-bit `C || C'` single-pair 输入。
不要把它直接用于 ciphertext_pair_xor_bits 或 multi-pair 宽输入。
```

Pairwise Adaptive DBitNet：

```text
adaptive_dbitnet_pairwise
adaptive_dbitnet_pairwise_mean
adaptive_dbitnet_pairwise_max
adaptive_dbitnet_pairwise_mean_max
```

说明：

```text
adaptive_dbitnet_pairwise == adaptive_dbitnet_pairwise_mean_max
```

`adaptive_dbitnet_pairwise` 不是 Bellini et al. DBitNet 的原始结构，而是本项目基于 DBitNet-style
自适应扩张卷积和 multi-pair 输入组织设计的 pairwise 变体。

MoE 与 selector：

```text
moe_uniform
moe_hard
moe_soft
moe_v2_uniform
moe_v2_hard
moe_v2_soft
moe_v3_uniform
moe_v3_hard
moe_v3_soft
selector_rule
selector_rule_v2
```

`selector_rule_v2` 规则：

| condition | selected model |
|---|---|
| `pairs_per_sample > 1` | `adaptive_dbitnet_pairwise` |
| ARX single-pair | `resnet_bitslice` |
| SPN single-pair | `senet_resnext` |
| Feistel-like single-pair | `multiscale_dense_resnet` |
| fallback | `mlp` |

## 6. 快速 smoke 测试

先跑一个很小的 SPECK 实验，确认 pipeline 能通：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models mlp adaptive_dbitnet_pairwise_mean_max \
  --rounds 1 \
  --seeds 0 \
  --samples-per-class 32 \
  --epochs 1 \
  --batch-size 16 \
  --hidden-bits 8 \
  --feature-encoding ciphertext_pair_xor_bits \
  --pairs-per-sample 2 \
  --difference-profile speck32_gohr2019 \
  --output outputs/readme_smoke.jsonl
```

汇总：

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/readme_smoke.jsonl \
  --output outputs/readme_smoke_summary.csv
```

查看 JSONL 是否使用 GPU：

```bash
python -c 'import json; rows=[json.loads(l) for l in open("outputs/readme_smoke.jsonl", encoding="utf-8")]; print(len(rows)); print(rows[0]["training"]["device"]); print(rows[0]["training"])'
```

如果走 GPU，应看到：

```text
cuda
```

## 7. 复现实验：selector_rule_v2 单对/多对路由对照

这组实验用于毕业论文创新一主线，验证：

```text
结构适配不仅要看密码结构，也要看输入组织。
```

已有计划文件：

```text
outputs/innovation_one_selector_rule_v2_pair_contrast_plan.csv
```

运行：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --plan outputs/innovation_one_selector_rule_v2_pair_contrast_plan.csv \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 32 \
  --learning-rate 0.001 \
  --output outputs/innovation_one_selector_rule_v2_pair_contrast.jsonl
```

汇总：

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/innovation_one_selector_rule_v2_pair_contrast.jsonl \
  --output outputs/innovation_one_selector_rule_v2_pair_contrast_summary.csv
```

检查输出行数：

```bash
wc -l outputs/innovation_one_selector_rule_v2_pair_contrast_plan.csv \
      outputs/innovation_one_selector_rule_v2_pair_contrast.jsonl \
      outputs/innovation_one_selector_rule_v2_pair_contrast_summary.csv
```

期望：

```text
plan:    91 行，含 header
jsonl:   90 行
summary: 31 行，含 header
```

## 8. 复现实验：pairwise pooling 与 pair 数量消融

这组实验同时服务：

- 毕业论文：输入组织消融。
- 中文核心小论文：共享 pair encoder 与 pooling 方法。

已有计划文件：

```text
outputs/innovation_one_pairwise_pooling_speck_present_plan.csv
```

运行：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --plan outputs/innovation_one_pairwise_pooling_speck_present_plan.csv \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 32 \
  --learning-rate 0.001 \
  --output outputs/innovation_one_pairwise_pooling_speck_present.jsonl
```

汇总：

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/innovation_one_pairwise_pooling_speck_present.jsonl \
  --output outputs/innovation_one_pairwise_pooling_speck_present_summary.csv
```

检查输出行数：

```bash
wc -l outputs/innovation_one_pairwise_pooling_speck_present_plan.csv \
      outputs/innovation_one_pairwise_pooling_speck_present.jsonl \
      outputs/innovation_one_pairwise_pooling_speck_present_summary.csv
```

期望：

```text
plan:    121 行，含 header
jsonl:   120 行
summary: 41 行，含 header
```

快速打印每个 cipher/pairs 的最佳模型：

```bash
python -c 'import csv; rows=list(csv.DictReader(open("outputs/innovation_one_pairwise_pooling_speck_present_summary.csv", encoding="utf-8"))); keys=sorted({(r["cipher"], r["pairs_per_sample"]) for r in rows}); [print(k, max([r for r in rows if (r["cipher"], r["pairs_per_sample"])==k], key=lambda r: float(r["calibrated_accuracy_mean"]))["model"]) for k in keys]'
```

## 9. 自己新跑一组实验

不使用 plan 时，建议一次只跑一个密码，因为不同密码通常需要不同的
`--difference-profile`。跨密码文献差分实验建议用 CSV plan。

SPECK：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models mlp adaptive_dbitnet adaptive_dbitnet_pairwise_mean adaptive_dbitnet_pairwise_mean_max \
  --rounds 6 \
  --seeds 0 1 2 \
  --samples-per-class 8192 \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 32 \
  --feature-encoding ciphertext_pair_xor_bits \
  --pairs-per-sample 4 \
  --difference-profile speck32_gohr2019 \
  --output outputs/custom_speck_pairwise.jsonl
```

PRESENT：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers present80 \
  --models mlp adaptive_dbitnet adaptive_dbitnet_pairwise_mean adaptive_dbitnet_pairwise_mean_max \
  --rounds 5 \
  --seeds 0 1 2 \
  --samples-per-class 8192 \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 32 \
  --feature-encoding ciphertext_pair_xor_bits \
  --pairs-per-sample 4 \
  --difference-profile present_wang_jain2021 \
  --difference-member 0 \
  --output outputs/custom_present_pairwise.jsonl
```

SM4 输入更宽，建议先降低 batch size：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers sm4 \
  --models mlp adaptive_dbitnet adaptive_dbitnet_pairwise_mean adaptive_dbitnet_pairwise_mean_max \
  --rounds 4 \
  --seeds 0 1 2 \
  --samples-per-class 8192 \
  --epochs 5 \
  --batch-size 512 \
  --hidden-bits 32 \
  --feature-encoding ciphertext_pair_xor_bits \
  --pairs-per-sample 4 \
  --difference-profile sm4_yu2023_conv_resnet \
  --output outputs/custom_sm4_pairwise.jsonl
```

## 10. 查看结果

汇总 CSV：

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/custom_speck_pairwise.jsonl \
  --output outputs/custom_speck_pairwise_summary.csv
```

按 calibrated accuracy 排序查看：

```bash
python -c 'import csv; rows=list(csv.DictReader(open("outputs/custom_speck_pairwise_summary.csv", encoding="utf-8"))); rows=sorted(rows, key=lambda r: -float(r["calibrated_accuracy_mean"])); [print(r["cipher"], r["pairs_per_sample"], r["model"], r["calibrated_accuracy_mean"], r["auc_mean"]) for r in rows]'
```

检查每条训练使用的设备：

```bash
python -c 'import json; rows=[json.loads(l) for l in open("outputs/custom_speck_pairwise.jsonl", encoding="utf-8")]; print(sorted({r["training"]["device"] for r in rows}))'
```

期望：

```text
['cuda']
```

## 11. 结果字段说明

JSONL 每行包含：

| 字段 | 说明 |
|---|---|
| `cipher` | 密码名称 |
| `structure` | 结构类型 |
| `model` | 原始模型 key |
| `selected_model` | selector 实际选择的模型 |
| `rounds` | reduced-round 轮数 |
| `input_difference` | 输入差分 |
| `difference_profile` | 文献差分 profile |
| `pairs_per_sample` | 每个样本包含的 pair 数 |
| `feature_encoding` | 输入编码 |
| `metrics` | 最终验证指标 |
| `history` | 每 epoch 训练历史 |
| `training.device` | `cuda` 或 `cpu` |
| `training.input_bits` | 输入 bit 宽度 |
| `training.pair_bits` | pairwise 模型每个 pair 的 bit 宽度 |

常用指标：

| metric | 说明 |
|---|---|
| `accuracy` | 固定阈值 0.5 的准确率 |
| `calibrated_accuracy` | 在验证集上找最佳阈值后的准确率 |
| `auc` | 阈值无关排序指标 |
| `advantage` | `2 * accuracy - 1` |
| `calibrated_advantage` | `2 * calibrated_accuracy - 1` |

论文表格建议同时报告：

```text
calibrated_accuracy mean/std
AUC mean/std
```

## 12. 重要注意事项

1. `outputs/` 是实验产物，通常不提交 git。
2. 跑跨密码文献差分时优先用 plan CSV，因为不同密码需要不同 profile。
3. SPECK Gohr-style single-pair 协议和 multi-pair pairwise 协议不能直接混写成 SOTA 对比。
4. SM4 的输入宽，`pairs_per_sample=8` 可能显存较高，先用 `--batch-size 512`。
5. 如果 `nvidia-smi` 没看到训练，不一定代表没用 GPU；训练结束后显存会释放。以 JSONL 的 `training.device` 字段为准。
