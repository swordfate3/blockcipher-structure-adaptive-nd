# Blockcipher Structure-Adaptive ND Project Structure

This project is organized around innovation one: structure-aware neural differential distinguishers for reduced-round block ciphers. The refactor branch uses canonical paths only; old root-level experiment assets and single-file model/data shims are removed.

## Source Layout

```text
src/blockcipher_ai_eval/
├── ciphers/                         # Reduced-round cipher implementations
│   ├── arx/                         # SPECK, CHAM, LEA
│   ├── feistel/                     # SIMON, SIMECK, DES, SM4, Camellia
│   └── spn/                         # PRESENT, GIFT, AES, ARIA
├── features/                        # Feature encodings and structure descriptors
│   ├── registry.py                  # Supported feature encodings and pair-width lookup
│   ├── pair_features.py             # Ciphertext pair / xor / SPN-aligned pair encodings
│   ├── profile.py                   # Cipher structure profile vector for MoE/routing
│   ├── spn_aligned.py               # SPN inverse-permutation-aligned differences
│   ├── arx_aligned.py               # Future ARX-aware feature namespace
│   └── feistel_aligned.py           # Future Feistel-aware feature namespace
├── models/                          # Neural distinguisher architectures
│   ├── common/                      # Shared activations, normalization, pooling
│   ├── baseline/                    # Cipher-agnostic and literature-inspired baselines
│   ├── structure/                   # Structure-aware models and experts
│   │   ├── adaptive_dbitnet.py      # Adaptive / structure-conditioned DBitNet backbones
│   │   ├── moe.py                   # Structure-aware MoE and routing
│   │   ├── spn/                     # SPN-specific experts
│   │   │   ├── cell_pairset.py
│   │   │   ├── nibble_conv_pairset.py
│   │   │   └── token_mixer_pairset.py
│   │   ├── arx/                     # Future ARX-specific experts
│   │   └── feistel/                 # Future Feistel-specific experts
│   ├── registry.py                  # Model registry for canonical model keys
├── data/                            # Differential dataset configs, generation, and disk cache
├── experiments/                     # Cipher/model factories and difference profiles
├── evaluation/                      # Result summaries and comparison utilities
└── training/                        # Binary training utilities
```

## Canonical Imports

New code should prefer these paths:

```python
from blockcipher_ai_eval.models.baseline import MlpDistinguisher
from blockcipher_ai_eval.models.common import build_activation
from blockcipher_ai_eval.models.structure import StructureAwareMoEDistinguisher
from blockcipher_ai_eval.models.structure.spn import SpnTokenMixerPairSetDistinguisher
from blockcipher_ai_eval.features.registry import pair_bits_for_encoding
from blockcipher_ai_eval.features.pair_features import encode_ciphertext_pair
from blockcipher_ai_eval.features.spn_aligned import inverse_permutation_difference
```

Avoid removed compatibility paths such as `blockcipher_ai_eval.datasets` and `blockcipher_ai_eval.models.mlp`. Use canonical package paths:

```python
from blockcipher_ai_eval.data.differential import DifferentialDatasetConfig
from blockcipher_ai_eval.data.differential.generator import make_differential_dataset
from blockcipher_ai_eval.data.cache import make_chunked_differential_dataset
from blockcipher_ai_eval.features.pair_features import int_to_bits
```

## Innovation-One Boundary

The current SPN result is built from two separate concerns:

```text
Feature side:
  src/blockcipher_ai_eval/features/spn_aligned.py
  src/blockcipher_ai_eval/features/pair_features.py

Model side:
  src/blockcipher_ai_eval/models/structure/spn/token_mixer_pairset.py
```

This keeps the paper claim clean: public SPN structure enters through an explicit aligned feature representation, and the SPN TokenMixer consumes that representation.

## Experiments

```text
experiments/
├── build_plan.py                    # Generic JSON-config -> CSV plan builder
├── build_innovation_one_matrix.py   # Literature-ranked matrix builder
├── innovation1/                     # Canonical innovation-one assets
│   ├── configs/                     # JSON plan configs
│   ├── configs/remote/              # Remote Windows GPU run specs
│   ├── plans/                       # Generated CSV matrices
│   ├── hparam_spaces/               # HPO search spaces
│   └── summaries/                   # Curated result summaries
├── run_innovation_one_matrix.py     # Main matrix runner
└── summarize_*.py                   # Thin CLI wrappers over evaluation/

archive/legacy/experiments/builders/ # Historical build_innovation1_* builders
```

Historical one-off builders are archived under `archive/legacy/experiments/builders/` for reference. New experiments use `experiments/build_plan.py` with JSON configs under `experiments/innovation1/configs/`. For example:

```bash
uv run python experiments/build_plan.py experiments/innovation1/configs/spn_present_strict_crosskey_10seed.json
```

## Remote Execution

```text
scripts/
├── generators/                           # Canonical generators for reproducible scripts/assets
├── generated/                            # Generated run/launch/schedule/monitor files
└── monitor_remote_results.py             # Generic result-branch monitor/retriever
```

Stable remote workflow:

```text
local commit/push -> remote G:/lxy/<project> pull -> run torch310 -> push results branch -> local monitor retrieves outputs/remote_results
```

Remote configs live under `experiments/innovation1/configs/remote/`. New remote experiments should prefer:

```bash
uv run python scripts/generators/generate_remote_experiment_scripts.py experiments/innovation1/configs/remote/<run>.json
```

Historical hand-written remote scripts are archived under `archive/legacy/scripts/` because they are part of prior result reproducibility, not active entry points.
