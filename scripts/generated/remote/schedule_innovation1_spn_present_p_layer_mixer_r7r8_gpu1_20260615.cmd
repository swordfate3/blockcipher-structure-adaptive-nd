@echo off
schtasks /Create /TN innovation1_spn_present_p_layer_mixer_r7r8_gpu1_20260615 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-p-layer-mixer-r7r8-gpu1-20260615.cmd" /F
schtasks /Run /TN innovation1_spn_present_p_layer_mixer_r7r8_gpu1_20260615
schtasks /Query /TN innovation1_spn_present_p_layer_mixer_r7r8_gpu1_20260615 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_p_layer_mixer_r7r8_gpu1_20260615 /F
