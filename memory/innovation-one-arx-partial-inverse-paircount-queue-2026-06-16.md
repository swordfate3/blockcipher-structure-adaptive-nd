# Innovation 1 ARX Partial-Inverse Pair-Count Queue

Date: 2026-06-16

Reason for insertion:

The ARX review identified `structure_adaptive_pairset_dbitnet + ciphertext_pair_xor_arx_partial_inverse_bits` as the strongest and cleanest SPECK32 r7 signal so far. Before spending more GPU time on richer carrychain features, the queue should test whether increasing independent ciphertext pairs per sample improves the strict multi-key r7 evidence.

New run:

- run id: `innovation1-arx-speck32-partial-inverse-paircount-r7-screen-gpu1-20260616`
- plan: `experiments/innovation1/plans/innovation1_arx_speck32_partial_inverse_paircount_r7_screen.csv`
- model: `structure_adaptive_pairset_dbitnet`
- features: `ciphertext_pair_xor_bits` and `ciphertext_pair_xor_arx_partial_inverse_bits`
- pairs per sample: `4` and `8`
- rounds/seeds: r7, seeds 0..3
- protocol: `independent_pairs`, `key_rotation_interval=1024`
- scale: `samples_per_class=131072`, 16 rows total

Queue order after this insertion:

1. `innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616`
2. `innovation1-arx-speck32-partial-inverse-r7-clean-ablation-10seed-gpu1-20260616`
3. `innovation1-arx-speck32-partial-inverse-paircount-r7-screen-gpu1-20260616`
4. `innovation1-arx-speck32-round-stats-only-r7-screen-gpu1-20260616`
5. `innovation1-arx-speck32-carrychain-plus-r7-confirm-4seed-gpu1-20260616`

Decision rule:

- If p8 partial-inverse clearly improves over p4 and raw p8 remains much weaker, expand p8 partial-inverse to 10 seeds.
- If p8 does not improve, keep p4 as the ARX mainline and treat carrychain/round-stats as exploratory.
