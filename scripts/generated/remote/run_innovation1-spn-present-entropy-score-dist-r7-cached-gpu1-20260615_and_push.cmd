@echo off
setlocal
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ROOT=G:\lxy
set PROJECT_ID=blockcipher-structure-adaptive-nd
set PROJECT_DIR=%ROOT%\%PROJECT_ID%
set CLONE_URL=https://github.com/swordfate3/blockcipher-structure-adaptive-nd.git
set REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set RESULT_REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git
set BRANCH=refactor/model-project-structure
set GITHUB_SSH_KEY=C:/Users/1304Lijinlin/.ssh/github_blockcipher_20260612_result_pusher_ed25519
set GIT_SSH_COMMAND=ssh -i %GITHUB_SSH_KEY% -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new
set RUN_ID=innovation1-spn-present-entropy-score-dist-r7-cached-gpu1-20260615
set EXPECTED_ROWS=1
set RUN_ROOT=%ROOT%\%PROJECT_ID%-runs
set RUN_DIR=%RUN_ROOT%\%RUN_ID%
set ARCHIVE_WORK=%ROOT%\archive_work\innovation1_spn_present_entropy_score_dist_r7_cached_gpu1_20260615
set PY=F:/Anaconda/envs/DWT/torch310/python.exe

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
git fetch origin
git checkout %BRANCH%
git pull --ff-only origin %BRANCH%

cd /d %RUN_ROOT%
if exist %RUN_ID% rmdir /s /q %RUN_ID%
git -c core.longpaths=true clone --no-checkout --local %PROJECT_DIR% %RUN_ID%

cd /d %RUN_DIR%
git config --global --add safe.directory %RUN_DIR%
git config core.longpaths true
git config core.sparseCheckout true
if not exist .git/info mkdir .git/info
echo /.gitignore> .git/info\sparse-checkout
echo /README.md>> .git/info\sparse-checkout
echo /pyproject.toml>> .git/info\sparse-checkout
echo /uv.lock>> .git/info\sparse-checkout
echo /src/>> .git/info\sparse-checkout
echo /experiments/>> .git/info\sparse-checkout
echo /scripts/>> .git/info\sparse-checkout
git checkout %BRANCH%
git remote set-url origin %REPO_URL%

if not exist logs mkdir logs
if not exist results mkdir results
if not exist dataset_cache mkdir dataset_cache
if exist logs/%RUN_ID%_stdout.txt del logs/%RUN_ID%_stdout.txt
if exist logs/%RUN_ID%_stderr.txt del logs/%RUN_ID%_stderr.txt
if exist logs/%RUN_ID%_progress.jsonl del logs/%RUN_ID%_progress.jsonl
if exist results/%RUN_ID%.jsonl del results/%RUN_ID%.jsonl
if exist results/%RUN_ID%_summary.csv del results/%RUN_ID%_summary.csv

git rev-parse HEAD > logs/%RUN_ID%_git_revision.txt
git status --short --branch > logs/%RUN_ID%_git_status_before_run.txt
nvidia-smi > logs/%RUN_ID%_gpu_info.txt
%PY% -c "import sys, torch; print('python', sys.executable); print('torch', torch.__version__); print('cuda_version', torch.version.cuda); print('cuda_available', torch.cuda.is_available()); print('device_count', torch.cuda.device_count()); print('device0', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NA')" > logs/%RUN_ID%_torch_info.txt 2> logs/%RUN_ID%_torch_info_stderr.txt

%PY% experiments/run_score_distribution.py ^
  --cipher present80 ^
  --rounds 7 ^
  --difference-profile present_entropy2026_gohr ^
  --difference-member 0 ^
  --feature-encoding ciphertext_pair_bits ^
  --selected-bit-indices "[0, 2, 3, 4, 6, 8, 10, 11, 16, 18, 20, 22, 24, 26, 27, 32, 34, 36, 40, 42, 43, 48, 50, 52, 54, 56, 58, 59, 64, 66, 67, 68, 70, 72, 74, 75, 80, 82, 84, 86, 88, 90, 91, 96, 98, 100, 104, 106, 107, 112, 114, 116, 118, 120, 122, 123]" ^
  --negative-mode encrypted_random_plaintexts ^
  --sample-structure independent_pairs ^
  --key-rotation-interval 1024 ^
  --base-samples-per-class 131072 ^
  --meta-samples-per-class 8192 ^
  --score-group-size 16 ^
  --base-model mlp ^
  --base-hidden-bits 64 ^
  --base-epochs 30 ^
  --base-batch-size 4096 ^
  --base-learning-rate 0.0001 ^
  --base-loss mse ^
  --dataset-cache-root dataset_cache ^
  --dataset-cache-chunk-size 8192 ^
  --meta-hidden-bits 96 ^
  --meta-epochs 30 ^
  --meta-batch-size 1024 ^
  --meta-learning-rate 0.001 ^
  --seed 0 ^
  --device cuda:1 ^
  --progress-output logs/%RUN_ID%_progress.jsonl ^
  --output results/%RUN_ID%.jsonl ^
  > logs/%RUN_ID%_stdout.txt ^
  2> logs/%RUN_ID%_stderr.txt
if errorlevel 1 goto run_failed

set RESULT_LINES=0
for /f "tokens=3" %%L in ('find /c /v "" results/%RUN_ID%.jsonl') do set RESULT_LINES=%%L
echo result_lines=%RESULT_LINES% > logs/%RUN_ID%_result_gate.txt
echo expected_rows=%EXPECTED_ROWS% >> logs/%RUN_ID%_result_gate.txt
if not "%RESULT_LINES%"=="%EXPECTED_ROWS%" goto incomplete_results

