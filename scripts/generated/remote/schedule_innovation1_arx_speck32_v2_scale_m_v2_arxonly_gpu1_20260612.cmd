@echo off
schtasks /Create /TN innovation1_arx_speck32_v2_scale_m_v2_arxonly_gpu1_20260612 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-arx-speck32-v2-scale-m-v2-arxonly-gpu1-20260612.cmd" /F
schtasks /Run /TN innovation1_arx_speck32_v2_scale_m_v2_arxonly_gpu1_20260612
schtasks /Query /TN innovation1_arx_speck32_v2_scale_m_v2_arxonly_gpu1_20260612 /V /FO LIST
schtasks /Delete /TN innovation1_arx_speck32_v2_scale_m_v2_arxonly_gpu1_20260612 /F
