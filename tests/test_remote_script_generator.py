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
    assert "--plan experiments\\innovation1\\plans\\demo.csv" in run_text
    assert "--device cuda:0" in run_text
    assert "--epochs 3" in run_text
    assert "--batch-size 128" in run_text
    assert "--key-rotation-interval 128" in run_text
    assert "--progress-output logs\\%RUN_ID%_progress.jsonl" in run_text
    assert "--dataset-cache-root dataset_cache" in run_text
    assert "--dataset-cache-chunk-size 4096" in run_text
    assert 'copy "%RUN_DIR%\\logs\\%RUN_ID%_progress.jsonl"' in run_text
    assert "dataset_cache_root=dataset_cache" in run_text
    assert "dataset_cache_chunk_size=4096" in run_text
    assert "key_rotation_interval=128" in run_text
    assert "git add results_archive\\%RUN_ID%" in run_text
    assert "git push origin results/%RUN_ID%" in run_text
    assert "validation=demo_validation" in run_text
    assert "git pull --ff-only origin %BRANCH%" in run_text
    assert "git reset --hard" not in run_text

    launcher_text = generated.launch_script.read_text(encoding="utf-8")
    assert "run_innovation1-demo-gpu0-20260608_and_push.cmd" in launcher_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote" in launcher_text
    assert "C:\\Users" not in launcher_text
    assert "set LAUNCH_LOG_DIR=%RUN_ROOT%\\launcher_logs" in launcher_text
    assert "start \"progress_innovation1-demo-gpu0-20260608\"" in launcher_text
    assert "innovation1-demo-gpu0-20260608_progress.jsonl" in launcher_text
    assert "scripts\\tail_progress.py" in launcher_text
    assert "--interval 5" in launcher_text

    schedule_text = generated.schedule_script.read_text(encoding="utf-8")
    assert "schtasks /Create /TN innovation1_demo_gpu0_20260608" in schedule_text
    assert "G:\\lxy\\blockcipher-structure-adaptive-nd\\scripts\\generated\\remote\\launch_innovation1-demo-gpu0-20260608.cmd" in schedule_text
    assert "C:\\Users" not in schedule_text

    monitor_text = generated.monitor_script.read_text(encoding="utf-8")
    assert "innovation1-demo-gpu0-20260608=4" in monitor_text
    assert "scripts/monitor_remote_results.py" in monitor_text


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
