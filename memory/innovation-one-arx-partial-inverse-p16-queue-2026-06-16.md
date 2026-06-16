# Innovation 1 ARX Partial-Inverse p16 Queue - 2026-06-16

Purpose:

- Continue the ARX/SPECK32 Innovation 1 line instead of letting it trail the SPN/PRESENT work.
- Keep the cleanest currently supported ARX hypothesis: public keyless partial-inverse structure features should become more stable when more independent ciphertext pairs are aggregated per sample.
- Extend the existing p4/p8 strict multi-key screen with p16, keeping raw controls.

Experiment:

- run id: `innovation1-arx-speck32-partial-inverse-paircount-p16-r7-screen-gpu1-20260616`
- plan: `experiments/innovation1/plans/innovation1_arx_speck32_partial_inverse_paircount_p16_r7_screen.csv`
- model: `structure_adaptive_pairset_dbitnet`
- round: SPECK32/64 r7
- seeds: 0,1,2,3
- samples/class: 131072
- pairs/sample: 16
- features:
  - `ciphertext_pair_xor_bits` as raw control
  - `ciphertext_pair_xor_arx_partial_inverse_bits` as structure-aligned feature
- protocol:
  - `key_rotation_interval=1024`
  - `sample_structure=independent_pairs`
  - `negative_mode=encrypted_random_plaintexts`
  - `difference_profile=speck32_gohr2019`
- training:
  - 20 epochs
  - batch size 512
  - AdamW, lr 1e-4, weight decay 1e-4
  - cyclic max lr 0.002 from plan
  - checkpoint metric: `val_auc`

Queue placement:

`partial_inverse_r7_confirm`
-> `partial_inverse_r7_clean_ablation`
-> `partial_inverse_paircount_r7_screen` (p4/p8)
-> `partial_inverse_paircount_p16_r7_screen`
-> `round_stats_only_r7_screen`
-> `carrychain_plus_r7_confirm`

Interpretation:

- If p16 partial-inverse improves over p4/p8 and raw p16 stays near random, the ARX structure feature has a stronger pair-count scaling story.
- If p16 does not improve, the ARX line should prioritize protocol-corrected p4/p8 confirmation and avoid over-claiming larger pair count.
