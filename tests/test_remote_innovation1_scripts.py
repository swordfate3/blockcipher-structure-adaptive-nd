from pathlib import Path


def test_remote_debug_large_scripts_use_expected_devices_and_plans():
    gpu0 = Path("scripts/remote/run_innovation1_debug_large_gpu0_and_push.cmd").read_text(encoding="utf-8")
    gpu1 = Path("scripts/remote/run_innovation1_debug_large_gpu1_and_push.cmd").read_text(encoding="utf-8")

    assert "set ROOT=G:\\lxy" in gpu0
    assert "set RUN_ROOT=%ROOT%\\%PROJECT_ID%-runs" in gpu0
    assert "set RUN_DIR=%RUN_ROOT%\\%RUN_ID%" in gpu0
    assert "set PY=F:\\Anaconda\\envs\\DWT\\torch310\\python.exe" in gpu0
    assert "git config --global --add safe.directory %RUN_DIR%" in gpu0
    assert "experiments\\plans\\innovation1_debug_large_gpu0.csv" in gpu0
    assert "--device cuda:0" in gpu0
    assert "--batch-size 2048" in gpu0
    assert "set EXPECTED_ROWS=216" in gpu0
    assert "RUN_GATE_BLOCKED_INCOMPLETE_RESULTS" in gpu0
    assert "git push origin results/%RUN_ID%" in gpu0

    assert "experiments\\plans\\innovation1_debug_large_gpu1.csv" in gpu1
    assert "git config --global --add safe.directory %RUN_DIR%" in gpu1
    assert "--device cuda:1" in gpu1
    assert "--batch-size 1024" in gpu1
    assert "set EXPECTED_ROWS=108" in gpu1
    assert "RUN_GATE_BLOCKED_INCOMPLETE_RESULTS" in gpu1
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
        assert "copy logs\\%RUN_ID%_result_gate.txt results_archive\\%RUN_ID%\\" in text
        assert "RUN_GATE_PASS" in text


def test_remote_structure_pairset_scripts_use_expected_devices_plans_and_gates():
    gpu0 = Path("scripts/remote/run_innovation1_structure_pairset_gpu0_and_push.cmd").read_text(encoding="utf-8")
    gpu1 = Path("scripts/remote/run_innovation1_structure_pairset_gpu1_and_push.cmd").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-structure-pairset-gpu0-20260605" in gpu0
    assert "experiments\\plans\\innovation1_structure_pairset_gpu0.csv" in gpu0
    assert "--device cuda:0" in gpu0
    assert "--batch-size 2048" in gpu0
    assert "set EXPECTED_ROWS=72" in gpu0
    assert "git push origin results/%RUN_ID%" in gpu0

    assert "set RUN_ID=innovation1-structure-pairset-gpu1-20260605" in gpu1
    assert "experiments\\plans\\innovation1_structure_pairset_gpu1.csv" in gpu1
    assert "--device cuda:1" in gpu1
    assert "--batch-size 1024" in gpu1
    assert "set EXPECTED_ROWS=36" in gpu1
    assert "git push origin results/%RUN_ID%" in gpu1


def test_remote_spn_pairset_v2_script_uses_expected_plan_and_gate():
    script = Path("scripts/remote/run_innovation1_spn_pairset_v2_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_spn_pairset_v2_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_spn_pairset_v2_present.cmd").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-spn-pairset-v2-present-gpu1-20260605" in script
    assert "experiments\\plans\\innovation1_spn_pairset_v2_present.csv" in script
    assert "--device cuda:1" in script
    assert "--batch-size 1024" in script
    assert "set EXPECTED_ROWS=48" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "run_innovation1_spn_pairset_v2_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_spn_pairset_v2_present_gpu1_20260605" in scheduler



def test_remote_spn_nibble_hpo_script_uses_expected_search_space_and_gate():
    script = Path("scripts/remote/run_innovation1_spn_nibble_hpo_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_spn_nibble_hpo_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_spn_nibble_hpo_present.cmd").read_text(encoding="utf-8")
    monitor = Path("scripts/monitor_innovation1_spn_nibble_hpo_present_results.sh").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-spn-nibble-hpo-present-gpu1-20260605" in script
    assert "experiments\\run_hparam_search.py" in script
    assert "experiments\\hparam_spaces\\spn_nibble_conv_pairset_present.json" in script
    assert "--mode random" in script
    assert "--max-trials 12" in script
    assert "--device cuda:1" in script
    assert "set EXPECTED_ROWS=12" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "git add results_archive\\%RUN_ID%" in script
    assert "git add ." not in script
    assert "run_innovation1_spn_nibble_hpo_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_spn_nibble_hpo_present_gpu1_20260605" in scheduler
    assert "innovation1-spn-nibble-hpo-present-gpu1-20260605=12" in monitor


def test_remote_spn_token_mixer_script_uses_expected_plan_and_gate():
    script = Path("scripts/remote/run_innovation1_spn_token_mixer_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_spn_token_mixer_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_spn_token_mixer_present.cmd").read_text(encoding="utf-8")
    monitor = Path("scripts/monitor_innovation1_spn_token_mixer_present_results.sh").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-spn-token-mixer-present-gpu1-20260605" in script
    assert "experiments\\plans\\innovation1_spn_token_mixer_present.csv" in script
    assert "--device cuda:1" in script
    assert "--batch-size 1024" in script
    assert "set EXPECTED_ROWS=10" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "git add results_archive\\%RUN_ID%" in script
    assert "git add ." not in script
    assert "run_innovation1_spn_token_mixer_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_spn_token_mixer_present_gpu1_20260605" in scheduler
    assert "innovation1-spn-token-mixer-present-gpu1-20260605=10" in monitor


