# 主流分组密码 KAT 来源清单

时间：2026-06-03

用途：为“主流分组密码补全”提供集中、可追溯的 Known Answer Test 输入。新增密码实现只有通过这里对应的公开向量，并接入实验工厂后，才能进入完成矩阵。

## 已确认官方 / 标准来源

### ARIA-128/192/256

来源：RFC 5794, Appendix A, Example Data of ARIA

结构归类：SPN / involutional SPN

轮数：

- ARIA-128：12 rounds
- ARIA-192：14 rounds
- ARIA-256：16 rounds

测试向量：

| key | plaintext | ciphertext |
| --- | --- | --- |
| `000102030405060708090a0b0c0d0e0f` | `00112233445566778899aabbccddeeff` | `d718fbd6ab644c739da95f3be6451778` |
| `000102030405060708090a0b0c0d0e0f1011121314151617` | `00112233445566778899aabbccddeeff` | `26449c1805dbe7aa25a468ce263a9e79` |
| `000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f` | `00112233445566778899aabbccddeeff` | `f92bd7c79fb72e2f2b8f80c1972d24fc` |

后续实现文件建议：

- `src/blockcipher_ai_eval/ciphers/spn/aria.py`
- factory keys：`aria128`、`aria192`、`aria256`

### Camellia-128/192/256

来源：RFC 3713, Appendix A, Example Data of Camellia

结构归类：Feistel-like / Feistel-SPN hybrid

轮数：

- Camellia-128：18 Feistel rounds plus FL/FLINV layers
- Camellia-192：24 Feistel rounds plus FL/FLINV layers
- Camellia-256：24 Feistel rounds plus FL/FLINV layers

测试向量：

| key | plaintext | ciphertext |
| --- | --- | --- |
| `0123456789abcdeffedcba9876543210` | `0123456789abcdeffedcba9876543210` | `67673138549669730857065648eabe43` |
| `0123456789abcdeffedcba98765432100011223344556677` | `0123456789abcdeffedcba9876543210` | `b4993401b3e996f84ee5cee7d79b09b9` |
| `0123456789abcdeffedcba987654321000112233445566778899aabbccddeeff` | `0123456789abcdeffedcba9876543210` | `9acc237dff16d76c20ef7c919e3a7509` |

后续实现文件建议：

- `src/blockcipher_ai_eval/ciphers/feistel/camellia.py`
- factory keys：`camellia128`、`camellia192`、`camellia256`

## 已找到论文 / 项目来源，待二次确认

### GIFT-64 / GIFT-128

候选来源：

- GIFT 原论文 / 官方 reference implementation
- secworks/gift 项目说明提到使用 official GIFT test vectors

当前状态：

- `src/blockcipher_ai_eval/ciphers/spn/gift.py` 已实现 GIFT-64/128-key。
- 已使用官方 `giftcipher/gift` repository 的 `GIFT64_test_vector_1..3.txt` 通过 KAT。

### SKINNY

候选来源：

- ePrint 2016/660, The SKINNY Family of Block Ciphers

当前状态：

- 待实现。
- 需要决定论文实验默认采用 `SKINNY-64-128` 还是同时覆盖 `SKINNY-64-64`、`SKINNY-128-128`。
- 如果使用 tweakey 结构，必须在测试和文档中写清楚 TK1/TK2/TK3 的拼接和固定 tweak 策略。

### LED

候选来源：

- ePrint 2012/600, The LED Block Cipher
- 原论文提到更多测试向量在 LED 项目页

当前状态：

- 待实现。
- 需要优先选择 `LED-64` 或 `LED-128`，并以公开 KAT 固定。

### RECTANGLE

候选来源：

- RECTANGLE: A Bit-slice Ultra-Lightweight Block Cipher Suitable for Multiple Platforms

当前状态：

- 待实现。
- 需要确认 `RECTANGLE-80` 和 `RECTANGLE-128` 的公开向量。

### CHAM

候选来源：

- CHAM 原论文 / reference implementation

当前状态：

- 待实现。
- 建议优先 `CHAM-64/128`，因为适合 ARX 结构专家模型实验。

### Simeck

候选来源：

- CHES 2015, The Simeck Family of Lightweight Block Ciphers

当前状态：

- 待实现。
- 论文神经区分器常用 Simeck，因此建议优先 `simeck32` 和/或 `simeck64`。

## 恢复执行器后的 TDD 顺序

1. 将本文件 ARIA 向量加入 `tests/test_mainstream_cipher_required_vectors.py`。
2. 实现 `src/blockcipher_ai_eval/ciphers/spn/aria.py`。
3. 跑 ARIA 单测。
4. 接入 `build_cipher()` 与 `default_difference()`。
5. 跑 factory coverage。
6. 将 Camellia 向量加入 required vectors。
7. 实现 `src/blockcipher_ai_eval/ciphers/feistel/camellia.py`。
8. 跑 Camellia 单测和全量 cipher 回归。
