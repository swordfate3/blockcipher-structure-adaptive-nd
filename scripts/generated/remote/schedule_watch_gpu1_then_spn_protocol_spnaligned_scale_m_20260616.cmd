@echo off
schtasks /Create /TN innovation1_watch_gpu1_then_spn_protocol_spnaligned_scale_m_20260616 /SC ONCE /ST 23:59 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\watch_gpu1_then_schedule_innovation1_spn_present_protocol_spnaligned_scale_m_20260616.ps1" /F
schtasks /Run /TN innovation1_watch_gpu1_then_spn_protocol_spnaligned_scale_m_20260616
schtasks /Query /TN innovation1_watch_gpu1_then_spn_protocol_spnaligned_scale_m_20260616 /V /FO LIST
