@echo off
schtasks /Create /TN watch_after_spn_strict_spnaligned_to_sinv_strict_r7r8_20260616 /SC ONCE /ST 23:59 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\watch_after_spn_strict_spnaligned_to_sinv_strict_r7r8_20260616.ps1" /F
schtasks /Run /TN watch_after_spn_strict_spnaligned_to_sinv_strict_r7r8_20260616
schtasks /Query /TN watch_after_spn_strict_spnaligned_to_sinv_strict_r7r8_20260616 /V /FO LIST
