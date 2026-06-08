# Project Memory

本目录用于保存项目长期上下文记忆，区别于 `docs/experiments/` 的实验记录和 `docs/research/` 的文献整理。

记忆文件用于帮助后续继续推进时快速恢复上下文，包括：

- 当前论文创新点判断。
- 已实现模型和实验管线状态。
- 关键实验结论。
- 已发现的问题和下一步优先级。
- GPU 实验运行注意事项。

## 文件索引

- `remote-gpu-runs-2026-06-03.md`：远端 Windows A6000 GPU sanity run、项目重命名上下文和下一步远端实验建议。
- `innovation-one.md`：创新一长期定位、已实现模型、文献边界、实验路线和毕业论文/小论文双轨安排。
- `innovation-one-spn-aligned-results-2026-06-07.md`：PRESENT/SPN 结构对齐输入 + SPN-TokenMixer 的正式远程实验结果、创新边界、密钥泄露/攻击协议判断和后续 cross-key 消融优先级。
- `innovation-one-spn-protocol-stress-results-2026-06-08.md`：PRESENT/SPN 结构对齐在 cross-key、encrypted_random_plaintexts 负样本和输入消融下的压力测试结果，以及下一步 10 seeds 严格协议计划。
- `innovation-one-gift64-spn-aligned-results-2026-06-08.md`：GIFT-64 raw vs SPN aligned 迁移筛查结果，证明 PRESENT 的 SPN 结构对齐收益可迁移到另一个轻量 SPN 密码。
- `cipher_implementation_status_2026-06-03.md`：分组密码算法实现与测试覆盖状态。
- `conversation-archive-2026-06-05.md`：截至 2026-06-05 的连续对话归档，重点记录创新一模型路线、远程实验结论、SPN v2 负向结果和下一步 MoE v5 / SPN nibble expert 方向。
- `innovation-one-speck32-arx-aligned-plan-2026-06-08.md`：SPECK32/64 ARX 结构对齐特征、筛查计划和本地验证。
