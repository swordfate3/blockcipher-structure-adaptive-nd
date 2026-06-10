# Project Structure Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the repository toward the approved research-grade project structure while preserving existing experiment commands, model keys, and remote result compatibility.

**Architecture:** Implement the redesign in small compatibility-preserving phases. Canonical modules move into `data/`, `models/structure/*`, `evaluation/`, and grouped experiment asset folders, while old public import paths remain shims until all active thesis experiments stabilize.

**Tech Stack:** Python 3.10, PyTorch, NumPy memmap datasets, pytest, uv, GitHub-synced remote Windows GPU experiment scripts.

---

## File Structure Map

### Already Completed Baseline on Branch

- `src/blockcipher_ai_eval/models/structure/arx/pairset_dbitnet.py`: ARX-specific wrapper for the structure-adaptive pair-set DBitNet.
- `src/blockcipher_ai_eval/models/README.md`: canonical model layout and compatibility shim policy.
- `src/blockcipher_ai_eval/models/registry.py`: model key aliases for ARX-specific entry points.
- `src/blockcipher_ai_eval/experiments/factories.py`: factory support for ARX-specific model keys.

### Phase 2 Data Layer Files

- Create: `src/blockcipher_ai_eval/data/__init__.py`
- Create: `src/blockcipher_ai_eval/data/differential/__init__.py`
- Create: `src/blockcipher_ai_eval/data/differential/config.py`
- Create: `src/blockcipher_ai_eval/data/differential/generator.py`
- Create: `src/blockcipher_ai_eval/data/cache/__init__.py`
- Create: `src/blockcipher_ai_eval/data/cache/disk.py`
- Modify: `src/blockcipher_ai_eval/datasets.py`
- Modify tests only if imports need canonical coverage: `tests/test_datasets.py`

### Phase 3 Experiment Asset Files

- Create directories: `experiments/innovation1/plans/`, `experiments/innovation1/configs/`, `experiments/innovation1/configs/remote/`, `experiments/innovation1/hparam_spaces/`, `experiments/innovation1/summaries/`
- Modify: `scripts/generate_remote_experiment_scripts.py`
- Modify: `experiments/run_innovation_one_matrix.py` only if plan/config resolution needs helpers.
- Modify tests: `tests/test_remote_script_generator.py`, `tests/test_experiment_matrix_runner.py`

### Phase 4 Script Layout Files

- Create directories: `scripts/generators/`, `scripts/monitors/`, `scripts/local/`
- Move canonical generator: `scripts/generators/generate_remote_experiment_scripts.py`
- Keep wrapper: `scripts/generate_remote_experiment_scripts.py`
- Move generated monitors to `scripts/monitors/` when generator support is ready.
- Keep user-facing root monitor wrappers for manually used commands.

### Phase 5 Evaluation Files

- Create: `src/blockcipher_ai_eval/evaluation/__init__.py`
- Create: `src/blockcipher_ai_eval/evaluation/summary.py`
- Create: `src/blockcipher_ai_eval/evaluation/metrics.py`
- Modify summarizer CLI scripts to call `evaluation` library functions.

---

### Task 1: Verify Current Refactor Branch Baseline

**Files:**
- Read: `docs/superpowers/specs/2026-06-10-project-structure-redesign.md`
- Read: `src/blockcipher_ai_eval/models/README.md`

- [ ] **Step 1: Confirm branch and clean state**

Run:

```bash
git status --short --branch
```

Expected:

```text
## refactor/model-project-structure
```

If there are uncommitted changes, inspect them with:

```bash
git diff --stat
```

- [ ] **Step 2: Run model baseline tests**

Run:

```bash
uv run pytest tests/test_adaptive_dbitnet_model.py tests/test_candidate_models.py tests/test_structure_moe.py tests/test_model_components.py tests/test_gohr_speck_model.py -q
```

Expected:

```text
75 passed
```

- [ ] **Step 3: Commit only if baseline drift exists**

