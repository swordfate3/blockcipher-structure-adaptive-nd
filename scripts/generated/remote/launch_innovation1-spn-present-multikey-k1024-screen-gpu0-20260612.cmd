@echo off
setlocal
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set RUN_ID=innovation1-spn-present-multikey-k1024-screen-gpu0-20260612
set RUN_ROOT=G:\lxy\blockcipher-structure-adaptive-nd-runs
set LAUNCH_LOG_DIR=%RUN_ROOT%\launcher_logs
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %LAUNCH_LOG_DIR% mkdir %LAUNCH_LOG_DIR%
start "progress_innovation1-spn-present-multikey-k1024-screen-gpu0-20260612" cmd.exe /c powershell -NoProfile -ExecutionPolicy Bypass -Command "while ($true) { if (Test-Path 'G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-spn-present-multikey-k1024-screen-gpu0-20260612\scripts\tail_progress.py') { & 'F:\Anaconda\envs\DWT\torch310\python.exe' 'G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-spn-present-multikey-k1024-screen-gpu0-20260612\scripts\tail_progress.py' 'G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-spn-present-multikey-k1024-screen-gpu0-20260612\logs\innovation1-spn-present-multikey-k1024-screen-gpu0-20260612_progress.jsonl' --interval 5; break }; cls; Write-Host 'waiting for progress viewer G:\lxy\blockcipher-structure-adaptive-nd-runs\innovation1-spn-present-multikey-k1024-screen-gpu0-20260612\scripts\tail_progress.py'; Start-Sleep -Seconds 2 }"
call G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\run_innovation1-spn-present-multikey-k1024-screen-gpu0-20260612_and_push.cmd > %LAUNCH_LOG_DIR%\%RUN_ID%_launcher_stdout.txt 2> %LAUNCH_LOG_DIR%\%RUN_ID%_launcher_stderr.txt
endlocal
