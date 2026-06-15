# Innovation 1 SPN/ARX Queue State - 2026-06-15

Current branch:

```text
refactor/model-project-structure
```

Remote project:

```text
G:/lxy/blockcipher-structure-adaptive-nd
```

Remote code was fast-forwarded to:

```text
9c8d5fb feat(innovation1): add PRESENT S-box DDT back2 screen
```

## SPN/PRESENT

High-round PRESENT/SPN is still not proven beyond r6. The current high-round rescue chain is:

```text
innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615
  -> innovation1-spn-present-sboxddt-top2-highround-screen-gpu0-20260615
  -> innovation1-spn-present-sboxddt-back2-highround-screen-gpu0-20260615
```

The new local relay script:

```text
scripts/generated/monitors/relay_after_spn_sboxddt_top2_to_back2.sh
```

waits for the top2 run result branch to gate at 4 rows, then schedules:

```text
G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\schedule_innovation1_spn_present_sboxddt_back2_highround_screen_gpu0_20260615.cmd
```

Existing queues:

```text
innovation1-spn-sboxddt-queue
relay_spn_sboxddt_top2
```

## ARX/SPECK

ARX must continue in parallel with SPN. The strongest verified ARX evidence so far remains:

```text
SPECK32/64 r7
model: structure_adaptive_pairset_dbitnet
feature: ciphertext_pair_xor_arx_partial_inverse_bits
samples_per_class: 131072
pairs_per_sample: 4
seeds: 0..3
cal_acc_mean: 0.789639
auc_mean: 0.869151
```

This is a strong structure-adaptive feature result, but not yet a universal SPECK SOTA claim because protocol and attack setup must be compared carefully.

The next ARX candidate is already implemented and queued:

```text
run_id: innovation1-arx-speck32-word-mixer-r7r8-gpu1-20260615
plan: experiments/innovation1/plans/innovation1_arx_speck32_word_mixer_r7r8_screen.csv
model: arx_word_mixer_pairset
feature: ciphertext_pair_xor_arx_partial_inverse_bits
rounds: 7,8
seeds: 0..3
samples_per_class: r7=131072, r8=262144
pairs_per_sample: 4
key_rotation_interval: 1024
```

This candidate matches innovation one's structure-adaptive goal: public keyless partial inverse feature plus a SPECK-style word/rotation/carry-aware pair-set model.

Local queue:

```text
tmux session: innovation1-arx-queue
script: scripts/generated/monitors/wait_gpu1_then_launch_innovation1_arx_speck32_word_mixer_r7r8.sh
```

It waits for GPU1 to become idle before scheduling the ARX word mixer run.

## Remote State Observed

Both old PRESENT jobs were still active and writing progress logs:

```text
GPU0 process 31416:
innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
progress around index 9/30, dataset cache validation chunks for seed 8

GPU1 process 16484:
innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
progress around index 5/24, dataset cache train chunks for seed 1
```

`nvidia-smi` showed low instantaneous GPU utilization but Python processes still existed and progress JSONL files were updating. This indicates dataset generation/cache activity, not fake training.

## Verification

Local checks passed:

```text
bash -n scripts/generated/monitors/relay_after_spn_sboxddt_top2_to_back2.sh
21 passed feature/SPN runner/model tests
5 passed ARX word mixer/feature tests
```

Warnings about uv env locks and pytest cache writes are from the read-only filesystem/cache behavior and did not affect test pass status.