If Step 1 found uncommitted model-only drift and Step 2 passes, commit with:

```bash
git add src/blockcipher_ai_eval/models tests/test_adaptive_dbitnet_model.py tests/test_candidate_models.py tests/test_structure_moe.py tests/test_model_components.py tests/test_gohr_speck_model.py
git commit -m "refactor(models): 稳定模型结构整理基线"
```

Expected: either no commit needed, or a clean commit on `refactor/model-project-structure`.

---

### Task 2: Split Dataset Types and Config Into `data/differential/config.py`

**Files:**
- Create: `src/blockcipher_ai_eval/data/__init__.py`
- Create: `src/blockcipher_ai_eval/data/differential/__init__.py`
- Create: `src/blockcipher_ai_eval/data/differential/config.py`
- Modify: `src/blockcipher_ai_eval/datasets.py`
- Test: `tests/test_datasets.py`

- [ ] **Step 1: Write import compatibility test**

Append this test to `tests/test_datasets.py`:

```python
def test_differential_dataset_config_is_available_from_canonical_data_module():
    from blockcipher_ai_eval.data.differential import (
        DifferentialDataset,
        DifferentialDatasetConfig,
        DiskDifferentialDataset,
    )

    assert DifferentialDatasetConfig is not None
    assert DifferentialDataset is not None
    assert DiskDifferentialDataset is not None
```

- [ ] **Step 2: Run test to verify it fails before implementation**

Run:

```bash
uv run pytest tests/test_datasets.py::test_differential_dataset_config_is_available_from_canonical_data_module -q
```

Expected before implementation:

```text
ModuleNotFoundError: No module named 'blockcipher_ai_eval.data'
```

If the module already exists from a previous attempt, continue and make sure the final test passes.

- [ ] **Step 3: Create `data` package files**

Create `src/blockcipher_ai_eval/data/__init__.py`:

```python
from blockcipher_ai_eval.data.differential import (
    DifferentialDataset,
    DifferentialDatasetConfig,
    DiskDifferentialDataset,
)

__all__ = [
    "DifferentialDataset",
    "DifferentialDatasetConfig",
    "DiskDifferentialDataset",
]
```

Create `src/blockcipher_ai_eval/data/differential/config.py` by moving these definitions from `src/blockcipher_ai_eval/datasets.py` without changing field names:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from blockcipher_ai_eval.ciphers.base import ReducedRoundCipher


@dataclass(frozen=True)
class DifferentialDatasetConfig:
    cipher: ReducedRoundCipher
    input_difference: int
    samples_per_class: int
    seed: int = 0
    feature_encoding: str = "ciphertext_pair_bits"
    negative_mode: str = "random_ciphertext"
    pairs_per_sample: int = 1
    key: int | None = None
    shuffle: bool = True


@dataclass(frozen=True)
class DifferentialDataset:
    features: np.ndarray
    labels: np.ndarray
    metadata: dict[str, Any]


@dataclass(frozen=True)
class DiskDifferentialDataset:
    features: np.memmap
    labels: np.memmap
    metadata: dict[str, Any]
    cache_dir: Path
```

Create `src/blockcipher_ai_eval/data/differential/__init__.py`:

```python
from blockcipher_ai_eval.data.differential.config import (
    DifferentialDataset,
    DifferentialDatasetConfig,
    DiskDifferentialDataset,
)

