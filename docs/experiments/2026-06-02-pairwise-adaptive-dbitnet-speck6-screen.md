# Pairwise Adaptive DBitNet SPECK6 筛查

日期：2026-06-02

## 目的

上一轮 MoE v2 消融显示：把旧 `dbitnet_dilated_cnn` 替换为 `adaptive_dbitnet`
能改善 hard gate，但直接把 `pairs_per_sample=4` 的 384-bit 宽输入作为一条长 bit
序列训练，仍明显低于 MLP。

因此新增 `adaptive_dbitnet_pairwise`：

- 将输入按 `pair_bits=96` 拆成多个 ciphertext-pair 子输入。
- 每个 pair 共享同一个 adaptive DBitNet encoder。
- 对 pair-level embeddings 做 mean pooling 和 max pooling。
- 拼接 pooled embedding 后分类。

这更贴近多密文对神经区分器中的“每对先提特征，再跨 pair 融合”思路。

## 新增模型

模型 key：

```text
adaptive_dbitnet_pairwise
```

当前默认用于：

```text
feature_encoding = ciphertext_pair_xor_bits
pair_bits = 96
```

在 SPECK32/64 上，`pairs_per_sample=4` 时输入宽度为：

```text
4 * 96 = 384 bits
```

## 实验命令

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models mlp adaptive_dbitnet adaptive_dbitnet_pairwise \
  --rounds 6 \
  --seeds 0 1 2 \
  --samples-per-class 8192 \
  --pairs-per-sample 4 \
  --epochs 5 \
  --batch-size 1024 \
  --hidden-bits 64 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_pairwise_dbitnet_speck6_screen.jsonl
```

## 结果

| model | calibrated accuracy mean | AUC mean |
|---|---:|---:|
| `adaptive_dbitnet_pairwise` | 0.7861 | 0.8625 |
| `mlp` | 0.6286 | 0.6695 |
| `adaptive_dbitnet` | 0.6001 | 0.6355 |

## 结论

- `adaptive_dbitnet_pairwise` 显著超过直接宽输入 `adaptive_dbitnet`：
  `0.6001 -> 0.7861`。
- 它也显著超过同预算 MLP：`0.6286 -> 0.7861`。
- 这说明多密文对场景下，先按 pair 共享编码、再跨 pair 融合，比直接把 384-bit
  输入当作长序列更适合 SPECK6。
- 该结果接近 Gohr 2019 SPECK6 单 pair 文献准确率约 `0.788`，但协议不同：
  本实验使用 `pairs_per_sample=4` 和 `ciphertext_pair_xor_bits`，不能写成单 pair
  Gohr 复现或直接超越 Gohr。

## 对创新一的意义

这是目前创新一最强的结构优化证据之一：

> 针对多密文对输入，结构感知的 pairwise DBitNet 专家显著优于把所有 bit 直接串接
> 的通用 DBitNet，也优于 MLP baseline，说明密码输入组织方式与网络结构之间存在
> 明确适配关系。

后续应将该模型接入 MoE v3 专家池，替换 MoE v2 中的 `adaptive_dbitnet` 专家。
