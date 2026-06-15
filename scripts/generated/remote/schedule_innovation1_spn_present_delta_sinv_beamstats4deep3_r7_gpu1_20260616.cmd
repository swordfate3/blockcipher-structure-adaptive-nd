@echo off
schtasks /Create /TN innovation1_spn_present_delta_sinv_beamstats4deep3_r7_gpu1_20260616 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-delta-sinv-beamstats4deep3-r7-gpu1-20260616.cmd" /F
schtasks /Run /TN innovation1_spn_present_delta_sinv_beamstats4deep3_r7_gpu1_20260616
schtasks /Query /TN innovation1_spn_present_delta_sinv_beamstats4deep3_r7_gpu1_20260616 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_delta_sinv_beamstats4deep3_r7_gpu1_20260616 /F
