# Structure-Aware MoE Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a structure-aware mixture-of-experts neural distinguisher that fuses existing experts through uniform, hard-structure, and soft-structure gates.

**Architecture:** Implement a reusable structure-vector encoder from `CipherProfile`, then add `StructureAwareMoEDistinguisher` under `models/`. The first implementation keeps per-cipher input widths and stores a per-run structure vector in the model so the existing training loop can remain unchanged.

**Tech Stack:** Python, PyTorch, NumPy, pytest, existing `uv` workflow.

---

## File Structure

- Create `src/blockcipher_ai_eval/structure_features.py`: convert `CipherProfile` and round count into an auditable numeric structure vector.
- Create `src/blockcipher_ai_eval/models/structure_moe.py`: define expert labels, gate modes, hard gate priors, and `StructureAwareMoEDistinguisher`.
- Modify `src/blockcipher_ai_eval/models/__init__.py`: export the MoE model.
- Modify `src/blockcipher_ai_eval/experiments/factories.py`: support `moe_uniform`, `moe_hard`, and `moe_soft`.
- Modify `experiments/run_innovation_one_matrix.py`: attach structure vectors to MoE models and write gate metadata to JSONL.
- Modify `experiments/summarize_innovation_one_results.py`: preserve `gate_mode` in summary grouping.
- Create `tests/test_structure_features.py`: verify structure-vector encoding.
- Create `tests/test_structure_moe.py`: verify gates, output shape, and gate summary.
- Update `tests/test_experiment_matrix_runner.py`: verify CLI can train a MoE model and emits gate metadata.
- Update docs after implementation.

---

### Task 1: Structure Feature Encoder

**Files:**
- Create: `src/blockcipher_ai_eval/structure_features.py`
- Test: `tests/test_structure_features.py`

- [ ] **Step 1: Write failing tests**

```python
from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.structure_features import (
    STRUCTURE_FEATURE_NAMES,
    structure_feature_vector,
)


def test_structure_feature_vector_marks_arx_traits_and_normalized_sizes():
    vector = structure_feature_vector(CipherProfile.speck32_64(), rounds=7)
    values = dict(zip(STRUCTURE_FEATURE_NAMES, vector.tolist()))

    assert values["is_arx"] == 1.0
    assert values["is_spn"] == 0.0
    assert values["has_modular_addition"] == 1.0
    assert values["has_sbox_layer"] == 0.0
    assert values["block_bits_div_128"] == 0.25
    assert values["key_bits_div_128"] == 0.5
    assert values["rounds_div_32"] == 7 / 32


def test_structure_feature_vector_marks_sm4_as_feistel_like():
    vector = structure_feature_vector(CipherProfile.sm4(), rounds=4)
    values = dict(zip(STRUCTURE_FEATURE_NAMES, vector.tolist()))

    assert values["is_feistel_like"] == 1.0
    assert values["has_sbox_layer"] == 1.0
    assert values["has_linear_diffusion"] == 1.0
    assert values["has_round_recurrence"] == 1.0
```

- [ ] **Step 2: Run tests and verify failure**

Run: `uv run pytest tests/test_structure_features.py -q`

Expected: FAIL because `blockcipher_ai_eval.structure_features` does not exist.

- [ ] **Step 3: Implement encoder**

