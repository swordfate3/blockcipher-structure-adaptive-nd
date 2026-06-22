@echo off
schtasks /Create /TN innovation1_spn_present_zhang_wang2022_keras_official_anchor_smoke_gpu1_20260621 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-zhang-wang2022-keras-official-anchor-smoke-gpu1-20260621.cmd" /F
schtasks /Run /TN innovation1_spn_present_zhang_wang2022_keras_official_anchor_smoke_gpu1_20260621
schtasks /Query /TN innovation1_spn_present_zhang_wang2022_keras_official_anchor_smoke_gpu1_20260621 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_zhang_wang2022_keras_official_anchor_smoke_gpu1_20260621 /F
