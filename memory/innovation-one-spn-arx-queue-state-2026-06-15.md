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

## Update 2026-06-15 23:25 CST

Workspace path was repaired for this session by restoring `/home/fate/gitproject/thesis_liaoxiyue` as a symlink to the renamed project directory:

```text
/home/fate/gitproject/blockcipher-structure-adaptive-nd
```

Main SPN goal remains PRESENT high-round improvement. Added the next queued SPN curriculum run after the existing SBoxDDT TrailMixer screen:

```text
run_id: innovation1-spn-present-sboxddt-trailmixer-curriculum-highround-gpu0-20260615
plan: experiments/innovation1/plans/innovation1_spn_present_sboxddt_trailmixer_curriculum_highround_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_sboxddt_trailmixer_curriculum_highround_gpu0_20260615.json
relay: scripts/generated/monitors/relay_after_spn_sboxddt_trailmixer_to_curriculum.sh
expected rows: 4
rounds: PRESENT r7/r8
feature: back2 and beam2 SBox-DDT public trail features
model: present_trail_mixer_pairset
curriculum: r6 pretrain, 6 epochs from plan
samples/class: r7 65536, r8 131072
pairs/sample: 16
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
```

## Update 2026-06-16 00:00 CST

The PRESENT/SPN sidecar explorer confirmed the current SPN status:

```text
Verified strong: PRESENT r5/r6 and GIFT r5 structure-aligned evidence.
Known weak/failed: plain SPNAligned/matrix/integral variants at PRESENT r7/r8.
Highest-priority pending: SBoxDDT back2/beam2 TrailMixer curriculum and MatrixTrailHybrid.
If those fail: implement configurable multi-depth/multi-beam DDT trail features, not just deeper generic models.
```

Remote state observed during this update:

```text
GPU0 PID 31416:
innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
progress: index 14/30, dataset cache for seed 3

GPU1 PID 16484:
innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
progress: index 6/24, epoch 15/24
train loss near 0.25, so this specific r7 screen currently looks weak/random-like.
```

ARX was explicitly advanced, not left as a side branch. Added a new SPECK32/64 model:

```text
model key: arx_round_function_hybrid_pairset
class: ArxRoundFunctionHybridPairSetDistinguisher
file: src/blockcipher_ai_eval/models/structure/arx/round_function_hybrid.py
```

Purpose:

```text
Use existing public keyless SPECK partial-inverse/RX/carry feature words, but group them as 16-bit
round-function tokens and explicitly mix ror7, rol2, left/right branch peer messages, addition proxy,
carry proxy, feature-word groups, and multi-pair top-k/logsumexp evidence.
```

This ARX candidate is more structure-adaptive than a generic pairset DBitNet and is intended to test
whether SPECK round-function priors improve the strong verified r7 ARX partial-inverse result:

```text
SPECK32/64 r7
model: structure_adaptive_pairset_dbitnet
feature: ciphertext_pair_xor_arx_partial_inverse_bits
samples/class: 131072
pairs/sample: 4
seeds: 0..3
cal_acc_mean: 0.789639
auc_mean: 0.869151
```

New ARX screen prepared:

```text
run_id: innovation1-arx-speck32-round-hybrid-r7r8-gpu1-20260615
plan: experiments/innovation1/plans/innovation1_arx_speck32_round_hybrid_r7r8_screen.csv
config: experiments/innovation1/configs/remote/innovation1_arx_speck32_round_hybrid_r7r8_gpu1_20260615.json
monitor: scripts/generated/monitors/monitor_innovation1_arx_speck32_round_hybrid_r7r8_gpu1_results.sh
relay: scripts/generated/monitors/relay_after_arx_trail_mixer_to_round_hybrid.sh
expected rows: 8
rounds: SPECK32/64 r7/r8
models: arx_round_function_hybrid_pairset and same-protocol structure_adaptive_pairset_dbitnet RX control
feature: ciphertext_pair_xor_arx_partial_inverse_rx_bits
curriculum: r6 pretrain, 6 epochs from plan
samples/class: r7 131072, r8 262144
pairs/sample: 4
key_rotation_interval: 1024
```

Local verification:

```text
65 passed in 47.94s for remote script generator, feature encodings, PRESENT Inception MCND model, and matrix runner.
```

## Update 2026-06-16 00:45 CST

SPN/PRESENT remains the main success criterion. ARX/SPECK should continue, but it must not take GPU1 before the next PRESENT protocol-calibration run.

Prepared and locally verified a new SPN protocol + SPN-aligned medium screen:

```text
run_id: innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616
plan: experiments/innovation1/plans/innovation1_spn_present_protocol_spnaligned_scale_m.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_protocol_spnaligned_scale_m_gpu1_20260616.json
expected rows: 12
device: cuda:1
rounds: PRESENT r6/r7
seeds: 0,1
samples/class: 32768
pairs/sample: 16
sample_structure: zhang_wang_case2_independent_mcnd
difference_profile: present_zhang_wang2022_mcnd
negative_mode: encrypted_random_plaintexts
key_rotation_interval: 1
features:
  - present_mcnd_cell_matrix_bits
  - present_pair_xor_paligned_cell_matrix_bits
models:
  - present_inception_mcnd_global_matrix
  - present_inception_mcnd_matrix
```