echo run_id,rounds,metric_accuracy,metric_auc,base_accuracy,base_auc > results/%RUN_ID%_summary.csv
%PY% -c "import json, os; p='results/%RUN_ID%.jsonl'; r=json.loads(open(p,encoding='utf-8').readline()); print(','.join([os.environ['RUN_ID'], str(r['rounds']), str(r['metrics']['accuracy']), str(r['metrics']['auc']), str(r['base_metrics']['accuracy']), str(r['base_metrics']['auc'])]))" >> results/%RUN_ID%_summary.csv 2> logs/%RUN_ID%_summary_stderr.txt
if errorlevel 1 goto summary_failed
if not exist logs/%RUN_ID%_summary_stdout.txt echo summary_status=score_distribution_inline > logs/%RUN_ID%_summary_stdout.txt

if exist %ARCHIVE_WORK% rmdir /s /q %ARCHIVE_WORK%
git -c core.longpaths=true clone --local %RUN_DIR% %ARCHIVE_WORK%
cd /d %ARCHIVE_WORK%
git config --global --add safe.directory %ARCHIVE_WORK%
git config user.name "fate"
git config user.email "2968195987@qq.com"
git remote set-url origin %RESULT_REPO_URL%
git checkout -B results/%RUN_ID%
if exist results_archive/%RUN_ID% rmdir /s /q results_archive/%RUN_ID%
mkdir results_archive/%RUN_ID%
copy "%RUN_DIR%/results/%RUN_ID%.jsonl" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/results/%RUN_ID%_summary.csv" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_git_revision.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_git_status_before_run.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_gpu_info.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_torch_info.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_torch_info_stderr.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_stdout.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_stderr.txt" "results_archive/%RUN_ID%/"
if exist "%RUN_DIR%/logs/%RUN_ID%_progress.jsonl" copy "%RUN_DIR%/logs/%RUN_ID%_progress.jsonl" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_result_gate.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_summary_stdout.txt" "results_archive/%RUN_ID%/"
copy "%RUN_DIR%/logs/%RUN_ID%_summary_stderr.txt" "results_archive/%RUN_ID%/"

echo run_id=%RUN_ID%> results_archive/%RUN_ID%/run_manifest.txt
echo project_id=%PROJECT_ID%>> results_archive/%RUN_ID%/run_manifest.txt
echo project_dir=%PROJECT_DIR%>> results_archive/%RUN_ID%/run_manifest.txt
echo run_dir=%RUN_DIR%>> results_archive/%RUN_ID%/run_manifest.txt
echo branch=%BRANCH%>> results_archive/%RUN_ID%/run_manifest.txt
echo runner=experiments/run_score_distribution.py>> results_archive/%RUN_ID%/run_manifest.txt
echo expected_rows=%EXPECTED_ROWS%>> results_archive/%RUN_ID%/run_manifest.txt
echo device=cuda:1>> results_archive/%RUN_ID%/run_manifest.txt
echo rounds=7>> results_archive/%RUN_ID%/run_manifest.txt
echo difference_profile=present_entropy2026_gohr>> results_archive/%RUN_ID%/run_manifest.txt
echo feature_encoding=ciphertext_pair_bits>> results_archive/%RUN_ID%/run_manifest.txt
echo selected_bit_indices=[0, 2, 3, 4, 6, 8, 10, 11, 16, 18, 20, 22, 24, 26, 27, 32, 34, 36, 40, 42, 43, 48, 50, 52, 54, 56, 58, 59, 64, 66, 67, 68, 70, 72, 74, 75, 80, 82, 84, 86, 88, 90, 91, 96, 98, 100, 104, 106, 107, 112, 114, 116, 118, 120, 122, 123]>> results_archive/%RUN_ID%/run_manifest.txt
echo base_samples_per_class=131072>> results_archive/%RUN_ID%/run_manifest.txt
echo meta_samples_per_class=8192>> results_archive/%RUN_ID%/run_manifest.txt
echo score_group_size=16>> results_archive/%RUN_ID%/run_manifest.txt
echo dataset_cache_root=dataset_cache>> results_archive/%RUN_ID%/run_manifest.txt
echo dataset_cache_chunk_size=8192>> results_archive/%RUN_ID%/run_manifest.txt
echo validation=entropy_selected_score_distribution_r7>> results_archive/%RUN_ID%/run_manifest.txt

git add results_archive/%RUN_ID%
git commit -m "results: %RUN_ID% remote run"
git push origin results/%RUN_ID%
if errorlevel 1 goto push_failed

echo RUN_GATE_PASS
echo RUN_DIR %RUN_DIR%
type "%RUN_DIR%/logs/%RUN_ID%_git_revision.txt"
type "%RUN_DIR%/logs/%RUN_ID%_torch_info.txt"
type "%RUN_DIR%/logs/%RUN_ID%_result_gate.txt"
for %%A in ("%RUN_DIR%/logs/%RUN_ID%_stderr.txt") do echo STDERR_BYTES %%~zA
for %%A in ("%RUN_DIR%/results/%RUN_ID%.jsonl") do echo RESULT_BYTES %%~zA
exit /b 0

:incomplete_results
echo RUN_GATE_BLOCKED_INCOMPLETE_RESULTS
type logs/%RUN_ID%_result_gate.txt
exit /b 4

:run_failed
echo RUN_GATE_BLOCKED_RUN_FAILED
type logs/%RUN_ID%_stderr.txt
exit /b 1

:summary_failed
echo RUN_GATE_BLOCKED_SUMMARY_FAILED
type logs/%RUN_ID%_summary_stderr.txt
exit /b 2

:push_failed
echo RUN_GATE_BLOCKED_PUSH_FAILED
exit /b 3
