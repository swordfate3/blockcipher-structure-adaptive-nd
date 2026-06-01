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
  --models mlp cnn resnet_bitslice dbitnet_dilated_cnn lstm_roundseq transformer_encoder \
  --rounds 1 2 \
  --seeds 0 \
  --samples-per-class 64 \
  --epochs 2 \
  --batch-size 32 \
  --hidden-bits 16 \
  --feature-encoding ciphertext_pair_xor_bits \
  --output outputs/innovation_one_matrix_smoke.jsonl
```

Summarize JSONL results into a CSV table:

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/innovation_one_matrix_smoke.jsonl \
  --output outputs/innovation_one_matrix_smoke_summary.csv
```

The matrix runner currently supports `mlp`, `cnn`, `resnet_bitslice`,
`dbitnet_dilated_cnn`, `lstm_roundseq`, and `transformer_encoder`.

Build a literature-ranked experiment plan before running paper-scale jobs:

```bash
uv run python experiments/build_innovation_one_matrix.py \
  --top-k 2 \
  --rounds 3 4 5 \
  --seeds 0 1 2 \
  --samples-per-class 1048576 \
  --output outputs/innovation_one_literature_ranked_matrix.csv
```

The ranked CSV records the cipher structure, recommended architecture,
experiment `model_key`, matching score, evidence text, supporting literature,
and the literature-backed input-difference profile used by the runner.

Literature-backed input differences can also be selected explicitly:

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models resnet_bitslice cnn dbitnet_dilated_cnn \
  --rounds 5 6 7 \
  --seeds 0 1 \
  --samples-per-class 8192 \
  --epochs 8 \
  --batch-size 512 \
  --hidden-bits 64 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_speck_gohr_profile_screen.jsonl
```

Current curated profiles:

- `speck32_gohr2019`: Gohr 2019 SPECK32/64 input difference `0x0040/0000`,
  encoded as `0x00400000` for this repository's `(x, y)` word layout.
- `present_wang_jain2021`: four PRESENT differences reported through the
  Wang/Jain/Kohli/Mishra line; select one with `--difference-member 0..3`.
- `sm4_yu2023_conv_resnet`: Yu/Wu/Zhang 2023 SM4 difference
  `(0, 0, 0, 1)`.
- `sm4_li_sun_2025_19r_family`: recorded as a constrained differential
  family for documentation; it is not used as a fixed neural input difference
  until constrained sampling is implemented.

Run the literature-ranked plan directly:

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --plan outputs/innovation_one_literature_ranked_matrix.csv \
  --epochs 5 \
  --batch-size 256 \
  --hidden-bits 64 \
  --feature-encoding ciphertext_pair_xor_bits \
  --output outputs/innovation_one_literature_ranked_results.jsonl
```

Summarize the planned experiment while keeping architecture rank and literature
metadata:

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/innovation_one_literature_ranked_results.jsonl \
  --output outputs/innovation_one_literature_ranked_summary.csv
```

Supported feature encodings:

- `ciphertext_pair_bits`: concatenate `C || C'`.
- `ciphertext_pair_xor_bits`: concatenate `C || C' || (C xor C')`.

The summary CSV reports both fixed-threshold metrics and calibrated metrics
(`calibrated_accuracy`, `calibrated_advantage`) because neural distinguishers
often learn a useful ranking before their probability threshold is calibrated.
It also keeps `difference_profile`, `difference_member`, and
`difference_source` so ablation rows remain traceable to the literature setting.
