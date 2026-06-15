# Innovation 1 PRESENT/SPN Results and Score-Distribution Push - 2026-06-15

Updated at 2026-06-15 17:23 CST.

## Completed Remote Result: SPN-Aligned Matrix Scale-S

Run id: `innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615`

Local retrieval path:

```text
outputs/remote_results/innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615
```

Gate:

```text
result_lines=9
expected_rows=9
```

Summary from `innovation1-spn-present-zw2022-matrix-spnaligned-scale-s-gpu1-20260615_summary.csv`:

| rounds | seeds | acc mean | AUC mean | interpretation |
| --- | ---: | ---: | ---: | --- |
| 6 | 3 | 0.8822021484 | 0.9518969798 | strong distinguisher signal |
| 7 | 3 | 0.5 | 0.5059904313 | essentially random; no useful r7 signal |
| 8 | 3 | 0.5 | 0.5037461811 | random; no r8 signal |

Conclusion: the current SPN-aligned matrix feature `C || C' || Delta || P^-1(Delta)` with Zhang/Wang-style MCND scaffold is strong at 6 rounds but does not reproduce/beat Zhang-Wang 7-round reported performance. Do not claim r7 breakthrough from this route. Use it as evidence of structure adaptation at r6 and as a negative boundary result for r7/r8.

## Remote Status at Update

- Raw matrix run `innovation1-spn-present-zw2022-matrix-scale-m-gpu0-20260615`: 7/9 rows earlier, process PID 37584 on GPU0.
- Score-distribution run `innovation1-spn-present-entropy-score-dist-r7-gpu1-20260615`: started, run dir exists, progress currently only has `run_start`; process PID 30876 was using CPU, stderr empty. It is likely generating the first base dataset in memory before writing `base_dataset_ready`.

## New Route Implemented

Commit `676ea73`: `feat(innovation1): add PRESENT score distribution experiment`
Commit `8e1954d`: `fix(remote): repair score distribution launch scripts`

Added:

- `experiments/run_score_distribution.py`
- `predict_binary_probabilities` in `src/blockcipher_ai_eval/training/binary.py`
- tests in `tests/test_score_distribution.py` and `tests/test_training.py`
- remote scripts for `innovation1-spn-present-entropy-score-dist-r7-gpu1-20260615`

Experiment idea: train a base weak single-pair entropy-selected PRESENT r7 scorer, then group probabilities into score-distribution features: sorted scores + mean/std/min/max/q25/q75. Train a second-stage MLP on these distribution features. This is intended to amplify weak high-round signal, unlike the SPN-aligned matrix route that directly failed at r7.

## Next Actions

1. Monitor score-distribution run. If it stays at only `run_start` too long, stop and patch `run_score_distribution.py` to generate base/meta datasets in chunked/progress-aware mode.
2. Pull raw matrix result when its gate reaches 9/9.
3. Compare final tables:
   - SPN-aligned matrix r6/r7/r8.
   - raw matrix r5/r6/r7.
   - entropy-selected score-distribution r7.
4. If score-distribution shows signal above random, scale to multiple seeds and possibly r8. If it is random, prioritize exact protocol reproduction/statistical delta-C entropy sanity checks.

## Update 2026-06-15 17:55 CST

Score-distribution remote run `innovation1-spn-present-entropy-score-dist-r7-gpu1-20260615` progressed beyond dataset generation into base training. Observed base-training validation AUC around `0.4993` at epoch 1 and `0.5003` at epoch 8, so the entropy-selected single-pair base scorer currently shows essentially random r7 signal under this protocol. This does not yet prove the two-stage score-distribution route is useless, but it makes it a high-risk amplification route because the first-stage scores may not carry enough information.

Implementation improvement made locally before restarting/scaling: `experiments/run_score_distribution.py` now supports `--dataset-cache-root` and `--dataset-cache-chunk-size`. Base train, base validation, meta train source, and meta validation source all go through a shared `_make_single_pair_dataset` helper. With cache enabled, data is generated in chunks with progress events and stored under `score_distribution/<cipher>/r<round>/<stage>/seed-<seed>`. This fixes the previous blind spot where large in-memory dataset generation had no progress and could not be reused.

Validation: `uv run pytest tests/test_score_distribution.py tests/test_training.py::test_predict_binary_probabilities_returns_one_probability_per_row -q` passed (`6 passed`).