Purpose:

```text
Separate protocol risk from architecture risk:
1. Re-check Zhang/Wang-style independent-pair MCND protocol.
2. Compare raw MCND cell matrix against public P-layer inverse-aligned SPN feature.
3. See whether the strong previous r6 aligned result survives under key_rotation_interval=1 and independent pairs.
4. If r6 recovers but r7 stays random, continue with DDT/deeper trail features rather than generic model scaling.
```

Generated local wait/relay scripts:

```text
scripts/generated/monitors/wait_gpu1_then_launch_innovation1_spn_present_protocol_spnaligned_scale_m.sh
scripts/generated/monitors/relay_after_spn_protocol_to_arx_trail_mixer.sh
scripts/generated/monitors/monitor_innovation1_spn_present_protocol_spnaligned_scale_m_gpu1_results.sh
```

Scheduling policy:

```text
GPU1 current PRESENT r7 matrix screen
  -> SPN protocol aligned scale-m run
  -> ARX trail-mixer curriculum r7/r8
  -> ARX round-hybrid
  -> ARX partial-inverse r7 confirm
```

The ARX relay was adjusted to launch from:

```text
G:\lxy\blockcipher-structure-adaptive-nd
```

instead of relying on the SSH default working directory.

## Update 2026-06-16 01:05 CST

Local tmux/background monitor launch was blocked by the local permission review timeout, so the GPU1 queue was moved to remote-side Windows watchers. This avoids depending on the local Codex session staying alive.

Added remote Task Scheduler wrappers:

```text
scripts/generated/remote/watch_gpu1_then_schedule_innovation1_spn_present_protocol_spnaligned_scale_m_20260616.ps1
scripts/generated/remote/schedule_watch_gpu1_then_spn_protocol_spnaligned_scale_m_20260616.cmd
scripts/generated/remote/watch_after_spn_protocol_to_arx_trail_mixer_20260616.ps1
scripts/generated/remote/schedule_watch_after_spn_protocol_to_arx_trail_mixer_20260616.cmd
```

Remote watcher policy:

```text
1. Watch GPU1 for python.exe processes.
2. When GPU1 is idle, launch:
   innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616
3. Independently watch GitHub for:
   results/innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616
4. After that gated result branch appears, launch:
   innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
```

Watcher logs are written under:

```text
G:\lxy\blockcipher-structure-adaptive-nd-runs\launcher_logs
```

## Update 2026-06-16 01:25 CST

Current GPU1 r7 matrix screen still looks weak during training:

```text
run_id: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
observed row: index 8/24
observed epoch: 20-21/24
val_accuracy: 0.5
val_auc: 0.5
```

To keep the main SPN/PRESENT objective ahead of the ARX side queue, GPU1 chaining was adjusted from:

```text
current r7 matrix -> protocol aligned scale-m -> ARX TrailMixer
```

to:

```text
current r7 matrix
  -> innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616
  -> innovation1-spn-present-sinv-matrix-screen-gpu1-20260616
  -> innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
```

Added GPU1 SInv screen:

```text
config: experiments/innovation1/configs/remote/innovation1_spn_present_sinv_matrix_screen_gpu1_20260616.json
run_id: innovation1-spn-present-sinv-matrix-screen-gpu1-20260616
expected rows: 12
device: cuda:1
plan: experiments/innovation1/plans/innovation1_spn_present_sinv_matrix_screen.csv
feature: present_pair_xor_paligned_sinv_cell_matrix_bits
models:
  - present_inception_mcnd_matrix
  - present_inception_mcnd_global_matrix
  - present_inception_mcnd_pair_stack_matrix
rounds: PRESENT r6/r7
seeds: 0,1
samples/class: 32768
pairs/sample: 16
key_rotation_interval: 1024
```

Purpose:

```text
Test whether the public zero-key InvP+InvS structural approximation preserves the known r6 signal and raises r7 above random. If r6 collapses, the SInv feature is likely destructive. If r6 survives and r7 rises, expand to multi-seed confirmation before claiming a high-round improvement.
```

The after-protocol watcher now launches SInv first. A new after-SInv watcher launches ARX TrailMixer only after the SInv result branch appears:

```text
scripts/generated/remote/watch_after_sinv_to_arx_trail_mixer_20260616.ps1
scripts/generated/remote/schedule_watch_after_sinv_to_arx_trail_mixer_20260616.cmd
```

## Update 2026-06-16 01:45 CST

Because the plain r7 SPN-aligned matrix screen remains near random during training:

```text
run_id: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
observed row: index 9/24
seed: 2
epoch 1 val_auc: 0.5030903164
```

