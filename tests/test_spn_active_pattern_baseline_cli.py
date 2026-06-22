import runpy
import sys


def test_spn_active_pattern_baseline_help_runs(capsys):
    sys.argv = ["run_spn_active_pattern_baseline.py", "--help"]
    try:
        runpy.run_path("experiments/innovation1/run_spn_active_pattern_baseline.py", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "--samples-per-class" in captured.out
    assert "--feature-encoding" in captured.out
    assert "--device" in captured.out
