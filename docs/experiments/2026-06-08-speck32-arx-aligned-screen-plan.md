# 2026-06-08 SPECK32/64 ARX 对齐筛查计划与结果

## 目的

创新一需要证明结构适配不是只对 SPN 有效。本计划把 ARX/SPECK 分支接入同一套 raw vs aligned 对照协议，测试公开轮函数结构中的 word rotation 对齐差分是否能给神经区分器提供更稳定的输入归纳偏置。

## 新增特征

新增 `ciphertext_pair_xor_arx_aligned_bits`。对 SPECK32/64，每个样本内单个密文对编码为：

```text
C || C_prime || Delta_C || Align_ARX(Delta_C)
```

其中 `Delta_C = C xor C_prime`，按 SPECK32 的两个 16-bit word 拆分：

```text
Delta_C = Delta_L || Delta_R
Align_ARX(Delta_C) = ROR7(Delta_L) || ROL2(Delta_R)
```

因此单对宽度从 raw `3 * 32 = 96` bits 增加为 aligned `4 * 32 = 128` bits。多对输入继续由 dataset 按 `pairs_per_sample` 串接。

## 远程筛查协议

- 配置：`experiments/innovation1/configs/arx_speck32_aligned_screen.json`
- 计划：`experiments/innovation1/plans/innovation1_arx_speck32_aligned_screen.csv`
- 远程配置：`experiments/innovation1/configs/remote/innovation1_arx_speck32_aligned_screen_gpu1.json`
- run id：`innovation1-arx-speck32-aligned-screen-gpu1-20260608`
- 行数：16
- cipher：SPECK32/64
- rounds：6, 7
- seeds：0,1,2,3
- feature：`ciphertext_pair_xor_bits` vs `ciphertext_pair_xor_arx_aligned_bits`
- pairs_per_sample：4
- samples_per_class：32768
- negative_mode：`encrypted_random_plaintexts`
- difference_profile：`speck32_gohr2019`
- train_key：`0x1918111009080100`
- validation_key：`0x0f0e0d0c0b0a0908`
- model：`structure_adaptive_pairset_dbitnet`

## 本地验证

已完成：

```text
uv run pytest tests/test_feature_encodings.py tests/test_build_plan_config.py tests/test_experiment_matrix_runner.py tests/test_remote_script_generator.py -q
36 passed

uv run pytest -q
231 passed
```

本地 tiny smoke 用 2 行临时计划跑通，维度符合预期：

```text
ciphertext_pair_xor_bits              input_bits=192 pair_bits=96
ciphertext_pair_xor_arx_aligned_bits  input_bits=256 pair_bits=128
```

## 远程结果

结果已由 monitor 拉回本地：

```text
outputs/remote_results/innovation1-arx-speck32-aligned-screen-gpu1-20260608/
```

Gate 通过：

```text
result_lines=16
expected_rows=16
stderr bytes=0
```

分组结果：

| rounds | feature | seeds | accuracy_mean | calibrated_accuracy_mean | auc_mean | loss_mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 6 | raw `ciphertext_pair_xor_bits` | 4 | 0.874374 | 0.875275 | 0.941063 | 0.329188 |
| 6 | ARX aligned `ciphertext_pair_xor_arx_aligned_bits` | 4 | 0.880196 | 0.883820 | 0.947691 | 0.331033 |
| 7 | raw `ciphertext_pair_xor_bits` | 4 | 0.509819 | 0.513657 | 0.515719 | 0.786432 |
| 7 | ARX aligned `ciphertext_pair_xor_arx_aligned_bits` | 4 | 0.509636 | 0.513039 | 0.515586 | 0.751059 |

Paired delta：

| rounds | calibrated_accuracy_delta | auc_delta | positive_seeds |
| --- | ---: | ---: | ---: |
| 6 | +0.008545 | +0.006628 | 4/4 |
| 7 | -0.000618 | -0.000133 | 3/4 |

## 初步结论

ARX aligned 在 SPECK32/64 6 轮上有稳定小幅提升，4 个 seed 全部为正；7 轮接近随机水平，ARX aligned 没有有效提升。这说明 ARX 结构对齐输入有苗头，但目前只构成“低/中轮有效”的初步证据，还不能说已经提升 SPECK 最高轮次。

## 论文意义

这条线是创新一的第二个结构家族证据：SPN 已有 PRESENT/GIFT 的 inverse-permutation aligned 结果，ARX 现在进入 SPECK 的 rotation aligned 对照。当前结果支持“结构公开算子对齐输入特征 + 结构自适应模型”在 ARX 上有一定效果，但下一步需要继续优化 ARX 专家或差分表示，重点看 7 轮能否从随机附近拉开。
