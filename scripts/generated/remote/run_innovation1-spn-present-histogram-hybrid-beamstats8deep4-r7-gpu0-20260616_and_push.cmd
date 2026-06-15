@echo off
setlocal
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set PROJECT_DIR=%ROOT%\%PROJECT_ID%
set CLONE_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set RESULT_REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set BRANCH=refactor/model-project-structure
set GITHUB_SSH_KEY=C:/Users/1304Lijinlin/.ssh/github_blockcipher_20260612_result_pusher_ed25519
set GIT_SSH_COMMAND=ssh -i %GITHUB_SSH_KEY% -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new
set RUN_ID=innovation1-spn-present-histogram-hybrid-beamstats8deep4-r7-gpu0-20260616
set EXPECTED_ROWS=4
set RUN_ROOT=%ROOT%\%PROJECT_ID%-runs
set RUN_DIR=%RUN_ROOT%\%RUN_ID%
set ARCHIVE_WORK=%ROOT%\archive_work\spn_present_histogram_hybrid_beamstats8deep4_r7_gpu0_20260616
set PY=F:\Anaconda\envs\DWT\torch310\python.exe
set PYTHONPATH=%RUN_DIR%\src;%PYTHONPATH%

if not exist %ROOT% mkdir %ROOT%
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %ROOT%\archive_work mkdir %ROOT%\archive_work
git config --global core.longpaths true
cd /d %ROOT%
if not exist %PROJECT_DIR% (
  git -c core.longpaths=true -c http.proxy= -c https.proxy= clone %CLONE_URL% %PROJECT_ID%
)

cd /d %PROJECT_DIR%
git config --global --add safe.directory %PROJECT_DIR%
git config --global --add safe.directory %PROJECT_DIR%\.git
git fetch origin %BRANCH%
git checkout %BRANCH%
git merge --ff-only FETCH_HEAD

cd /d %RUN_ROOT%
if exist %RUN_ID% rmdir /s /q %RUN_ID%
git -c core.longpaths=true clone --local %PROJECT_DIR% %RUN_ID%

cd /d %RUN_DIR%
git config --global --add safe.directory %RUN_DIR%
git config core.longpaths true
git checkout %BRANCH%
git remote set-url origin %REPO_URL%

if not exist logs mkdir logs
if not exist results mkdir results
if not exist dataset_cache mkdir dataset_cache
if exist logs\%RUN_ID%_stdout.txt del logs\%RUN_ID%_stdout.txt
if exist logs\%RUN_ID%_stderr.txt del logs\%RUN_ID%_stderr.txt
if exist logs\%RUN_ID%_progress.jsonl del logs\%RUN_ID%_progress.jsonl
if exist results\%RUN_ID%.jsonl del results\%RUN_ID%.jsonl
if exist results\%RUN_ID%_summary.csv del results\%RUN_ID%_summary.csv

git rev-parse HEAD > logs\%RUN_ID%_git_revision.txt
git status --short --branch > logs\%RUN_ID%_git_status_before_run.txt
nvidia-smi > logs\%RUN_ID%_gpu_info.txt
%PY% -c "import sys, torch; print('python', sys.executable); print('torch', torch.__version__); print('cuda_version', torch.version.cuda); print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print('device0', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NA')" > logs\%RUN_ID%_torch_info.txt 2> logs\%RUN_ID%_torch_info_stderr.txt

set GPU_BUSY_COUNT=0
for /f "usebackq delims=" %%P in (`wmic process where "name='python.exe'" get CommandLine /VALUE ^| findstr /I /C:"run_innovation_one_matrix.py" ^| findstr /I /C:"--device cuda:0"`) do set /a GPU_BUSY_COUNT+=1
echo gpu_guard_device=cuda:0 > logs\%RUN_ID%_gpu_guard.txt
echo gpu_busy_count=%GPU_BUSY_COUNT% >> logs\%RUN_ID%_gpu_guard.txt
if not "%GPU_BUSY_COUNT%"=="0" goto gpu_busy


