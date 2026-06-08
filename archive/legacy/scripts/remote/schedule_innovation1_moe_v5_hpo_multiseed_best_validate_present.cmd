@echo off
schtasks /Create /TN innovation1_moe_v5_hpo_multiseed_best_validate_present_gpu1_20260606 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1_moe_v5_hpo_multiseed_best_validate_present_gpu1.cmd" /F
schtasks /Run /TN innovation1_moe_v5_hpo_multiseed_best_validate_present_gpu1_20260606
schtasks /Query /TN innovation1_moe_v5_hpo_multiseed_best_validate_present_gpu1_20260606 /V /FO LIST
