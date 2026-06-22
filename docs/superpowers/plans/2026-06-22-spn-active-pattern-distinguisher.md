# SPN Active-Pattern Distinguisher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the high PRESENT/SPN active-nibble auxiliary signal into an explicit real-vs-random distinguisher route with diagnostics, baselines, and scale-gated remote experiments.

**Architecture:** Add a deterministic active-pattern evidence extractor for PRESENT beamstats/candidate-trail encodings, then train small active-only baselines before using larger neural models. Report active-label imbalance and real-vs-random separation separately from final accuracy so `active_nibble_bit_accuracy` cannot be misread as raw distinguisher accuracy.

**Tech Stack:** Python, NumPy, PyTorch existing experiment runner patterns, `uv run pytest`, Innovation 1 CSV plan/config flow, remote Windows GPU under `G:\lxy`.

---

## Research Rules

- `active nibble` means a 4-bit differential or candidate-trail cell is non-zero.
- It does not mean the ciphertext nibble value is non-zero.
- `active_nibble_bit_accuracy` is averaged over `rows * 16` binary active/inactive position labels; it is not real-vs-random accuracy and not whole-sample trail accuracy.
- Strict negative samples must use `negative_mode=encrypted_random_plaintexts`.
- `8k`, `16k`, `32k`, and `65k/class` runs are smoke/screen/medium diagnostics only.
- Do not claim formal SPN/PRESENT failure or breakthrough before completed, retrieved, plan-aligned `>=1000000/class` multi-seed evidence.

## File Structure

- Create `src/blockcipher_ai_eval/features/spn_active_pattern.py`
  - Decode bit rows for PRESENT pair-set encodings into 64-bit words.
  - Extract active-position masks, active counts, candidate disagreement summaries, confidence summaries, margin summaries, and pair-set consistency features.
  - Keep this file independent from experiment runners so tests can call it directly.
- Create `tests/test_spn_active_pattern.py`
  - Verify active mask semantics on hand-built 64-bit words.
  - Verify inactive-class baseline calculations.
  - Verify feature vector shape for the existing `present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits` layout.
- Create `experiments/innovation1/run_spn_active_pattern_baseline.py`
  - Generate train/validation datasets with existing `DifferentialDatasetConfig`.
  - Extract active-pattern evidence features.
  - Train deterministic baselines: logistic regression-style PyTorch linear head and small MLP.
  - Save JSONL rows with active diagnostics and real-vs-random metrics.
- Create `experiments/innovation1/summarize_spn_active_pattern.py`
  - Summarize per-seed metrics, active imbalance, all-inactive baseline, active precision/recall/F1, accuracy, calibrated accuracy, and AUC.
- Create `experiments/innovation1/plans/innovation1_spn_present_active_pattern_r7_screen.csv`
  - Include active-only and active-plus-candidate-statistics rows.
  - Use r7, `samples_per_class=65536`, `pairs_per_sample=16`, `negative_mode=encrypted_random_plaintexts`, `sample_structure=zhang_wang_case2_mcnd`.
- Create `experiments/innovation1/configs/remote/innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622.json`
  - Remote run config under `G:\lxy`.
  - Generated schedule commands must use `cmd.exe /c`.

## Task 1: Active-Pattern Feature Extractor

**Files:**
- Create: `src/blockcipher_ai_eval/features/spn_active_pattern.py`
- Test: `tests/test_spn_active_pattern.py`

- [ ] **Step 1: Write tests for basic active semantics**

Add this to `tests/test_spn_active_pattern.py`:

