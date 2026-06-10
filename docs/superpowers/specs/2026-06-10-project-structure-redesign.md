# Project Structure Redesign Design

## Goal

Restructure `blockcipher-structure-adaptive-nd` into a research-grade codebase that supports the thesis and paper workflow for neural differential cryptanalysis. The structure should make the main research story explicit:

- Ciphers are grouped by cryptographic structure.
- Data generation and cache protocols are reproducible and inspectable.
- Feature encodings are separate from neural architectures.
- Neural models are grouped by baseline, common components, and structure-aware designs.
- Experiments are grouped by thesis innovation and can run locally or remotely through generated scripts.
- Results, memory notes, papers, and docs remain separated from source code.

The redesign must keep old experiment artifacts reproducible. Existing model keys, runner commands, and remote result branches should continue to work during the transition.

## Non-Goals

- Do not rewrite neural network math during the structure migration.
- Do not rename completed remote result branches.
- Do not break current `main` remote runs.
- Do not delete compatibility import shims until the thesis experiments are stable.
- Do not move large `outputs/` artifacts into tracked source code.

## Recommended Architecture

### Source Package

```text
src/blockcipher_ai_eval/
├── ciphers/
│   ├── arx/
│   ├── spn/
│   ├── feistel/
│   └── sponge/
├── data/
│   ├── differential/
│   ├── cache/
│   └── protocols/
├── features/
│   ├── arx/
│   ├── spn/
│   ├── feistel/
│   └── registry.py
├── models/
│   ├── baseline/
│   ├── common/
│   ├── structure/
│   │   ├── arx/
│   │   ├── spn/
│   │   ├── feistel/
│   │   └── moe/
│   └── registry.py
├── training/
├── evaluation/
├── experiments/
└── utils/
```

### Repository Root

```text
blockcipher-structure-adaptive-nd/
├── src/
├── tests/
├── experiments/
│   ├── innovation1/
│   │   ├── plans/
│   │   ├── configs/
│   │   ├── hparam_spaces/
│   │   └── summaries/
│   ├── baselines/
│   └── ablations/
├── scripts/
│   ├── local/
│   ├── remote/
│   ├── monitors/
│   └── generators/
├── outputs/
│   ├── local/
│   ├── remote_results/
│   ├── hparam_search/
│   └── dataset_cache/
├── docs/
│   ├── architecture/
│   ├── experiments/
│   ├── research/
│   └── usage/
├── memory/
├── papers/
└── archive/
```

## Module Boundaries

### `ciphers/`

Cipher implementations and validation vectors live here. They must not depend on training, datasets, models, or experiment runners.

Canonical direction:

```text
ciphers/arx/      SPECK, CHAM, LEA
ciphers/spn/      AES, PRESENT, GIFT, ARIA, SM4-like SPN components when applicable
ciphers/feistel/  DES, Simon/Simeck-like Feistel families where appropriate
ciphers/sponge/   ASCON-style permutation or AEAD adapters if retained
```

### `data/`

Move dataset generation and disk caching here over time. This separates sampling protocols from feature engineering.

Target modules:

```text
data/differential/config.py      DifferentialDatasetConfig and dataset metadata
data/differential/generator.py   positive/negative pair generation
data/cache/disk.py               DiskDifferentialDataset and memmap cache helpers
data/protocols/negative.py       random-ciphertext vs encrypted-random-plaintext protocols
```

Compatibility: keep `blockcipher_ai_eval.datasets` as a shim until all runners and docs migrate.

### `features/`

Feature encodings transform cipher observations into neural inputs. They should depend on `ciphers/` but not on `models/` or `training/`.

Target modules:

```text
features/arx/aligned.py
features/arx/partial_inverse.py
features/spn/aligned.py
features/feistel/aligned.py
features/pair_features.py
features/registry.py
```

### `models/`

Neural architectures are grouped by role:

```text
models/baseline/       literature baselines and generic networks
models/common/         neural components shared by models
models/structure/arx/  ARX-specific structure-aware entry points
models/structure/spn/  SPN-specific TokenMixer / cell / nibble models
models/structure/moe/  expert routing and structure-aware fusion
```

Top-level files such as `models/adaptive_dbitnet.py`, `models/spn.py`, and `models/structure_moe.py` remain compatibility shims during the thesis cycle. New code should import from canonical paths documented in `models/README.md`.

### `training/`

Training should own loops, torch datasets, optimizers, schedulers, checkpoints, metrics emitted during training, and progress logging.

A required follow-up is adding progress logs for long remote jobs:

```text
progress.jsonl events:
  run_start
  row_start
  cache_ready
  epoch_end
  validation_start
  row_done
  run_done
```

### `evaluation/`

Move result aggregation and statistical analysis here. Summarizers can remain CLI wrappers but should call library code from this package.

