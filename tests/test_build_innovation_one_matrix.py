import csv
import subprocess
import sys
from pathlib import Path


def test_build_innovation_one_matrix_can_emit_literature_ranked_top_k(tmp_path: Path):
    output_path = tmp_path / "recommended.csv"
    command = [
        sys.executable,
        "experiments/build_innovation_one_matrix.py",
        "--rounds",
        "3",
        "--seeds",
        "0",
        "--samples-per-class",
        "1024",
        "--top-k",
        "2",
        "--output",
        str(output_path),
    ]

    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    rows = list(csv.DictReader(output_path.open()))

    assert completed.returncode == 0
    assert len(rows) == 6
    assert {"architecture_rank", "score", "evidence", "literature"}.issubset(rows[0])
    speck_rows = [row for row in rows if row["cipher"] == "SPECK32/64"]
    assert speck_rows[0]["network"] == "ResNet-BitSlice"
    assert speck_rows[0]["architecture_rank"] == "1"
    assert "Gohr 2019" in speck_rows[0]["literature"]
    assert "Wrote 6 literature-ranked experiment rows" in completed.stdout

