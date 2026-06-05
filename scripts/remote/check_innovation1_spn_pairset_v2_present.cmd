@echo off
echo ====NVIDIA_SMI====
nvidia-smi
echo ====TASKLIST_PYTHON====
tasklist /FI "IMAGENAME eq python.exe" /V
echo ====SCHEDULED_TASK====
schtasks /Query /TN innovation1_spn_pairset_v2_present_gpu1_20260605 /V /FO LIST
echo ====RESULTS_DIR====
dir G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-spn-pairset-v2-present-gpu1-20260605\results
echo ====LOGS_DIR====
dir G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-spn-pairset-v2-present-gpu1-20260605\logs
