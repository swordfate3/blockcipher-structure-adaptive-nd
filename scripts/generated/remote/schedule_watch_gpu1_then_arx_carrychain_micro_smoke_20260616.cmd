@echo off
schtasks /Create /TN watch_gpu1_then_arx_carrychain_micro_smoke_20260616 /SC ONCE /ST 23:59 /TR "powershell -NoProfile -ExecutionPolicy Bypass -File G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\watch_gpu1_then_arx_carrychain_micro_smoke_20260616.ps1" /F
schtasks /Run /TN watch_gpu1_then_arx_carrychain_micro_smoke_20260616
schtasks /Query /TN watch_gpu1_then_arx_carrychain_micro_smoke_20260616 /V /FO LIST
schtasks /Delete /TN watch_gpu1_then_arx_carrychain_micro_smoke_20260616 /F
