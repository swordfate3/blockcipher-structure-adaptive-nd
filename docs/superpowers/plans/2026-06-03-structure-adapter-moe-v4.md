# Structure Adapter MoE v4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first structure-adapter MoE variant that explicitly applies ARX/SPN/Feistel-like input adapters before expert fusion, then document which literature-inspired neural structures are already represented.

**Architecture:** Keep the existing MoE interface stable and introduce lightweight same-width adapters inside `StructureAwareMoEDistinguisher`. `moe_v4_*` uses the v3 pairwise expert pool plus an adapter bank selected from the 19-bit structure feature vector, so the first implementation proves the structure-adapter path without changing dataset schemas.

**Tech Stack:** Python, PyTorch, pytest, existing `uv` workflow.

---

### Task 1: Add Failing Tests for Adapter MoE v4

**Files:**
- Modify: `tests/test_structure_moe.py`
- Modify: `tests/test_experiment_matrix_runner.py`

- [ ] **Step 1: Write tests expecting `v4_structure_adapter` support**

Add tests that import `V4_EXPERT_KEYS`, build `StructureAwareMoEDistinguisher(..., expert_set="v4_structure_adapter")`, assert output shape, assert the pairwise expert is present, assert adapter summaries are exposed, and assert the CLI can train `moe_v4_hard` with a tiny matrix.

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/test_structure_moe.py tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_train_structure_adapter_moe_v4 -q
```

Expected: fail because `V4_EXPERT_KEYS` and `moe_v4_hard` do not exist.

### Task 2: Implement Structure Adapter MoE v4

**Files:**
- Modify: `src/blockcipher_ai_eval/models/structure_moe.py`
- Modify: `src/blockcipher_ai_eval/experiments/factories.py`

- [ ] **Step 1: Add adapter modules**

Implement same-width PyTorch adapters:

```text
IdentityAdapter
ArxWordMixAdapter
SpnCellMixAdapter
FeistelBranchMixAdapter
```

The adapters transform input features but preserve `(batch, input_bits)`, so all existing experts remain usable.

- [ ] **Step 2: Add v4 expert set**

Add `V4_EXPERT_KEYS` equal to the v3 expert list and allow `expert_set="v4_structure_adapter"`.

- [ ] **Step 3: Apply adapter before experts**

For v4 only, choose adapter from structure features:

```text
ARX -> arx_word_mix
SPN -> spn_cell_mix
Feistel-like -> feistel_branch_mix
unknown -> identity
```

Expose `adapter_mode` and `adapter_name` in `gate_summary()`.

- [ ] **Step 4: Register model keys**

Add:

```text
moe_v4_uniform
moe_v4_hard
moe_v4_soft
```

to `build_model()`.

- [ ] **Step 5: Run target tests**

Run the failing tests again and confirm they pass.

### Task 3: Sync Documentation State

**Files:**
- Modify: `docs/research/neural_differential_models_survey.md`
- Modify: `README.md`
- Modify: `memory/innovation-one.md`

- [ ] **Step 1: Update implemented-vs-not-implemented status**

Record that `senet_resnext`, `multiscale_dense_resnet`, `adaptive_dbitnet_pairwise`, and `moe_v4_*` are implemented. Keep GPD, RX, polytopic, score-distribution, NNBits, and two-difference as future data/feature extensions rather than MoE experts.

- [ ] **Step 2: Run docs-related greps**

Run:

```bash
rg -n "moe_v4|v4_structure_adapter|未实现|senet_resnext|multiscale_dense_resnet" README.md docs/research/neural_differential_models_survey.md memory/innovation-one.md
```

Expected: new v4 entries are present and stale implemented-model statuses are removed or clarified.

### Task 4: Verify and Commit

**Files:**
- All modified files.

- [ ] **Step 1: Run focused tests**

```bash
uv run pytest tests/test_structure_moe.py tests/test_experiment_matrix_runner.py -q
```

- [ ] **Step 2: Run full tests**

```bash
uv run pytest -q
```

- [ ] **Step 3: Commit**

```bash
git add src/blockcipher_ai_eval/models/structure_moe.py src/blockcipher_ai_eval/experiments/factories.py tests/test_structure_moe.py tests/test_experiment_matrix_runner.py README.md docs/research/neural_differential_models_survey.md memory/innovation-one.md docs/superpowers/plans/2026-06-03-structure-adapter-moe-v4.md
git commit -m "feat(models): 添加结构适配MoE v4"
```
