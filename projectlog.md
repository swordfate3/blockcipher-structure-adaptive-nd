2026-06-02 17:58:12
docs/experiments/2026-06-02-adaptive-dbitnet-implementation.md：记录 Adaptive DBitNet 的文献来源、实现细节、smoke 命令和后续筛查方案（用于归档本轮从“MLP 为何占优”转向“自适应输入维度 DBitNet”后的实验路线）。

2026-06-02 17:58:12
src/blockcipher_ai_eval/models/adaptive_dbitnet.py：新增 `adaptive_dbitnet` 模型，按输入 bit 宽度自动生成 DBitNet-style dilation rates，并使用 `256 -> 256 -> 64 -> 1` 强预测头（用于替代旧 `dbitnet_dilated_cnn` 的固定 dilation 轻量近似，支持多输入宽度实验）。

2026-06-02 17:58:12
src/blockcipher_ai_eval/experiments/factories.py：注册 `adaptive_dbitnet` 模型 key（允许后续通过 `experiments/run_innovation_one_matrix.py --models adaptive_dbitnet` 直接运行筛查实验）。

2026-06-02 17:58:12
tests/test_adaptive_dbitnet_model.py：新增 Adaptive DBitNet 单元测试，覆盖 `64/96/128/384` 输入宽度的自适应 dilation、强 prediction head 形状和 factory key（防止后续改模型时破坏输入宽度自适应逻辑）。

2026-06-02 17:58:12
docs/experiments/2026-06-02-innovation-one-speck6-main-v1.md：记录 SPECK6 中等规模主表与容量消融结论：当前 MLP 只是项目内部强基线，`calibrated_accuracy` 约 0.6767，尚未达到 Gohr/DBitNet 文献中 SPECK6 约 0.78 的水平；multi-pair 输入需要与模型容量匹配。

2026-06-02 17:58:12
实验路线记忆：下一步先跑可控筛查，不直接大规模占满显存；建议配置为 SPECK6、`models=mlp adaptive_dbitnet dbitnet_dilated_cnn resnet_bitslice`，分别比较 `ciphertext_pair_bits/pairs=1` 与 `ciphertext_pair_xor_bits/pairs=4`，`samples_per_class=8192`、`epochs=5`、`seeds=0 1 2`、`hidden_bits=32`。

2026-06-02 17:58:12
运行注意事项：每次启动 GPU 长实验前后使用 `nvidia-smi` 检查显存和进程；若出现残留 `run_innovation_one_matrix.py` 进程，应先停止再继续，避免再次发生 hidden=128 MoE 容量消融占满显存的问题。
