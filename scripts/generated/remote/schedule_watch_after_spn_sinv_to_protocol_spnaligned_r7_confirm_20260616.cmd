@echo off
schtasks /Create /TN innovation1_watch_after_spn_sinv_to_protocol_spnaligned_r7_confirm_20260616 /SC ONCE /ST 23:59 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\watch_after_spn_sinv_to_protocol_spnaligned_r7_confirm_20260616.ps1" /F
schtasks /Run /TN innovation1_watch_after_spn_sinv_to_protocol_spnaligned_r7_confirm_20260616
schtasks /Query /TN innovation1_watch_after_spn_sinv_to_protocol_spnaligned_r7_confirm_20260616 /V /FO LIST
