@echo off
schtasks /Create /TN innovation1_spn_present_inception_mcnd_feature_screen_gpu1_20260614 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-inception-mcnd-feature-screen-gpu1-20260614.cmd" /F
schtasks /Run /TN innovation1_spn_present_inception_mcnd_feature_screen_gpu1_20260614
schtasks /Query /TN innovation1_spn_present_inception_mcnd_feature_screen_gpu1_20260614 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_inception_mcnd_feature_screen_gpu1_20260614 /F
