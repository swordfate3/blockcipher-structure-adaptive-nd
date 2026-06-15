# Innovation 1 PRESENT SBox-DDT Beam2 Plan - 2026-06-15

Goal remains PRESENT/SPN high-round improvement beyond the current verified r6 evidence. Do not claim a breakthrough until remote result gates complete and metrics beat the relevant baseline/literature protocol.

## New Feature

```text
present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits
```

For each ciphertext pair `(C, C')`, this feature encodes 12 public 64-bit words as PRESENT cell-matrix bit planes:

```text
C
C'
Delta = C xor C'
InvP(Delta)
Layer1 DDT top1 input-delta candidate
Layer1 DDT top2 input-delta candidate
Layer1 top1 confidence
Layer1 top2 confidence
Layer1 top1-vs-top2 margin
Layer2 DDT top1 after InvP(layer1_top1)
Layer2 DDT top1 after InvP(layer1_top2)
Layer2 beam disagreement = layer2_from_top1 xor layer2_from_top2
```

This is keyless and uses only public PRESENT `P^-1` and public S-box DDT statistics. It does not use the secret key or decrypt with the key.

## Why Beam2

Previous SBox-DDT features used top1 or top2 local candidates, and back2 followed only the top1 path for two layers. High-round differential paths are uncertain, so betting on a single top1 local predecessor can be brittle. Beam2 keeps two local candidates plus confidence/margin and a second-layer disagreement signal, giving the model information about public differential-path ambiguity rather than only one guessed path.

## Files

Implemented:

```text
src/blockcipher_ai_eval/features/pair_features.py
src/blockcipher_ai_eval/features/registry.py
tests/test_feature_encodings.py
```

Remote plan/config/scripts:

```text
experiments/innovation1/plans/innovation1_spn_present_sboxddt_beam2_highround_screen.csv
experiments/innovation1/configs/remote/innovation1_spn_present_sboxddt_beam2_highround_screen_gpu0_20260615.json
scripts/generated/remote/run_innovation1-spn-present-sboxddt-beam2-highround-screen-gpu0-20260615_and_push.cmd
scripts/generated/remote/launch_innovation1-spn-present-sboxddt-beam2-highround-screen-gpu0-20260615.cmd
scripts/generated/remote/schedule_innovation1_spn_present_sboxddt_beam2_highround_screen_gpu0_20260615.cmd
scripts/generated/monitors/monitor_innovation1_spn_present_sboxddt_beam2_highround_screen_gpu0_results.sh
scripts/generated/monitors/relay_after_spn_sboxddt_back2_to_beam2.sh
```

## Experiment

```text
run_id: innovation1-spn-present-sboxddt-beam2-highround-screen-gpu0-20260615
expected_rows: 4
rounds: 7,8
seed: 0
samples_per_class: 65536
pairs_per_sample: 16
feature: present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits
models:
  present_inception_mcnd_matrix
  present_p_layer_mixer_pairset
device: cuda:0
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
checkpoint_metric: val_auc
```

This run is chained after:

```text
innovation1-spn-present-sboxddt-back2-highround-screen-gpu0-20260615
```

Local relay session to start/keep:

```text
tmux session: relay_spn_sboxddt_beam2
script: scripts/generated/monitors/relay_after_spn_sboxddt_back2_to_beam2.sh
```

## Verification

Local validation completed:

```text
pytest tests/test_feature_encodings.py -q
20 passed

tiny true-training smoke:
run_innovation_one_matrix.py with beam2 feature, PRESENT r2, CPU, 1 epoch, wrote 1 JSONL row

combined related tests:
22 passed
```

`compileall` is not useful in this environment because writing `__pycache__` is blocked by the read-only filesystem behavior. The source path is validated through pytest using `PYTHONDONTWRITEBYTECODE=1`.

## Result Interpretation Rule

Beam2 is only a candidate. A successful result requires the result branch to exist, result gate to pass at 4 rows, stderr to be clean, and r7/r8 metrics to beat the current SPN high-round candidates under the same protocol. If it does not beat them, continue with stronger beam width/model scaling rather than reporting completion.
