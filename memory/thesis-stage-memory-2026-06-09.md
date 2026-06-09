# Thesis Stage Memory Snapshot (2026-06-09)

本文件是阶段性存档，用于在毕业论文全部创新点完成前保存当前上下文。它不是最终论文整理稿；等创新一、创新二、创新三都做完后，再统一归并为论文叙事、实验总表、小论文材料和答辩材料。

## 当前主线

毕业论文主题暂定为面向分组密码结构的神经差分区分方法。创新一当前没有偏移，核心仍是：让神经区分器的输入表征和网络结构适配分组密码内部结构，而不是只堆模型容量或训练数据量。

当前表述边界：

- SPN 分支已经形成较强证据。
- ARX 分支正在筛查更合适的公开结构特征和模型结构。
- 不能直接宣称已经超越所有前沿最高轮。
- 多密文对准确率不能直接等同于单密文对前沿结果，论文中必须说明协议差异。
- 所有结构特征必须只来自公开密文、公开差分和公开轮函数关系，不能使用密钥或真实中间状态。

## 项目位置和远程流程

主仓库：

```text
/home/fate/gitproject/blockcipher-structure-adaptive-nd
```

GitHub：

```text
https://github.com/swordfate3/blockcipher-structure-adaptive-nd
```

远程 Windows GPU 项目根目录：

```text
G:/lxy/blockcipher-structure-adaptive-nd
```

远程 Python：

```text
F:/Anaconda/envs/DWT/torch310/python.exe
```

远程实验流程已经固定为：本地实现与测试 -> commit/push main -> 生成 `scripts/remote/*.cmd` -> 远程 Task Scheduler 拉取代码并运行 -> 远程推送 `results/<run_id>` 分支 -> 本地 monitor 拉回 `outputs/remote_results/<run_id>/`。

监控 GitHub 偶尔会出现 TLS 错误，这不一定表示远程实验失败，需要同时检查远程任务状态、结果分支和本地结果目录。

## 创新一：SPN 分支

SPN 当前最清晰的方法是公开逆置换差分对齐输入：

```text
raw:     C || C' || Delta_C
aligned: C || C' || Delta_C || P^-1(Delta_C)
```

这里的 `P^-1` 是公开逆置换层。PRESENT 使用 `Present80.inverse_permutation_layer`，GIFT-64 使用 `Gift64.inverse_permutation_layer`。该特征不使用密钥，也不使用真实中间状态，只是把输出差分按公开扩散层逆向对齐到更接近 S-box/nibble 局部结构的位置。

主模型：

```text
spn_token_mixer_pairset
```

实现位置：

```text
src/blockcipher_ai_eval/models/structure/spn/_pairset_impl.py
```

模型要点：4-bit nibble token、位置嵌入、MLP-Mixer 风格 token/channel mixing、pair embedding、多密文对 attention/mean/max 聚合、MLP 分类器。

当前主要协议：cross-key validation、`encrypted_random_plaintexts` 负样本、`pairs_per_sample=4`、主要确认实验使用 10 seeds。

## SPN 关键结果

GIFT-64 10-seed confirmation 是当前创新一最强结果之一：

```text
run_id: innovation1-spn-gift64-aligned-confirm-10seed-gpu0-20260608
result_dir: outputs/remote_results/innovation1-spn-gift64-aligned-confirm-10seed-gpu0-20260608/
```

GIFT-64 round 5：

```text
raw calibrated accuracy:     0.750476
aligned calibrated accuracy: 0.867969
delta:                       +0.117493
raw AUC:                     0.828513
aligned AUC:                 0.941747
delta AUC:                   +0.113235
positive seeds:              10/10
```

GIFT-64 round 6：

```text
raw calibrated accuracy:     0.503983
aligned calibrated accuracy: 0.518094
delta:                       +0.014111
raw AUC:                     0.501735
aligned AUC:                 0.522215
delta AUC:                   +0.020479
positive seeds:              9/10
```

结论口径：round 5 是强证据，可以进入论文主表；round 6 是弱边界信号，不能包装成强高轮突破。该结果说明 PRESENT 上的 SPN 对齐收益可迁移到 GIFT-64，不是单密码偶然现象。

对应详细记忆：

```text
memory/innovation-one-gift64-spn-aligned-results-2026-06-08.md
```

## 创新一：ARX 分支

ARX 不能直接套 SPN 的 `P^-1(Delta_C)`，因为 SPECK 是 ARX 结构，没有 SPN 的 bit permutation + S-box 局部结构。ARX 应围绕 word、rotation、modular addition、carry proxy、keyless partial inverse 做结构适配。

ARX v1 已完成：

```text
ciphertext_pair_xor_arx_aligned_bits
C || C' || Delta_C || (ROR7(Delta_L) || ROL2(Delta_R))
```

