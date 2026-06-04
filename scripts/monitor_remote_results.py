#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunSpec:
    run_id: str
    expected_rows: int

    @property
    def branch(self) -> str:
        return f"results/{self.run_id}"


def run_git(repo_root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def parse_run_spec(value: str) -> RunSpec:
    if "=" not in value:
        raise argparse.ArgumentTypeError("run spec must use RUN_ID=EXPECTED_ROWS")
    run_id, expected = value.split("=", 1)
    run_id = run_id.strip()
    if not run_id:
        raise argparse.ArgumentTypeError("run id cannot be empty")
    try:
        expected_rows = int(expected)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected rows must be an integer") from exc
    if expected_rows <= 0:
        raise argparse.ArgumentTypeError("expected rows must be positive")
    return RunSpec(run_id=run_id, expected_rows=expected_rows)


def branch_exists(repo_root: Path, remote: str, branch: str) -> bool:
    result = run_git(repo_root, ["ls-remote", "--heads", remote, branch], check=False)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git ls-remote failed"
        raise RuntimeError(message)
    return bool(result.stdout.strip())


def fetch_branch(repo_root: Path, remote: str, spec: RunSpec) -> str:
    local_ref = f"refs/remotes/{remote}/{spec.branch}"
    run_git(repo_root, ["fetch", remote, f"{spec.branch}:{local_ref}"])
    return local_ref


def read_file_from_ref(repo_root: Path, ref: str, relative_path: str) -> str:
    return run_git(repo_root, ["show", f"{ref}:{relative_path}"]).stdout


def verify_gate(repo_root: Path, ref: str, spec: RunSpec) -> None:
    gate_path = f"results_archive/{spec.run_id}/{spec.run_id}_result_gate.txt"
    gate = read_file_from_ref(repo_root, ref, gate_path)
    expected_lines = {
        f"result_lines={spec.expected_rows}",
        f"expected_rows={spec.expected_rows}",
    }
    observed = {line.strip() for line in gate.splitlines() if line.strip()}
    missing = expected_lines - observed
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise RuntimeError(f"{spec.run_id} gate mismatch, missing: {missing_text}")


def export_archive(repo_root: Path, ref: str, spec: RunSpec, output_dir: Path) -> None:
    destination = output_dir / spec.run_id
    tmp_destination = output_dir / f".{spec.run_id}.tmp"
    if tmp_destination.exists():
        shutil.rmtree(tmp_destination)
    tmp_destination.mkdir(parents=True, exist_ok=True)

    prefix = f"results_archive/{spec.run_id}/"
    files = run_git(repo_root, ["ls-tree", "-r", "--name-only", ref, prefix]).stdout.splitlines()
    if not files:
        raise RuntimeError(f"{spec.run_id} has no archived files at {prefix}")

    for file_name in files:
        relative = file_name.removeprefix(prefix)
        target = tmp_destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        content = run_git(repo_root, ["show", f"{ref}:{file_name}"]).stdout
        target.write_text(content, encoding="utf-8")

    if destination.exists():
        shutil.rmtree(destination)
    tmp_destination.replace(destination)


def check_and_retrieve(repo_root: Path, remote: str, specs: list[RunSpec], output_dir: Path) -> bool:
    missing = [spec.branch for spec in specs if not branch_exists(repo_root, remote, spec.branch)]
    if missing:
        print("WAIT missing result branches: " + ", ".join(missing))
        return False

    fetched_refs: list[tuple[RunSpec, str]] = []
    for spec in specs:
        ref = fetch_branch(repo_root, remote, spec)
        verify_gate(repo_root, ref, spec)
        fetched_refs.append((spec, ref))

    output_dir.mkdir(parents=True, exist_ok=True)
    for spec, ref in fetched_refs:
        export_archive(repo_root, ref, spec, output_dir)
        print(f"RETRIEVED {spec.run_id} -> {output_dir / spec.run_id}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor remote result branches and retrieve verified archives.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--interval-minutes", type=float, default=30.0)
    parser.add_argument("--once", action="store_true")
    parser.add_argument(
        "--run-id",
        dest="run_specs",
        action="append",
        type=parse_run_spec,
        required=True,
        help="Result run id and expected rows, formatted as RUN_ID=EXPECTED_ROWS.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    output_dir = args.output_dir or repo_root / "outputs" / "remote_results"

    while True:
        try:
            done = check_and_retrieve(repo_root, args.remote, args.run_specs, output_dir.resolve())
        except Exception as exc:
            print(f"BLOCKED {exc}", file=sys.stderr)
            if args.once:
                return 1
            sleep_seconds = max(args.interval_minutes, 0.1) * 60
            print(f"sleeping {sleep_seconds:.0f}s before next check")
            time.sleep(sleep_seconds)
            continue
        if done:
            print("DONE all remote results retrieved")
            return 0
        if args.once:
            return 2
        sleep_seconds = max(args.interval_minutes, 0.1) * 60
        print(f"sleeping {sleep_seconds:.0f}s before next check")
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
