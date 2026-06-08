# 记忆：创新一 SPECK32/64 ARX 对齐计划（2026-06-08）

本轮不等待 GIFT-64 十种子确认，推进创新一 ARX/SPECK 分支。

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

下一步：提交并推送后，在远程 Windows GPU 工作站拉取 main，执行 `scripts/remote/schedule_innovation1_arx_speck32_aligned_screen_gpu1_20260608.cmd`，本地可用 `scripts/monitor_innovation1_arx_speck32_aligned_screen_results.sh` 监控并拉回结果分支。
