from __future__ import annotations

import argparse
from pathlib import Path

from blockcipher_ai_eval.evaluation import (
    HPARAM_SUMMARY_FIELDS,
    hparam_summary_rows,
    load_jsonl_rows,
    write_csv_rows,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize HPO JSONL results to a sorted CSV.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = hparam_summary_rows(load_jsonl_rows(Path(args.input)))
    output = Path(args.output)
    write_csv_rows(output, rows, HPARAM_SUMMARY_FIELDS)
    print(f"wrote {len(rows)} HPO summary rows to {output}")


if __name__ == "__main__":
    main()
