#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GeneratedRemoteScripts:
    run_script: Path
    launch_script: Path
    schedule_script: Path
    monitor_script: Path


def _required(spec: dict[str, Any], key: str) -> Any:
    if key not in spec or spec[key] in {None, ""}:
        raise ValueError(f"missing required remote run spec field: {key}")
    return spec[key]


def _cmd_name(prefix: str, run_id: str) -> str:
    return f"{prefix}_{run_id}.cmd"


def _schedule_name(spec: dict[str, Any]) -> str:
    task_name = spec.get("task_name")
    if task_name:
        return f"schedule_{task_name}.cmd"
    return f"schedule_{str(_required(spec, 'run_id')).replace('-', '_')}.cmd"


def _format_float(value: Any) -> str:
    text = str(value)
    if text.endswith(".0"):
        return text[:-2]
    return text


def render_run_script(spec: dict[str, Any]) -> str:
    run_id = str(_required(spec, "run_id"))
    plan = str(_required(spec, "plan"))
    expected_rows = int(_required(spec, "expected_rows"))
    device = str(_required(spec, "device"))
    epochs = int(spec.get("epochs", 10))
    batch_size = int(spec.get("batch_size", 1024))
    hidden_bits = int(spec.get("hidden_bits", 64))
    learning_rate = _format_float(spec.get("learning_rate", 0.001))
    optimizer = str(spec.get("optimizer", "adamw"))
    weight_decay = _format_float(spec.get("weight_decay", 0.0001))
    key_rotation_interval = int(spec.get("key_rotation_interval", 0))
    sample_structure = str(spec.get("sample_structure", "independent_pairs"))
    integral_active_nibble = int(spec.get("integral_active_nibble", 0))
    plan_scoped_fields = {str(field) for field in spec.get("plan_scoped_fields", [])}
    integral_active_nibble_manifest = (
        "from_plan"
        if "integral_active_nibble" in plan_scoped_fields
        else str(integral_active_nibble)
    )
    checkpoint_metric = str(spec.get("checkpoint_metric", "val_accuracy"))
    restore_best_checkpoint = bool(spec.get("restore_best_checkpoint", False))
    early_stopping_patience = int(spec.get("early_stopping_patience", 0))
    early_stopping_min_delta = _format_float(spec.get("early_stopping_min_delta", 0.0))
    project_id = str(spec.get("project_id", "blockcipher-structure-adaptive-nd"))
    clone_url = str(spec.get("clone_url", "https://github.com/swordfate3/blockcipher-structure-adaptive-nd.git"))
    repo_url = str(spec.get("repo_url", "git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git"))
    result_repo_url = str(spec.get("result_repo_url", repo_url))
    branch = str(spec.get("branch", "main"))
    root = str(spec.get("root", r"G:\lxy"))
    python_exe = str(spec.get("python", r"F:\Anaconda\envs\DWT\torch310\python.exe"))
    github_ssh_key = str(
        spec.get(
            "github_ssh_key",
            "C:/Users/1304Lijinlin/.ssh/github_blockcipher_20260612_result_pusher_ed25519",
        )
    )
    git_user_name = str(spec.get("git_user_name", "fate"))
    git_user_email = str(spec.get("git_user_email", "2968195987@qq.com"))
    archive_work_id = str(spec.get("archive_work_id", run_id.replace("-", "_")))
    validation_label = str(spec.get("validation_label", "remote_experiment"))
    runner = str(spec.get("runner", r"experiments\run_innovation_one_matrix.py"))
    summarizer = str(spec.get("summarizer", r"experiments\summarize_innovation_one_results.py"))
    dataset_cache_root = str(spec.get("dataset_cache_root", r"dataset_cache"))
    dataset_cache_chunk_size = int(spec.get("dataset_cache_chunk_size", 8192))
    dataset_cache_args = ""
    dataset_cache_manifest = ""
    if bool(spec.get("dataset_cache", False)):
        dataset_cache_args = (
            " ^\n"
            f"  --dataset-cache-root {dataset_cache_root} ^\n"
            f"  --dataset-cache-chunk-size {dataset_cache_chunk_size}"
        )
        dataset_cache_manifest = (
            f"echo dataset_cache_root={dataset_cache_root}>> results_archive\\%RUN_ID%\\run_manifest.txt\n"
            f"echo dataset_cache_chunk_size={dataset_cache_chunk_size}>> results_archive\\%RUN_ID%\\run_manifest.txt"
        )
    checkpoint_args = (
        " ^\n"
        f"  --checkpoint-metric {checkpoint_metric} ^\n"
        f"  --early-stopping-patience {early_stopping_patience} ^\n"
        f"  --early-stopping-min-delta {early_stopping_min_delta}"
    )
    if restore_best_checkpoint:
        checkpoint_args = (
            " ^\n"
            f"  --checkpoint-metric {checkpoint_metric} ^\n"
            "  --restore-best-checkpoint ^\n"
            f"  --early-stopping-patience {early_stopping_patience} ^\n"
            f"  --early-stopping-min-delta {early_stopping_min_delta}"
        )

    return rf"""@echo off
setlocal
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=
set ROOT={root}
set PROJECT_ID={project_id}
set PROJECT_DIR=%ROOT%\%PROJECT_ID%
set CLONE_URL={clone_url}
set REPO_URL={repo_url}
set RESULT_REPO_URL={result_repo_url}
set BRANCH={branch}
set GITHUB_SSH_KEY={github_ssh_key}
set GIT_SSH_COMMAND=ssh -i %GITHUB_SSH_KEY% -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new
set RUN_ID={run_id}
set EXPECTED_ROWS={expected_rows}
set RUN_ROOT=%ROOT%\%PROJECT_ID%-runs
set RUN_DIR=%RUN_ROOT%\%RUN_ID%
set ARCHIVE_WORK=%ROOT%\archive_work\{archive_work_id}
set PY={python_exe}

if not exist %ROOT% mkdir %ROOT%
if not exist %RUN_ROOT% mkdir %RUN_ROOT%
if not exist %ROOT%\archive_work mkdir %ROOT%\archive_work
cd /d %ROOT%
if not exist %PROJECT_DIR% (
  git -c http.proxy= -c https.proxy= clone %CLONE_URL% %PROJECT_ID%
)

cd /d %PROJECT_DIR%
git config --global --add safe.directory %PROJECT_DIR%
git config --global --add safe.directory %PROJECT_DIR%\.git
git fetch origin
git checkout %BRANCH%
git pull --ff-only origin %BRANCH%

cd /d %RUN_ROOT%
if exist %RUN_ID% rmdir /s /q %RUN_ID%
git clone --local %PROJECT_DIR% %RUN_ID%

cd /d %RUN_DIR%
git config --global --add safe.directory %RUN_DIR%
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

%PY% {runner} ^
  --plan {plan} ^
  --epochs {epochs} ^
  --batch-size {batch_size} ^
  --hidden-bits {hidden_bits} ^
  --learning-rate {learning_rate} ^
  --optimizer {optimizer} ^
  --weight-decay {weight_decay} ^
  --key-rotation-interval {key_rotation_interval} ^
  --sample-structure {sample_structure} ^
  --integral-active-nibble {integral_active_nibble} ^
  --device {device}{dataset_cache_args}{checkpoint_args} ^
  --progress-output logs\%RUN_ID%_progress.jsonl ^
  --output results\%RUN_ID%.jsonl ^
  > logs\%RUN_ID%_stdout.txt ^
  2> logs\%RUN_ID%_stderr.txt
if errorlevel 1 goto run_failed

set RESULT_LINES=0
for /f "tokens=3" %%L in ('find /c /v "" results\%RUN_ID%.jsonl') do set RESULT_LINES=%%L
echo result_lines=%RESULT_LINES% > logs\%RUN_ID%_result_gate.txt
echo expected_rows=%EXPECTED_ROWS% >> logs\%RUN_ID%_result_gate.txt
if not "%RESULT_LINES%"=="%EXPECTED_ROWS%" goto incomplete_results

if exist {summarizer} (
  %PY% {summarizer} ^
    --input results\%RUN_ID%.jsonl ^
    --output results\%RUN_ID%_summary.csv ^
    > logs\%RUN_ID%_summary_stdout.txt ^
    2> logs\%RUN_ID%_summary_stderr.txt
)
if not exist results\%RUN_ID%_summary.csv (
  echo summary_status=fallback_missing_summarizer > logs\%RUN_ID%_summary_stdout.txt
  echo run_id,result_lines,expected_rows > results\%RUN_ID%_summary.csv
  echo %RUN_ID%,%RESULT_LINES%,%EXPECTED_ROWS% >> results\%RUN_ID%_summary.csv
  if not exist logs\%RUN_ID%_summary_stderr.txt echo summary_fallback_no_stderr > logs\%RUN_ID%_summary_stderr.txt
)

if exist %ARCHIVE_WORK% rmdir /s /q %ARCHIVE_WORK%
git clone --local %RUN_DIR% %ARCHIVE_WORK%
cd /d %ARCHIVE_WORK%
git config --global --add safe.directory %ARCHIVE_WORK%
git config user.name "{git_user_name}"
git config user.email "{git_user_email}"
git remote set-url origin %RESULT_REPO_URL%
git checkout -B results/%RUN_ID%
if exist results_archive\%RUN_ID% rmdir /s /q results_archive\%RUN_ID%
mkdir results_archive\%RUN_ID%
copy "%RUN_DIR%\results\%RUN_ID%.jsonl" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\results\%RUN_ID%_summary.csv" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\{plan}" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_revision.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_git_status_before_run.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_gpu_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info.txt" "results_archive\%RUN_ID%\"
copy "%RUN_DIR%\logs\%RUN_ID%_torch_info_stderr.txt" "results_archive\%RUN_ID%\"
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
echo plan={plan}>> results_archive\%RUN_ID%\run_manifest.txt
echo device={device}>> results_archive\%RUN_ID%\run_manifest.txt
echo expected_rows=%EXPECTED_ROWS%>> results_archive\%RUN_ID%\run_manifest.txt
echo epochs={epochs}>> results_archive\%RUN_ID%\run_manifest.txt
echo batch_size={batch_size}>> results_archive\%RUN_ID%\run_manifest.txt
echo hidden_bits={hidden_bits}>> results_archive\%RUN_ID%\run_manifest.txt
echo optimizer={optimizer}>> results_archive\%RUN_ID%\run_manifest.txt
echo weight_decay={weight_decay}>> results_archive\%RUN_ID%\run_manifest.txt
echo key_rotation_interval={key_rotation_interval}>> results_archive\%RUN_ID%\run_manifest.txt
echo sample_structure={sample_structure}>> results_archive\%RUN_ID%\run_manifest.txt
echo integral_active_nibble={integral_active_nibble_manifest}>> results_archive\%RUN_ID%\run_manifest.txt
echo checkpoint_metric={checkpoint_metric}>> results_archive\%RUN_ID%\run_manifest.txt
echo restore_best_checkpoint={restore_best_checkpoint}>> results_archive\%RUN_ID%\run_manifest.txt
echo early_stopping_patience={early_stopping_patience}>> results_archive\%RUN_ID%\run_manifest.txt
echo early_stopping_min_delta={early_stopping_min_delta}>> results_archive\%RUN_ID%\run_manifest.txt
{dataset_cache_manifest}
echo validation={validation_label}>> results_archive\%RUN_ID%\run_manifest.txt

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

:summary_failed
echo RUN_GATE_BLOCKED_SUMMARY_FAILED
type logs\%RUN_ID%_summary_stderr.txt
exit /b 2

:push_failed
echo RUN_GATE_BLOCKED_PUSH_FAILED
exit /b 3
"""


