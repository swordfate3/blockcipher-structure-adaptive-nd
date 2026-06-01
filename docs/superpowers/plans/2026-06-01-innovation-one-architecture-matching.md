# Innovation One Architecture Matching Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a first, testable version of innovation point 1: a structure-aware neural distinguisher architecture matching method for block ciphers.

**Architecture:** Keep the first version lightweight and reproducible. Represent each cipher and neural network as a profile, rank candidate networks by structure-trait overlap, generate an experiment matrix, and document the thesis-ready method boundary with literature support.

**Tech Stack:** Python 3.10, pytest, Markdown, CSV.

---

### Task 1: Define The Matching API

**Files:**
- Create: `src/blockcipher_ai_eval/__init__.py`
- Create: `src/blockcipher_ai_eval/innovation_one.py`
- Test: `tests/test_innovation_one.py`

- [ ] **Step 1: Write tests for cipher/network ranking**

Create tests that verify SPECK32/64 maps to `ResNet-BitSlice`, PRESENT-80 maps to `CNN-SBoxLocal` or `DBitNet-DilatedCNN`, and SM4 keeps `Transformer-Encoder` as a high-cost ablation rather than the first candidate.

- [ ] **Step 2: Verify the tests fail**

Run: `python -m pytest tests/test_innovation_one.py -q`

Expected: import failure because `blockcipher_ai_eval` does not exist.

- [ ] **Step 3: Implement profiles and ranking**

Create frozen dataclasses for `CipherProfile`, `NetworkProfile`, `RankedArchitecture`, and `ExperimentPlan`. Implement `rank_architectures`, `build_experiment_matrix`, and `summarize_recommendation`.

- [ ] **Step 4: Verify the tests pass**

Run: `python -m pytest tests/test_innovation_one.py -q`

Expected: all tests pass.

### Task 2: Add Experiment Matrix Generation

**Files:**
- Create: `experiments/build_innovation_one_matrix.py`

- [ ] **Step 1: Add CLI script**

Create a script with `--output`, `--samples-per-class`, `--rounds`, and `--seeds` arguments. It should write a CSV grid over cipher, structure, network, rounds, seed, and sample count.

- [ ] **Step 2: Run a smoke test**

Run: `python experiments/build_innovation_one_matrix.py --rounds 3 4 --seeds 0 1 --samples-per-class 1024 --output /tmp/innovation_one_matrix.csv`

Expected: 72 rows for 3 ciphers, 6 networks, 2 round settings, and 2 seeds.

### Task 3: Write The Thesis-Facing Document

**Files:**
- Create: `docs/创新一_结构感知神经区分器匹配方案.md`

- [ ] **Step 1: Write related-work synthesis**

Summarize Gohr 2019, Benamira et al. 2021, Bao et al. 2022, Bellini et al. 2023, Gohr/Leander/Neumann 2022, NNBits 2023, Ebrahimi et al. 2022/2023, and the 2024 SoK.

- [ ] **Step 2: Define the innovation claim**

State that the contribution is not the first neural distinguisher and not the first generic pipeline, but a structure-aware, unified experimental protocol for empirical architecture matching.

- [ ] **Step 3: Define metrics and experiment tables**

Include Accuracy, AUC, advantage, critical round, data complexity, training cost, stability, and cross-key generalization.

### Task 4: Verify Deliverables

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add pytest source path**

Configure pytest to read source from `src`.

- [ ] **Step 2: Run tests**

Run: `python -m pytest -q`

Expected: all tests pass.
