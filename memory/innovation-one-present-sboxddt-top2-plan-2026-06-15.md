# Memory: PRESENT/SPN SBox-DDT Top2 Follow-up (2026-06-15)

## Motivation

Single best DDT input-difference may be too brittle for high-round PRESENT. Added a top-2 DDT uncertainty feature so the network can see both the highest and second-highest public S-box DDT candidate plus confidence words. This is still keyless and uses only public PRESENT S-box DDT and ciphertext-pair differences.

## New Feature

```text
present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits
```

Per pair, eight 64-bit words in cell-matrix bit-plane order:

```text
C || Cprime || Delta || InvP(Delta) || DDTTop1 || DDTTop2 || ConfidenceTop1 || ConfidenceTop2
```

## Validation

Local validation passed:

```text
UV_CACHE_DIR=/tmp/uv-cache PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/test_feature_encodings.py tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_accepts_spn_aligned_feature_encoding tests/test_adaptive_dbitnet_model.py::test_present_p_layer_mixer_pairset_forward_and_position_mapping -q
=> 20 passed, 1 pytest cache warning due read-only .pytest_cache

Top2 direct smoke:
PRESENT-80 r=2 model=present_p_layer_mixer_pairset seed=0 pairs=2
wrote 1 row to /tmp/innovation1_spn_sboxddt_top2_smoke.jsonl

Top2 plan smoke:
PRESENT-80 r=2 model=present_inception_mcnd_matrix seed=0 pairs=2
wrote 1 row to /tmp/innovation1_spn_sboxddt_top2_plan_smoke.jsonl
```

## Commits

```text
2537408 feat(innovation1): add PRESENT S-box DDT top2 screen
60f3347 chore(remote): relay SPN SBox-DDT to top2 screen
```

## Remote Plan

```text
run_id: innovation1-spn-present-sboxddt-top2-highround-screen-gpu0-20260615
expected_rows: 4
rounds: 7,8
seed: 0
samples_per_class: 65536
pairs_per_sample: 16
feature: present_pair_xor_paligned_sboxddt_top2_cell_matrix_bits
models: present_inception_mcnd_matrix, present_p_layer_mixer_pairset
checkpoint_metric: val_auc
```

## Relay State

Top2 is intentionally not launched immediately. A local tmux relay waits for the upstream single-best SBox-DDT screen to gate first:

```text
tmux session: relay_spn_sboxddt_top2
script: scripts/generated/monitors/relay_after_spn_sboxddt_to_top2.sh
upstream: innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615=8
next: innovation1-spn-present-sboxddt-top2-highround-screen-gpu0-20260615=4
```

Observed output:

```text
WAIT missing result branches: results/innovation1-spn-present-sboxddt-top2-highround-screen-gpu0-20260615
WAIT missing result branches: results/innovation1-spn-present-sboxddt-highround-screen-gpu0-20260615
WAIT upstream not gated yet
```

Remote main project synced to:

```text
60f3347
```

## Current Dependency

GPU0 is still occupied by old r6 controls. The SBox-DDT queue will launch the upstream screen only after that process exits. Then this relay will launch top2 after upstream result branch passes gate.
