# 记忆：创新一 SPECK32/64 ARX 对齐计划与结果（2026-06-08/09）

本轮不等待 GIFT-64 十种子确认，推进创新一 ARX/SPECK 分支，并已取得第一轮远程筛查结果。

已完成：

- 新增 ARX 对齐特征 `ciphertext_pair_xor_arx_aligned_bits`。
- SPECK32/64 对齐规则：`C || C_prime || Delta_C || (ROR7(Delta_L) || ROL2(Delta_R))`。
- 单对宽度：raw `96` bits，ARX aligned `128` bits；多对输入按 `pairs_per_sample` 串接。
- 新增并通过测试：`tests/test_feature_encodings.py`、`tests/test_build_plan_config.py`、`tests/test_experiment_matrix_runner.py`。
- 新增 SPECK32 ARX screen：16 行，rounds 6/7，seeds 0..3，raw vs arx_aligned，pairs_per_sample=4，samples_per_class=32768。
- 新增远程脚本，run id：`innovation1-arx-speck32-aligned-screen-gpu1-20260608`。

验证：

- 相关测试：36 passed。
- 全量测试：231 passed。
- 本地 tiny smoke：2 行真实训练跑通，raw input_bits=192/pair_bits=96，arx_aligned input_bits=256/pair_bits=128。

远程结果已拉回：

- 本地目录：`outputs/remote_results/innovation1-arx-speck32-aligned-screen-gpu1-20260608/`
- Gate：16/16 行，stderr 为空。
- 提交：`201fb8b73c15a1dd8564c3770fd88922c5aa73a3`
- 远程环境：torch 2.5.1+cu118，cuda available，2 x RTX A6000。

核心结果：

- SPECK32/64 6 轮：ARX aligned calibrated accuracy 0.883820，raw 0.875275，delta +0.008545；AUC delta +0.006628；4/4 seeds 为正。
- SPECK32/64 7 轮：ARX aligned calibrated accuracy 0.513039，raw 0.513657，delta -0.000618；AUC delta -0.000133；整体接近随机。

结论：ARX 结构对齐输入在 6 轮有稳定小幅提升，但 7 轮没有拉开。它证明 ARX 分支不是完全无效，但当前还不能作为“超越 SPECK 高轮前沿”的结果。下一步应围绕 ARX 专家/差分表示优化，而不是直接宣称 SPECK 7 轮突破。