%PY% experiments\run_innovation_one_matrix.py --plan experiments\innovation1\plans\innovation1_spn_present_histogram_hybrid_beamstats8deep4_r7_screen.csv --epochs 16 --batch-size 64 --hidden-bits 32 --learning-rate 0.0001 --optimizer adam --weight-decay 1e-05 --key-rotation-interval 1024 --sample-structure zhang_wang_case2_mcnd --integral-active-nibble 0 --device cuda:0 --dataset-cache-root dataset_cache --dataset-cache-chunk-size 512 --checkpoint-metric val_auc --restore-best-checkpoint --early-stopping-patience 0 --early-stopping-min-delta 0 --progress-output logs\%RUN_ID%_progress.jsonl --output results\%RUN_ID%.jsonl > logs\%RUN_ID%_stdout.txt 2> logs\%RUN_ID%_stderr.txt
if errorlevel 1 goto run_failed

set RESULT_LINES=0
for /f "tokens=3" %%L in ('find /c /v "" results\%RUN_ID%.jsonl') do set RESULT_LINES=%%L
echo result_lines=%RESULT_LINES% > logs\%RUN_ID%_result_gate.txt
echo expected_rows=%EXPECTED_ROWS% >> logs\%RUN_ID%_result_gate.txt
if not "%RESULT_LINES%"=="%EXPECTED_ROWS%" goto incomplete_results

if exist experiments\summarize_innovation_one_results.py (
  %PY% experiments\summarize_innovation_one_results.py --input results\%RUN_ID%.jsonl --output results\%RUN_ID%_summary.csv > logs\%RUN_ID%_summary_stdout.txt 2> logs\%RUN_ID%_summary_stderr.txt
)
if not exist results\%RUN_ID%_summary.csv (
  echo summary_status=fallback_missing_summarizer > logs\%RUN_ID%_summary_stdout.txt
  echo run_id,result_lines,expected_rows > results\%RUN_ID%_summary.csv
  echo %RUN_ID%,%RESULT_LINES%,%EXPECTED_ROWS% >> results\%RUN_ID%_summary.csv
  if not exist logs\%RUN_ID%_summary_stderr.txt echo summary_fallback_no_stderr > logs\%RUN_ID%_summary_stderr.txt
)

if exist %ARCHIVE_WORK% rmdir /s /q %ARCHIVE_WORK%
git -c core.longpaths=true clone --local %RUN_DIR% %ARCHIVE_WORK%
cd /d %ARCHIVE_WORK%
git config --global --add safe.directory %ARCHIVE_WORK%
git config user.name "fate"
git config user.email "2968195987@qq.com"
git remote set-url origin %RESULT_REPO_URL%
git checkout -B results/%RUN_ID%
if exist results_archive\%RUN_ID% rmdir /s /q results_archive\%RUN_ID%
mkdir results_archive\%RUN_ID%
copy "%RUN_DIR%\results\%RUN_ID%.jsonl" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\results\%RUN_ID%_summary.csv" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\experiments\innovation1\plans\innovation1_spn_present_histogram_hybrid_beamstats8deep4_r7_screen.csv" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_revision.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_status_before_run.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_gpu_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info_stderr.txt" "results_archive\%RUN_ID%\"
if exist "%RUN_DIR%\logs\%RUN_ID%_gpu_guard.txt" copy "%RUN_DIR%\logs\%RUN_ID%_gpu_guard.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_stdout.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_stderr.txt" "results_archive\%RUN_ID%\"
if exist "%RUN_DIR%\logs\%RUN_ID%_progress.jsonl" copy "%RUN_DIR%\logs\%RUN_ID%_progress.jsonl" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_result_gate.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_summary_stdout.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_summary_stderr.txt" "results_archive\%RUN_ID%\"

