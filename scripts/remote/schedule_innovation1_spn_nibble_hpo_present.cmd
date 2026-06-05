@echo off
schtasks /Create /TN innovation1_spn_nibble_hpo_present_gpu1_20260605 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1_spn_nibble_hpo_present_gpu1.cmd" /F
schtasks /Run /TN innovation1_spn_nibble_hpo_present_gpu1_20260605
schtasks /Query /TN innovation1_spn_nibble_hpo_present_gpu1_20260605 /V /FO LIST
