import json
import subprocess
import sys
from pathlib import Path


def test_tail_progress_formats_dataset_cache_and_training_events(tmp_path: Path):
    progress_path = tmp_path / "progress.jsonl"
    progress_rows = [
        {
            "event": "cache_positive_chunk",
            "stage": "dataset_cache",
            "index": 1,
            "total": 8,
            "split": "train",
            "class_rows_done": 256,
            "class_total": 512,
            "rows_done": 256,
            "total_rows": 1024,
            "chunk_rows": 128,
        },
        {
            "event": "train_batch",
            "stage": "training",
            "index": 1,
            "total": 8,
            "epoch": 3,
            "epochs": 24,
            "step": 40,
            "steps_per_epoch": 100,
            "train_loss": 0.68123,
            "learning_rate": 0.001,
        },
    ]
    progress_path.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in progress_rows) + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/tail_progress.py",
            str(progress_path),
            "--once",
            "--lines",
            "5",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "dataset_cache row 1/8 train cache_positive_chunk 256/512 50.0%" in completed.stdout
    assert "training row 1/8 epoch 3/24 step 40/100 40.0%" in completed.stdout
    assert "loss=0.68123" in completed.stdout