echo run_id=%RUN_ID%> results_archive\%RUN_ID%\run_manifest.txt
echo project_id=%PROJECT_ID%>> results_archive\%RUN_ID%\run_manifest.txt
echo project_dir=%PROJECT_DIR%>> results_archive\%RUN_ID%\run_manifest.txt
echo run_dir=%RUN_DIR%>> results_archive\%RUN_ID%\run_manifest.txt
echo archive_work=%ARCHIVE_WORK%>> results_archive\%RUN_ID%\run_manifest.txt
echo branch=%BRANCH%>> results_archive\%RUN_ID%\run_manifest.txt
echo plan=experiments\innovation1\plans\innovation1_spn_present_histogram_hybrid_beamstats8deep4_r7_screen.csv>> results_archive\%RUN_ID%\run_manifest.txt
echo device=cuda:0>> results_archive\%RUN_ID%\run_manifest.txt
echo gpu_guard=enabled:cuda:0>> results_archive\%RUN_ID%\run_manifest.txt
echo expected_rows=%EXPECTED_ROWS%>> results_archive\%RUN_ID%\run_manifest.txt
echo epochs=16>> results_archive\%RUN_ID%\run_manifest.txt
echo batch_size=64>> results_archive\%RUN_ID%\run_manifest.txt
echo hidden_bits=32>> results_archive\%RUN_ID%\run_manifest.txt
echo optimizer=adam>> results_archive\%RUN_ID%\run_manifest.txt
echo weight_decay=1e-05>> results_archive\%RUN_ID%\run_manifest.txt
echo key_rotation_interval=1024>> results_archive\%RUN_ID%\run_manifest.txt
echo sample_structure=zhang_wang_case2_mcnd>> results_archive\%RUN_ID%\run_manifest.txt
echo integral_active_nibble=0>> results_archive\%RUN_ID%\run_manifest.txt
echo checkpoint_metric=val_auc>> results_archive\%RUN_ID%\run_manifest.txt
echo restore_best_checkpoint=True>> results_archive\%RUN_ID%\run_manifest.txt
echo early_stopping_patience=0>> results_archive\%RUN_ID%\run_manifest.txt
echo early_stopping_min_delta=0>> results_archive\%RUN_ID%\run_manifest.txt
echo pretrain_rounds=from_plan>> results_archive\%RUN_ID%\run_manifest.txt
echo pretrain_epochs=from_plan>> results_archive\%RUN_ID%\run_manifest.txt
echo dataset_cache_root=dataset_cache>> results_archive\%RUN_ID%\run_manifest.txt
echo dataset_cache_chunk_size=512>> results_archive\%RUN_ID%\run_manifest.txt
echo validation=spn_present_histogram_hybrid_beamstats8deep4_r7_gpu0>> results_archive\%RUN_ID%\run_manifest.txt

git add results_archive\%RUN_ID%
git commit -m "results: %RUN_ID% remote run"
git push origin results/%RUN_ID%
if errorlevel 1 goto push_failed

echo RUN_GATE_PASS
echo RUN_DIR %RUN_DIR%
echo ARCHIVE_WORK %ARCHIVE_WORK%
type "%RUN_DIR%\logs\%RUN_ID%_git_revision.txt"
type "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt"
type "%RUN_DIR%\logs\%RUN_ID%_result_gate.txt"
for %%A in ("%RUN_DIR%\logs\%RUN_ID%_stderr.txt") do echo STDERR_BYTES %%~zA
for %%A in ("%RUN_DIR%\results\%RUN_ID%.jsonl") do echo RESULT_BYTES %%~zA
exit /b 0

:incomplete_results
echo RUN_GATE_BLOCKED_INCOMPLETE_RESULTS
type logs\%RUN_ID%_result_gate.txt
exit /b 4

:run_failed
echo RUN_GATE_BLOCKED_RUN_FAILED
type logs\%RUN_ID%_stderr.txt
exit /b 1

:gpu_busy
echo RUN_GATE_BLOCKED_GPU_BUSY
type logs\%RUN_ID%_gpu_guard.txt
exit /b 5

:summary_failed
echo RUN_GATE_BLOCKED_SUMMARY_FAILED
type logs\%RUN_ID%_summary_stderr.txt
exit /b 2

:push_failed
echo RUN_GATE_BLOCKED_PUSH_FAILED
exit /b 3