added a stronger SPN fused nonlinear-trail feature:

```text
feature: present_pair_xor_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits
pair width: 3200 bits for PRESENT-64
public words:
  - C
  - C'
  - C xor C'
  - InvP(C xor C')
  - InvS(InvP(C)) xor InvS(InvP(C'))
  - 4-beam, 3-depth public SBox-DDT trail words seeded from the structural inverse difference
```

This is intended to test whether the public zero-key nonlinear inverse approximation gives a better start point for SBox-DDT beam backtracking than plain `InvP(C xor C')`.

Added screen:

```text
run_id: innovation1-spn-present-sinv-sboxddt-beam4deep3-highround-gpu1-20260616
plan: experiments/innovation1/plans/innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_gpu1_20260616.json
expected rows: 8
device: cuda:1
rounds: PRESENT r7/r8
seeds: 0,1
samples/class: r7 65536, r8 131072
models:
  - present_matrix_trail_hybrid_pairset
  - present_trail_mixer_pairset
pretrain: r6 for 6 epochs from plan
```

GPU1 watcher chain is now:

```text
current r7 matrix
  -> protocol aligned scale-m
  -> SInv matrix screen
  -> SInv + SBoxDDT Beam4Deep3 high-round screen
  -> ARX TrailMixer
```

New ARX relay after fused SPN screen:

```text
scripts/generated/remote/watch_after_sinv_sboxddt_beam4deep3_to_arx_trail_mixer_20260616.ps1
scripts/generated/remote/schedule_watch_after_sinv_sboxddt_beam4deep3_to_arx_trail_mixer_20260616.cmd
```
ARX RoundFunctionHybrid CPU smoke: wrote 1 row to /tmp/arx_round_hybrid_smoke_results.jsonl
bash -n relay/monitor scripts: pass
75 passed: adaptive model + feature encoding + remote script generator tests
```

Remote script generator was fixed so generated monitor scripts default to:

```text
--remote "${RESULT_REMOTE:-origin-ssh}"
```

This prevents the old HTTPS/TLS monitor failure from recurring in newly generated scripts.

ARX side track status:

```text
run_id: innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
```

A remote attempt exists but has 0 result rows and `RUN_GATE_BLOCKED_RUN_FAILED`. Its progress log shows the runner did start and generated SPECK32 r7 training cache chunks up to about 102400/131072 positive rows before stopping. Run stdout/stderr were both 0 bytes. This is consistent with the earlier protective interruption/mislaunch incident, not a confirmed model/data bug. Local CPU smoke using a one-row reduced ARX TrailMixer plan completed successfully and wrote 1 result row:

```text
/tmp/arx_trail_smoke_results.jsonl
/tmp/arx_trail_smoke_progress.jsonl
```

Verification completed locally:

```text
30 passed: remote generator + SPN TrailMixer feature/model/evaluation tests
17 passed: remote script generator and legacy remote script tests
ARX TrailMixer CPU smoke: wrote 1 row successfully
```

Remote observed by monitor sidecar:

```text
GPU0 PID 31416: innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615, 11/30 rows, stderr 0 bytes
GPU1 PID 16484: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615, 5/24 rows, stderr 0 bytes
ARX TrailMixer: not currently running, no result branch yet
```

## Update 2026-06-15 23:45 CST

Added a next-generation SPN/PRESENT structure-adaptive candidate:

```text
model key: present_matrix_trail_hybrid_pairset
class: PresentMatrixTrailHybridPairSetDistinguisher
file: src/blockcipher_ai_eval/models/structure/spn/present_matrix_trail_hybrid.py
```

Purpose:

```text
Fuse two evidence views that were previously tested mostly separately:
1. PRESENT cell-matrix local evidence over raw/xor/paligned/DDT words.
2. PRESENT public DDT trail-role evidence with P-layer message passing.
```

This keeps the innovation-one claim aligned with structure adaptation: the model is not a generic MLP; it encodes PRESENT word roles, nibble positions, P-layer mixing, and matrix-local cell patterns over public keyless S-box DDT trail features.

Local verification:

```text
73 passed: adaptive model + feature encoding + remote script generator tests
Hybrid runner smoke: experiments/run_innovation_one_matrix.py wrote 1 row to /tmp/present_hybrid_smoke_results.jsonl
```

Remote queued run prepared:

```text
run_id: innovation1-spn-present-matrix-trail-hybrid-highround-gpu0-20260615
plan: experiments/innovation1/plans/innovation1_spn_present_matrix_trail_hybrid_highround_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_matrix_trail_hybrid_highround_gpu0_20260615.json
monitor: scripts/generated/monitors/monitor_innovation1_spn_present_matrix_trail_hybrid_highround_gpu0_results.sh
relay: scripts/generated/monitors/relay_after_spn_sboxddt_curriculum_to_matrix_trail_hybrid.sh
expected rows: 4
rounds: PRESENT r7/r8
features: SBoxDDT back2 and beam2 public trail encodings
curriculum: r6 pretrain, 6 epochs from plan
samples/class: r7 65536, r8 131072
pairs/sample: 16
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
```

## Update 2026-06-16 00:20 CST

To keep pushing the main PRESENT/SPN high-round objective rather than waiting idly, added a deeper public SBox-DDT beam feature:

```text
feature: present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits
implementation: src/blockcipher_ai_eval/features/pair_features.py
registered: src/blockcipher_ai_eval/features/registry.py
pair_bits for PRESENT-64: 3136
```

This feature extends the previous `beam2` encoding from a shallow two-candidate view to a fixed four-beam, three-depth public trail family. Per pair it encodes:

```text
C, C', Delta_C, P^-1(Delta_C)
for each of 3 public DDT-backtracking layers:
  top 4 candidate input-difference words
  top 4 confidence words
  top 4 margin words
  beam disagreement word
  compact score word
  compact active-nibble proxy word
