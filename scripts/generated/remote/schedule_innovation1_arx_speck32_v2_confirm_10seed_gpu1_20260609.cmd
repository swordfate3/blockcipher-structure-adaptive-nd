@echo off
schtasks /Create /TN innovation1_arx_speck32_v2_confirm_10seed_gpu1_20260609 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-arx-speck32-v2-confirm-10seed-gpu1-20260609.cmd" /F
schtasks /Run /TN innovation1_arx_speck32_v2_confirm_10seed_gpu1_20260609
schtasks /Query /TN innovation1_arx_speck32_v2_confirm_10seed_gpu1_20260609 /V /FO LIST
