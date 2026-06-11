@echo off
schtasks /Create /TN innovation1_arx_speck32_v2_scale_smoke_v2_gpu1_20260611 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611.cmd" /F
schtasks /Run /TN innovation1_arx_speck32_v2_scale_smoke_v2_gpu1_20260611
schtasks /Query /TN innovation1_arx_speck32_v2_scale_smoke_v2_gpu1_20260611 /V /FO LIST
