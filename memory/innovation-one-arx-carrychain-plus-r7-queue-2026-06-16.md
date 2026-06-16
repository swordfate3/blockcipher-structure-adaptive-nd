# Innovation 1 ARX CarryChain-Plus r7 Queue

Date: 2026-06-16

Purpose: keep ARX/SPECK32 moving in parallel with the SPN/PRESENT high-round push.

New queued experiment:

- run id: `innovation1-arx-speck32-carrychain-plus-r7-confirm-4seed-gpu1-20260616`
- plan: `experiments/innovation1/plans/innovation1_arx_speck32_carrychain_plus_r7_confirm_4seed.csv`
- model: `arx_round_function_hybrid_pairset`
- feature: `ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_plus_bits`
- protocol: `independent_pairs`, `key_rotation_interval=1024`, train key `0x1918111009080100`, validation key `0x0f0e0d0c0b0a0908`
- scale: r7, seeds 0..3, `samples_per_class=131072`, `pairs_per_sample=4`, r6 curriculum pretrain for 6 epochs
- remote device: `cuda:1`

Rationale:

Earlier ARX `trail_mixer` r7 rows showed weak but nonrandom signal, while the strongest old ARX evidence came from public partial-inverse features. This queue tests a richer public SPECK round-boundary representation: ciphertext pair, XOR difference, rotation alignment, partial inverse, RX proxies, carry-chain masks, and addition-delta proxies. The model groups these role words using `ArxRoundFunctionHybridPairSetDistinguisher`, so this is closer to the Innovation 1 claim of ARX-structure-adaptive neural distinguishers than a plain pairset baseline.

Queue position:

Existing GPU1 queue remains:

1. `innovation1-arx-speck32-trail-mixer-curriculum-r7r8-gpu1-20260615`
2. `innovation1-arx-speck32-partial-inverse-r7-confirm-10seed-gpu1-20260616`
3. `innovation1-arx-speck32-partial-inverse-r7-clean-ablation-10seed-gpu1-20260616`
4. `innovation1-arx-speck32-round-stats-only-r7-screen-gpu1-20260616`
5. `innovation1-arx-speck32-carrychain-plus-r7-confirm-4seed-gpu1-20260616`

Success gate:

Do not claim ARX breakthrough from this queue alone. Treat it as positive if it beats the trail-mixer r7 signal and approaches or improves the previous partial-inverse r7 baseline under the corrected multi-key protocol.
