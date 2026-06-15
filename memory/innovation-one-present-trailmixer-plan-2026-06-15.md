# Innovation 1 PRESENT TrailMixer Plan - 2026-06-15

Goal remains PRESENT/SPN high-round improvement. This entry records a model-side candidate, not a completed breakthrough.

## New Model

```text
present_trail_mixer_pairset
```

Implementation:

```text
src/blockcipher_ai_eval/models/structure/spn/present_trail_mixer.py
```

Registration:

```text
src/blockcipher_ai_eval/models/structure/spn/__init__.py
src/blockcipher_ai_eval/models/structure/__init__.py
src/blockcipher_ai_eval/models/registry.py
src/blockcipher_ai_eval/experiments/factories.py
```

The model is designed for multi-word PRESENT public trail features such as SBox-DDT back2 and beam2. Unlike `present_p_layer_mixer_pairset`, it keeps the 64-bit word role axis explicit. Each pair is treated as:

```text
words_per_pair x 16 nibbles x 4 bits
```

It uses:

```text
nibble encoder
word-role embedding
P-layer message passing over nibble tokens
role-level Transformer mixer over public trail words
pair-set evidence pooling
```

This is intended to test whether a network that knows which 64-bit word is `Delta`, `InvP(Delta)`, DDT candidate, confidence, or beam-disagreement can use SBox-DDT trail hints better than generic matrix or P-layer token models.

## Remote Experiment

```text
run_id: innovation1-spn-present-sboxddt-trailmixer-highround-screen-gpu0-20260615
expected_rows: 4
model: present_trail_mixer_pairset
features:
  present_pair_xor_paligned_sboxddt_back2_cell_matrix_bits
  present_pair_xor_paligned_sboxddt_beam2_cell_matrix_bits
rounds: 7,8
seed: 0
samples_per_class: 65536
pairs_per_sample: 16
key_rotation_interval: 1024
sample_structure: zhang_wang_case2_mcnd
device: cuda:0
```

Files:

```text
experiments/innovation1/plans/innovation1_spn_present_sboxddt_trailmixer_highround_screen.csv
experiments/innovation1/configs/remote/innovation1_spn_present_sboxddt_trailmixer_highround_screen_gpu0_20260615.json
scripts/generated/remote/run_innovation1-spn-present-sboxddt-trailmixer-highround-screen-gpu0-20260615_and_push.cmd
scripts/generated/remote/launch_innovation1-spn-present-sboxddt-trailmixer-highround-screen-gpu0-20260615.cmd
scripts/generated/remote/schedule_innovation1_spn_present_sboxddt_trailmixer_highround_screen_gpu0_20260615.cmd
scripts/generated/monitors/monitor_innovation1_spn_present_sboxddt_trailmixer_highround_screen_gpu0_results.sh
scripts/generated/monitors/relay_after_spn_sboxddt_beam2_to_trailmixer.sh
```

The relay chain now extends to:

```text
SBoxDDT highround -> top2 -> back2 -> beam2 -> trailmixer
```

## Verification

Local checks completed:

```text
pytest tests/test_adaptive_dbitnet_model.py::test_present_trail_mixer_pairset_preserves_word_roles_and_evidence_pooling
pytest tests/test_adaptive_dbitnet_model.py::test_build_model_supports_present_trail_mixer_pairset_key_and_options
pytest tests/test_feature_encodings.py::test_present_paligned_sboxddt_beam2_cell_matrix_encoding_preserves_beam_uncertainty
3 passed
```

Tiny true-training smoke completed:

```text
run_innovation_one_matrix.py with present_trail_mixer_pairset + beam2 feature, PRESENT r2, CPU, 1 epoch, wrote 1 JSONL row
```

## Interpretation Rule

The TrailMixer run only becomes evidence if the remote result branch gates at 4 rows and metrics beat the matching matrix/PLayerMixer SBox-DDT candidates. If it does not improve r7/r8, next model-side escalation should consider larger token_dim/depth, role-specific heads, or beam width > 2.
