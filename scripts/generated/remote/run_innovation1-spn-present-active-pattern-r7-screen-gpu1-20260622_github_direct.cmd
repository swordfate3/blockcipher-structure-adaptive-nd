@echo off
setlocal
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set RESULT_REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set BRANCH=refactor/model-project-structure
set GITHUB_SSH_KEY=%ROOT%\.ssh\github_blockcipher_20260612_result_pusher_ed25519
set GIT_SSH_COMMAND=ssh -i %GITHUB_SSH_KEY% -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new
set RUN_ID=innovation1-spn-present-active-pattern-r7-screen-gpu1-20260622
set EXPECTED_ROWS=2
set RUN_ROOT=%ROOT%\%PROJECT_ID%-runs
set RUN_DIR=%RUN_ROOT%\%RUN_ID%
set ARCHIVE_WORK=%ROOT%\archive_work\spn_present_active_pattern_r7_screen_gpu1_20260622
set PY=F:\Anaconda\envs\DWT\torch310\python.exe

if not exist %ROOT% mkdir %ROOT%
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %ROOT%\archive_work mkdir %ROOT%\archive_work
git config --global core.longpaths true

cd /d %RUN_ROOT%
if exist %RUN_ID% rmdir /s /q %RUN_ID%
git -c core.longpaths=true -c http.proxy= -c https.proxy= clone %REPO_URL% %RUN_ID%
if errorlevel 1 goto clone_failed

cd /d %RUN_DIR%
git config --global --add safe.directory %RUN_DIR%
git config core.longpaths true
git fetch origin %BRANCH%
if errorlevel 1 goto git_sync_failed
git checkout %BRANCH%
if errorlevel 1 goto git_sync_failed
git merge --ff-only FETCH_HEAD
if errorlevel 1 goto git_sync_failed
set PYTHONPATH=%RUN_DIR%\src;%PYTHONPATH%

if not exist logs mkdir logs
if not exist results mkdir results
git rev-parse HEAD > logs\%RUN_ID%_git_revision.txt
git status --short --branch > logs\%RUN_ID%_git_status_before_run.txt
nvidia-smi > logs\%RUN_ID%_gpu_info.txt
%PY% -c "import sys, torch; print('python', sys.executable); print('torch', torch.__version__); print('cuda_version', torch.version.cuda); print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print('device1', torch.cuda.get_device_name(1) if torch.cuda.is_available() and torch.cuda.device_count() > 1 else 'NA')" > logs\%RUN_ID%_torch_info.txt 2> logs\%RUN_ID%_torch_info_stderr.txt

set GPU_BUSY_COUNT=0
for /f "usebackq delims=" %%P in (`wmic process where "name='python.exe'" get CommandLine /VALUE ^| findstr /I /C:"run_spn_active_pattern_baseline.py" ^| findstr /I /C:"--device cuda:1"`) do set /a GPU_BUSY_COUNT+=1
echo gpu_guard_device=cuda:1 > logs\%RUN_ID%_gpu_guard.txt
echo gpu_busy_count=%GPU_BUSY_COUNT% >> logs\%RUN_ID%_gpu_guard.txt
if not "%GPU_BUSY_COUNT%"=="0" goto gpu_busy

%PY% experiments\innovation1\run_spn_active_pattern_baseline.py --output results\%RUN_ID%_seed0.jsonl --rounds 7 --seed 0 --samples-per-class 65536 --pairs-per-sample 16 --feature-encoding present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits --negative-mode encrypted_random_plaintexts --sample-structure zhang_wang_case2_mcnd --epochs 20 --learning-rate 0.01 --device cuda:1 >> logs\%RUN_ID%_stdout.txt 2>> logs\%RUN_ID%_stderr.txt
if errorlevel 1 goto run_failed
%PY% experiments\innovation1\run_spn_active_pattern_baseline.py --output results\%RUN_ID%_seed1.jsonl --rounds 7 --seed 1 --samples-per-class 65536 --pairs-per-sample 16 --feature-encoding present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits --negative-mode encrypted_random_plaintexts --sample-structure zhang_wang_case2_mcnd --epochs 20 --learning-rate 0.01 --device cuda:1 >> logs\%RUN_ID%_stdout.txt 2>> logs\%RUN_ID%_stderr.txt
if errorlevel 1 goto run_failed

copy /b results\%RUN_ID%_seed0.jsonl+results\%RUN_ID%_seed1.jsonl results\%RUN_ID%.jsonl
set RESULT_LINES=0
for /f %%L in ('%PY% -c "from pathlib import Path; p=Path(r'results\%RUN_ID%.jsonl'); print(sum(1 for _ in p.open('rb')))"') do set RESULT_LINES=%%L
echo result_lines=%RESULT_LINES% > logs\%RUN_ID%_result_gate.txt
echo expected_rows=%EXPECTED_ROWS% >> logs\%RUN_ID%_result_gate.txt
echo runner_exit_code=0 >> logs\%RUN_ID%_result_gate.txt
if not "%RESULT_LINES%"=="%EXPECTED_ROWS%" goto incomplete_results

%PY% experiments\innovation1\summarize_spn_active_pattern.py results\%RUN_ID%.jsonl > results\%RUN_ID%_summary.txt 2> logs\%RUN_ID%_summary_stderr.txt
if errorlevel 1 goto summary_failed

