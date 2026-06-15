# Memory: PRESENT/SPN SBox-DDT High-Round Queue (2026-06-15)

## Goal

The active Innovation 1 target remains PRESENT/SPN high-round breakthrough, not just low-round r6 evidence. This step adds a keyless public S-box DDT feature intended to expose weak local S-box consistency evidence for r7/r8.

## New Feature

Feature key:

```text
present_pair_xor_paligned_sboxddt_cell_matrix_bits
```

Per ciphertext pair it encodes six 64-bit PRESENT words in existing cell-matrix bit-plane order:

```text
C || Cprime || Delta || InvP(Delta) || DDTBestInputDelta || DDTConfidence
```

Construction:

```text
Delta = C xor Cprime
aligned = inverse_permutation_layer(Delta)
For each 4-bit nibble of aligned output difference:
  use public PRESENT S-box DDT
  choose the input difference with the largest DDT count
  encode the best input-difference nibble
  encode a 4-bit confidence nibble derived from the DDT count
```

This uses only public cipher structure and ciphertext pair differences. It does not use round keys or secret-key leakage.

## Code and Validation

Committed and pushed:

```text
fb73404 feat(innovation1): add PRESENT S-box DDT high-round screen
a5a2a41 chore(remote): queue SPN SBox-DDT run after GPU0 frees
```

Touched files include:

```text
src/blockcipher_ai_eval/features/pair_features.py
src/blockcipher_ai_eval/features/registry.py
experiments/run_innovation_one_matrix.py
tests/test_feature_encodings.py
experiments/innovation1/plans/innovation1_spn_present_sboxddt_highround_screen.csv
experiments/innovation1/configs/remote/innovation1_spn_present_sboxddt_highround_screen_gpu0_20260615.json
scripts/generated/remote/run_innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615_and_push.cmd
scripts/generated/remote/launch_innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615.cmd
scripts/generated/remote/schedule_innovation1_spn_present_sboxddt_highround_screen_gpu0_20260615.cmd
scripts/generated/monitors/monitor_innovation1_spn_present_sboxddt_highround_screen_gpu0_results.sh
scripts/generated/monitors/wait_gpu0_then_launch_innovation1_spn_sboxddt_highround_screen.sh
```

Local validation:

```text
UV_CACHE_DIR=/tmp/uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/test_feature_encodings.py tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_accepts_spn_aligned_feature_encoding tests/test_present_inception_mcnd_model.py tests/test_adaptive_dbitnet_model.py::test_present_p_layer_mixer_pairset_forward_and_position_mapping tests/test_adaptive_dbitnet_model.py::test_build_model_supports_present_p_layer_mixer_pairset_key -q
=> 26 passed, 1 pytest cache warning due read-only local .pytest_cache

SBox-DDT plan smoke:
PRESENT-80 r=2 model=present_inception_mcnd_matrix seed=0 pairs=2
wrote 1 row to /tmp/innovation1_spn_sboxddt_plan_smoke.jsonl
```

`experiments/run_innovation_one_matrix.py` now uses `choices=sorted(FEATURE_ENCODINGS)` so new feature encodings registered in `features/registry.py` are automatically accepted by the CLI.

## Remote Plan

Run id:

```text
innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615
expected_rows: 8
plan: experiments/innovation1/plans/innovation1_spn_present_sboxddt_highround_screen.csv
device: cuda:0
rounds: 7,8
seeds: 0,1
samples_per_class: 65536
pairs_per_sample: 16
sample_structure: zhang_wang_case2_mcnd
difference_profile: present_zhang_wang2022_mcnd
feature: present_pair_xor_paligned_sboxddt_cell_matrix_bits
checkpoint_metric: val_auc
epochs: 20
batch_size: 128
dataset_cache_chunk_size: 2048
```

Models in the screen:

```text
present_inception_mcnd_matrix
  kernel_sizes=[[1,1],[1,2],[2,4],[4,4]], blocks=3, pooling=attention_mean_max

present_p_layer_mixer_pairset
  pooling=topk_logsumexp, top_k=2, token_dim=64, mixer_depth=4
```

## Queue State

Remote project synced to:

```text
a5a2a41
```

The run was not launched immediately because GPU0 still has the existing r6 controls training process:

```text
ProcessId 31416
run: innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
device: cuda:0
```

Local tmux queue started:

```text
tmux session: innovation1-spn-sboxddt-queue
script: scripts/generated/monitors/wait_gpu0_then_launch_innovation1_spn_sboxddt_highround_screen.sh
interval: 600 seconds
```

Observed queue output:

```text
WAIT missing result branches: results/innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615
GPU0 still has an active matrix training process; sleeping
```

## Result Gate

Do not claim a high-round improvement until:

```text
results/innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615 exists
result_gate has result_lines=8 and expected_rows=8
stderr has no training error
local archive is retrieved under outputs/remote_results/<run_id>/
r7/r8 summary is compared against existing SPN aligned/matrix/p-layer results and literature protocol boundaries
```
