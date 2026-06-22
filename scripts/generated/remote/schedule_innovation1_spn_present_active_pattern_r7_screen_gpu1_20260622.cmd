@echo off
schtasks /Create /TN innovation1_spn_present_active_pattern_r7_screen_gpu1_20260622 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-active-pattern-r7-screen-gpu1-20260622.cmd" /F
schtasks /Run /TN innovation1_spn_present_active_pattern_r7_screen_gpu1_20260622
schtasks /Query /TN innovation1_spn_present_active_pattern_r7_screen_gpu1_20260622 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_active_pattern_r7_screen_gpu1_20260622 /F
