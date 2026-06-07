@echo off
schtasks /Create /TN innovation1_spn_crosskey_negative_present_gpu0_20260607 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1-spn-crosskey-negative-present-gpu0-20260607.cmd" /F
schtasks /Run /TN innovation1_spn_crosskey_negative_present_gpu0_20260607
schtasks /Query /TN innovation1_spn_crosskey_negative_present_gpu0_20260607 /V /FO LIST
schtasks /Create /TN innovation1_spn_input_ablation_present_gpu1_20260607 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1-spn-input-ablation-present-gpu1-20260607.cmd" /F
schtasks /Run /TN innovation1_spn_input_ablation_present_gpu1_20260607
schtasks /Query /TN innovation1_spn_input_ablation_present_gpu1_20260607 /V /FO LIST
