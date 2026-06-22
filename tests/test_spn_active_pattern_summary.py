import json
import runpy
import sys


def test_summarize_spn_active_pattern_writes_mean_metrics(tmp_path, capsys):
    result = tmp_path / "result.jsonl"
    result.write_text(
        json.dumps({"val_accuracy": 0.6, "val_auc": 0.7, "feature_dim": 24}) + "\n"
        + json.dumps({"val_accuracy": 0.8, "val_auc": 0.9, "feature_dim": 24}) + "\n",
        encoding="utf-8",
    )
    sys.argv = ["summarize_spn_active_pattern.py", str(result)]

    runpy.run_path("experiments/innovation1/summarize_spn_active_pattern.py", run_name="__main__")

    captured = capsys.readouterr()
    assert "mean_accuracy=0.700000" in captured.out
    assert "mean_auc=0.800000" in captured.out
