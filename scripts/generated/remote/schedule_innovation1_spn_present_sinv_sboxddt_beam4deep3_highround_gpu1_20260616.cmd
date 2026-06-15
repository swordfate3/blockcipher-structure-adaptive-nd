@echo off
schtasks /Create /TN innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_gpu1_20260616 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-sinv-sboxddt-beam4deep3-highround-gpu1-20260616.cmd" /F
schtasks /Run /TN innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_gpu1_20260616
schtasks /Query /TN innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_gpu1_20260616 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_gpu1_20260616 /F
