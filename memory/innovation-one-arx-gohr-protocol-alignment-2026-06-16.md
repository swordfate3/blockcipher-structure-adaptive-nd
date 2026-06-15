# Innovation 1 ARX Gohr Protocol Alignment - 2026-06-16

## Context

Innovation 1 needs ARX progress, not only SPN/PRESENT. The previous SPECK32/64
ARX carrychain-plus micro smoke completed on the remote A6000 node and showed
that public carry-chain feature stacking alone does not produce a useful r7
signal.

## Completed Remote Result

Run id:

```text
innovation1-arx-speck32-carrychain-plus-micro-smoke-gpu1-20260616
```

Remote gate:

```text
result_lines=2
expected_rows=2
```

Local archive:

```text
outputs/remote_results/innovation1-arx-speck32-carrychain-plus-micro-smoke-gpu1-20260616/
```

Metrics:

```text
r6: accuracy ~= 0.8330, calibrated_accuracy ~= 0.8341, AUC ~= 0.8948
r7: accuracy = 0.5000, calibrated_accuracy ~= 0.5084, AUC ~= 0.5049
```

Conclusion:

```text
carrychain-plus keeps r6 learnable but remains random at r7 in the tiny smoke.
Do not scale carrychain-plus blindly.
```

## New ARX Direction

Next experiment is a protocol-alignment smoke matrix:

```text
experiments/innovation1/plans/innovation1_arx_speck32_gohr_protocol_alignment_smoke.csv
```

It compares under the same SPECK32/64 Gohr 2019 difference profile:

```text
1. gohr_resnet_speck_depth10, ciphertext_pair_bits, pairs_per_sample=1
2. structure_adaptive_pairset_dbitnet, ciphertext_pair_xor_bits, pairs_per_sample=4
3. structure_adaptive_pairset_dbitnet, ciphertext_pair_xor_arx_partial_inverse_bits, pairs_per_sample=4
4. arx_round_function_hybrid_pairset, ciphertext_pair_xor_arx_partial_inverse_rx_bits, pairs_per_sample=4
5. arx_round_function_hybrid_pairset, ciphertext_pair_xor_arx_partial_inverse_rx_carrychain_bits, pairs_per_sample=4
```

Rounds:

```text
r6 and r7, seed=0, samples_per_class=16384
```

Training:

```text
loss=mse
optimizer=adam
lr_scheduler=cyclic
checkpoint_metric=val_auc
r7 pretrains from r6 for 3 epochs
key_rotation_interval=1024
sample_structure=independent_pairs
```

Remote config:

```text
experiments/innovation1/configs/remote/innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_20260616.json
```

Generated scripts:

```text
scripts/generated/remote/run_innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616_and_push.cmd
scripts/generated/remote/launch_innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616.cmd
scripts/generated/remote/schedule_innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_20260616.cmd
scripts/generated/monitors/monitor_innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_results.sh
```

## Verification

Tests passed:

```text
uv run pytest tests/test_build_plan_config.py::test_speck32_arx_gohr_protocol_alignment_smoke_plan_shape tests/test_gohr_speck_model.py tests/test_adaptive_dbitnet_model.py::test_arx_round_function_hybrid_pairset_preserves_rx_groups_and_evidence_pooling tests/test_adaptive_dbitnet_model.py::test_arx_round_function_hybrid_pairset_exposes_carrychain_role_groups tests/test_remote_script_generator.py -q

15 passed, 2 warnings
```

Tiny local CLI checks passed:

```text
gohr_resnet_speck_depth10 + ciphertext_pair_bits + pairs_per_sample=1
arx_round_function_hybrid_pairset + ciphertext_pair_xor_arx_partial_inverse_rx_bits + pairs_per_sample=4
```

## Decision Rule

If protocol-alignment smoke shows that Gohr depth10 learns r7 but ARX pairset
does not, focus on ARX model/protocol adaptation. If neither learns r7 at this
scale, first increase data/epochs for Gohr baseline before claiming ARX failure.

If any ARX structure-adaptive row gives clear r7 signal, scale that row to
multi-seed confirm.
