@echo off
schtasks /Create /TN innovation1_spn_present_delta_paligned_matrix_screen_gpu0_20260615 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-delta-paligned-matrix-screen-gpu0-20260615.cmd" /F
schtasks /Run /TN innovation1_spn_present_delta_paligned_matrix_screen_gpu0_20260615
schtasks /Query /TN innovation1_spn_present_delta_paligned_matrix_screen_gpu0_20260615 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_delta_paligned_matrix_screen_gpu0_20260615 /F
