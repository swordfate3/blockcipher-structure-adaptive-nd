@echo off
schtasks /Create /TN innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_20260616 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-arx-speck32-round-hybrid-rx-r7-confirm-10seed-gpu0-20260616.cmd" /F
schtasks /Run /TN innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_20260616
schtasks /Query /TN innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_20260616 /V /FO LIST
schtasks /Delete /TN innovation1_arx_speck32_round_hybrid_rx_r7_confirm_10seed_gpu0_20260616 /F