Target modules:

```text
evaluation/metrics.py
evaluation/summary.py
evaluation/statistics.py
evaluation/comparison.py
```

### `experiments/` Package vs Root `experiments/`

`src/blockcipher_ai_eval/experiments/` contains reusable factories, profiles, and programmatic experiment definitions.

Root `experiments/` contains concrete assets and CLI entry points:

```text
experiments/innovation1/plans/
experiments/innovation1/configs/
experiments/innovation1/hparam_spaces/
experiments/innovation1/summaries/
```

Existing paths such as `experiments/plans/*.csv` should be supported by compatibility wrappers or symlinks during migration.

## Experiment Asset Strategy

The current flat experiment/script layout should migrate gradually:

```text
experiments/configs/innovation1/*.json -> experiments/innovation1/configs/*.json
experiments/configs/remote/*.json      -> experiments/innovation1/configs/remote/*.json
experiments/plans/*.csv                -> experiments/innovation1/plans/*.csv
experiments/hparam_spaces/*.json       -> experiments/innovation1/hparam_spaces/*.json
scripts/remote/*.cmd                   -> scripts/remote/*.cmd, generated only
monitor_*.sh                           -> scripts/monitors/*.sh
script generators                      -> scripts/generators/
```

The script generator should be the source of truth for remote `.cmd` and monitor scripts. Hand-written per-run scripts should move to `archive/legacy/` after the generated path is verified.

## Backward Compatibility Rules

1. Existing model keys remain valid:
   - `structure_adaptive_pairset_dbitnet`
   - `spn_token_mixer_pairset`
   - `moe_v5_soft`, `moe_v5_hard`
2. New clearer model keys may be added:
   - `arx_structure_adaptive_pairset_dbitnet`
   - `arx_pairset_dbitnet`
3. Existing runner paths keep working until all docs and remote specs migrate.
4. Compatibility shims may warn later, but should not warn during active remote experiments.
5. Result archive paths and branch names are immutable.

## Migration Plan

### Phase 1: Model Layer Boundary

Already started on `refactor/model-project-structure`:

- Add `models/structure/arx/pairset_dbitnet.py`.
- Keep generic implementation in `models/structure/adaptive_dbitnet.py`.
- Add ARX-specific model keys.
- Update tests and internal imports to canonical paths.
- Document model layout in `models/README.md`.

### Phase 2: Data Layer Split

Move dataset generation and disk caching from `datasets.py` into `data/` modules. Keep `datasets.py` as a public shim.

Validation:

```text
uv run pytest tests/test_datasets.py tests/test_training.py tests/test_experiment_matrix_runner.py -q
```

### Phase 3: Experiment Asset Layout

Create `experiments/innovation1/` and migrate configs/plans/hparam spaces. Update script generator to resolve both old and new paths. Keep old assets until remote scripts are regenerated and verified.

Validation:

```text
uv run pytest tests/test_remote_script_generator.py tests/test_experiment_matrix_runner.py -q
```

### Phase 4: Script Layout

Move monitor scripts under `scripts/monitors/` and generators under `scripts/generators/`. Keep thin root-level wrappers only where users already run them manually.

Validation:

```text
uv run pytest tests/test_remote_script_generator.py -q
```

### Phase 5: Evaluation and Reporting

Move summarization/statistical comparison logic into `src/blockcipher_ai_eval/evaluation/`. Keep CLI scripts as wrappers.

Validation:

```text
uv run pytest tests -q
```

## Testing Strategy

Each phase must have a focused test gate before committing:

- Model phase: model construction, registry, MoE tests.
- Data phase: dataset generation/cache/training tests.
- Experiment phase: matrix runner and remote script generator tests.
- Script phase: monitor and generator tests.
- Final phase: broad test pass.

Remote experiments should not be restarted solely because of refactoring. Push refactor branches separately and only schedule remote validation after local tests pass and the user approves.

## Risks and Mitigations

- Risk: path migration breaks old remote scripts.
  - Mitigation: keep old paths and wrappers until generated remote scripts are verified.
- Risk: model key rename invalidates old result files.
  - Mitigation: never remove old keys; add new clearer aliases.
- Risk: massive one-shot refactor becomes hard to review.
  - Mitigation: phase commits by layer.
- Risk: long remote jobs still look stuck.
  - Mitigation: add training progress logs before the next large-scale run.

## Acceptance Criteria

The redesign is successful when:

1. New code has clear canonical locations documented in `models/README.md` and architecture docs.
2. Old imports, model keys, and runner paths still work during transition.
3. Innovation-one ARX, SPN, and MoE model mappings are obvious from directory names.
4. Experiment assets are grouped under `experiments/innovation1/` without breaking current scripts.
5. Remote jobs emit progress logs before final result rows are written.
6. The relevant test suites pass after each migration phase.
