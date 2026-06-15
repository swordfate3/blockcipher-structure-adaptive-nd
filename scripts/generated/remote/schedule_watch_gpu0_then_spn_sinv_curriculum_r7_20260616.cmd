@echo off
schtasks /Create /TN watch_gpu0_then_spn_sinv_curriculum_r7_20260616 /SC ONCE /ST 23:59 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\watch_gpu0_then_spn_sinv_curriculum_r7_20260616.ps1" /F
schtasks /Run /TN watch_gpu0_then_spn_sinv_curriculum_r7_20260616
schtasks /Query /TN watch_gpu0_then_spn_sinv_curriculum_r7_20260616 /V /FO LIST
schtasks /Delete /TN watch_gpu0_then_spn_sinv_curriculum_r7_20260616 /F
