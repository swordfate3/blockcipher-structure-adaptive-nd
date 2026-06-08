# 2026-06-08 SPECK32/64 ARX 对齐筛查计划

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

- 配置：`experiments/configs/innovation1/arx_speck32_aligned_screen.json`
- 计划：`experiments/plans/innovation1_arx_speck32_aligned_screen.csv`
- 远程配置：`experiments/configs/remote/innovation1_arx_speck32_aligned_screen_gpu1.json`
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

## 论文意义

这条线是创新一的第二个结构家族证据：SPN 已有 PRESENT/GIFT 的 inverse-permutation aligned 结果，ARX 现在进入 SPECK 的 rotation aligned 对照。若远程结果出现稳定提升，可作为“结构公开算子对齐输入特征 + 结构自适应模型”的跨结构证据。
