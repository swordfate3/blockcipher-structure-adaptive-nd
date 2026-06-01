# Block Cipher AI Evaluation

Structure-aware neural distinguisher experiments for block ciphers.

## Environment

Use `uv` to create and manage the virtual environment:

```bash
uv sync
uv run pytest -q
```

The project uses PyTorch for neural models and NumPy for dataset generation.

## Innovation One Smoke Experiment

Run a small SPECK32/64 neural distinguisher experiment:

```bash
uv run python experiments/run_innovation_one_smoke.py \
  --cipher speck32 \
  --rounds 2 \
  --samples-per-class 256 \
  --epochs 3 \
  --batch-size 64 \
  --hidden-bits 64 \
  --output outputs/innovation_one_speck32_round2_mlp_smoke.json
```

The JSON output records the cipher structure, model, training history, accuracy,
AUC, advantage, and loss. This is a smoke experiment for checking the pipeline,
not a paper-scale result.

Run a small structure/model matrix over SPECK32/64, PRESENT-80, and SM4:

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 present80 sm4 \
  --models mlp cnn \
  --rounds 1 2 \
  --seeds 0 \
  --samples-per-class 64 \
  --epochs 2 \
  --batch-size 32 \
  --hidden-bits 16 \
  --output outputs/innovation_one_matrix_smoke.jsonl
```

Summarize JSONL results into a CSV table:

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/innovation_one_matrix_smoke.jsonl \
  --output outputs/innovation_one_matrix_smoke_summary.csv
```

The matrix runner currently supports `mlp` and `cnn`. These are early baselines
for validating the experiment protocol before adding ResNet-BitSlice and DBitNet.
