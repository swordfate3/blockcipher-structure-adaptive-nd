@echo off
schtasks /Create /TN innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_20260616 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-arx-speck32-gohr-protocol-alignment-smoke-gpu1-20260616.cmd" /F
schtasks /Run /TN innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_20260616
schtasks /Query /TN innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_20260616 /V /FO LIST
schtasks /Delete /TN innovation1_arx_speck32_gohr_protocol_alignment_smoke_gpu1_20260616 /F