```python
from __future__ import annotations

import numpy as np

from blockcipher_ai_eval.innovation_one import CipherProfile


STRUCTURE_FEATURE_NAMES = (
    "is_arx",
    "is_spn",
    "is_feistel_like",
    "has_modular_addition",
    "has_xor",
    "has_rotation",
    "has_carry_propagation",
    "has_word_parallelism",
    "has_sbox_layer",
    "has_permutation_layer",
    "has_sbox_locality",
    "has_bit_permutation",
    "has_lightweight_spn",
    "has_unbalanced_round_update",
    "has_linear_diffusion",
    "has_round_recurrence",
    "block_bits_div_128",
    "key_bits_div_128",
    "rounds_div_32",
)


def structure_feature_vector(cipher: CipherProfile, rounds: int) -> np.ndarray:
    traits = set(cipher.traits)
    values = {
        "is_arx": cipher.structure == "ARX",
        "is_spn": cipher.structure == "SPN",
        "is_feistel_like": cipher.structure == "Feistel-like",
        "has_modular_addition": "modular_addition" in traits,
        "has_xor": "xor" in traits,
        "has_rotation": "rotation" in traits,
        "has_carry_propagation": "carry_propagation" in traits,
        "has_word_parallelism": "word_parallelism" in traits,
        "has_sbox_layer": "sbox_layer" in traits,
        "has_permutation_layer": "permutation_layer" in traits,
        "has_sbox_locality": "sbox_locality" in traits,
        "has_bit_permutation": "bit_permutation" in traits,
        "has_lightweight_spn": "lightweight_spn" in traits,
        "has_unbalanced_round_update": "unbalanced_round_update" in traits,
        "has_linear_diffusion": "linear_diffusion" in traits,
        "has_round_recurrence": "round_recurrence" in traits,
        "block_bits_div_128": cipher.block_bits / 128.0,
        "key_bits_div_128": cipher.key_bits / 128.0,
        "rounds_div_32": rounds / 32.0,
    }
    return np.array([float(values[name]) for name in STRUCTURE_FEATURE_NAMES], dtype=np.float32)
```

- [ ] **Step 4: Run tests and verify pass**

Run: `uv run pytest tests/test_structure_features.py -q`

Expected: PASS.

---

### Task 2: MoE Model

**Files:**
- Create: `src/blockcipher_ai_eval/models/structure_moe.py`
- Modify: `src/blockcipher_ai_eval/models/__init__.py`
- Test: `tests/test_structure_moe.py`

- [ ] **Step 1: Write failing tests**

```python
import torch

from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.models import StructureAwareMoEDistinguisher
from blockcipher_ai_eval.structure_features import structure_feature_vector


def _features(cipher, rounds):
    return torch.tensor(structure_feature_vector(cipher, rounds), dtype=torch.float32)


def test_uniform_moe_outputs_expected_shape_and_equal_weights():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="uniform",
    )
    model.set_structure_features(_features(CipherProfile.speck32_64(), rounds=5))

    output = model(torch.zeros((3, 96), dtype=torch.float32))
    weights = model.current_gate_weights(batch_size=3)

    assert output.shape == (3, 1)
    assert torch.allclose(weights[0], torch.tensor([0.25, 0.25, 0.25, 0.25]))


def test_hard_moe_prefers_resnet_for_arx_and_dbitnet_for_sm4():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="hard",
    )
    model.set_structure_features(_features(CipherProfile.speck32_64(), rounds=5))

    arx_summary = model.gate_summary()

    assert arx_summary["gate_mode"] == "hard"
    assert arx_summary["gate_weight_resnet_bitslice"] == 0.55
    assert arx_summary["gate_weight_dbitnet_dilated_cnn"] == 0.30

    model.set_structure_features(_features(CipherProfile.sm4(), rounds=4))
    sm4_summary = model.gate_summary()

    assert sm4_summary["gate_weight_dbitnet_dilated_cnn"] == 0.50
    assert sm4_summary["gate_weight_resnet_bitslice"] == 0.30


def test_soft_moe_weights_sum_to_one():
    model = StructureAwareMoEDistinguisher(
        input_bits=96,
        hidden_bits=8,
        structure_feature_bits=19,
        gate_mode="soft",
    )
    model.set_structure_features(_features(CipherProfile.present80(), rounds=4))

    weights = model.current_gate_weights(batch_size=2)

    assert weights.shape == (2, 4)
    assert torch.allclose(weights.sum(dim=1), torch.ones(2), atol=1e-6)
```

- [ ] **Step 2: Run tests and verify failure**

Run: `uv run pytest tests/test_structure_moe.py -q`

Expected: FAIL because `StructureAwareMoEDistinguisher` does not exist.

- [ ] **Step 3: Implement model and exports**

Create `structure_moe.py` with:

```python
from __future__ import annotations

from typing import Any

import torch
from torch import nn

from blockcipher_ai_eval.models.cnn import CnnDistinguisher
from blockcipher_ai_eval.models.dbitnet import DBitNetDistinguisher
from blockcipher_ai_eval.models.mlp import MlpDistinguisher
from blockcipher_ai_eval.models.resnet_bitslice import ResNetBitSliceDistinguisher


EXPERT_KEYS = (
    "resnet_bitslice",
    "dbitnet_dilated_cnn",
    "cnn",
    "mlp",
)

HARD_GATE_WEIGHTS = {
    "ARX": (0.55, 0.30, 0.10, 0.05),
    "SPN": (0.10, 0.45, 0.40, 0.05),
    "Feistel-like": (0.30, 0.50, 0.15, 0.05),
}


class StructureAwareMoEDistinguisher(nn.Module):
    def __init__(
        self,
        input_bits: int,
        hidden_bits: int,
        structure_feature_bits: int,
        gate_mode: str,
    ) -> None:
        super().__init__()
        if gate_mode not in {"uniform", "hard", "soft"}:
            raise ValueError(f"unsupported gate_mode: {gate_mode}")
        self.input_bits = input_bits
        self.hidden_bits = hidden_bits
        self.structure_feature_bits = structure_feature_bits
        self.gate_mode = gate_mode
        self.experts = nn.ModuleList(
            [
                ResNetBitSliceDistinguisher(input_bits=input_bits, channels=hidden_bits),
                DBitNetDistinguisher(input_bits=input_bits, channels=hidden_bits),
                CnnDistinguisher(input_bits=input_bits, channels=hidden_bits),
                MlpDistinguisher(input_bits=input_bits, hidden_bits=hidden_bits),
            ]
        )
        self.soft_gate = nn.Sequential(
            nn.Linear(structure_feature_bits, hidden_bits),
            nn.ReLU(),
            nn.Linear(hidden_bits, len(EXPERT_KEYS)),
        )
        self.register_buffer(
            "_structure_features",
            torch.zeros(structure_feature_bits, dtype=torch.float32),
        )

    def set_structure_features(self, structure_features: torch.Tensor) -> None:
        if structure_features.shape != (self.structure_feature_bits,):
            raise ValueError(
                "structure_features must have shape "
                f"({self.structure_feature_bits},), got {tuple(structure_features.shape)}"
            )
        self._structure_features.copy_(structure_features.detach().to(self._structure_features))

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        expert_logits = torch.cat([expert(features) for expert in self.experts], dim=1)
        weights = self.current_gate_weights(batch_size=features.shape[0]).to(features.device)
        return (expert_logits * weights).sum(dim=1, keepdim=True)

    def current_gate_weights(self, batch_size: int) -> torch.Tensor:
        structure = self._structure_features.unsqueeze(0).expand(batch_size, -1)
        if self.gate_mode == "uniform":
            return torch.full(
                (batch_size, len(EXPERT_KEYS)),
                1.0 / len(EXPERT_KEYS),
                dtype=structure.dtype,
                device=structure.device,
            )
        if self.gate_mode == "hard":
            weights = torch.tensor(
                self._hard_weights_from_structure(),
                dtype=structure.dtype,
                device=structure.device,
            )
            return weights.unsqueeze(0).expand(batch_size, -1)
        return torch.softmax(self.soft_gate(structure), dim=1)

    def gate_summary(self) -> dict[str, Any]:
        weights = self.current_gate_weights(batch_size=1).detach().cpu()[0]
        return {
            "gate_mode": self.gate_mode,
            **{
                f"gate_weight_{key}": round(float(weight), 10)
                for key, weight in zip(EXPERT_KEYS, weights)
            },
        }

    def _hard_weights_from_structure(self) -> tuple[float, float, float, float]:
        is_arx = bool(self._structure_features[0].item())
        is_spn = bool(self._structure_features[1].item())
        is_feistel_like = bool(self._structure_features[2].item())
        if is_arx:
            return HARD_GATE_WEIGHTS["ARX"]
        if is_spn:
            return HARD_GATE_WEIGHTS["SPN"]
        if is_feistel_like:
            return HARD_GATE_WEIGHTS["Feistel-like"]
        return (0.25, 0.25, 0.25, 0.25)
```

Export from `models/__init__.py`:

```python
from blockcipher_ai_eval.models.structure_moe import StructureAwareMoEDistinguisher
```