```python
import numpy as np

from blockcipher_ai_eval.features.spn_active_pattern import (
    active_mask16_from_word,
    active_pattern_summary_from_words,
)


def test_active_mask16_from_word_marks_nonzero_nibbles_only():
    word = 0x0000000000F0000A

    mask = active_mask16_from_word(word)

    assert mask.dtype == np.uint8
    assert mask.shape == (16,)
    assert mask.tolist() == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def test_active_pattern_summary_from_words_counts_positions_and_density():
    words = np.array(
        [
            [0x000000000000000F, 0x00000000000000F0],
            [0x0000000000000000, 0x0000000000000F00],
        ],
        dtype=np.uint64,
    )

    summary = active_pattern_summary_from_words(words)

    assert summary["active_masks"].shape == (2, 2, 16)
    assert summary["active_count"].tolist() == [[1, 1], [0, 1]]
    assert summary["position_frequency"].shape == (2, 16)
    assert summary["position_frequency"][0, :3].tolist() == [0.5, 0.5, 0.0]
    assert summary["density_mean"].tolist() == [0.0625, 0.03125]
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py -q
```

Expected: FAIL because `blockcipher_ai_eval.features.spn_active_pattern` does not exist yet.

- [ ] **Step 3: Implement the active semantics**

Create `src/blockcipher_ai_eval/features/spn_active_pattern.py`:

```python
from __future__ import annotations

from typing import TypedDict

import numpy as np
from numpy.typing import NDArray


class ActivePatternSummary(TypedDict):
    active_masks: NDArray[np.uint8]
    active_count: NDArray[np.uint8]
    position_frequency: NDArray[np.float32]
    density_mean: NDArray[np.float32]
    density_std: NDArray[np.float32]
    density_span: NDArray[np.float32]


def active_mask16_from_word(word: int) -> NDArray[np.uint8]:
    mask = np.zeros(16, dtype=np.uint8)
    for nibble_index in range(16):
        mask[nibble_index] = 1 if ((int(word) >> (4 * nibble_index)) & 0xF) != 0 else 0
    return mask


def active_masks16_from_words(words: NDArray[np.uint64]) -> NDArray[np.uint8]:
    flat = np.asarray(words, dtype=np.uint64).reshape(-1)
    masks = np.stack([active_mask16_from_word(int(word)) for word in flat], axis=0)
    return masks.reshape(*words.shape, 16)


def active_pattern_summary_from_words(words: NDArray[np.uint64]) -> ActivePatternSummary:
    word_array = np.asarray(words, dtype=np.uint64)
    if word_array.ndim != 2:
        raise ValueError("words must have shape (rows, words_per_row)")
    active_masks = active_masks16_from_words(word_array)
    active_count = active_masks.sum(axis=-1).astype(np.uint8)
    density = active_count.astype(np.float32) / 16.0
    return {
        "active_masks": active_masks,
        "active_count": active_count,
        "position_frequency": active_masks.mean(axis=1, dtype=np.float32),
        "density_mean": density.mean(axis=1, dtype=np.float32),
        "density_std": density.std(axis=1, dtype=np.float32),
        "density_span": (density.max(axis=1) - density.min(axis=1)).astype(np.float32),
    }
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/blockcipher_ai_eval/features/spn_active_pattern.py tests/test_spn_active_pattern.py
git commit -m "feat(spn): add active pattern feature extraction"
```

## Task 2: Decode PRESENT Cell-Matrix Rows

**Files:**
- Modify: `src/blockcipher_ai_eval/features/spn_active_pattern.py`
- Modify: `tests/test_spn_active_pattern.py`

- [ ] **Step 1: Add tests for bit-row decoding and feature shape**

Append to `tests/test_spn_active_pattern.py`:

```python
from blockcipher_ai_eval.features.spn_active_pattern import (
    extract_active_pattern_features,
    uint64_words_from_bit_rows,
)


def test_uint64_words_from_bit_rows_round_trips_big_endian_words():
    rows = np.array(
        [
            [int(bit) for bit in f"{0x8000000000000001:064b}{0x00000000000000F0:064b}"],
        ],
        dtype=np.uint8,
    )

    words = uint64_words_from_bit_rows(rows, words_per_row=2)

    assert words.shape == (1, 2)
    assert words[0, 0] == 0x8000000000000001
    assert words[0, 1] == 0x00000000000000F0


def test_extract_active_pattern_features_has_stable_shape():
    rows = np.zeros((3, 4 * 64), dtype=np.uint8)
    rows[0, 63] = 1
    rows[0, 127] = 1
    rows[1, 60:64] = 1

    features = extract_active_pattern_features(rows, words_per_row=4)

    assert features.shape == (3, 16 + 4 + 4)
    assert features.dtype == np.float32
    assert features[0, 0] > 0.0
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py -q
```

