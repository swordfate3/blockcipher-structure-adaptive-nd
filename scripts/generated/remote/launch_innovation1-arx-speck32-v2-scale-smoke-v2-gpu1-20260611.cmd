@echo off
setlocal
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set RUN_ID=innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611
set RUN_ROOT=G:\lxy\blockcipher-structure-adaptive-nd-runs
set LAUNCH_LOG_DIR=%RUN_ROOT%\launcher_logs
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %LAUNCH_LOG_DIR% mkdir %LAUNCH_LOG_DIR%
start "progress_innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611" cmd.exe /k powershell -NoProfile -ExecutionPolicy Bypass -Command "while ($true) { if (Test-Path 'G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611\scripts\tail_progress.py') { & 'F:\Anaconda\envs\DWT\torch310\python.exe' 'G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611\scripts\tail_progress.py' 'G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611\logs\innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611_progress.jsonl' --interval 5; break }; cls; Write-Host 'waiting for progress viewer G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611\scripts\tail_progress.py'; Start-Sleep -Seconds 2 }"
call G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\run_innovation1-arx-speck32-v2-scale-smoke-v2-gpu1-20260611_and_push.cmd > %LAUNCH_LOG_DIR%\%RUN_ID%_launcher_stdout.txt 2> %LAUNCH_LOG_DIR%\%RUN_ID%_launcher_stderr.txt
endlocal