v1 SPECK32/64 结果：

```text
run_id: innovation1-arx-speck32-aligned-screen-gpu1-20260608
round 6 raw cal_acc:         0.875275
round 6 arx aligned cal_acc: 0.883820
delta:                       +0.008545
positive seeds:              4/4
round 7 raw cal_acc:         0.513657
round 7 arx aligned cal_acc: 0.513039
delta:                       -0.000618
```

v1 结论：6 轮有小幅稳定收益，7 轮没有改善，不能宣称 SPECK 高轮突破。

ARX v2/v3 已实现并启动远程筛查：

```text
ciphertext_pair_xor_arx_partial_inverse_bits
ciphertext_pair_xor_arx_partial_inverse_rx_bits
```

v2 keyless partial inverse：

```text
pre_y       = ROR2(y xor x)
pre_y_prime = ROR2(y_prime xor x_prime)
Delta_pre_y = pre_y xor pre_y_prime
```

基于公开关系：

```text
y_out = ROL2(y_in) xor x_out
```

v3 在 v2 基础上加入 RX/carry-inspired public proxies。

当前远程筛查：

```text
run_id: innovation1-arx-speck32-v2-feature-screen-gpu1-20260609
expected_rows: 32
cipher: SPECK32/64
model: structure_adaptive_pairset_dbitnet
rounds: 6, 7
seeds: 0..3
features: raw, arx_aligned_v1, partial_inverse_v2, partial_inverse_rx_v3
samples_per_class: 32768
pairs_per_sample: 4
epochs: 8
device: cuda:1
```

本地监控：

```text
scripts/monitor_innovation1_arx_speck32_v2_feature_screen_results.sh
tmux session: innovation1_arx_speck32_v2_monitor
monitor log: outputs/remote_results/monitor_logs/innovation1_arx_speck32_v2_monitor.log
```

待判断：如果 v2/v3 在 7 轮明显优于 raw/v1，则固定最优 feature 做 10-seed confirmation；如果仍没有明显改善，则 ARX 下一步应转向结构模型，例如 `ArxWordMixerPairSet`。

## 多密文对协议边界

当前多密文对是一个样本包含多个满足同一差分/标签构造方式的密文对，网络聚合这些 pair 后输出一个区分结果。`pairs_per_sample=1` 是单对协议，`pairs_per_sample=4` 是多对聚合协议。

论文中需要明确：多对结果可以作为神经区分证据，但与 Gohr 等单对或 score aggregation 协议比较时要说明协议差异。创新一最稳妥主张是同协议 baseline 下结构对齐和结构适配模型带来显著提升，而不是直接宣称绝对最高轮超越所有前人。

## 小论文和毕业论文安排

小论文更适合先围绕 SPN 单独成文，题目可暂定：

```text
基于公开逆置换差分对齐的轻量级SPN分组密码神经区分方法
```

小论文贡献：公开逆置换差分对齐输入、SPN-TokenMixer-PairSet、严格 cross-key/encrypted-negative/10-seed 协议、PRESENT 到 GIFT-64 的迁移证据。

毕业论文创新一应更完整地覆盖结构适配框架：SPN 已较成熟，ARX 正在推进，Feistel/其他结构可作为后续补充或展望。

## 下一步优先级

1. 拉回并解析 `innovation1-arx-speck32-v2-feature-screen-gpu1-20260609`。
2. 根据 ARX v2/v3 结果决定做 10-seed confirmation，或实现 `ArxWordMixerPairSet`。
3. SPN 侧补充 paper-grade 控制实验：same-dimension control、`P^-1(Delta_C)` ablation、`pairs_per_sample=1 vs 4`、PRESENT/GIFT-64 mean +/- std 表。
4. ARX 侧坚持 word/rotation/addition/carry 结构适配，不能机械照搬 SPN。
5. 等创新一闭环后，再推进创新二/创新三。
6. 等毕业论文所有创新点完成后，再统一整理 memory、docs、论文大纲、小论文材料。

## 快速恢复命令

```bash
cd /home/fate/gitproject/blockcipher-structure-adaptive-nd
git status --short --branch
tail -120 outputs/remote_results/monitor_logs/innovation1_arx_speck32_v2_monitor.log
find outputs/remote_results -maxdepth 1 -type d | rg 'innovation1-arx-speck32-v2-feature-screen'
uv run python scripts/monitor_remote_results.py --once --run-id innovation1-arx-speck32-v2-feature-screen-gpu1-20260609=32
```

当前完成度判断：SPN 分支约 70%-80%，ARX 分支约 30%-45%，Feistel/其他结构尚未闭环，创新一整体约 50%-60%。方向没有偏移，仍围绕“密码结构适配神经区分”。