Expected: FAIL because row decoding helpers do not exist.

- [ ] **Step 3: Implement row decoding and compact features**

Add to `src/blockcipher_ai_eval/features/spn_active_pattern.py`:

```python
def uint64_words_from_bit_rows(bit_rows: NDArray[np.uint8], *, words_per_row: int) -> NDArray[np.uint64]:
    rows = np.asarray(bit_rows, dtype=np.uint8)
    if rows.ndim != 2:
        raise ValueError("bit_rows must have shape (rows, bits)")
    expected_bits = words_per_row * 64
    if rows.shape[1] != expected_bits:
        raise ValueError(f"expected {expected_bits} bits, got {rows.shape[1]}")
    reshaped = rows.reshape(rows.shape[0], words_per_row, 64)
    powers = (1 << np.arange(63, -1, -1, dtype=np.uint64)).reshape(1, 1, 64)
    return (reshaped.astype(np.uint64) * powers).sum(axis=2, dtype=np.uint64)


def extract_active_pattern_features(bit_rows: NDArray[np.uint8], *, words_per_row: int) -> NDArray[np.float32]:
    words = uint64_words_from_bit_rows(bit_rows, words_per_row=words_per_row)
    summary = active_pattern_summary_from_words(words)
    active_count = summary["active_count"].astype(np.float32)
    count_mean = active_count.mean(axis=1, keepdims=True) / 16.0
    count_std = active_count.std(axis=1, keepdims=True) / 16.0
    count_min = active_count.min(axis=1, keepdims=True) / 16.0
    count_max = active_count.max(axis=1, keepdims=True) / 16.0
    density_stats = np.stack(
        [
            summary["density_mean"],
            summary["density_std"],
            summary["density_span"],
            summary["position_frequency"].std(axis=1, dtype=np.float32),
        ],
        axis=1,
    )
    return np.concatenate(
        [
            summary["position_frequency"].astype(np.float32),
            np.concatenate([count_mean, count_std, count_min, count_max], axis=1).astype(np.float32),
            density_stats.astype(np.float32),
        ],
        axis=1,
    )
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/blockcipher_ai_eval/features/spn_active_pattern.py tests/test_spn_active_pattern.py
git commit -m "feat(spn): decode active pattern rows"
```

## Task 3: Active Imbalance Diagnostics

**Files:**
- Modify: `src/blockcipher_ai_eval/features/spn_active_pattern.py`
- Modify: `tests/test_spn_active_pattern.py`

- [ ] **Step 1: Add diagnostics tests**

Append to `tests/test_spn_active_pattern.py`:

```python
from blockcipher_ai_eval.features.spn_active_pattern import active_label_diagnostics


def test_active_label_diagnostics_reports_all_inactive_baseline():
    labels = np.array(
        [
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
        ],
        dtype=np.uint8,
    )

    metrics = active_label_diagnostics(labels)

    assert metrics["active_positive_rate"] == 2 / 12
    assert metrics["all_inactive_accuracy"] == 10 / 12
    assert metrics["positions"] == 4
```

