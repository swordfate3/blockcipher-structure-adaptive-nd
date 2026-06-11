@echo off
schtasks /Create /TN innovation1_spn_gift64_aligned_screen_gpu1_20260608 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-gift64-aligned-screen-gpu1-20260608.cmd" /F
schtasks /Run /TN innovation1_spn_gift64_aligned_screen_gpu1_20260608
schtasks /Query /TN innovation1_spn_gift64_aligned_screen_gpu1_20260608 /V /FO LIST
