# Remote GPU Runs - 2026-06-03

## Project Rename Context

- Old local directory: `/home/fate/gitproject/thesis_liaoxiyue`
- New local directory: `/home/fate/gitproject/blockcipher-structure-adaptive-nd`
- Rename mode: scheme A, outer project directory only.
- Python package remains: `blockcipher_ai_eval`.

## Remote Windows GPU Skill

Used skill: `remote-windows-gpu-conda-ssh`.

Remote target:

```text
host: 10.115.39.172
ssh user: 1304Lijinlin
remote machine: DESKTOP-BBLPACJ
remote workspace: G:\lxy\innovation1-moe-v4-sanity
python: F:\Anaconda\envs\DWT\torch310\python.exe
```

Credential handling note: SSH password was used only interactively during the run and must not be saved in memory, logs, reports, or code.

## GPU / Torch Gate

Clean local gate file:

- `outputs/remote_results/innovation1-moe-v4-sanity/logs/torch_info.txt`

Verified values:

```text
torch 2.5.1+cu118
cuda_version 11.8
cuda_available True
device_count 2
device0 NVIDIA RTX A6000
```

`gpu_info.txt` also records 2 x NVIDIA RTX A6000 with driver 528.49 and driver CUDA capability 12.0.

## Sanity Run

Purpose: prove remote upload/run/retrieve flow and verify `moe_v4_hard` runs on CUDA. This is not a thesis-quality performance result.

Settings:

```text
ciphers: speck32 present80 sm4
models: mlp adaptive_dbitnet_pairwise moe_v3_hard moe_v4_hard selector_rule_v2
rounds: 2
seeds: 0
samples_per_class: 512
epochs: 2
batch_size: 128
hidden_bits: 32
feature_encoding: ciphertext_pair_xor_bits
pairs_per_sample: 2
```

Local result files after retrieval:

- `outputs/remote_results/innovation1-moe-v4-sanity/results/innovation_one_moe_v4_sanity.jsonl`
- `outputs/remote_results/innovation1-moe-v4-sanity/summary.csv`
- `outputs/remote_results/innovation1-moe-v4-sanity/result_summary.md`
- `outputs/remote_results/innovation1-moe-v4-sanity/artifacts_manifest.json`
- `outputs/remote_results/innovation1-moe-v4-sanity/logs/train_stdout.txt`
- `outputs/remote_results/innovation1-moe-v4-sanity/logs/train_stderr.txt`
- `outputs/remote_results/innovation1-moe-v4-sanity/logs/gpu_info.txt`
- `outputs/remote_results/innovation1-moe-v4-sanity/logs/torch_info.txt`

Gate:

```text
SSH: PASS
Env: PASS
GPU: PASS
PyTorch CUDA: PASS
Upload: PASS
Experiment command: PASS
Result retrieval: PASS
Artifact gate: PASS
train_stderr.txt: 0 bytes
result rows: 15
training device: cuda
```

Key observation:

- Adapter routing was recorded correctly: SPECK -> `arx_word_mix`, PRESENT -> `spn_cell_mix`, SM4 -> `feistel_branch_mix`.
- On this easy r=2 sanity setting, PRESENT/SM4 are saturated and SPECK shows `moe_v4_hard` below `adaptive_dbitnet_pairwise`/`selector_rule_v2`; this is a signal for later adapter ablation, not a final conclusion.

## Next Remote Run Recommendation

Run a harder MoE v4 main matrix on the remote A6000 machine:

```text
ciphers: speck32 lea128 cham64 simon64 simeck64 present80 gift64 sm4
models: mlp adaptive_dbitnet_pairwise moe_v3_hard moe_v4_hard selector_rule_v2
rounds: 4 5 6
seeds: 0 1 2
samples_per_class: 8192
epochs: 5
pairs_per_sample: 4
```

Before claiming paper-level results, generate a structured summary and compare v3 vs v4 vs selector_rule_v2 by cipher structure and round.
