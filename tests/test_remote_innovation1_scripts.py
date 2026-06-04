from pathlib import Path


def test_remote_debug_large_scripts_use_expected_devices_and_plans():
    gpu0 = Path("scripts/remote/run_innovation1_debug_large_gpu0_and_push.cmd").read_text(encoding="utf-8")
    gpu1 = Path("scripts/remote/run_innovation1_debug_large_gpu1_and_push.cmd").read_text(encoding="utf-8")

    assert "set ROOT=G:\\lxy" in gpu0
    assert "set RUN_ROOT=%ROOT%\\%PROJECT_ID%-runs" in gpu0
    assert "set RUN_DIR=%RUN_ROOT%\\%RUN_ID%" in gpu0
    assert "set PY=F:\\Anaconda\\envs\\DWT\\torch310\\python.exe" in gpu0
    assert "experiments\\plans\\innovation1_debug_large_gpu0.csv" in gpu0
    assert "--device cuda:0" in gpu0
    assert "--batch-size 2048" in gpu0
    assert "git push origin results/%RUN_ID%" in gpu0

    assert "experiments\\plans\\innovation1_debug_large_gpu1.csv" in gpu1
    assert "--device cuda:1" in gpu1
    assert "--batch-size 1024" in gpu1
    assert "git push origin results/%RUN_ID%" in gpu1


def test_remote_debug_large_scripts_archive_curated_results_only():
    for script_path in [
        "scripts/remote/run_innovation1_debug_large_gpu0_and_push.cmd",
        "scripts/remote/run_innovation1_debug_large_gpu1_and_push.cmd",
    ]:
        text = Path(script_path).read_text(encoding="utf-8")
        assert "git add ." not in text
        assert "git add results_archive\\%RUN_ID%" in text
        assert "copy results\\%RUN_ID%.jsonl results_archive\\%RUN_ID%\\" in text
        assert "copy results\\%RUN_ID%_summary.csv results_archive\\%RUN_ID%\\" in text
        assert "RUN_GATE_PASS" in text
