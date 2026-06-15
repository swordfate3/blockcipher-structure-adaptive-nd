# Innovation 1 SPN/ARX Stats-Hybrid Queue - 2026-06-16

## Scope

Innovation 1 is still structure-adaptive neural distinguishers. PRESENT/SPN
remains the pressure point for high-round improvement, but ARX/SPECK32 is being
advanced in parallel because the user explicitly asked that ARX also continue.

## SPN Update

Added `PresentPairSetStatsHybridDistinguisher`.

Files:

- `src/blockcipher_ai_eval/models/structure/spn/present_pairset_stats_hybrid.py`
- `experiments/innovation1/plans/innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_screen.csv`
- `experiments/innovation1/configs/remote/innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_gpu0_20260616.json`
- `scripts/generated/remote/watch_after_spn_parameterized_to_stats_hybrid_beamstats8deep4_20260616.ps1`

Purpose:

- Fuse PRESENT public DDT/InvP/InvS trail pair embeddings with explicit
  cross-pair nibble and word statistics.
- Target weak r7 signal that may not be visible in a single pair embedding.

Local verification:

```text
uv run pytest tests/test_adaptive_dbitnet_model.py::test_present_pairset_stats_hybrid_fuses_trail_and_cross_pair_statistics tests/test_adaptive_dbitnet_model.py::test_build_model_supports_present_pairset_stats_hybrid_key_and_options tests/test_build_plan_config.py::test_present_stats_hybrid_beamstats8deep4_r7_plan_shape tests/test_feature_encodings.py tests/test_remote_script_generator.py -q
37 passed, 2 warnings
```

Remote sync:

```text
local commit: 280dc18 experiment: add spn pairset stats hybrid screen
remote/GitHub equivalent: 03126cf on refactor/model-project-structure
```

Watcher:

```text
task: innovation1_watch_after_spn_parameterized_to_stats_hybrid_beamstats8deep4_20260616
waits for: results/innovation1-spn-present-parameterized-sboxddt-beam8deep4-r7-gpu0-20260616
then launches: innovation1-spn-present-stats-hybrid-beamstats8deep4-r7-gpu0-20260616
status at 2026-06-16 06:02:59 CST: upstream branch not ready; sleeping 600s
```

## ARX Update

Added `ArxPairSetStatsHybridDistinguisher`.

Files:

- `src/blockcipher_ai_eval/models/structure/arx/pairset_stats_hybrid.py`
- `experiments/innovation1/plans/innovation1_arx_speck32_stats_hybrid_r7_screen.csv`
- `experiments/innovation1/configs/remote/innovation1_arx_speck32_stats_hybrid_r7_screen_gpu1_20260616.json`
- `scripts/generated/remote/watch_after_arx_r8_boundary_to_stats_hybrid_20260616.ps1`

Purpose:

- Keep the current strongest ARX feature line:
  `ciphertext_pair_xor_arx_partial_inverse_bits`.
- Reuse SPECK word/rotation/carry word-mixer pair encoder.
- Add cross-pair 16-bit half-word and 32-bit feature-word statistics:
  mean, variance, max, min, first-last pair delta, word edge, rotation vs
  partial-inverse density contrast, and word density delta.

Experiment:

```text
run_id: innovation1-arx-speck32-stats-hybrid-r7-screen-gpu1-20260616
plan: experiments/innovation1/plans/innovation1_arx_speck32_stats_hybrid_r7_screen.csv
rows: 4
models: structure_adaptive_pairset_dbitnet control and arx_pairset_stats_hybrid
round: SPECK32/64 r7
seeds: 0,1
samples_per_class: 131072
pairs_per_sample: 4
feature: ciphertext_pair_xor_arx_partial_inverse_bits
key_rotation_interval: 1024
sample_structure: independent_pairs
pretrain: r6 for 4 epochs from plan
```

Local verification:

```text
uv run pytest tests/test_adaptive_dbitnet_model.py::test_arx_pairset_stats_hybrid_fuses_word_mixing_and_cross_pair_statistics tests/test_adaptive_dbitnet_model.py::test_build_model_supports_arx_pairset_stats_hybrid_key_and_options tests/test_build_plan_config.py::test_speck32_arx_stats_hybrid_r7_screen_plan_shape tests/test_remote_script_generator.py -q
9 passed

uv run python experiments/run_innovation_one_matrix.py --ciphers speck32 --models arx_pairset_stats_hybrid --rounds 2 --seeds 0 --samples-per-class 8 --pairs-per-sample 2 --feature-encoding ciphertext_pair_xor_arx_partial_inverse_bits --negative-mode encrypted_random_plaintexts --difference-profile speck32_gohr2019 --key-rotation-interval 4 --sample-structure independent_pairs --epochs 1 --batch-size 4 --hidden-bits 4 --checkpoint-metric val_auc --output /tmp/arx_stats_hybrid_smoke.jsonl
wrote 1 rows
```

Remote sync:

```text
local commit: 5937669 experiment: add arx pairset stats hybrid screen
remote/GitHub equivalent: 3d5775a on refactor/model-project-structure
```

Watcher:

```text
task: innovation1_watch_after_arx_r8_boundary_to_stats_hybrid_20260616
waits for: results/innovation1-arx-speck32-partial-inverse-r8-boundary-10seed-gpu1-20260616
then launches: innovation1-arx-speck32-stats-hybrid-r7-screen-gpu1-20260616
started: 2026-06-16 06:10 CST
```

## Remote State Snapshot

At 2026-06-16 06:10 CST, remote GPU processes still included:

```text
31416: innovation1-spn-present-spnaligned-r6-controls-10seed-gpu0-20260615
44896: innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615
44756: innovation1-spn-present-protocol-spnaligned-scale-m-gpu1-20260616
```

Subagent monitoring at about 06:03 CST reported:

```text
spn r6 controls: 28/30 rows, progress updating
arx trail mixer curriculum: 2 rows, entered r8 dataset cache, progress updating
spn protocol scale-m: 4 rows, progress updating
```

No high-round breakthrough should be claimed yet. These changes only expand the
queue with structure-aligned statistical models and keep remote experiments
moving behind result-gated watchers.