def render_launch_script(run_script_name: str, run_id: str, spec: dict[str, Any]) -> str:
    root = str(spec.get("root", r"G:\lxy"))
    project_id = str(spec.get("project_id", "blockcipher-structure-adaptive-nd"))
    python_exe = str(spec.get("python", r"F:\Anaconda\envs\DWT\torch310\python.exe"))
    project_dir = rf"{root}\{project_id}"
    run_root = rf"{root}\{project_id}-runs"
    run_dir = rf"{run_root}\{run_id}"
    progress_path = rf"{run_dir}\logs\{run_id}_progress.jsonl"
    tail_script = rf"{run_dir}\scripts\tail_progress.py"
    run_script_path = rf"{project_dir}\scripts\generated\remote\{run_script_name}"
    progress_command = (
        "while ($true) { "
        f"if (Test-Path '{tail_script}') {{ & '{python_exe}' '{tail_script}' '{progress_path}' --interval 5; break }}; "
        "cls; "
        f"Write-Host 'waiting for progress viewer {tail_script}'; "
        "Start-Sleep -Seconds 2 "
        "}"
    )
    return (
        "@echo off\n"
        "setlocal\n"
        f"set ROOT={root}\n"
        f"set PROJECT_ID={project_id}\n"
        f"set RUN_ID={run_id}\n"
        f"set RUN_ROOT={run_root}\n"
        "set LAUNCH_LOG_DIR=%RUN_ROOT%\\launcher_logs\n"
        "if not exist %RUN_ROOT% mkdir %RUN_ROOT%\n"
        "if not exist %LAUNCH_LOG_DIR% mkdir %LAUNCH_LOG_DIR%\n"
        f"start \"progress_{run_id}\" cmd.exe /c powershell -NoProfile -ExecutionPolicy Bypass -Command \"{progress_command}\"\n"
        f"call {run_script_path} > "
        f"%LAUNCH_LOG_DIR%\\%RUN_ID%_launcher_stdout.txt 2> "
        f"%LAUNCH_LOG_DIR%\\%RUN_ID%_launcher_stderr.txt\n"
        "endlocal\n"
    )