def test_remote_moe_v5_script_uses_expected_plan_and_gate():
    script = Path("scripts/remote/run_innovation1_moe_v5_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_moe_v5_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_moe_v5_present.cmd").read_text(encoding="utf-8")
    monitor = Path("scripts/monitor_innovation1_moe_v5_present_results.sh").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-moe-v5-present-gpu1-20260606" in script
    assert "experiments\\plans\\innovation1_moe_v5_present.csv" in script
    assert "--device cuda:1" in script
    assert "--batch-size 1024" in script
    assert "set EXPECTED_ROWS=10" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "git add results_archive\\%RUN_ID%" in script
    assert "git add ." not in script
    assert "run_innovation1_moe_v5_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_moe_v5_present_gpu1_20260606" in scheduler
    assert "innovation1-moe-v5-present-gpu1-20260606=10" in monitor



def test_remote_moe_v5_hpo_script_uses_expected_space_and_gate():
    script = Path("scripts/remote/run_innovation1_moe_v5_hpo_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_moe_v5_hpo_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_moe_v5_hpo_present.cmd").read_text(encoding="utf-8")
    monitor = Path("scripts/monitor_innovation1_moe_v5_hpo_present_results.sh").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-moe-v5-hpo-present-gpu1-20260606" in script
    assert r"experiments\run_hparam_search.py" in script
    assert "experiments\\hparam_spaces\\moe_v5_present_components.json" in script
    assert r"experiments\summarize_hparam_search.py" in script
    assert "--mode random" in script
    assert "--max-trials 24" in script
    assert "--device cuda:1" in script
    assert "set EXPECTED_ROWS=24" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "git add results_archive\\%RUN_ID%" in script
    assert "git add ." not in script
    assert "run_innovation1_moe_v5_hpo_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_moe_v5_hpo_present_gpu1_20260606" in scheduler
    assert "innovation1-moe-v5-hpo-present-gpu1-20260606=24" in monitor


def test_remote_moe_v5_hpo_best_validation_script_uses_expected_plan_and_gate():
    script = Path("scripts/remote/run_innovation1_moe_v5_hpo_best_validate_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_moe_v5_hpo_best_validate_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_moe_v5_hpo_best_validate_present.cmd").read_text(encoding="utf-8")
    monitor = Path("scripts/monitor_innovation1_moe_v5_hpo_best_validate_present_results.sh").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-moe-v5-hpo-best-validate-present-gpu1-20260606" in script
    assert r"experiments\plans\innovation1_moe_v5_hpo_best_validate_present.csv" in script
    assert "--device cuda:1" in script
    assert "--batch-size 1024" in script
    assert "--epochs 10" in script
    assert "set EXPECTED_ROWS=20" in script
    assert "fixed_hpo_model=moe_v5_soft_hpo_present_best" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "git add results_archive\\%RUN_ID%" in script
    assert "git add ." not in script
    assert "run_innovation1_moe_v5_hpo_best_validate_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_moe_v5_hpo_best_validate_present_gpu1_20260606" in scheduler
    assert "innovation1-moe-v5-hpo-best-validate-present-gpu1-20260606=20" in monitor


def test_remote_moe_v5_hpo_multiseed_script_uses_expected_space_seeds_and_gate():
    script = Path("scripts/remote/run_innovation1_moe_v5_hpo_multiseed_present_gpu1_and_push.cmd").read_text(encoding="utf-8")
    launcher = Path("scripts/remote/launch_innovation1_moe_v5_hpo_multiseed_present_gpu1.cmd").read_text(encoding="utf-8")
    scheduler = Path("scripts/remote/schedule_innovation1_moe_v5_hpo_multiseed_present.cmd").read_text(encoding="utf-8")
    monitor = Path("scripts/monitor_innovation1_moe_v5_hpo_multiseed_present_results.sh").read_text(encoding="utf-8")

    assert "set RUN_ID=innovation1-moe-v5-hpo-multiseed-present-gpu1-20260606" in script
    assert "experiments\\run_hparam_search.py" in script
    assert "experiments\\hparam_spaces\\moe_v5_present_components.json" in script
    assert "--mode random" in script
    assert "--max-trials 12" in script
    assert "--trial-seeds 0 1 2" in script
    assert "--device cuda:1" in script
    assert "set EXPECTED_ROWS=12" in script
    assert "trial_seeds=0,1,2" in script
    assert "git push origin results/%RUN_ID%" in script
    assert "git add results_archive\\%RUN_ID%" in script
    assert "git add ." not in script
    assert "run_innovation1_moe_v5_hpo_multiseed_present_gpu1_and_push.cmd" in launcher
    assert "innovation1_moe_v5_hpo_multiseed_present_gpu1_20260606" in scheduler
    assert "innovation1-moe-v5-hpo-multiseed-present-gpu1-20260606=12" in monitor
