@echo off
schtasks /Create /TN i1_spn_trailpos_r7_scale_med_gpu0_20260622 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_i1-spn-trailpos-r7-scale-med-gpu0-20260622.cmd" /F
schtasks /Run /TN i1_spn_trailpos_r7_scale_med_gpu0_20260622
schtasks /Query /TN i1_spn_trailpos_r7_scale_med_gpu0_20260622 /V /FO LIST
schtasks /Delete /TN i1_spn_trailpos_r7_scale_med_gpu0_20260622 /F
