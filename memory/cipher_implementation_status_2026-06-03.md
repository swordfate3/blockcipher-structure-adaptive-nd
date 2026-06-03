# 分组密码实现补全状态记忆

时间：2026-06-03

目标：补全主流分组密码实现，按结构分类文件夹组织，并为每个新增密码添加公开测试向量或等价正确性检测。

## 已由前序提交完成并测试

- SPN：AES-128/192/256、PRESENT-80、ARIA-128/192/256
- ARX：SPECK32/64
- Feistel-like：DES、3DES、SIMON64/128、SM4

前序验证命令曾通过：

```bash
uv run pytest tests/test_ciphers.py tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_writes_jsonl_rows -q
```

结果：18 passed。

## 本轮新增文件

- `src/blockcipher_ai_eval/ciphers/arx/lea.py`
  - LEA-128/192/256
  - 结构：ARX
  - 状态：已实现、已接入 build_cipher、LEA KAT 与工厂覆盖 pytest 已通过
  - 测试向量来源：公开 LEA 测试记录，包含 128/192/256-bit key 的明文、密文和 round key。

- `tests/test_lea_cipher.py`
  - LEA-128：
    - key: `0f1e2d3c4b5a69788796a5b4c3d2e1f0`
    - plaintext: `101112131415161718191a1b1c1d1e1f`
    - ciphertext: `9fc84e3528c6c6185532c7a704648bfd`
  - LEA-192：
    - key: `0f1e2d3c4b5a69788796a5b4c3d2e1f0f0e1d2c3b4a59687`
    - plaintext: `202122232425262728292a2b2c2d2e2f`
    - ciphertext: `6fb95e325aad1b878cdcf5357674c6f2`
  - LEA-256：
    - key: `0f1e2d3c4b5a69788796a5b4c3d2e1f0f0e1d2c3b4a5968778695a4b3c2d1e0f`
    - plaintext: `303132333435363738393a3b3c3d3e3f`
    - ciphertext: `d651aff647b189c13a8900ca27f9e197`

- `src/blockcipher_ai_eval/ciphers/spn/gift.py`
  - GIFT-64/128-key
  - 结构：SPN / bit permutation lightweight
  - 状态：实现草案，未接入、未 KAT 验证。必须先找到官方或可信 KAT 并跑通后才能纳入完成清单。

## 当前阻塞

普通沙箱执行器无法启动 shell；已通过提权执行恢复验证路径：

```text
Failed to create unified exec process: No such file or directory
```

LEA 批次已经完成读取、接入和 pytest 验证；普通沙箱仍异常，后续命令需继续使用提权执行。

## 后续第一优先级

1. 跑完整测试回归并提交 LEA 稳定批次。
2. 推进 Camellia、GIFT、SKINNY、LED、RECTANGLE、CHAM、Simeck。