- [ ] **Step 4: Run tests and verify pass**

Run: `uv run pytest tests/test_structure_moe.py -q`

Expected: PASS.

---

### Task 3: Factory and Runner Integration

**Files:**
- Modify: `src/blockcipher_ai_eval/experiments/factories.py`
- Modify: `experiments/run_innovation_one_matrix.py`
- Test: `tests/test_experiment_matrix_runner.py`

- [ ] **Step 1: Write failing CLI test**

Add to `tests/test_experiment_matrix_runner.py`:

```python
def test_run_innovation_one_matrix_can_train_structure_moe(tmp_path: Path):
    output_path = tmp_path / "moe.jsonl"

    completed = subprocess.run(
        [
            sys.executable,
            "experiments/run_innovation_one_matrix.py",
            "--ciphers",
            "speck32",
            "--models",
            "moe_hard",
            "--rounds",
            "1",
            "--seeds",
            "0",
            "--samples-per-class",
            "8",
            "--epochs",
            "1",
            "--batch-size",
            "8",
            "--hidden-bits",
            "8",
            "--difference-profile",
            "speck32_gohr2019",
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = [json.loads(line) for line in output_path.read_text().splitlines()]

    assert completed.returncode == 0
    assert rows[0]["model"] == "moe_hard"
    assert rows[0]["gate_mode"] == "hard"
    assert rows[0]["gate_weights_mean"]["resnet_bitslice"] == 0.55
    assert rows[0]["gate_weights_mean"]["dbitnet_dilated_cnn"] == 0.30
```

- [ ] **Step 2: Run test and verify failure**

Run: `uv run pytest tests/test_experiment_matrix_runner.py::test_run_innovation_one_matrix_can_train_structure_moe -q`

Expected: FAIL because `moe_hard` is unsupported.

- [ ] **Step 3: Update factory**

Modify `factories.py`:

```python
from blockcipher_ai_eval.models import StructureAwareMoEDistinguisher
from blockcipher_ai_eval.structure_features import STRUCTURE_FEATURE_NAMES
```

Add to `build_model()`:

```python
    if name == "moe_uniform":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="uniform",
        )
    if name == "moe_hard":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="hard",
        )
    if name == "moe_soft":
        return StructureAwareMoEDistinguisher(
            input_bits=input_bits,
            hidden_bits=hidden_bits,
            structure_feature_bits=len(STRUCTURE_FEATURE_NAMES),
            gate_mode="soft",
        )
```

- [ ] **Step 4: Add structure metadata to runner**

In `run_innovation_one_matrix.py`, import:

```python
import torch
from blockcipher_ai_eval.innovation_one import CipherProfile
from blockcipher_ai_eval.structure_features import structure_feature_vector
```

Add helper:

```python
def _cipher_profile(cipher_key: str) -> CipherProfile:
    mapping = {
        "speck32": CipherProfile.speck32_64,
        "present80": CipherProfile.present80,
        "sm4": CipherProfile.sm4,
    }
    try:
        return mapping[cipher_key]()
    except KeyError as exc:
        raise ValueError(f"unsupported cipher key: {cipher_key}") from exc
```

After `model = build_model(...)`, call:

```python
        _configure_structure_aware_model(model, task["cipher_key"], task["rounds"])
```

Add:

```python
def _configure_structure_aware_model(model: Any, cipher_key: str, rounds: int) -> None:
    if not hasattr(model, "set_structure_features"):
        return
    vector = structure_feature_vector(_cipher_profile(cipher_key), rounds)
    model.set_structure_features(torch.tensor(vector, dtype=torch.float32))
```

In result row, add:

```python
                **_model_metadata(model),
```

Add:

```python
def _model_metadata(model: Any) -> dict[str, Any]:
    if not hasattr(model, "gate_summary"):
        return {}
    summary = model.gate_summary()
    gate_weights = {
        key.removeprefix("gate_weight_"): value
        for key, value in summary.items()
        if key.startswith("gate_weight_")
    }
    return {
        "gate_mode": summary["gate_mode"],
        "gate_weights_mean": gate_weights,
    }
```

- [ ] **Step 5: Run focused tests**

Run:

