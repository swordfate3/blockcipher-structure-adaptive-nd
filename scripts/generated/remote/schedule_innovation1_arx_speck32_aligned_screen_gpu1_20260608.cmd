@echo off
schtasks /Create /TN innovation1_arx_speck32_aligned_screen_gpu1_20260608 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1-arx-speck32-aligned-screen-gpu1-20260608.cmd" /F
schtasks /Run /TN innovation1_arx_speck32_aligned_screen_gpu1_20260608
schtasks /Query /TN innovation1_arx_speck32_aligned_screen_gpu1_20260608 /V /FO LIST