def render_schedule_script(task_name: str, launch_script_name: str, spec: dict[str, Any]) -> str:
    root = str(spec.get("root", r"G:\lxy"))
    project_id = str(spec.get("project_id", "blockcipher-structure-adaptive-nd"))
    launch_script_path = rf"{root}\{project_id}\scripts\generated\remote\{launch_script_name}"
    return (
        "@echo off\n"
        f"schtasks /Create /TN {task_name} /SC ONCE /ST 23:59 /TR "
        f"\"cmd.exe /c {launch_script_path}\" /F\n"
        f"schtasks /Run /TN {task_name}\n"
        f"schtasks /Query /TN {task_name} /V /FO LIST\n"
        f"schtasks /Delete /TN {task_name} /F\n"
    )


def render_monitor_script(run_id: str, expected_rows: int) -> str:
    return (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "cd \"$(dirname \"$0\")/../../..\"\n"
        "uv run python scripts/monitor_remote_results.py \\\n"
        f"  --run-id {run_id}={expected_rows}\n"
    )


def generate_remote_scripts(
    spec_path: Path,
    *,
    output_dir: Path = Path("scripts/generated/remote"),
    monitor_dir: Path = Path("scripts/generated/monitors"),
) -> GeneratedRemoteScripts:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    run_id = str(_required(spec, "run_id"))
    task_name = str(spec.get("task_name", run_id.replace("-", "_")))
    expected_rows = int(_required(spec, "expected_rows"))

    output_dir.mkdir(parents=True, exist_ok=True)
    monitor_dir.mkdir(parents=True, exist_ok=True)

    run_script = output_dir / f"run_{run_id}_and_push.cmd"
    launch_script = output_dir / f"launch_{run_id}.cmd"
    schedule_script = output_dir / _schedule_name(spec)
    monitor_script = monitor_dir / str(spec.get("monitor_script_name", f"monitor_{run_id.replace('-', '_')}_results.sh"))

    run_script.write_text(render_run_script(spec), encoding="utf-8")
    launch_script.write_text(render_launch_script(run_script.name, run_id, spec), encoding="utf-8")
    schedule_script.write_text(render_schedule_script(task_name, launch_script.name, spec), encoding="utf-8")
    monitor_script.write_text(render_monitor_script(run_id, expected_rows), encoding="utf-8")
    monitor_script.chmod(0o755)

    return GeneratedRemoteScripts(
        run_script=run_script,
        launch_script=launch_script,
        schedule_script=schedule_script,
        monitor_script=monitor_script,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate remote Windows GPU experiment scripts from a JSON spec.")
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("scripts/generated/remote"))
    parser.add_argument("--monitor-dir", type=Path, default=Path("scripts/generated/monitors"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    generated = generate_remote_scripts(args.spec, output_dir=args.output_dir, monitor_dir=args.monitor_dir)
    for path in generated.__dict__.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
