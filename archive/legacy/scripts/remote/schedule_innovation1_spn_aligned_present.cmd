@echo off
schtasks /Create /TN innovation1_spn_aligned_present_gpu1_20260607 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1_spn_aligned_present_gpu1.cmd" /F
schtasks /Run /TN innovation1_spn_aligned_present_gpu1_20260607
schtasks /Query /TN innovation1_spn_aligned_present_gpu1_20260607 /V /FO LIST
