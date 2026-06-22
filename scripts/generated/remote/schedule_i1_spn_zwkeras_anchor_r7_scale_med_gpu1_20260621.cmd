@echo off
schtasks /Create /TN i1_spn_zwkeras_anchor_r7_scale_med_gpu1_20260621 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_i1-spn-zwkeras-anchor-r7-scale-med-gpu1-20260621.cmd" /F
schtasks /Run /TN i1_spn_zwkeras_anchor_r7_scale_med_gpu1_20260621
schtasks /Query /TN i1_spn_zwkeras_anchor_r7_scale_med_gpu1_20260621 /V /FO LIST
schtasks /Delete /TN i1_spn_zwkeras_anchor_r7_scale_med_gpu1_20260621 /F
