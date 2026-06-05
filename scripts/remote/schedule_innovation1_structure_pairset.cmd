@echo off
schtasks /Create /TN innovation1_structure_pairset_gpu0_20260605 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1_structure_pairset_gpu0.cmd" /F
schtasks /Run /TN innovation1_structure_pairset_gpu0_20260605
schtasks /Create /TN innovation1_structure_pairset_gpu1_20260605 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1_structure_pairset_gpu1.cmd" /F
schtasks /Run /TN innovation1_structure_pairset_gpu1_20260605
schtasks /Query /TN innovation1_structure_pairset_gpu0_20260605 /V /FO LIST
schtasks /Query /TN innovation1_structure_pairset_gpu1_20260605 /V /FO LIST