__all__ = [
    "DifferentialDataset",
    "DifferentialDatasetConfig",
    "DiskDifferentialDataset",
]
```

- [ ] **Step 4: Update `datasets.py` imports**

In `src/blockcipher_ai_eval/datasets.py`, remove local dataclass definitions for `DifferentialDatasetConfig`, `DifferentialDataset`, and `DiskDifferentialDataset`, then import them:

```python
from blockcipher_ai_eval.data.differential import (
    DifferentialDataset,
    DifferentialDatasetConfig,
    DiskDifferentialDataset,
)
```

Keep existing public imports working by leaving these names in module scope.

- [ ] **Step 5: Run focused tests**

Run:

```bash
uv run pytest tests/test_datasets.py -q
```

Expected: all dataset tests pass.

- [ ] **Step 6: Commit**

Run:

```bash
git add src/blockcipher_ai_eval/data src/blockcipher_ai_eval/datasets.py tests/test_datasets.py
git commit -m "refactor(data): 提取差分数据集类型"
```

---

### Task 3: Move Disk Cache Helpers Into `data/cache/disk.py`

**Files:**
- Create: `src/blockcipher_ai_eval/data/cache/__init__.py`
- Create: `src/blockcipher_ai_eval/data/cache/disk.py`
- Modify: `src/blockcipher_ai_eval/datasets.py`
- Test: `tests/test_datasets.py`

- [ ] **Step 1: Add canonical cache import test**

Append this test to `tests/test_datasets.py`:

```python
def test_chunked_dataset_cache_builder_is_available_from_canonical_cache_module():
    from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset

    assert make_chunked_differential_dataset is not None
```

- [ ] **Step 2: Run test to verify it fails before implementation**

Run:

```bash
uv run pytest tests/test_datasets.py::test_chunked_dataset_cache_builder_is_available_from_canonical_cache_module -q
```

Expected before implementation:

```text
ImportError
```

If already implemented, continue and verify pass.

- [ ] **Step 3: Create cache module**

Create `src/blockcipher_ai_eval/data/cache/disk.py` with these imports and by moving `make_chunked_differential_dataset`, `_dataset_metadata`, and `_cache_matches` from `src/blockcipher_ai_eval/datasets.py`:

```python
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from blockcipher_ai_eval.data.differential import (
    DifferentialDatasetConfig,
    DiskDifferentialDataset,
)
from blockcipher_ai_eval.datasets import (
    _generate_negative_row,
    _generate_positive_row,
)
```

The moved function signature must stay:

```python
def make_chunked_differential_dataset(
    config: DifferentialDatasetConfig,
    cache_dir: str | Path,
    *,
    chunk_size: int = 8192,
    reuse: bool = True,
) -> DiskDifferentialDataset:
    ...
```

Create `src/blockcipher_ai_eval/data/cache/__init__.py`:

```python
from blockcipher_ai_eval.data.cache.disk import make_chunked_differential_dataset