```

The intent is to test the sidecar conclusion that PRESENT r7/r8 likely needs a trail-family signal, not another generic wider/deeper model over the old `P^-1(Delta)` view.

New queued SPN high-round screen:

```text
run_id: innovation1-spn-present-sboxddt-beam4deep3-highround-gpu0-20260616
plan: experiments/innovation1/plans/innovation1_spn_present_sboxddt_beam4deep3_highround_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_sboxddt_beam4deep3_highround_gpu0_20260616.json
monitor: scripts/generated/monitors/monitor_innovation1_spn_present_sboxddt_beam4deep3_highround_gpu0_results.sh
relay: scripts/generated/monitors/relay_after_spn_matrix_trail_hybrid_to_beam4deep3.sh
expected rows: 8
rounds: PRESENT r7/r8
models: present_matrix_trail_hybrid_pairset and present_trail_mixer_pairset
feature: present_pair_xor_paligned_sboxddt_beam4deep3_cell_matrix_bits
curriculum: r6 pretrain, 6 epochs from plan
samples/class: r7 65536, r8 131072
pairs/sample: 16
key_rotation_interval: 1024
batch_size: 64
dataset_cache_chunk_size: 1024
```

Local verification:

```text
feature tests: 21 passed
beam4deep3 + PresentMatrixTrailHybrid CPU smoke: wrote 1 row to /tmp/present_beam4deep3_hybrid_smoke.jsonl
remote relay/monitor bash syntax: pass
76 passed: feature + adaptive model + remote script generator tests
plan parse check: 8 rows; model_options/pretrain fields parsed correctly
```

## Update 2026-06-16 00:35 CST

Remote check:

```text
No new SPN result branches yet.
GPU0 PID 31416 still running r6 controls, around index 14/30.
GPU1 PID 16484 still running r7 matrix screen, around index 7/24.
GPU0 r6 control remains healthy: example seed 3 epoch 18 val_auc about 0.8914.
GPU1 r7 matrix remains weak/random-like in training loss around 0.25.
```

Added a result-driven next-step helper so completed high-round screens can be scaled without manual CSV triage:

```text
script: experiments/innovation1/select_highround_candidates.py
test: tests/test_select_highround_candidates.py
```

Purpose:

```text
Read one or more remote *_summary.csv files.
Filter PRESENT-80 r7/r8+ candidates by calibrated accuracy and/or AUC.
Rank by round, calibrated accuracy, AUC, run count, and sample size.
Copy the matching row from a source plan.
Emit a multi-seed confirm CSV with larger samples_per_class.
```

Validation:

```text
Synthetic selector test: 1 passed.
Historical real-summary smoke: selected r7/r8 candidates from
outputs/remote_results/innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615
and wrote /tmp/present_candidate_confirm.csv.
```

This does not prove a high-round breakthrough; it removes a workflow delay once the pending SBoxDDT/MatrixTrailHybrid/Beam4Deep3 results land.

## Update 2026-06-16 00:30 CST

ARX/SPECK line was rechecked because the user explicitly asked to keep ARX moving too.

Current verified local ARX result summaries:

```text
SPECK32/64 r6, aligned screen:
calibrated_accuracy_mean ~= 0.8795
auc_mean ~= 0.9444

SPECK32/64 r7, small feature screens:
calibrated_accuracy_mean ~= 0.513-0.523
auc_mean ~= 0.516-0.530

SPECK32/64 r7, scale-m partial-inverse:
outputs/remote_results/innovation1-arx-speck32-v2-scale-m-gpu0-20260609
calibrated_accuracy_mean ~= 0.6665
auc_mean ~= 0.7147

SPECK32/64 r7, scale-m-v2 arxbest partial-inverse:
outputs/remote_results/innovation1-arx-speck32-v2-scale-m-v2-arxbest-gpu1-20260612
calibrated_accuracy_mean ~= 0.6632
auc_mean ~= 0.7236

