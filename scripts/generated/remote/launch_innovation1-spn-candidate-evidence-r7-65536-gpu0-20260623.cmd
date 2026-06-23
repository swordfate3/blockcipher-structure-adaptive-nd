@echo off
setlocal
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set RUN_ID=innovation1-spn-candidate-evidence-r7-65536-gpu0-20260623
set RUN_ROOT=G:\lxy\blockcipher-structure-adaptive-nd-runs
set LAUNCH_LOG_DIR=%RUN_ROOT%\launcher_logs
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %LAUNCH_LOG_DIR% mkdir %LAUNCH_LOG_DIR%
call G:\lxy\blockcipher-structure-adaptive-nd\scripts\generated\remote\run_innovation1-spn-candidate-evidence-r7-65536-gpu0-20260623_and_push.cmd > %LAUNCH_LOG_DIR%\%RUN_ID%_launcher_stdout.txt 2> %LAUNCH_LOG_DIR%\%RUN_ID%_launcher_stderr.txt
endlocal
