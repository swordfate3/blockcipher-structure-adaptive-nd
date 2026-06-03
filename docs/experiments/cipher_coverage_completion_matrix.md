# 分组密码实现覆盖矩阵

本文档用于约束“主流分组密码补全”的完成口径。只有同时满足以下条件的算法，才能标记为完成：

1. 位于结构化目录：`arx/`、`spn/`、`feistel/` 或后续明确新增的结构目录。
2. 实现提供统一接口：`rounds`、`key`、`name`、`structure`、`block_bits`、`key_bits`、`encrypt(int) -> int`。
3. 至少一组公开测试向量或等价正确性检测通过。
4. 已接入 `build_cipher()`，创新一实验 CLI 可以按 cipher key 运行。
5. 已在 README 或实验文档中列出。

## 当前覆盖

| 结构 | 算法 | key | 状态 | 正确性证据 |
| --- | --- | --- | --- | --- |
| SPN | AES-128 | `aes128` | 已完成 | FIPS 197 KAT |
| SPN | AES-192 | `aes192` | 已完成 | FIPS 197 KAT |
| SPN | AES-256 | `aes256` | 已完成 | FIPS 197 KAT |
| SPN | PRESENT-80 | `present80` | 已完成 | 公开 KAT |
| SPN | ARIA-128 | `aria128` | 已完成 | RFC 5794 KAT，pytest 已通过 |
| SPN | ARIA-192 | `aria192` | 已完成 | RFC 5794 KAT，pytest 已通过 |
| SPN | ARIA-256 | `aria256` | 已完成 | RFC 5794 KAT，pytest 已通过 |
| SPN | GIFT-64 | `gift64` | 实现草案 | 待 KAT、本地测试 |
| ARX | SPECK32/64 | `speck32` | 已完成 | NSA guide KAT |
| ARX | LEA-128 | `lea128` | 已完成 | 公开 LEA KAT，pytest 已通过 |
| ARX | LEA-192 | `lea192` | 已完成 | 公开 LEA KAT，pytest 已通过 |
| ARX | LEA-256 | `lea256` | 已完成 | 公开 LEA KAT，pytest 已通过 |
| Feistel-like | DES | `des` | 已完成 | DES KAT |
| Feistel-like | 3DES | `3des` | 已完成 | DES 退化一致性与 roundtrip |
| Feistel-like | SIMON64/128 | `simon64` | 已完成 | NSA guide KAT |
| Feistel-like | SM4 | `sm4` | 已完成 | GB/T 32907 public KAT |

## 待补主流/论文常用算法

| 结构 | 算法 | 计划 key | 备注 |
| --- | --- | --- | --- |
| Feistel-like hybrid | Camellia-128/192/256 | `camellia128`/`camellia192`/`camellia256` | 使用 RFC 3713 KAT |
| SPN | SKINNY-64/128 | `skinny64`/`skinny128` | 需明确 tweak 固定策略 |
| SPN | LED | `led64` 或 `led128` | 需公开 KAT |
| SPN | RECTANGLE | `rectangle80` 或 `rectangle128` | 需公开 KAT |
| ARX | CHAM | `cham64`/`cham128` | 需官方 KAT |
| Feistel-like / AND-RX | Simeck | `simeck32`/`simeck64` | 需公开 KAT |

## 当前回归命令

```bash
uv run pytest tests/test_mainstream_cipher_required_vectors.py tests/test_cipher_factory_coverage.py -q
uv run pytest tests/test_ciphers.py tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_writes_jsonl_rows -q
```

ARIA/Camellia 的 RFC 向量测试目前使用 `pytest.importorskip` 作为 future gate；实现对应模块后应自动进入 KAT 验证。
