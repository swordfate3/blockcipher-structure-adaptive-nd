# 项目结构说明

当前代码按“创新一最小实验闭环”组织，先保证密码原语、差分数据集、结构-网络匹配规则能独立验证，再逐步接入训练器和可视化平台。

## 目录分层

```text
src/blockcipher_ai_eval/
├── ciphers/
│   ├── __init__.py      # 对外导出密码类，保持稳定导入路径
│   ├── base.py          # ReducedRoundCipher 协议与公共位运算
│   ├── speck.py         # SPECK32/64 reduced/full-round 实现
│   ├── present.py       # PRESENT-80 reduced/full-round 实现
│   └── sm4.py           # SM4 reduced/full-round 实现
├── models/
│   ├── __init__.py      # 对外导出神经网络模型
│   └── mlp.py           # MLP baseline 神经区分器
├── training/
│   ├── __init__.py      # 对外导出训练 API
│   └── binary.py        # 二分类训练循环、Accuracy/AUC/Advantage 指标
├── datasets.py          # 神经区分器差分数据集生成与 bit 编码
└── innovation_one.py    # 结构特征、网络特征、匹配评分与实验矩阵
```

## 设计约束

1. 每个分组密码算法必须独立成文件，不能把多个算法堆在一个 `ciphers.py` 中。
2. `ciphers/base.py` 只放公共协议和通用位运算，不放具体算法常量。
3. 新增密码时优先创建 `src/blockcipher_ai_eval/ciphers/<cipher_name>.py`，并在 `ciphers/__init__.py` 导出。
4. 每个密码必须有公开测试向量或自说明的 reduced-round 测试，放在 `tests/test_ciphers.py` 或独立测试文件中。
5. 数据集生成只依赖 `ReducedRoundCipher` 协议，不能绑定具体算法类。
6. 神经网络模型放在 `models/`，训练逻辑放在 `training/`，实验脚本放在仓库根目录的 `experiments/`。

## 下一步建议结构

后续接入训练时建议继续拆分：

```text
src/blockcipher_ai_eval/
├── experiments/         # 实验配置解析和批量运行
└── reporting/           # 表格、曲线、论文报告生成
```

这样创新一的“密码结构 - 网络架构 - 实验协议”三层会比较清楚，不会在一个脚本里混成一团。