```bash
uv run pytest tests/test_structure_features.py tests/test_structure_moe.py tests/test_experiment_matrix_runner.py -q
```

Expected: PASS.

---

### Task 4: Summary and Documentation

**Files:**
- Modify: `experiments/summarize_innovation_one_results.py`
- Modify: `README.md`
- Modify: `docs/创新一_结构感知神经区分器匹配方案.md`
- Test: `tests/test_summarize_results.py`

- [ ] **Step 1: Update summary test**

Add to each input row in `tests/test_summarize_results.py`:

```python
"gate_mode": "hard",
```

Assert:

```python
assert summary_rows[0]["gate_mode"] == "hard"
```

- [ ] **Step 2: Run test and verify failure**

Run: `uv run pytest tests/test_summarize_results.py -q`

Expected: FAIL because `gate_mode` is not in summary fields.

- [ ] **Step 3: Update summary grouping**

Add `"gate_mode"` to `GROUP_FIELDS` in `experiments/summarize_innovation_one_results.py`.

- [ ] **Step 4: Update docs**

Add a short section to `README.md` showing:

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models moe_uniform moe_hard moe_soft \
  --rounds 5 \
  --seeds 0 \
  --samples-per-class 4096 \
  --epochs 4 \
  --batch-size 512 \
  --hidden-bits 32 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_moe_smoke.jsonl
```

Add to `docs/创新一_结构感知神经区分器匹配方案.md`:

- SA-MoE formula.
- Gate modes.
- Current limitation: per-cipher input width, not cross-cipher mixed batches.

- [ ] **Step 5: Run full tests**

Run: `uv run pytest -q`

Expected: PASS.

---

### Task 5: MoE Smoke Experiment

**Files:**
- No committed output files.

- [ ] **Step 1: Run a small SPECK MoE screen**

```bash
uv run python experiments/run_innovation_one_matrix.py \
  --ciphers speck32 \
  --models resnet_bitslice dbitnet_dilated_cnn moe_uniform moe_hard moe_soft \
  --rounds 5 \
  --seeds 0 \
  --samples-per-class 2048 \
  --epochs 3 \
  --batch-size 512 \
  --hidden-bits 32 \
  --feature-encoding ciphertext_pair_xor_bits \
  --difference-profile speck32_gohr2019 \
  --output outputs/innovation_one_speck_moe_smoke.jsonl
```

Expected: writes 5 rows.

- [ ] **Step 2: Summarize**

```bash
uv run python experiments/summarize_innovation_one_results.py \
  --input outputs/innovation_one_speck_moe_smoke.jsonl \
  --output outputs/innovation_one_speck_moe_smoke_summary.csv
```

Expected: writes 5 summary rows.

- [ ] **Step 3: Inspect gate metadata**

Run:

```bash
python -c "import json; [print(row['model'], row.get('gate_mode'), row.get('gate_weights_mean')) for row in map(json.loads, open('outputs/innovation_one_speck_moe_smoke.jsonl'))]"
```

Expected: `moe_uniform`, `moe_hard`, and `moe_soft` rows include gate metadata.

---

### Task 6: Final Commit

**Files:**
- Commit all source, test, and doc changes.
- Do not commit generated files under `outputs/`.

- [ ] **Step 1: Verify clean checks**

Run:

```bash
git diff --check
uv run pytest -q
```

Expected: no diff-check output and all tests pass.

- [ ] **Step 2: Stage changes**

```bash
git add README.md docs/创新一_结构感知神经区分器匹配方案.md \
  experiments/run_innovation_one_matrix.py experiments/summarize_innovation_one_results.py \
  src/blockcipher_ai_eval/experiments/factories.py src/blockcipher_ai_eval/models/__init__.py \
  src/blockcipher_ai_eval/models/structure_moe.py src/blockcipher_ai_eval/structure_features.py \
  tests/test_experiment_matrix_runner.py tests/test_structure_features.py tests/test_structure_moe.py \
  tests/test_summarize_results.py docs/superpowers/plans/2026-06-01-structure-aware-moe.md
```

- [ ] **Step 3: Commit**

```bash
git commit -m "feat(models): 添加结构感知专家融合区分器"
```

Expected: commit succeeds.
