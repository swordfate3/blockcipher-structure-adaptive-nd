import importlib.util
import json
import sys
from pathlib import Path


def _load_generator():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "generators"
        / "generate_remote_experiment_scripts.py"
    )
    spec = importlib.util.spec_from_file_location("generate_remote_experiment_scripts", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.generate_remote_scripts


generate_remote_scripts = _load_generator()


def test_generate_remote_scripts_writes_run_launch_schedule_and_monitor(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-demo-gpu0-20260608",
                "task_name": "innovation1_demo_gpu0_20260608",
                "plan": "experiments\\innovation1\\plans\\demo.csv",
                "expected_rows": 4,
                "device": "cuda:0",
                "epochs": 3,
                "batch_size": 128,
                "hidden_bits": 32,
                "learning_rate": 0.002,
                "optimizer": "adamw",
                "weight_decay": 0.0001,
                "key_rotation_interval": 128,
                "sample_structure": "plaintext_integral_nibble",
                "integral_active_nibble": 0,
                "checkpoint_metric": "val_auc",
                "restore_best_checkpoint": True,
                "early_stopping_patience": 3,
                "early_stopping_min_delta": 0.001,
                "pretrain_rounds": 6,
                "pretrain_epochs": 2,
                "archive_work_id": "demo_20260608",
                "validation_label": "demo_validation",
                "monitor_script_name": "monitor_demo_results.sh",
                "dataset_cache": True,
                "dataset_cache_root": "dataset_cache",
                "dataset_cache_chunk_size": 4096,
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)

    assert generated.run_script.name == "run_innovation1-demo-gpu0-20260608_and_push.cmd"
    assert generated.launch_script.name == "launch_innovation1-demo-gpu0-20260608.cmd"
    assert generated.schedule_script.name == "schedule_innovation1_demo_gpu0_20260608.cmd"
    assert generated.monitor_script.name == "monitor_demo_results.sh"

    run_text = generated.run_script.read_text(encoding="utf-8")
    assert "set ROOT=G:\\lxy" in run_text
    assert "set RUN_ID=innovation1-demo-gpu0-20260608" in run_text
    assert "set EXPECTED_ROWS=4" in run_text
    assert "set RESULT_REPO_URL=git@github.com:swordfate3/blockcipher-structure-adaptive-nd.git" in run_text
    assert "set PYTHONPATH=%RUN_DIR%\\src;%PYTHONPATH%" in run_text
    assert "set GITHUB_SSH_KEY=%ROOT%\\.ssh\\github_blockcipher_20260612_result_pusher_ed25519" in run_text
    assert "C:/Users" not in run_text
    assert "set GIT_SSH_COMMAND=ssh -i %GITHUB_SSH_KEY% -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new" in run_text
    assert "--plan experiments\\innovation1\\plans\\demo.csv" in run_text
    assert "--device cuda:0" in run_text
    assert "--epochs 3" in run_text
    assert "--batch-size 128" in run_text
    assert "--key-rotation-interval 128" in run_text
    assert "--sample-structure plaintext_integral_nibble" in run_text
    assert "--integral-active-nibble 0" in run_text
    assert "--checkpoint-metric val_auc" in run_text
    assert "--restore-best-checkpoint" in run_text
    assert "--early-stopping-patience 3" in run_text
    assert "--early-stopping-min-delta 0.001" in run_text
    assert "--pretrain-rounds 6" in run_text
    assert "--pretrain-epochs 2" in run_text
    assert "--progress-output %RUN_DIR%\\logs\\%RUN_ID%_progress.jsonl" in run_text
    assert "--output %RUN_DIR%\\results\\%RUN_ID%.jsonl" in run_text
    assert "--dataset-cache-root dataset_cache" in run_text
    assert "--dataset-cache-chunk-size 4096" in run_text
    run_command = next(
        line for line in run_text.splitlines() if "experiments\\run_innovation_one_matrix.py" in line
    )
    assert "^" not in run_command
    assert " > logs\\%RUN_ID%_stdout.txt 2> logs\\%RUN_ID%_stderr.txt" in run_command
    assert "set RUNNER_EXIT_CODE=%ERRORLEVEL%" in run_text
    assert "runner_exit_code=%RUNNER_EXIT_CODE%" in run_text
    assert "if not exist results\\%RUN_ID%.jsonl goto run_failed" in run_text
    assert 'copy "%RUN_DIR%\\logs\\%RUN_ID%_progress.jsonl"' in run_text
    assert 'copy "%RUN_DIR%\\logs\\%RUN_ID%_runner_exit.txt"' in run_text
    assert "dataset_cache_root=dataset_cache" in run_text
    assert "dataset_cache_chunk_size=4096" in run_text
    assert "key_rotation_interval=128" in run_text
    assert "sample_structure=plaintext_integral_nibble" in run_text
    assert "integral_active_nibble=0" in run_text
    assert "checkpoint_metric=val_auc" in run_text
    assert "restore_best_checkpoint=True" in run_text
    assert "early_stopping_patience=3" in run_text
    assert "early_stopping_min_delta=0.001" in run_text
    assert "pretrain_rounds=6" in run_text
    assert "pretrain_epochs=2" in run_text
    assert "git config user.name \"fate\"" in run_text
    assert "git config user.email \"2968195987@qq.com\"" in run_text
    assert "git remote set-url origin %RESULT_REPO_URL%" in run_text
    assert "git add results_archive\\%RUN_ID%" in run_text
    assert "git push origin results/%RUN_ID%" in run_text
    assert "validation=demo_validation" in run_text
    assert "git fetch origin %BRANCH%" in run_text
    assert "git merge --ff-only FETCH_HEAD" in run_text
    assert "git config --global core.longpaths true" in run_text
    assert "git -c core.longpaths=true -c http.proxy= -c https.proxy= clone %CLONE_URL% %PROJECT_ID%" in run_text
    assert "git -c core.longpaths=true clone --local %PROJECT_DIR% %RUN_ID%" in run_text
    assert "git -c core.longpaths=true clone --local %RUN_DIR% %ARCHIVE_WORK%" in run_text
    assert "set GPU_BUSY_COUNT=0" in run_text
    assert 'findstr /I /C:"run_innovation_one_matrix.py"' in run_text
    assert 'findstr /I /C:"--device cuda:0"' in run_text
    assert "goto gpu_busy" in run_text
    assert "RUN_GATE_BLOCKED_GPU_BUSY" in run_text
    assert "gpu_guard=enabled:cuda:0" in run_text
    assert "git reset --hard" not in run_text

    launcher_text = generated.launch_script.read_text(encoding="utf-8")
    assert "run_innovation1-demo-gpu0-20260608_and_push.cmd" in launcher_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote" in launcher_text
    assert "C:\\Users" not in launcher_text
    assert "set LAUNCH_LOG_DIR=%RUN_ROOT%\\launcher_logs" in launcher_text
    assert "start \"progress_innovation1-demo-gpu0-20260608\"" in launcher_text
    assert "cmd.exe /c powershell" in launcher_text
    assert "cmd.exe /k" not in launcher_text
    assert "innovation1-demo-gpu0-20260608_progress.jsonl" in launcher_text
    assert "scripts\\tail_progress.py" in launcher_text
    assert "--interval 5" in launcher_text

    schedule_text = generated.schedule_script.read_text(encoding="utf-8")
    assert "schtasks /Create /TN innovation1_demo_gpu0_20260608" in schedule_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote\\launch_innovation1-demo-gpu0-20260608.cmd" in schedule_text
    assert "schtasks /Delete /TN innovation1_demo_gpu0_20260608 /F" in schedule_text
    assert "C:\\Users" not in schedule_text

    monitor_text = generated.monitor_script.read_text(encoding="utf-8")
    assert "innovation1-demo-gpu0-20260608=4" in monitor_text
    assert "scripts/monitor_remote_results.py" in monitor_text
    assert '--remote "${RESULT_REMOTE:-origin-ssh}"' in monitor_text
    assert '--fallback-remote-run-root "${FALLBACK_REMOTE_RUN_ROOT:-lxy-a6000:G:/lxy/blockcipher-structure-adaptive-nd-runs}"' in monitor_text
    assert '--fallback-output-dir "${FALLBACK_OUTPUT_DIR:-outputs/remote_results_incomplete}"' in monitor_text


def test_generate_remote_run_script_escapes_windows_paths(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-path-check-gpu0-20260608",
                "task_name": "innovation1_path_check_gpu0_20260608",
                "plan": "experiments\\innovation1\\plans\\demo.csv",
                "expected_rows": 1,
                "device": "cuda:0",
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")

    assert "\r" not in run_text
    assert "\a" not in run_text
    assert 'copy "%RUN_DIR%\\results\\%RUN_ID%.jsonl"' in run_text
    assert "results_archive\\%RUN_ID%\\run_manifest.txt" in run_text
    assert "set ARCHIVE_WORK=%ROOT%\\archive_work\\innovation1_path_check_gpu0_20260608" in run_text


def test_generate_remote_scripts_accepts_innovation1_plan_path(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-layout-gpu0-20260610",
                "task_name": "innovation1_layout_gpu0_20260610",
                "plan": "experiments\\innovation1\\plans\\demo.csv",
                "expected_rows": 1,
                "device": "cuda:0",
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")

    assert "--plan experiments\\innovation1\\plans\\demo.csv" in run_text
    assert 'copy "%RUN_DIR%\\experiments\\innovation1\\plans\\demo.csv"' in run_text


def test_remote_run_script_falls_back_when_summarizer_is_missing(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-summary-fallback-gpu0-20260610",
                "task_name": "innovation1_summary_fallback_gpu0_20260610",
                "plan": "experiments\\plans\\demo.csv",
                "expected_rows": 2,
                "device": "cuda:0",
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")

    assert "if exist {summarizer}" not in run_text
    assert "if exist experiments\\summarize_innovation_one_results.py" in run_text
    assert "summary_status=fallback_missing_summarizer" in run_text
    assert "if errorlevel 1 goto summary_failed" not in run_text
    assert 'copy "%RUN_DIR%\\results\\%RUN_ID%_summary.csv"' in run_text


def test_generate_remote_run_script_marks_plan_scoped_integral_nibble(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-plan-scoped-gpu0-20260613",
                "task_name": "innovation1_plan_scoped_gpu0_20260613",
                "plan": "experiments\\innovation1\\plans\\demo.csv",
                "expected_rows": 2,
                "device": "cuda:0",
                "sample_structure": "plaintext_integral_nibble",
                "integral_active_nibble": 0,
                "plan_scoped_fields": ["integral_active_nibble"],
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")

    assert "--integral-active-nibble 0" in run_text
    assert "integral_active_nibble=from_plan" in run_text


def test_generate_remote_run_script_can_disable_gpu_guard(tmp_path: Path):
    spec_path = tmp_path / "spec.json"
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "scripts"
    spec_path.write_text(
        json.dumps(
            {
                "run_id": "innovation1-no-guard-gpu0-20260616",
                "task_name": "innovation1_no_guard_gpu0_20260616",
                "plan": "experiments\\innovation1\\plans\\demo.csv",
                "expected_rows": 1,
                "device": "cuda:0",
                "gpu_guard": False,
            }
        ),
        encoding="utf-8",
    )

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")

    assert "set GPU_BUSY_COUNT=0" not in run_text
    assert "RUN_GATE_BLOCKED_GPU_BUSY" in run_text
    assert "gpu_guard=disabled" in run_text


def test_zhang_wang_keras_official_anchor_remote_config_generates_aligned_scripts(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "configs"
        / "remote"
        / "innovation1_spn_present_zhang_wang2022_keras_official_anchor_smoke_gpu1_20260621.json"
    )
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "monitors"

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")
    launcher_text = generated.launch_script.read_text(encoding="utf-8")
    schedule_text = generated.schedule_script.read_text(encoding="utf-8")
    monitor_text = generated.monitor_script.read_text(encoding="utf-8")

    assert (
        "--plan experiments\\innovation1\\plans\\"
        "innovation1_spn_present_zhang_wang2022_keras_official_anchor_smoke.csv"
    ) in run_text
    assert "--sample-structure zhang_wang_case2_official_mcnd" in run_text
    assert "--key-rotation-interval 0" in run_text
    assert "--hidden-bits 32" in run_text
    assert "--loss mse" in run_text
    assert "--lr-scheduler none" in run_text
    assert "--checkpoint-metric val_loss" in run_text
    assert 'xcopy "%PROJECT_DIR%\\experiments" "experiments\\" /E /I /Y' in run_text
    assert 'xcopy "%PROJECT_DIR%\\src\\blockcipher_ai_eval" "src\\blockcipher_ai_eval\\" /E /I /Y' in run_text
    assert "set ROOT=G:\\lxy" in run_text
    assert "C:\\Users" not in run_text
    assert "cmd.exe /k" not in launcher_text
    assert "cmd.exe /c powershell" in launcher_text
    assert "cmd.exe /c" in schedule_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote" in schedule_text
    assert (
        "innovation1-spn-present-zhang-wang2022-keras-official-anchor-smoke-gpu1-20260621=2"
        in monitor_text
    )


def test_zhang_wang_keras_official_anchor_scale_ladder_remote_config_generates_safe_scripts(
    tmp_path: Path,
):
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "configs"
        / "remote"
        / "innovation1_spn_zwkeras_anchor_r7_scale_med_gpu1_20260621.json"
    )
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "monitors"

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")
    launcher_text = generated.launch_script.read_text(encoding="utf-8")
    schedule_text = generated.schedule_script.read_text(encoding="utf-8")
    monitor_text = generated.monitor_script.read_text(encoding="utf-8")

    assert (
        "--plan experiments\\innovation1\\plans\\"
        "innovation1_spn_present_zhang_wang2022_keras_official_anchor_scale_ladder_r7.csv"
    ) in run_text
    assert "--sample-structure zhang_wang_case2_official_mcnd" in run_text
    assert "--key-rotation-interval 0" in run_text
    assert "--hidden-bits 32" in run_text
    assert "--epochs 50" in run_text
    assert "--loss mse" in run_text
    assert "--checkpoint-metric val_loss" in run_text
    assert "--early-stopping-patience 8" in run_text
    assert "--progress-output %RUN_DIR%\\logs\\%RUN_ID%_progress.jsonl" in run_text
    assert "--output %RUN_DIR%\\results\\%RUN_ID%.jsonl" in run_text
    assert 'xcopy "%PROJECT_DIR%\\experiments" "experiments\\" /E /I /Y' in run_text
    assert 'xcopy "%PROJECT_DIR%\\src\\blockcipher_ai_eval" "src\\blockcipher_ai_eval\\" /E /I /Y' in run_text
    assert "set ROOT=G:\\lxy" in run_text
    assert "C:\\Users" not in run_text
    assert "cmd.exe /k" not in launcher_text
    assert "cmd.exe /c powershell" in launcher_text
    assert "cmd.exe /c" in schedule_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote" in schedule_text
    assert (
        "i1-spn-zwkeras-anchor-r7-scale-med-gpu1-20260621=2"
        in monitor_text
    )
    assert "--fallback-remote-run-root" in monitor_text


def test_present_trail_position_scale_med_remote_config_generates_safe_scripts(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = (
        repo_root
        / "experiments"
        / "innovation1"
        / "configs"
        / "remote"
        / "innovation1_spn_trailpos_r7_scale_med_gpu0_20260622.json"
    )
    output_dir = tmp_path / "remote"
    monitor_dir = tmp_path / "monitors"

    generated = generate_remote_scripts(spec_path, output_dir=output_dir, monitor_dir=monitor_dir)
    run_text = generated.run_script.read_text(encoding="utf-8")
    launcher_text = generated.launch_script.read_text(encoding="utf-8")
    schedule_text = generated.schedule_script.read_text(encoding="utf-8")
    monitor_text = generated.monitor_script.read_text(encoding="utf-8")

    assert (
        "--plan experiments\\innovation1\\plans\\"
        "innovation1_spn_present_trail_position_stats_r7_scale_med.csv"
    ) in run_text
    assert "--sample-structure zhang_wang_case2_mcnd" in run_text
    assert "--key-rotation-interval 1024" in run_text
    assert "--loss mse" in run_text
    assert "--lr-scheduler cyclic" in run_text
    assert "--max-learning-rate 0.002" in run_text
    assert "--checkpoint-metric val_auc" in run_text
    assert "--pretrain-rounds" not in run_text
    assert "--pretrain-epochs" not in run_text
    assert "pretrain_rounds=from_plan" in run_text
    assert "pretrain_epochs=from_plan" in run_text
    assert "--dataset-cache-chunk-size 8192" in run_text
    assert (
        'xcopy "%PROJECT_DIR%\\src\\blockcipher_ai_eval\\models\\structure" '
        '"src\\blockcipher_ai_eval\\models\\structure\\" /E /I /Y'
    ) in run_text
    assert "set ROOT=G:\\lxy" in run_text
    assert "C:\\Users" not in run_text
    assert "cmd.exe /k" not in launcher_text
    assert "cmd.exe /c powershell" in launcher_text
    assert "cmd.exe /c" in schedule_text
    assert "cmd.exe /k" not in schedule_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote" in schedule_text
    assert (
        "i1-spn-trailpos-r7-scale-med-gpu0-20260622=2"
        in monitor_text
    )
    assert "--fallback-remote-run-root" in monitor_text


def test_spn_sinv_curriculum_direct_strict_r7r8_watcher_is_configured():
    repo_root = Path(__file__).resolve().parents[1]
    remote_dir = repo_root / "scripts" / "generated" / "remote"
    watcher = remote_dir / "watch_after_spn_sinv_to_sinv_strict_r7r8_20260616.ps1"
    schedule = remote_dir / "schedule_watch_after_spn_sinv_to_sinv_strict_r7r8_20260616.cmd"

    watcher_text = watcher.read_text(encoding="utf-8")
    schedule_text = schedule.read_text(encoding="utf-8")

    assert '$UpstreamRun = "innovation1-spn-present-sinv-curriculum-r7-gpu0-20260616"' in watcher_text
    assert '$NextRun = "innovation1-spn-present-sinv-strict-r7r8-confirm-gpu0-20260616"' in watcher_text
    assert (
        '$NextScheduleScript = Join-Path $ProjectPath '
        '"scripts\\generated\\remote\\schedule_innovation1_spn_present_sinv_strict_r7r8_confirm_gpu0_20260616.cmd"'
    ) in watcher_text
    assert '$GpuIndex = 0' in watcher_text
    assert '$LogPath = Join-Path $LogDir "watch_after_${UpstreamRun}_to_${NextRun}.log"' in watcher_text
    assert "watch_after_spn_sinv_to_sinv_strict_r7r8_20260616.ps1" in schedule_text


def test_spn_sinv_strict_to_sinv_sboxddt_beam4deep3_watcher_is_configured():
    repo_root = Path(__file__).resolve().parents[1]
    remote_dir = repo_root / "scripts" / "generated" / "remote"
    watcher = remote_dir / "watch_after_spn_sinv_strict_to_sinv_sboxddt_beam4deep3_20260616.ps1"
    schedule = remote_dir / "schedule_watch_after_spn_sinv_strict_to_sinv_sboxddt_beam4deep3_20260616.cmd"

    watcher_text = watcher.read_text(encoding="utf-8")
    schedule_text = schedule.read_text(encoding="utf-8")

    assert '$UpstreamRun = "innovation1-spn-present-sinv-strict-r7r8-confirm-gpu0-20260616"' in watcher_text
    assert '$NextRun = "innovation1-spn-present-sinv-sboxddt-beam4deep3-highround-gpu1-20260616"' in watcher_text
    assert (
        '$NextScheduleScript = Join-Path $ProjectPath '
        '"scripts\\generated\\remote\\schedule_innovation1_spn_present_sinv_sboxddt_beam4deep3_highround_gpu1_20260616.cmd"'
    ) in watcher_text
    assert '$GpuIndex = 1' in watcher_text
    assert 'Test-ResultBranch -BranchName "results/$NextRun"' in watcher_text
    assert '$LogPath = Join-Path $LogDir "watch_after_${UpstreamRun}_to_${NextRun}.log"' in watcher_text
    assert "watch_after_spn_sinv_strict_to_sinv_sboxddt_beam4deep3_20260616.ps1" in schedule_text
