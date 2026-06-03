# 分组密码实现覆盖与正确性检测

日期：2026-06-03

## 原则

分组密码实现必须满足：

```text
每个新增算法至少有一个公开 KAT / 标准测试向量。
没有 KAT 的实现不能声称正确。
```

本项目的 cipher 实现主要服务 reduced-round neural distinguisher 实验，因此接口统一为：

```python
cipher.encrypt(plaintext: int) -> int
```

并暴露：

```text
name
structure
block_bits
key_bits
rounds
```

## 目录架构

当前按结构分类：

```text
src/blockcipher_ai_eval/ciphers/
  base.py
  arx/
    speck.py
  spn/
    aes.py
    present.py
  feistel/
    des.py
    simon.py
    sm4.py
```

根包 `blockcipher_ai_eval.ciphers` 继续导出所有公开类，避免破坏上层代码。

## 当前已实现并测试的密码

| cipher key | class | block/key | structure | correctness test |
|---|---|---|---|---|
| `speck32` | `Speck32_64` | 32/64 | ARX | SPECK32/64 public test vector |
| `simon64` | `Simon64_128` | 64/128 | Feistel-like | NSA SIMON64/128 implementation guide test vector |
| `des` | `Des` | 64/64 | Feistel-like | DES public/FIPS test vector |
| `3des` | `TripleDes` | 64/192 | Feistel-like | degenerate-key consistency with DES |
| `present80` | `Present80` | 64/80 | SPN | PRESENT-80 public test vector |
| `sm4` | `Sm4Reduced` | 128/128 | Feistel-like | SM4 standard public test vector |
| `aes128` | `Aes128` | 128/128 | SPN | NIST FIPS 197 AES-128 KAT |
| `aes192` | `Aes192` | 128/192 | SPN | NIST FIPS 197 AES-192 KAT |
| `aes256` | `Aes256` | 128/256 | SPN | NIST FIPS 197 AES-256 KAT |

## 本轮新增

### AES 与 SIMON

新增文件：

- `src/blockcipher_ai_eval/ciphers/aes.py`

新增类：

```text
Aes128
Aes192
Aes256
```

测试向量：

| variant | key | plaintext | ciphertext |
|---|---|---|---|
| AES-128 | `000102030405060708090a0b0c0d0e0f` | `00112233445566778899aabbccddeeff` | `69c4e0d86a7b0430d8cdb78070b4c55a` |
| AES-192 | `000102030405060708090a0b0c0d0e0f1011121314151617` | `00112233445566778899aabbccddeeff` | `dda97ca4864cdfe06eaf70a0ec0d7191` |
| AES-256 | `000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f` | `00112233445566778899aabbccddeeff` | `8ea2b7ca516745bfeafc49904b496089` |

### SIMON

新增文件：

- `src/blockcipher_ai_eval/ciphers/simon.py`

新增类：

```text
Simon64_128
```

测试向量：

| variant | key | plaintext | ciphertext |
|---|---|---|---|
| SIMON64/128 | `1b1a1918131211100b0a090803020100` | `656b696c20646e75` | `44c8fc20b9dfa07a` |

注意：

- SIMON64/128 使用 z3 序列。
- key words 按 Implementation Guide 的 little-endian word order 生成 round keys。

### DES / 3DES

新增文件：

- `src/blockcipher_ai_eval/ciphers/feistel/des.py`

新增类：

```text
Des
TripleDes
```

测试向量：

| variant | key | plaintext | ciphertext |
|---|---|---|---|
| DES | `133457799bbcdff1` | `0123456789abcdef` | `85e813540f0ab405` |

3DES 当前测试：

- `key1 == key2 == key3` 时，3DES EDE 退化结果必须等于单 DES。
- `decrypt(encrypt(P)) == P`。

后续应补 3DES 多 key NIST KAT。

## 验证命令

运行所有 cipher KAT：

```bash
uv run pytest tests/test_ciphers.py -q
```

当前通过：

```text
18 passed
```

runner smoke：

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers aes128 \
  --models mlp \
  --rounds 1 \
  --seeds 0 \
  --samples-per-class 8 \
  --epochs 1 \
  --batch-size 8 \
  --hidden-bits 8 \
  --feature-encoding ciphertext_pair_xor_bits \
  --pairs-per-sample 1 \
  --output outputs/aes128_smoke.jsonl
```

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers simon64 \
  --models mlp \
  --rounds 1 \
  --seeds 0 \
  --samples-per-class 8 \
  --epochs 1 \
  --batch-size 8 \
  --hidden-bits 8 \
  --feature-encoding ciphertext_pair_xor_bits \
  --pairs-per-sample 1 \
  --output outputs/simon64_smoke.jsonl
```

## 后续主流密码补充计划

建议分批继续：

### 第二批：经典通用分组密码

- Camellia-128/192/256：RFC 3713 KAT。
- ARIA-128/192/256：RFC 5794 KAT。
- LEA：KISA/RFC KAT。

### 第三批：轻量 SPN / Feistel

- GIFT-64/128：官方 reference KAT。
- SKINNY-64/128：官方 paper/reference KAT。
- LED：论文/reference KAT。
- RECTANGLE：论文/reference KAT。

### 第四批：ARX / AND-RX 家族

- CHAM：官方论文/reference KAT。
- Simeck：paper/reference KAT。

原则：

```text
每批只在 KAT 通过后接入 build_cipher 和实验矩阵。
```
