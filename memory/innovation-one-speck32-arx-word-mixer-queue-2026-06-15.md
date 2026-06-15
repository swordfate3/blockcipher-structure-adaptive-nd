# Memory: SPECK32/64 ARX WordMixer Queue (2026-06-15)

## Why This Matters

Innovation 1 is not only the PRESENT/SPN branch. ARX also needs a structure-adaptive path. The strongest completed ARX evidence before this step is SPECK32/64 round 7 with the keyless public partial-inverse v2 feature:

```text
run_id: innovation1-arx-speck32-v2-scale-m-gpu0-20260609
model: structure_adaptive_pairset_dbitnet
feature: ciphertext_pair_xor_arx_partial_inverse_bits
rounds: 7
samples_per_class: 131072
pairs_per_sample: 4
seeds: 0..3
raw cal_acc mean: 0.543276, AUC mean: 0.560338
ARX v2 cal_acc mean: 0.789639, AUC mean: 0.869151
delta: +0.246363 cal_acc, +0.308813 AUC
```

Safe interpretation: this is strong structure-adaptation evidence under our protocol. It is not yet a universal SPECK neural distinguisher SOTA claim, because Gohr-style and later SPECK papers may use different input, data, training, related-key assumptions, or attack settings.

## New ARX WordMixer Implementation

Committed and pushed on branch `refactor/model-project-structure`:

```text
ce2b8c8 feat(innovation1): add ARX word mixer screen
caffae5 chore(remote): queue ARX run after GPU1 frees
```

Core model:

```text
model_key: arx_word_mixer_pairset
file: src/blockcipher_ai_eval/models/structure/arx/word_mixer_pairset.py
feature: ciphertext_pair_xor_arx_partial_inverse_bits
default pair_bits: 224
SPECK32 tokenization: each 32-bit feature word -> two 16-bit word tokens
messages: ROR7 token view, ROL2 token view, left/right peer message, carry proxy
pooling: topk_logsumexp or attention_mean_max
```

The design goal is to move beyond generic pair-set DBitNet and make the network match SPECK-style ARX structure: word granularity, public rotations, and carry-like nonlinear interaction proxies.

## Local Validation

Passed before remote queueing:

```text
Tiny plan smoke: run_innovation_one_matrix.py with arx_word_mixer_pairset, SPECK32 r2, CPU, wrote 1 row
Decoded config: pair_bits=224, input_bits=448, checkpoint_metric=val_auc
ARX model tests: 4 passed
Regression slice: 73 passed
```

Important tests include:

```text
test_arx_word_mixer_pairset_preserves_word_tokens_and_evidence_pooling
test_arx_word_mixer_block_uses_rotation_messages_and_carry_proxy
test_build_model_supports_arx_word_mixer_pairset_key_and_options
```

## Remote Plan

Remote plan prepared and committed:

```text
run_id: innovation1-arx-speck32-word-mixer-r7r8-gpu1-20260615
expected_rows: 16
plan: experiments/innovation1/plans/innovation1_arx_speck32_word_mixer_r7r8_screen.csv
device: cuda:1
rounds: 7, 8
seeds: 0,1,2,3
samples_per_class: r7 -> 131072, r8 -> 262144
pairs_per_sample: 4
feature: ciphertext_pair_xor_arx_partial_inverse_bits
negative_mode: encrypted_random_plaintexts
difference_profile: speck32_gohr2019
key_rotation_interval: 1024
checkpoint_metric: val_auc
epochs: 20
batch_size: 512
dataset_cache_chunk_size: 4096
```

Variants in the plan:

```text
ARX-WordMixer-v2-topk: pooling=topk_logsumexp, top_k=2, lse_temperature=0.75, token_dim=64, mixer_depth=4
ARX-WordMixer-v2-attn: pooling=attention_mean_max, token_dim=64, mixer_depth=4
```

## Remote State at Queue Time

Remote main project was synced to `caffae5`. GPU1 was not free because this process was still running:

```text
ProcessId: 16484
run: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
device: cuda:1
result rows observed: 3/24
recent stage: dataset_cache index 4/24
```

Therefore ARX was not launched immediately. A local tmux queue was started instead:

```text
tmux session: innovation1-arx-queue
script: scripts/generated/monitors/wait_gpu1_then_launch_innovation1_arx_speck32_word_mixer_r7r8.sh
interval: 600 seconds
behavior: wait until no remote run_innovation_one_matrix.py process uses --device cuda:1, then sync remote project and call the ARX schedule script
```

The queue script correctly reported:

```text
WAIT missing result branches: results/innovation1-arx-speck32-word-mixer-r7r8-gpu1-20260615
GPU1 still has an active matrix training process; sleeping
```

## Next Interpretation Gate

Do not call ARX WordMixer successful until all are true:

```text
result branch exists: results/innovation1-arx-speck32-word-mixer-r7r8-gpu1-20260615
result_gate: result_lines=16 and expected_rows=16
stderr has no real training error
local archive retrieved under outputs/remote_results/<run_id>/
summary confirms whether r7 beats the existing ARX v2 baseline and whether r8 rises above random
```

The first target is not necessarily a direct SOTA claim; it is to test whether an ARX-specific network can improve over the already strong v2 feature baseline and provide a clearer structure-adaptive story for Innovation 1.
