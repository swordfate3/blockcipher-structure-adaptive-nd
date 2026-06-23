@echo off
setlocal
set TASK_NAME=innovation1_spn_candidate_evidence_r7_65536_gpu0_20260623
schtasks /Create /TN %TASK_NAME% /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd-runs\launchers\launch_innovation1-spn-candidate-evidence-r7-65536-gpu0-20260623.cmd" /F
schtasks /Run /TN %TASK_NAME%
schtasks /Query /TN %TASK_NAME% /V /FO LIST
endlocal
