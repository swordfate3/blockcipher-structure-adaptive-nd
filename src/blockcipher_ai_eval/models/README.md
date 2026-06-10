# Model Package Layout

This package keeps implementation modules separate from compatibility shims.
New model code should be added to the canonical implementation areas below.

## Canonical Implementation Paths

- `baseline/`: cipher-agnostic and paper baseline networks.
  - Examples: `mlp.py`, `cnn.py`, `dbitnet.py`, `gohr_speck.py`, `resnet_bitslice.py`.
- `common/`: reusable neural-network components shared by multiple model families.
  - Examples: activation builders, normalization layers, attention pooling.
- `structure/`: structure-aware innovation-one models.
  - `structure/adaptive_dbitnet.py`: generic adaptive and structure-conditioned DBitNet blocks.
  - `structure/arx/`: ARX-specific entry points and future ARX-specialized modules.
  - `structure/spn/`: SPN-specific cell, nibble, and token-mixer pair-set models.
  - `structure/feistel/`: reserved for Feistel-specific models.
  - `structure/moe.py`: structure-aware expert fusion models.
- `registry.py`: stable `model_key -> class` lookup used by experiments.

## Compatibility Shims

The top-level files such as `mlp.py`, `cnn.py`, `dbitnet.py`, `adaptive_dbitnet.py`,
`spn.py`, `components.py`, and `structure_moe.py` are compatibility shims for
older scripts, notebooks, tests, and experiment artifacts. They should not receive
new implementation logic.

Prefer these imports in new code:

```python
from blockcipher_ai_eval.models.baseline.gohr_speck import GohrSpeckDistinguisher
from blockcipher_ai_eval.models.common.components import build_activation
from blockcipher_ai_eval.models.structure.arx import ArxStructureAdaptivePairSetDBitNetDistinguisher
from blockcipher_ai_eval.models.structure.spn import SpnTokenMixerPairSetDistinguisher
from blockcipher_ai_eval.models.structure.moe import StructureAwareMoEDistinguisher
```

Use `blockcipher_ai_eval.models` only as a stable public facade, and use
`registry.py` / `experiments.factories.build_model()` for experiment construction.