- [ ] **Step 2: Run tests and verify they fail**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py -q
```

Expected: FAIL because diagnostics helper does not exist.

- [ ] **Step 3: Implement diagnostics**

Add to `src/blockcipher_ai_eval/features/spn_active_pattern.py`:

```python
def active_label_diagnostics(labels: NDArray[np.uint8]) -> dict[str, float | int]:
    label_array = np.asarray(labels, dtype=np.uint8)
    if label_array.ndim != 2:
        raise ValueError("labels must have shape (rows, positions)")
    total = int(label_array.size)
    positives = int(label_array.sum())
    negatives = total - positives
    return {
        "rows": int(label_array.shape[0]),
        "positions": int(label_array.shape[1]),
        "active_positive_rate": positives / total if total else 0.0,
        "inactive_negative_rate": negatives / total if total else 0.0,
        "all_inactive_accuracy": negatives / total if total else 0.0,
        "mean_active_per_row": float(label_array.sum(axis=1).mean()) if label_array.shape[0] else 0.0,
    }
```

- [ ] **Step 4: Run tests and verify they pass**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

Run:

```bash
git add src/blockcipher_ai_eval/features/spn_active_pattern.py tests/test_spn_active_pattern.py
git commit -m "feat(spn): add active label diagnostics"
```

## Task 4: Local Active-Only Baseline Runner

**Files:**
- Create: `experiments/innovation1/run_spn_active_pattern_baseline.py`
- Create: `tests/test_spn_active_pattern_baseline_cli.py`

- [ ] **Step 1: Add CLI smoke test**

Create `tests/test_spn_active_pattern_baseline_cli.py`:

```python
import runpy
import sys


def test_spn_active_pattern_baseline_help_runs(capsys):
    sys.argv = ["run_spn_active_pattern_baseline.py", "--help"]
    try:
        runpy.run_path("experiments/innovation1/run_spn_active_pattern_baseline.py", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "--samples-per-class" in captured.out
    assert "--feature-encoding" in captured.out
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```bash
uv run pytest tests/test_spn_active_pattern_baseline_cli.py -q
```

Expected: FAIL because the script does not exist.

- [ ] **Step 3: Implement CLI skeleton with dataset generation**

Create `experiments/innovation1/run_spn_active_pattern_baseline.py`:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, roc_auc_score

from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.experiments.factories import build_cipher
from blockcipher_ai_eval.features.pair_features import pair_bits_for_encoding
from blockcipher_ai_eval.features.spn_active_pattern import extract_active_pattern_features


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=7)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--samples-per-class", type=int, default=4096)
    parser.add_argument("--pairs-per-sample", type=int, default=16)
    parser.add_argument("--feature-encoding", default="present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits")
    parser.add_argument("--negative-mode", default="encrypted_random_plaintexts")
    parser.add_argument("--sample-structure", default="zhang_wang_case2_mcnd")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--learning-rate", type=float, default=1e-2)
    return parser.parse_args()


def train_linear(features: np.ndarray, labels: np.ndarray, *, epochs: int, learning_rate: float) -> torch.nn.Module:
    torch.manual_seed(0)
    x = torch.from_numpy(features.astype(np.float32))
    y = torch.from_numpy(labels.astype(np.float32)).reshape(-1, 1)
    model = torch.nn.Linear(features.shape[1], 1)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    for _epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(x), y)
        loss.backward()
        optimizer.step()
    return model


