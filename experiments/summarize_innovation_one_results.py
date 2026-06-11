from __future__ import annotations

import argparse
from pathlib import Path

from blockcipher_ai_eval.evaluation import (
    innovation_one_summary_fields,
    innovation_one_summary_rows,
    load_jsonl_rows,
    write_csv_rows,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize innovation-one JSONL results to CSV.")
    parser.add_argument("--input", required=True, help="Input JSONL result file.")
    parser.add_argument("--output", required=True, help="Output CSV summary file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_jsonl_rows(Path(args.input))
    summary = innovation_one_summary_rows(rows)
    output = Path(args.output)
    write_csv_rows(output, summary, innovation_one_summary_fields())
    print(f"wrote {len(summary)} summary rows to {output}")


if __name__ == "__main__":
    main()