if exist %ARCHIVE_WORK% rmdir /s /q %ARCHIVE_WORK%
git -c core.longpaths=true clone --local %RUN_DIR% %ARCHIVE_WORK%
if errorlevel 1 goto archive_clone_failed
cd /d %ARCHIVE_WORK%
git config --global --add safe.directory %ARCHIVE_WORK%
git config user.name "fate"
git config user.email "2968195987@qq.com"
git remote set-url origin %RESULT_REPO_URL%
if errorlevel 1 goto push_failed
git checkout -B results/%RUN_ID%
if errorlevel 1 goto push_failed
if exist results_archive\%RUN_ID% rmdir /s /q results_archive\%RUN_ID%
mkdir results_archive\%RUN_ID%
copy "%RUN_DIR%\results\%RUN_ID%.jsonl" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\results\%RUN_ID%_summary.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\experiments\innovation1\plans\innovation1_spn_present_active_pattern_r7_screen.csv" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_revision.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_status_before_run.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_gpu_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info_stderr.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_gpu_guard.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_stdout.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_stderr.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_result_gate.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_summary_stderr.txt" "results_archive\%RUN_ID%\"

echo run_id=%RUN_ID%> results_archive\%RUN_ID%\run_manifest.txt
echo project_id=%PROJECT_ID%>> results_archive\%RUN_ID%\run_manifest.txt
echo run_dir=%RUN_DIR%>> results_archive\%RUN_ID%\run_manifest.txt
echo archive_work=%ARCHIVE_WORK%>> results_archive\%RUN_ID%\run_manifest.txt
echo branch=%BRANCH%>> results_archive\%RUN_ID%\run_manifest.txt
echo plan=experiments\innovation1\plans\innovation1_spn_present_active_pattern_r7_screen.csv>> results_archive\%RUN_ID%\run_manifest.txt
echo device=cuda:1>> results_archive\%RUN_ID%\run_manifest.txt
echo expected_rows=%EXPECTED_ROWS%>> results_archive\%RUN_ID%\run_manifest.txt
echo samples_per_class=65536>> results_archive\%RUN_ID%\run_manifest.txt
echo pairs_per_sample=16>> results_archive\%RUN_ID%\run_manifest.txt
echo feature_encoding=present_delta_paligned_sinv_sboxddt_beamstats4deep3_cell_matrix_bits>> results_archive\%RUN_ID%\run_manifest.txt
echo negative_mode=encrypted_random_plaintexts>> results_archive\%RUN_ID%\run_manifest.txt
echo sample_structure=zhang_wang_case2_mcnd>> results_archive\%RUN_ID%\run_manifest.txt
echo launch_mode=github_direct_clean_run_clone>> results_archive\%RUN_ID%\run_manifest.txt
echo claim_scope=SCREEN only: active-pattern baseline route for PRESENT r7 at 65536/class on GPU1; not formal or breakthrough evidence>> results_archive\%RUN_ID%\run_manifest.txt

if not exist "results_archive\%RUN_ID%\%RUN_ID%.jsonl" goto archive_incomplete
if not exist "results_archive\%RUN_ID%\%RUN_ID%_summary.txt" goto archive_incomplete
if not exist "results_archive\%RUN_ID%\%RUN_ID%_result_gate.txt" goto archive_incomplete
if not exist "results_archive\%RUN_ID%\run_manifest.txt" goto archive_incomplete
echo archive_integrity=pass > results_archive\%RUN_ID%\archive_integrity.txt
git add results_archive\%RUN_ID%
git commit -m "results: %RUN_ID% remote run"
git push origin results/%RUN_ID%
if errorlevel 1 goto push_failed

echo RUN_GATE_PASS
echo RUN_DIR %RUN_DIR%
type "%RUN_DIR%\logs\%RUN_ID%_git_revision.txt"
type "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt"
type "%RUN_DIR%\logs\%RUN_ID%_result_gate.txt"
exit /b 0

:clone_failed
echo RUN_GATE_BLOCKED_CLONE_FAILED
exit /b 12

:git_sync_failed
echo RUN_GATE_BLOCKED_GIT_SYNC_FAILED
exit /b 13

:gpu_busy
echo RUN_GATE_BLOCKED_GPU_BUSY
type logs\%RUN_ID%_gpu_guard.txt
exit /b 5

:run_failed
echo RUN_GATE_BLOCKED_RUN_FAILED
type logs\%RUN_ID%_stderr.txt
exit /b 1

:incomplete_results
echo RUN_GATE_BLOCKED_INCOMPLETE_RESULTS
type logs\%RUN_ID%_result_gate.txt
exit /b 4

:summary_failed
echo RUN_GATE_BLOCKED_SUMMARY_FAILED
type logs\%RUN_ID%_summary_stderr.txt
exit /b 2

:archive_clone_failed
echo RUN_GATE_BLOCKED_ARCHIVE_CLONE_FAILED
exit /b 10

:archive_incomplete
echo RUN_GATE_BLOCKED_ARCHIVE_INCOMPLETE
dir results_archive\%RUN_ID%
exit /b 11

:push_failed
echo RUN_GATE_BLOCKED_PUSH_FAILED
exit /b 3