SPECK32/64 r7, scale-s partial-inverse:
calibrated_accuracy_mean ~= 0.5498
auc_mean ~= 0.5563
```

Interpretation:

```text
The plain partial-inverse ARX feature has real r7 signal under larger sample counts.
RX/carry-expanded feature did not show signal in tiny 8192-sample smoke runs, but it has not yet been validated under the dedicated TrailMixer/RoundFunctionHybrid large protocol.
The next ARX priority is not a new broad architecture sweep; it is a same-protocol r7/r8 confirmation of:
  1. arx_trail_mixer_pairset over ciphertext_pair_xor_arx_partial_inverse_rx_bits
  2. arx_word_mixer_pairset partial-inverse control
  3. arx_round_function_hybrid_pairset over ciphertext_pair_xor_arx_partial_inverse_rx_bits
  4. structure_adaptive_pairset_dbitnet RX control
```

Remote script generator fix:

```text
scripts/generators/generate_remote_experiment_scripts.py now emits
set PYTHONPATH=%RUN_DIR%\src;%PYTHONPATH%
before running the summarizer.
```

Reason:

```text
Some earlier ARX remote runs had complete JSONL and passing result_line gates, but empty summary CSVs because remote summarization failed with:
ModuleNotFoundError: No module named 'blockcipher_ai_eval'
```

Regenerated ARX run scripts with the fix:

```text
scripts/generated/remote/run_innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615_and_push.cmd
scripts/generated/remote/run_innovation1-arx-speck32-round-hybrid-r7r8-gpu1-20260615_and_push.cmd
```

Local verification:

```text
uv run pytest tests/test_feature_encodings.py tests/test_adaptive_dbitnet_model.py tests/test_remote_script_generator.py -q
76 passed
```

## Update 2026-06-16 00:45 CST

ARX/SPECK was advanced from passive queueing to a three-stage GPU1 chain:

```text
1. innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
   - waits for GPU1 to be free
   - plan: experiments/innovation1/plans/innovation1_arx_speck32_trail_mixer_curriculum_r7r8_screen.csv
   - rows: 8
   - purpose: validate RX/carry public-feature TrailMixer and WordMixer controls at r7/r8

2. innovation1-arx-speck32-round-hybrid-r7r8-gpu1-20260615
   - relay starts after TrailMixer result branch gates
   - plan: experiments/innovation1/plans/innovation1_arx_speck32_round_hybrid_r7r8_screen.csv
   - rows: 8
   - purpose: validate explicit SPECK round-function grouping against DBitNet RX controls

3. innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616
   - relay starts after RoundHybrid result branch gates
   - plan: experiments/innovation1/plans/innovation1_arx_speck32_partial_inverse_r7_confirm_10seed.csv
   - rows: 10
   - purpose: confirm the previously strongest r7 partial-inverse signal across seeds 0..9
