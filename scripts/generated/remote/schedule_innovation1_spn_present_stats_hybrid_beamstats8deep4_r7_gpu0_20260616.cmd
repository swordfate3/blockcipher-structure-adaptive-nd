@echo off
schtasks /Create /TN innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_gpu0_20260616 /SC ONCE /ST 23:59 /TR "cmd.exe /c G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\launch_innovation1-spn-present-stats-hybrid-beamstats8deep4-r7-gpu0-20260616.cmd" /F
schtasks /Run /TN innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_gpu0_20260616
schtasks /Query /TN innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_gpu0_20260616 /V /FO LIST
schtasks /Delete /TN innovation1_spn_present_stats_hybrid_beamstats8deep4_r7_gpu0_20260616 /F
