@echo off
schtasks /Create /TN innovation1_spn_strict_crosskey_10seed_present_gpu0_20260608 /SC ONCE /ST 23:59 /TR "cmd.exe /c C:\Users\1304Lijinlin\launch_innovation1-spn-strict-crosskey-10seed-present-gpu0-20260608.cmd" /F
schtasks /Run /TN innovation1_spn_strict_crosskey_10seed_present_gpu0_20260608
schtasks /Query /TN innovation1_spn_strict_crosskey_10seed_present_gpu0_20260608 /V /FO LIST