__all__ = ["make_chunked_differential_dataset"]
```

- [ ] **Step 4: Keep `datasets.py` as compatibility facade**

In `src/blockcipher_ai_eval/datasets.py`, import the moved function:

```python
from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset
```

Keep `_generate_positive_row` and `_generate_negative_row` in `datasets.py` for this phase to avoid circular rewrites. This is an intermediate compatibility boundary.

- [ ] **Step 5: Run focused tests**

Run:

```bash
uv run pytest tests/test_datasets.py tests/test_training.py -q
```

Expected: tests pass.

- [ ] **Step 6: Commit**

Run:

```bash
git add src/blockcipher_ai_eval/data src/blockcipher_ai_eval/datasets.py tests/test_datasets.py
git commit -m "refactor(data): 拆分磁盘缓存构建模块"
```

---

### Task 4: Add Remote Training Progress Log Support

**Files:**
- Modify: `experiments/run_innovation_one_matrix.py`
- Modify: `scripts/generate_remote_experiment_scripts.py`
- Test: `tests/test_experiment_matrix_runner.py`
- Test: `tests/test_remote_script_generator.py`

- [ ] **Step 1: Add runner progress log test**

Add a test to `tests/test_experiment_matrix_runner.py` that runs a one-row smoke plan with a `--progress-output` path and asserts JSONL events exist:

```python
def test_run_innovation_one_matrix_writes_progress_events(tmp_path: Path):
    plan_path = tmp_path / "progress_plan.csv"
    output_path = tmp_path / "results.jsonl"
    progress_path = tmp_path / "progress.jsonl"
    plan_path.write_text(
        "\n".join(
            [
                "cipher,structure,network,model_key,family,architecture_rank,score,rounds,seed,samples_per_class,pairs_per_sample,feature_encoding,negative_mode,train_key,validation_key,difference_profile,difference_member,evidence,literature",
                "SPECK32/64,ARX,MLP,mlp,mlp,0,1,1,0,4,1,ciphertext_pair_xor_bits,encrypted_random_plaintexts,0x1918111009080100,0x0f0e0d0c0b0a0908,speck32_gohr2019,0,progress smoke,Gohr 2019",
            ]
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--plan",
            str(plan_path),
            "--epochs",
            "1",
            "--batch-size",
            "4",
            "--hidden-bits",
            "8",
            "--device",
            "cpu",
            "--progress-output",
            str(progress_path),
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    events = [json.loads(line)["event"] for line in progress_path.read_text().splitlines()]
    assert completed.returncode == 0
    assert events[0] == "run_start"
    assert "row_start" in events
    assert "cache_ready" in events
    assert "row_done" in events
    assert events[-1] == "run_done"
```

- [ ] **Step 2: Implement runner progress output**

In `experiments/run_innovation_one_matrix.py`, add CLI argument:

```python
parser.add_argument("--progress-output", help="Optional JSONL path for run progress events.")
```

Add helper:

```python
def _write_progress(path: str | None, event: str, payload: dict[str, Any] | None = None) -> None:
    if not path:
        return
    progress_path = Path(path)
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    record = {"event": event, **(payload or {})}
    with progress_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
```

Call `_write_progress` at:

```text
run_start before loop
row_start before dataset creation
cache_ready after train and validation datasets are built
row_done after row is written
run_done after loop
```

- [ ] **Step 3: Update remote script generator**

In `scripts/generate_remote_experiment_scripts.py`, add generated runner arg:

```text
--progress-output logs\%RUN_ID%_progress.jsonl ^
```

Also copy the progress file into `results_archive\%RUN_ID%\` if it exists:

```cmd
if exist "%RUN_DIR%\logs\%RUN_ID%_progress.jsonl" copy "%RUN_DIR%\logs\%RUN_ID%_progress.jsonl" "results_archive\%RUN_ID%\"
```

- [ ] **Step 4: Add generator test assertion**

In `tests/test_remote_script_generator.py`, assert generated script contains:

```python
assert "--progress-output logs\\%RUN_ID%_progress.jsonl" in run_text
assert "%RUN_ID%_progress.jsonl" in run_text
```

- [ ] **Step 5: Run tests**

Run:

```bash
uv run pytest tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_writes_progress_events tests/test_remote_script_generator.py -q
```

Expected: tests pass.

- [ ] **Step 6: Commit**

Run:

```bash
git add experiments/run_innovation_one_matrix.py scripts/generate_remote_experiment_scripts.py tests/test_experiment_matrix_runner.py tests/test_remote_script_generator.py
git commit -m "feat(experiments): 记录远程训练进度事件"
```

---

### Task 5: Introduce Innovation-One Experiment Asset Directories

**Files:**
- Create directories under `experiments/innovation1/`
- Modify: `scripts/generate_remote_experiment_scripts.py`
- Test: `tests/test_remote_script_generator.py`

- [ ] **Step 1: Create directories**

Run:

```bash
mkdir -p experiments/innovation1/plans experiments/innovation1/configs/remote experiments/innovation1/hparam_spaces experiments/innovation1/summaries
```

- [ ] **Step 2: Add path resolver tests**

In `tests/test_remote_script_generator.py`, add a spec using a plan path under `experiments\innovation1\plans\demo.csv` and assert it appears unchanged in the generated `.cmd`.

Test body:

```python
def test_generate_remote_scripts_accepts_innovation1_plan_path(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-layout-gpu0-20260610",
                "task_name": "innovation1_layout_gpu0_20260610",
                "plan": "experiments\\innovation1\\plans\\demo.csv",
                "expected_rows": 1,
                "device": "cuda:0",
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")

    assert "--plan experiments\\innovation1\\plans\\demo.csv" in run_text
    assert "copy \"%RUN_DIR%\\experiments\\innovation1\\plans\\demo.csv\"" in run_text
```

- [ ] **Step 3: Run generator tests**

Run:

```bash
uv run pytest tests/test_remote_script_generator.py -q
```

Expected: tests pass.

- [ ] **Step 4: Commit**

Run:

```bash
git add experiments/innovation1 tests/test_remote_script_generator.py
git commit -m "refactor(experiments): 新增创新一实验资产目录"
```

---

### Task 6: Move Remote Script Generator Behind Compatibility Wrapper

**Files:**
- Create: `scripts/generators/__init__.py`
- Move: `scripts/generate_remote_experiment_scripts.py` to `scripts/generators/generate_remote_experiment_scripts.py`
- Create wrapper: `scripts/generate_remote_experiment_scripts.py`
- Test: `tests/test_remote_script_generator.py`

- [ ] **Step 1: Move implementation file**

Run:

```bash
mkdir -p scripts/generators
git mv scripts/generate_remote_experiment_scripts.py scripts/generators/generate_remote_experiment_scripts.py
```

- [ ] **Step 2: Create compatibility wrapper**

Create `scripts/generate_remote_experiment_scripts.py`:

```python
from __future__ import annotations

from scripts.generators.generate_remote_experiment_scripts import main


if __name__ == "__main__":
    main()
```

Create `scripts/generators/__init__.py`:

```python
"""Script generators for reproducible local and remote experiment assets."""
```

- [ ] **Step 3: Update test loader**

In `tests/test_remote_script_generator.py`, update `_load_generator()` to import from the new canonical path:

```python
script_path = Path(__file__).resolve().parents[1] / "scripts" / "generators" / "generate_remote_experiment_scripts.py"
```

Add a smoke test that the wrapper exists:

```python
def test_remote_script_generator_compatibility_wrapper_exists():
    wrapper = Path(__file__).resolve().parents[1] / "scripts" / "generate_remote_experiment_scripts.py"
    assert wrapper.exists()
    assert "scripts.generators.generate_remote_experiment_scripts" in wrapper.read_text(encoding="utf-8")
```

- [ ] **Step 4: Run tests**

Run:

```bash
uv run pytest tests/test_remote_script_generator.py -q
```

Expected: tests pass.

- [ ] **Step 5: Commit**

Run:

```bash
git add scripts/generate_remote_experiment_scripts.py scripts/generators tests/test_remote_script_generator.py
git commit -m "refactor(scripts): 归档远程脚本生成器入口"
```

---

### Task 7: Final Integration Test and Branch Push

**Files:**
- No required file changes unless tests reveal issues.

- [ ] **Step 1: Run focused project-structure test gate**

Run:

```bash
uv run pytest tests/test_datasets.py tests/test_training.py tests/test_adaptive_dbitnet_model.py tests/test_candidate_models.py tests/test_structure_moe.py tests/test_model_components.py tests/test_gohr_speck_model.py tests/test_remote_script_generator.py -q
```

Expected: all tests pass.

- [ ] **Step 2: Run experiment runner smoke tests**

Run:

```bash
uv run pytest tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_train_structure_adaptive_pairset_dbitnet tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_execute_speck_arx_aligned_plan tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_execute_gift_spn_aligned_plan -q
```

Expected: all tests pass.

- [ ] **Step 3: Inspect git history and status**

Run:

```bash
git status --short --branch
git log --oneline -8
```

Expected: branch is `refactor/model-project-structure` and working tree is clean.

- [ ] **Step 4: Push branch**

Run:

```bash
git push origin refactor/model-project-structure
```

Expected: branch is available on GitHub for review without affecting `main` or remote experiment runs.
