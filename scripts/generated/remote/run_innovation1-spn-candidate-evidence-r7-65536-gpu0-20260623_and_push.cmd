@echo off
setlocal
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set PROJECT_DIR=%ROOT%\%PROJECT_ID%
set REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set RESULT_REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set BRANCH=refactor/model-project-structure
set GITHUB_SSH_KEY=%ROOT%\.ssh\github_blockcipher_20260612_result_pusher_ed25519
set GIT_SSH_COMMAND=ssh -i %GITHUB_SSH_KEY% -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new
set RUN_ID=innovation1-spn-candidate-evidence-r7-65536-gpu0-20260623
set EXPECTED_ROWS=2
set RUN_ROOT=%ROOT%\%PROJECT_ID%-runs
set RUN_DIR=%RUN_ROOT%\%RUN_ID%
set ARCHIVE_WORK=%ROOT%\archive_work\spn_candidate_evidence_r7_65536_gpu0_20260623
set PY=F:\Anaconda\envs\DWT\torch310\python.exe
set PYTHONPATH=%RUN_DIR%\src;%PYTHONPATH%

if not exist %ROOT% mkdir %ROOT%
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %ROOT%\archive_work mkdir %ROOT%\archive_work
git config --global core.longpaths true
cd /d %ROOT%
if not exist %PROJECT_DIR% (
  git -c core.longpaths=true -c http.proxy= -c https.proxy= clone %REPO_URL% %PROJECT_ID%
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
if exist logs\%RUN_ID%_stdout.txt del logs\%RUN_ID%_stdout.txt
if exist logs\%RUN_ID%_stderr.txt del logs\%RUN_ID%_stderr.txt
if exist results\%RUN_ID%.jsonl del results\%RUN_ID%.jsonl
if exist results\%RUN_ID%_seed0.jsonl del results\%RUN_ID%_seed0.jsonl
if exist results\%RUN_ID%_seed1.jsonl del results\%RUN_ID%_seed1.jsonl
if exist results\%RUN_ID%_summary.csv del results\%RUN_ID%_summary.csv

git rev-parse HEAD > logs\%RUN_ID%_git_revision.txt
git status --short --branch > logs\%RUN_ID%_git_status_before_run.txt
nvidia-smi > logs\%RUN_ID%_gpu_info.txt
%PY% -c "import sys, torch; print('python', sys.executable); print('torch', torch.__version__); print('cuda_version', torch.version.cuda); print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print('device0', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NA')" > logs\%RUN_ID%_torch_info.txt 2> logs\%RUN_ID%_torch_info_stderr.txt

%PY% experiments\innovation1\run_spn_candidate_evidence_baseline.py --output results\%RUN_ID%_seed0.jsonl --rounds 7 --seed 0 --samples-per-class 65536 --pairs-per-sample 16 --model mlp --epochs 30 --learning-rate 0.001 --device cuda:0 > logs\%RUN_ID%_seed0_stdout.txt 2> logs\%RUN_ID%_seed0_stderr.txt
if errorlevel 1 goto seed0_failed
%PY% experiments\innovation1\run_spn_candidate_evidence_baseline.py --output results\%RUN_ID%_seed1.jsonl --rounds 7 --seed 1 --samples-per-class 65536 --pairs-per-sample 16 --model mlp --epochs 30 --learning-rate 0.001 --device cuda:0 > logs\%RUN_ID%_seed1_stdout.txt 2> logs\%RUN_ID%_seed1_stderr.txt
if errorlevel 1 goto seed1_failed

type results\%RUN_ID%_seed0.jsonl > results\%RUN_ID%.jsonl
type results\%RUN_ID%_seed1.jsonl >> results\%RUN_ID%.jsonl
set RUNNER_EXIT_CODE=0
echo runner_exit_code=%RUNNER_EXIT_CODE% > logs\%RUN_ID%_runner_exit.txt

set RESULT_LINES=0
for /f %%L in ('%PY% -c "from pathlib import Path; p=Path(r'results\%RUN_ID%.jsonl'); print(sum(1 for _ in p.open('rb')))"') do set RESULT_LINES=%%L
echo result_lines=%RESULT_LINES% > logs\%RUN_ID%_result_gate.txt
echo expected_rows=%EXPECTED_ROWS% >> logs\%RUN_ID%_result_gate.txt
echo runner_exit_code=%RUNNER_EXIT_CODE% >> logs\%RUN_ID%_result_gate.txt
if not "%RESULT_LINES%"=="%EXPECTED_ROWS%" goto incomplete_results

%PY% experiments\innovation1\summarize_spn_candidate_evidence.py results\%RUN_ID%.jsonl results\%RUN_ID%_summary.csv > logs\%RUN_ID%_summary_stdout.txt 2> logs\%RUN_ID%_summary_stderr.txt
if errorlevel 1 goto summary_failed

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
copy "%RUN_DIR%\results\%RUN_ID%_seed0.jsonl" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\results\%RUN_ID%_seed1.jsonl" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\results\%RUN_ID%_summary.csv" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_revision.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_status_before_run.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_gpu_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info_stderr.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_runner_exit.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_seed0_stdout.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_seed0_stderr.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_seed1_stdout.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_seed1_stderr.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_result_gate.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_summary_stdout.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_summary_stderr.txt" "results_archive\%RUN_ID%\"

echo run_id=%RUN_ID%> results_archive\%RUN_ID%\run_manifest.txt
echo project_id=%PROJECT_ID%>> results_archive\%RUN_ID%\run_manifest.txt
echo project_dir=%PROJECT_DIR%>> results_archive\%RUN_ID%\run_manifest.txt
echo run_dir=%RUN_DIR%>> results_archive\%RUN_ID%\run_manifest.txt
echo archive_work=%ARCHIVE_WORK%>> results_archive\%RUN_ID%\run_manifest.txt
echo branch=%BRANCH%>> results_archive\%RUN_ID%\run_manifest.txt
echo runner=experiments\innovation1\run_spn_candidate_evidence_baseline.py>> results_archive\%RUN_ID%\run_manifest.txt
echo device=cuda:0>> results_archive\%RUN_ID%\run_manifest.txt
echo expected_rows=%EXPECTED_ROWS%>> results_archive\%RUN_ID%\run_manifest.txt
echo rounds=7>> results_archive\%RUN_ID%\run_manifest.txt
echo samples_per_class=65536>> results_archive\%RUN_ID%\run_manifest.txt
echo pairs_per_sample=16>> results_archive\%RUN_ID%\run_manifest.txt
echo model=mlp>> results_archive\%RUN_ID%\run_manifest.txt
echo epochs=30>> results_archive\%RUN_ID%\run_manifest.txt
echo learning_rate=0.001>> results_archive\%RUN_ID%\run_manifest.txt
echo negative_mode=encrypted_random_plaintexts>> results_archive\%RUN_ID%\run_manifest.txt
echo sample_structure=zhang_wang_case2_mcnd>> results_archive\%RUN_ID%\run_manifest.txt
echo difference_profile=present_zhang_wang2022_mcnd>> results_archive\%RUN_ID%\run_manifest.txt
echo input_difference=0x0000000000000009>> results_archive\%RUN_ID%\run_manifest.txt
echo key_rotation_interval=1024>> results_archive\%RUN_ID%\run_manifest.txt
echo claim_scope=SCREEN only: PRESENT r7 candidate-evidence MLP at 65536/class seeds 0,1; strict encrypted-random-plaintext negatives; not formal or breakthrough evidence>> results_archive\%RUN_ID%\run_manifest.txt
echo launch_policy=scale candidate-disagreement/margin/confidence evidence only after positive 4096/8192 local fast screens>> results_archive\%RUN_ID%\run_manifest.txt

if not exist "results_archive\%RUN_ID%\%RUN_ID%.jsonl" goto archive_incomplete
if not exist "results_archive\%RUN_ID%\%RUN_ID%_summary.csv" goto archive_incomplete
if not exist "results_archive\%RUN_ID%\%RUN_ID%_result_gate.txt" goto archive_incomplete
if not exist "results_archive\%RUN_ID%\run_manifest.txt" goto archive_incomplete
echo archive_integrity=pass > results_archive\%RUN_ID%\archive_integrity.txt
git add results_archive\%RUN_ID%
git commit -m "results: %RUN_ID% remote run"
git push origin results/%RUN_ID%
if errorlevel 1 goto push_failed

echo RUN_GATE_PASS
type "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt"
type "%RUN_DIR%\logs\%RUN_ID%_result_gate.txt"
for %%A in ("%RUN_DIR%\results\%RUN_ID%.jsonl") do echo RESULT_BYTES %%~zA
exit /b 0

:seed0_failed
echo RUN_GATE_BLOCKED_SEED0_FAILED
type logs\%RUN_ID%_seed0_stderr.txt
exit /b 1

:seed1_failed
echo RUN_GATE_BLOCKED_SEED1_FAILED
type logs\%RUN_ID%_seed1_stderr.txt
exit /b 1

:incomplete_results
echo RUN_GATE_BLOCKED_INCOMPLETE_RESULTS
type logs\%RUN_ID%_result_gate.txt
exit /b 4

:summary_failed
echo RUN_GATE_BLOCKED_SUMMARY_FAILED
type logs\%RUN_ID%_summary_stderr.txt
exit /b 2

:archive_incomplete
echo RUN_GATE_BLOCKED_ARCHIVE_INCOMPLETE
dir results_archive\%RUN_ID%
exit /b 11

:push_failed
echo RUN_GATE_BLOCKED_PUSH_FAILED
exit /b 3
