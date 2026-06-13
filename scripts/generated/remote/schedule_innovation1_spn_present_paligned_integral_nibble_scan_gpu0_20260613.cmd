@echo off
schtasks /Create /TN innovation1_spn_present_paligned_integral_nibble_scan_gpu0_20260613 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-paligned-integral-nibble-scan-gpu0-20260613.cmd" /F
schtasks /Run /TN innovation1_spn_present_paligned_integral_nibble_scan_gpu0_20260613
schtasks /Query /TN innovation1_spn_present_paligned_integral_nibble_scan_gpu0_20260613 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_paligned_integral_nibble_scan_gpu0_20260613 /F