def main() -> None:
    args = parse_args()
    cipher = build_cipher("present80", args.rounds)
    train_config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0000000000000040,
        samples_per_class=args.samples_per_class,
        seed=args.seed,
        feature_encoding=args.feature_encoding,
        pairs_per_sample=args.pairs_per_sample,
        negative_mode=args.negative_mode,
        sample_structure=args.sample_structure,
    )
    val_config = DifferentialDatasetConfig(
        cipher=cipher,
        input_difference=0x0000000000000040,
        samples_per_class=max(1024, args.samples_per_class // 4),
        seed=args.seed + 1000,
        feature_encoding=args.feature_encoding,
        pairs_per_sample=args.pairs_per_sample,
        negative_mode=args.negative_mode,
        sample_structure=args.sample_structure,
    )
    train_dataset = make_differential_dataset(train_config)
    val_dataset = make_differential_dataset(val_config)
    pair_bits = pair_bits_for_encoding(cipher.block_bits, args.feature_encoding)
    words_per_row = train_dataset.features.shape[1] // 64
    if pair_bits * args.pairs_per_sample != train_dataset.features.shape[1]:
        raise ValueError("dataset feature width does not match pair_bits * pairs_per_sample")
    train_x = extract_active_pattern_features(train_dataset.features, words_per_row=words_per_row)
    val_x = extract_active_pattern_features(val_dataset.features, words_per_row=words_per_row)
    model = train_linear(train_x, train_dataset.labels, epochs=args.epochs, learning_rate=args.learning_rate)
    with torch.no_grad():
        logits = model(torch.from_numpy(val_x.astype(np.float32))).numpy().reshape(-1)
    probs = 1.0 / (1.0 + np.exp(-logits))
    preds = (probs >= 0.5).astype(np.uint8)
    result = {
        "route": "spn_active_pattern_baseline",
        "rounds": args.rounds,
        "seed": args.seed,
        "samples_per_class": args.samples_per_class,
        "pairs_per_sample": args.pairs_per_sample,
        "feature_encoding": args.feature_encoding,
        "negative_mode": args.negative_mode,
        "sample_structure": args.sample_structure,
        "feature_dim": int(train_x.shape[1]),
        "val_accuracy": float(accuracy_score(val_dataset.labels, preds)),
        "val_auc": float(roc_auc_score(val_dataset.labels, probs)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run CLI tests**

Run:

```bash
uv run pytest tests/test_spn_active_pattern_baseline_cli.py tests/test_spn_active_pattern.py -q
```

Expected: PASS.

- [ ] **Step 5: Run a tiny local smoke**

Run:

```bash
uv run python experiments/innovation1/run_spn_active_pattern_baseline.py --output /tmp/spn_active_pattern_smoke.jsonl --samples-per-class 64 --epochs 2
```

Expected: `/tmp/spn_active_pattern_smoke.jsonl` exists and contains `val_accuracy` and `val_auc`.

- [ ] **Step 6: Commit**

Run:

```bash
git add experiments/innovation1/run_spn_active_pattern_baseline.py tests/test_spn_active_pattern_baseline_cli.py
git commit -m "feat(experiment): add spn active pattern baseline"
```

## Task 5: Summary Script And Screen Plan

**Files:**
- Create: `experiments/innovation1/summarize_spn_active_pattern.py`
- Create: `experiments/innovation1/plans/innovation1_spn_present_active_pattern_r7_screen.csv`
- Test: `tests/test_spn_active_pattern_summary.py`

- [ ] **Step 1: Add summary test**

Create `tests/test_spn_active_pattern_summary.py`:

```python
import json
import runpy
import sys
from pathlib import Path


def test_summarize_spn_active_pattern_writes_mean_metrics(tmp_path, capsys):
    result = tmp_path / "result.jsonl"
    result.write_text(
        json.dumps({"val_accuracy": 0.6, "val_auc": 0.7, "feature_dim": 24}) + "\n"
        + json.dumps({"val_accuracy": 0.8, "val_auc": 0.9, "feature_dim": 24}) + "\n",
        encoding="utf-8",
    )
    sys.argv = ["summarize_spn_active_pattern.py", str(result)]

    runpy.run_path("experiments/innovation1/summarize_spn_active_pattern.py", run_name="__main__")

    captured = capsys.readouterr()
    assert "mean_accuracy=0.700000" in captured.out
    assert "mean_auc=0.800000" in captured.out
```

- [ ] **Step 2: Run test and verify it fails**

Run:

```bash
uv run pytest tests/test_spn_active_pattern_summary.py -q
```

Expected: FAIL because summary script does not exist.

- [ ] **Step 3: Implement summary script**

Create `experiments/innovation1/summarize_spn_active_pattern.py`:

```python
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_spn_active_pattern.py RESULT_JSONL")
    path = Path(sys.argv[1])
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise SystemExit("no result rows")
    accuracies = [float(row["val_accuracy"]) for row in rows]
    aucs = [float(row["val_auc"]) for row in rows]
    print(f"rows={len(rows)}")
    print(f"mean_accuracy={statistics.fmean(accuracies):.6f}")
    print(f"mean_auc={statistics.fmean(aucs):.6f}")
    print(f"feature_dim={rows[0].get('feature_dim')}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create screen CSV**

Create `experiments/innovation1/plans/innovation1_spn_present_active_pattern_r7_screen.csv`:

```csv
cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,key_rotation_interval,sample_structure,integral_active_nibble,difference_profile,difference_member,loss,learning_rate,optimizer,weight_decay,lr_scheduler,max_learning_rate,checkpoint_metric,restore_best_checkpoint,early_stopping_patience,early_stopping_min_delta,pretrain_rounds,pretrain_epochs,model_options,evidence,literature
PRESENT-80,SPN,PRESENT-ActivePatternLinear-r7-screen,spn_active_pattern_linear,present_active_pattern_distinguisher,0,150,7,0,65536,16,present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits,encrypted_random_plaintexts,0x00000000000000000000,0xffffffffffffffffffff,1024,zhang_wang_case2_mcnd,0,present_zhang_wang2022_mcnd,0,bce,0.01,adam,0,none,0,val_auc,true,0,0.0,0,0,"{""baseline"":""linear"",""feature_family"":""active_pattern""}",PRESENT r7 active-pattern real-vs-random screen using active count position frequency and density consistency extracted from public Delta+InvP+InvS SBox-DDT beamstats8/deep4 evidence,Zhang/Wang 2022 PRESENT MCND; public InvP+InvS structural inverse; public SBox-DDT beam statistics; Innovation 1 SPN active-pattern consistency distinguisher
PRESENT-80,SPN,PRESENT-ActivePatternMLP-r7-screen,spn_active_pattern_mlp,present_active_pattern_distinguisher,1,160,7,1,65536,16,present_delta_paligned_sinv_sboxddt_beamstats8deep4_cell_matrix_bits,encrypted_random_plaintexts,0x00000000000000000000,0xffffffffffffffffffff,1024,zhang_wang_case2_mcnd,0,present_zhang_wang2022_mcnd,0,bce,0.001,adam,1e-05,none,0,val_auc,true,0,0.0,0,0,"{""baseline"":""mlp"",""feature_family"":""active_pattern""}",PRESENT r7 active-pattern MLP screen to test whether active-nibble trail consistency separates strict encrypted-random-plaintext negatives before larger neural scaling,Zhang/Wang 2022 PRESENT MCND; public InvP+InvS structural inverse; public SBox-DDT beam statistics; Innovation 1 SPN active-pattern consistency distinguisher
```

- [ ] **Step 5: Run tests**

Run:

```bash
uv run pytest tests/test_spn_active_pattern_summary.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

Run:

```bash
git add experiments/innovation1/summarize_spn_active_pattern.py experiments/innovation1/plans/innovation1_spn_present_active_pattern_r7_screen.csv tests/test_spn_active_pattern_summary.py
git commit -m "experiment(spn): add active pattern screen plan"
```

## Task 6: Remote Launch Configuration

**Files:**
- Create: `experiments/innovation1/configs/remote/innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622.json`
- Modify or create generated remote script only through the existing remote-script generator if supported.

- [ ] **Step 1: Add remote config**

Create `experiments/innovation1/configs/remote/innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622.json`:

```json
{
  "run_id": "innovation1-spn-present-active-pattern-r7-screen-gpu0-20260622",
  "task_name": "innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622",
  "plan": "experiments\\innovation1\\plans\\innovation1_spn_present_active_pattern_r7_screen.csv",
  "gpu": 0,
  "project_root": "G:\\lxy\\blockcipher-structure-adaptive-nd",
  "run_root": "G:\\lxy\\blockcipher-structure-adaptive-nd-runs",
  "python_exe": "F:\\Anaconda\\envs\\DWT\\torch310\\python.exe",
  "command": "experiments\\innovation1\\run_spn_active_pattern_baseline.py",
  "summary_command": "experiments\\innovation1\\summarize_spn_active_pattern.py",
  "expected_rows": 2,
  "claim_scope": "SCREEN only: active-pattern route diagnostics for PRESENT r7 at 65536/class; not formal or breakthrough evidence",
  "launch_policy": "use pushed GitHub commit, strict encrypted-random-plaintext negatives, generated commands must use cmd.exe /c and store artifacts only under G:\\lxy"
}
```

- [ ] **Step 2: Verify remote-path safety**

Run:

```bash
rg -F "cmd.exe /k" experiments/innovation1/configs/remote/innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622.json scripts/generated/remote || true
rg -F "C:\\Users" experiments/innovation1/configs/remote/innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622.json || true
```

Expected: no project artifact paths outside `G:\lxy` and no `cmd.exe /k`.

- [ ] **Step 3: Run targeted tests**

Run:

```bash
uv run pytest tests/test_spn_active_pattern.py tests/test_spn_active_pattern_baseline_cli.py tests/test_spn_active_pattern_summary.py tests/test_remote_script_generator.py -q
```

Expected: PASS.

- [ ] **Step 4: Commit and push**

Run:

```bash
git add experiments/innovation1/configs/remote/innovation1_spn_present_active_pattern_r7_screen_gpu0_20260622.json
git commit -m "experiment(spn): configure active pattern remote screen"
git push
```

## Task 7: Execute Screen, Then Gate Scale-Up

**Files:**
- No code edits unless a verified bug appears.
- Generated result artifacts belong under `outputs/remote_results/` or `outputs/remote_results_incomplete/`.

- [ ] **Step 1: Launch only after clean pushed workspace**

Run:

```bash
git status --short --branch
```

Expected: clean branch with local HEAD pushed.

- [ ] **Step 2: Launch remote screen using existing remote workflow**

Use the remote Windows GPU skill rules:

- Remote alias: `lxy-a6000`.
- Remote project root: `G:\lxy\blockcipher-structure-adaptive-nd`.
- Run outputs: `G:\lxy\blockcipher-structure-adaptive-nd-runs`.
- Generated scripts and logs must stay under `G:\lxy`.
- Commands must use `cmd.exe /c`.

- [ ] **Step 3: Do not main-thread SSH-poll after launch**

Start or verify a local tmux monitor for result retrieval. After launch, report states separately:

- `running`
- `completed remotely`
- `fallback-retrieved`
- `retrieved from verified result branch`
- `plan-aligned`

- [ ] **Step 4: Gate decision**

Scale to `262144/class` only if at least one active-pattern baseline beats the simple global-stat control or shows clear distribution separation:

```text
val_auc >= 0.72
or
val_accuracy >= 0.66
or
active-only diagnostics show stable real-vs-random separation across two seeds
```

Scale to `>=1000000/class` only after completed, retrieved, plan-aligned `262144/class` evidence improves or matches the current best r7 cluster.

## Self-Review

- Spec coverage: The plan captures the user's idea: convert high active-nibble auxiliary accuracy into a direct real-vs-random route, while preserving Innovation 1 SPN structure focus.
- Placeholder scan: No TBD or open-ended "implement later" steps remain.
- Type consistency: Function names are defined before later use: `active_mask16_from_word`, `active_pattern_summary_from_words`, `uint64_words_from_bit_rows`, `extract_active_pattern_features`, and `active_label_diagnostics`.
- Evidence gates: The plan explicitly separates auxiliary accuracy, raw single-sample accuracy/AUC, and later multi-query/application evidence.
