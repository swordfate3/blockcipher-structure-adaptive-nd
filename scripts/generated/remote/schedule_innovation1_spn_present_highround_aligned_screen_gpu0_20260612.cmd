@echo off
schtasks /Create /TN innovation1_spn_present_highround_aligned_screen_gpu0_20260612 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-highround-aligned-screen-gpu0-20260612.cmd" /F
schtasks /Run /TN innovation1_spn_present_highround_aligned_screen_gpu0_20260612
schtasks /Query /TN innovation1_spn_present_highround_aligned_screen_gpu0_20260612 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_highround_aligned_screen_gpu0_20260612 /F