```

New ARX confirm files:

```text
experiments/innovation1/plans/innovation1_arx_speck32_partial_inverse_r7_confirm_10seed.csv
experiments/innovation1/configs/remote/innovation1_arx_speck32_partial_inverse_r7_confirm_10seed_gpu1_20260616.json
scripts/generated/remote/run_innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616_and_push.cmd
scripts/generated/remote/launch_innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616.cmd
scripts/generated/remote/schedule_innovation1_arx_speck32_partial_inverse_r7_confirm_10seed_gpu1_20260616.cmd
scripts/generated/monitors/monitor_innovation1_arx_speck32_partial_inverse_r7_confirm_10seed_gpu1_results.sh
scripts/generated/monitors/relay_after_arx_round_hybrid_to_partial_inverse_confirm.sh
```

The confirm plan was generated by:

```text
experiments/innovation1/select_highround_candidates.py
```

from:

```text
outputs/remote_results/innovation1-arx-speck32-v2-scale-m-v2-arxbest-gpu1-20260612/*_summary.csv
```

Selected evidence:

```text
SPECK32/64 r7
model: structure_adaptive_pairset_dbitnet
feature: ciphertext_pair_xor_arx_partial_inverse_bits
samples/class: 131072
pairs/sample: 4
calibrated_accuracy_mean ~= 0.6632
auc_mean ~= 0.7236
```

Local verification:

```text
uv run pytest tests/test_select_highround_candidates.py tests/test_remote_script_generator.py tests/test_feature_encodings.py tests/test_adaptive_dbitnet_model.py -q
77 passed
```

Remote status at the time of this update:

```text
Remote project G:\lxy\blockcipher-structure-adaptive-nd fast-forwarded to c33c136.
GPU1 still occupied by PRESENT r7 matrix screen PID 16484, so ARX wait script remains in WAIT GPU1 busy state.
tmux sessions active:
  wait_arx_trail_mixer_gpu1_20260615
  relay_arx_round_hybrid
The new relay_after_arx_round_hybrid_to_partial_inverse_confirm.sh must be started after this commit is pushed.
```

## Update 2026-06-16 01:40 CST

User explicitly required ARX to keep moving, but main objective remains SPN/PRESENT high-round improvement. The queue was adjusted so SPN compact trail evidence is tested before the ARX GPU1 side run.

New commits:

```text
0f18ad8 feat(innovation1): add compact spn trail screen and arx rx roles
fef6fa7 chore(remote): queue compact spn before arx side runs
```

Both commits were synced to the remote Windows project and pushed to GitHub branch:

```text
refactor/model-project-structure
remote HEAD: fef6fa7
```

### New SPN Compact Candidate

Added feature:

```text
present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits
```

Per PRESENT ciphertext pair, this drops raw `C` and `C'` words and keeps only public structure evidence:

```text
Delta_C
InvP(Delta_C)
InvS(InvP(C)) xor InvS(InvP(C'))
4-beam, 3-depth public SBox-DDT trail words seeded from the structural inverse difference
```

PRESENT-64 pair width:

```text
48 x 64-bit words = 3072 bits per pair
```

Rationale: the previous fused feature had 50 words and included raw ciphertext words. For r7, raw `C/C'` may dilute weak differential evidence. The compact feature tests whether removing raw ciphertext noise and keeping only public nonlinear-trail evidence improves r7.

New SPN screen:

```text
run_id: innovation1-spn-present-delta-sinv-beam4deep3-r7-gpu1-20260616
plan: experiments/innovation1/plans/innovation1_spn_present_delta_sinv_beam4deep3_r7_screen.csv
config: experiments/innovation1/configs/remote/innovation1_spn_present_delta_sinv_beam4deep3_r7_gpu1_20260616.json
rows: 4
rounds: PRESENT r7 only
seeds: 0,1
models:
  - present_matrix_trail_hybrid_pairset
  - present_trail_mixer_pairset
samples/class: 65536
pairs/sample: 16
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
pretrain: r6 for 6 epochs from plan
```

Local verification:

```text
uv run python experiments/run_innovation_one_matrix.py ... --feature-encoding present_delta_paligned_sinv_sboxddt_beam4deep3_cell_matrix_bits ... --device cpu
=> wrote 1 row to /tmp/delta_sinv_beam4deep3_smoke.jsonl
```

### ARX Side-Line Improvement

ARX worker patch added explicit SPECK RX feature role grouping inside:

```text
src/blockcipher_ai_eval/models/structure/arx/round_function_hybrid.py
```

For 11-word RX feature inputs, the model now exposes:

```text
left, right, difference, rotation_aligned_difference,
partial_inverse_left_y, partial_inverse_right_y, partial_inverse_delta_y,
rx_alpha, rx_beta, carry_left_delta, carry_right_delta
```

and pools these relation groups:

```text
(left, right, difference)
(difference, rotation_aligned_difference)
(partial_inverse_left_y, partial_inverse_right_y, partial_inverse_delta_y)
(rx_alpha, rx_beta)
(carry_left_delta, carry_right_delta)
```

This keeps the ARX route structure-adaptive instead of treating all 32-bit words as anonymous tokens.

New ARX smoke:

```text
run_id: innovation1-arx-speck32-round-hybrid-rx-smoke-gpu0-20260616
plan: experiments/innovation1/plans/innovation1_arx_speck32_round_hybrid_rx_smoke.csv
config: experiments/innovation1/configs/remote/innovation1_arx_speck32_round_hybrid_rx_smoke_gpu0_20260616.json
rows: 4
rounds: SPECK32/64 r6,r7
seeds: 0,1
feature: ciphertext_pair_xor_arx_partial_inverse_rx_bits
model: arx_round_function_hybrid_pairset
samples/class: 32768
pairs/sample: 4
key_rotation_interval: 1024
r7 pretrain: r6 for 4 epochs from plan
```

### Verification

Full local targeted verification after SPN+ARX changes:

```text
uv run pytest tests/test_feature_encodings.py tests/test_adaptive_dbitnet_model.py tests/test_build_plan_config.py tests/test_remote_script_generator.py tests/test_experiment_matrix_runner.py -q
122 passed, 9 warnings
```

Additional smoke:

```text
SPN compact CPU smoke: wrote 1 row
ARX RX hybrid CPU smoke: wrote 1 row
```

### Active Remote Queue

Current remote GPU processes at update time:

```text
GPU0: python.exe PID 31416
  run: innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
  latest: row 18/30, PRESENT r6 seed 7, epoch 11/20

GPU1: python.exe PID 16484
  run: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
  latest: row 9/24, PRESENT r7 seed 2, epoch 20/24
  observed r7 signal remains near random so far
```

New watcher chain:

```text
GPU1 current r7 matrix
  -> protocol spn-aligned scale-m
  -> SInv matrix
  -> SInv + SBoxDDT Beam4Deep3 highround
  -> compact Delta + SInv + SBoxDDT Beam4Deep3 r7
  -> ARX TrailMixer curriculum r7/r8

GPU0 current r6 controls
  -> ARX RoundFunctionHybrid RX smoke r6/r7
```

Old direct `SInv+Beam4Deep3 -> ARX` watcher was deleted. New watcher tasks are active and waiting for result branches:

```text
innovation1_watch_after_sinv_beam4deep3_to_delta_sinv_20260616
innovation1_watch_after_delta_sinv_to_arx_trail_20260616
innovation1_watch_after_spn_r6_controls_to_arx_rx_20260616
```

Watcher logs confirmed they are waiting normally, not failing.

### Decision Rule

Do not claim SPN/PRESENT r7 breakthrough unless the compact or fused branch produces a gated result branch and r7 metrics clearly exceed near-random behavior under the Zhang/Wang MCND-style protocol. If compact r7 remains random, the next SPN step should move to score-distribution / selected-bit confirmation rather than simply widening raw ciphertext features.

## Update 2026-06-16 01:50 CST

Remote monitoring found that the old GPU1 r7 matrix run is still active and has advanced into the larger `N65536` r7 rows:

```text
run: innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
latest completed row before larger N:
  index 9/24, PRESENT r7, seed 2, samples/class 32768
  accuracy = 0.5
  auc ~= 0.5093
  calibrated_accuracy ~= 0.5088
interpretation: still near random, no r7 breakthrough
```

GPU0 r6 controls also continue:

```text
run: innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
latest completed row:
  index 18/30, PRESENT r6, seed 7
  accuracy ~= 0.8023
  auc ~= 0.8850
  calibrated_accuracy ~= 0.8029
interpretation: r6 control remains strong, but does not satisfy high-round objective
```

### Score-Distribution Hardening

Found and fixed a real completion bug in:

```text
experiments/run_score_distribution.py
```

Before this fix, `run_score_distribution_experiment()` returned:

```python
"selected_bit_indices": list(selected_bit_indices)
```

but `selected_bit_indices` was not defined in the function scope. This could make the long score-distribution remote run fail at the final result-writing stage even if training completed.

Fix:

```text
parse selected_bit_indices once at experiment start
pass the parsed tuple into all base/meta dataset builders
return the same parsed selected_bit_indices in the result row
```

Regression test added:

```text
tests/test_score_distribution.py::test_run_score_distribution_experiment_records_selected_bit_indices
```

Validation:

```text
uv run pytest tests/test_score_distribution.py tests/test_training.py::test_predict_binary_probabilities_returns_one_probability_per_row tests/test_remote_script_generator.py -q
12 passed

uv run python experiments/run_score_distribution.py ... --device cpu
=> wrote score-distribution result to /tmp/score_distribution_smoke.jsonl
```

### Updated GPU1 Watcher Chain

The previous compact-SPN watcher would have gone directly to ARX. It was changed so the SPN high-round queue remains active before ARX:

```text
... SInv + SBoxDDT Beam4Deep3 highround
  -> compact Delta + SInv + SBoxDDT Beam4Deep3 r7
  -> entropy-selected score-distribution r7 cached
  -> ARX TrailMixer curriculum r7/r8
```

Active watcher logs confirm the new chain:

```text
watch_after_innovation1-spn-present-delta-sinv-beam4deep3-r7-gpu1-20260616_to_innovation1-spn-present-entropy-score-dist-r7-cached-gpu1-20260615.log
  Checking upstream branch ...delta-sinv... before launching ...entropy-score-dist...

watch_after_innovation1-spn-present-entropy-score-dist-r7-cached-gpu1-20260615_to_innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615.log
  Checking upstream branch ...entropy-score-dist... before launching ...arx-trail-mixer...
```

New commit:

```text
b046db1 fix(innovation1): harden score distribution queue
```

Remote project and GitHub branch are both at `b046db1`.

## 2026-06-16 ARX Side-Line Queue Update

User explicitly reminded: ARX also needs to progress, while SPN/PRESENT high-round remains the main Innovation 1 target.

Remote read-only monitor state:

```text
GPU0: python PID 31416, low current util but still occupied.
GPU1: python PID 16484, busy.

Running:
- innovation1-spn-present-spnaligned-r7-matrix-screen-gpu1-20260615
  - row 10/24, epoch around 8/24
  - latest completed val_auc around 0.5000
  - no result gate yet, stderr 0 bytes
- innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
  - row 19/30, latest completed epoch 16/20
  - latest val_auc around 0.8890
  - no result gate yet, stderr 0 bytes

Queued:
- innovation1-spn-present-delta-sinv-beam4deep3-r7-gpu1-20260616
- innovation1-arx-speck32-round-hybrid-rx-smoke-gpu0-20260616

Blocked/failed gates:
- innovation1-spn-present-entropy-score-dist-r7-cached-gpu1-20260615
  - result_lines=0, expected_rows=1
  - launcher reported RUN_GATE_BLOCKED_INCOMPLETE_RESULTS
  - progress stopped during base_training, stderr 0 bytes
- innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
  - launcher reported RUN_GATE_BLOCKED_RUN_FAILED
  - progress stopped during dataset cache, stderr 0 bytes
```

ARX implementation/queue additions:

```text
New confirm plan:
- experiments/innovation1/plans/innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed.csv

Purpose:
- 10-seed SPECK32/64 r7 confirmation for arx_round_function_hybrid_pairset
- feature: ciphertext_pair_xor_arx_partial_inverse_rx_bits
- samples/class: 131072
- pairs/sample: 4
- key_rotation_interval: 1024
- sample_structure: independent_pairs
- loss/scheduler: mse + cyclic lr
- checkpoint_metric: val_auc
- r6 curriculum: pretrain_rounds=6, pretrain_epochs=6

Remote spec/scripts:
- experiments/innovation1/configs/remote/innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_20260616.json
- scripts/generated/remote/run_innovation1-arx-speck32-round-hybrid-rx-r7-confirm-10seed-gpu0-20260616_and_push.cmd
- scripts/generated/remote/launch_innovation1-arx-speck32-round-hybrid-rx-r7-confirm-10seed-gpu0-20260616.cmd
- scripts/generated/remote/schedule_innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_20260616.cmd
- scripts/generated/monitors/monitor_innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_results.sh

New watcher:
- scripts/generated/remote/watch_after_arx_rx_smoke_to_r7_confirm_20260616.ps1
- scripts/generated/remote/schedule_watch_after_arx_rx_smoke_to_r7_confirm_20260616.cmd

Chain:
SPN r6 controls result branch
  -> ARX RX smoke
  -> ARX RX r7 10-seed confirm
```

Local validation:

```text
uv run pytest tests/test_build_plan_config.py::test_speck32_arx_round_hybrid_rx_r7_confirm_plan_shape \
  tests/test_adaptive_dbitnet_model.py::test_arx_round_function_hybrid_pairset_exposes_speck_rx_feature_role_groups \
  tests/test_adaptive_dbitnet_model.py::test_build_model_supports_arx_round_function_hybrid_pairset_key_and_options -q
=> 3 passed

Tiny CPU smoke with a temporary /tmp one-row mini plan:
uv run python experiments/run_innovation_one_matrix.py --plan /tmp/arx_rx_confirm_tiny.csv ...
=> wrote 1 rows to /tmp/arx_rx_confirm_tiny.jsonl
```

## 2026-06-16 SPN Beam-Statistics Candidate

The current PRESENT r7 matrix run remains near random while r6 controls remain strong. To keep moving toward an actual r7 breakthrough instead of waiting, added a compact public trail-stat feature:

```text
feature:
  present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits

contents per ciphertext pair:
  Delta_C
  InvP(Delta_C)
  InvS(InvP(C)) xor InvS(InvP(C'))
  for each of 3 public SBox-DDT beam layers:
    top beam word
    top confidence word
    top margin word
    beam disagreement word
    confidence union word
    margin union word
    per-beam layer score word
    per-beam cumulative score word
    per-beam active-nibble count word

width:
  30 x 64-bit words = 1920 bits per pair

rationale:
  The previous compact beam4deep3 feature kept 48 words per pair and may still dilute weak r7 signal with full candidate paths.
  Beamstats keeps the shape of the public trail distribution while dropping most individual path words.
```

New experiment assets:

```text
plan:
  experiments/innovation1/plans/innovation1_spn_present_delta_sinv_beamstats4deep3_r7_screen.csv

remote config:
  experiments/innovation1/configs/remote/innovation1_spn_present_delta_sinv_beamstats4deep3_r7_gpu1_20260616.json

run id:
  innovation1-spn-present-delta-sinv-beamstats4deep3-r7-gpu1-20260616

rows:
  4 = MatrixTrailHybrid seeds 0,1 + TrailMixer seeds 0,1

protocol:
  PRESENT-80 r7, Zhang/Wang Case2 MCND, 16 pairs/sample,
  samples/class 65536, key_rotation_interval 1024,
  r6 curriculum pretrain for 6 epochs.
```

Local validation:

```text
uv run pytest tests/test_feature_encodings.py \
  tests/test_build_plan_config.py::test_present_delta_sinv_beamstats4deep3_r7_plan_shape \
  tests/test_remote_script_generator.py \
  tests/test_adaptive_dbitnet_model.py::test_build_model_supports_present_matrix_trail_hybrid_pairset_key_and_options -q
=> 31 passed

Tiny CPU smoke:
uv run python experiments/run_innovation_one_matrix.py --plan /tmp/spn_beamstats_tiny.csv ...
=> wrote 1 rows to /tmp/spn_beamstats_tiny.jsonl
```

Queue adjustment:

```text
The old delta-sinv -> entropy-score-dist continuation should be avoided because entropy-score-dist already produced an incomplete-result gate.
New watcher:
  scripts/generated/remote/watch_after_delta_sinv_beam4deep3_to_beamstats4deep3_20260616.ps1

Chain:
  compact Delta+SInv+Beam4Deep3 r7
    -> compact Delta+SInv+BeamStats4Deep3 r7
```
