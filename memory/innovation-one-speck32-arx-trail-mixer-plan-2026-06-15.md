# Innovation 1 SPECK32 ARX TrailMixer Plan - 2026-06-15

## Context

ARX progression should continue alongside the PRESENT/SPN high-round push. The current ARX evidence is SPECK32/64-specific: the strongest retrieved result remains r7 `structure_adaptive_pairset_dbitnet` with `ciphertext_pair_xor_arx_partial_inverse_bits`, `pairs_per_sample=4`, `samples_per_class=131072`, and `key_rotation_interval=1024` at about `cal_acc_mean=0.789639`, `auc_mean=0.869151` over seeds 0..3.

Goodall's read-only audit confirmed the minimum ARX gap is not cipher implementation: SPECK32, CHAM64, and LEA are implemented. The immediate gap is structure-specific ARX modeling: current ARX public features are SPECK32-only and the existing `arx_word_mixer_pairset` treats only the 7 partial-inverse 32-bit feature words. CHAM/LEA expansion should wait until the SPECK32 route proves useful.

## New Candidate

Implemented `arx_trail_mixer_pairset` in `src/blockcipher_ai_eval/models/structure/arx/trail_mixer_pairset.py`.

Design intent:

- Inputs are public SPECK32 trail-style pair features, especially `ciphertext_pair_xor_arx_partial_inverse_rx_bits`.
- Each pair is interpreted as 32-bit feature words, split into two 16-bit SPECK words.
- The model keeps feature-word roles explicit through embeddings.
- It uses SPECK-style ROR7/ROL2 message paths and carry proxy mixing via `ArxWordMixerBlock`.
- It adds a role-level Transformer over feature-word roles, then pair-set evidence pooling.

Default protocol shape:

- `partial_inverse_rx` gives 11 public 32-bit words per pair, so `pair_bits=352`.
- For `pairs_per_sample=4`, model input is 1408 bits.

## Verification

Local checks passed:

- `tests/test_adaptive_dbitnet_model.py::test_arx_trail_mixer_pairset_preserves_rx_trail_words_and_evidence_pooling`
- `tests/test_adaptive_dbitnet_model.py::test_build_model_supports_arx_trail_mixer_pairset_key_and_options`
- `tests/test_feature_encodings.py::test_pair_features_module_encodes_speck_arx_partial_inverse_rx_pair_features`
- CPU true-training smoke wrote `outputs/smoke_arx_trail_mixer_pairset.jsonl` with 1 row.

Also fixed summary grouping by adding `feature_encoding` to innovation-one summary groups so ARX feature ablations are not merged.

## Remote Experiment

New plan:

`experiments/innovation1/plans/innovation1_arx_speck32_trail_mixer_curriculum_r7r8_screen.csv`

Rows: 8

- `arx_trail_mixer_pairset + ciphertext_pair_xor_arx_partial_inverse_rx_bits`
- `arx_word_mixer_pairset + ciphertext_pair_xor_arx_partial_inverse_bits` as same-protocol control
- rounds 7 and 8
- seeds 0 and 1
- `samples_per_class`: r7=131072, r8=262144
- `pairs_per_sample=4`
- `pretrain_rounds=6`, `pretrain_epochs=6`
- `key_rotation_interval=1024`
- `loss=mse`, `optimizer=adam`, cyclic LR, checkpoint by `val_auc`

Run id:

`innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`

Expected gate:

- 8 JSONL rows
- result branch `results/innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`
- compare r7 against retrieved ARX baseline `0.789639/0.869151`
- treat r8 as exploratory unless clearly above random with clean stderr and consistent seeds

## Next

Commit and push this branch, sync remote `G:/lxy/blockcipher-structure-adaptive-nd`, then launch through Task Scheduler only when GPU1 is free. Do not stop existing SPN/PRESENT high-round tasks to run this.
