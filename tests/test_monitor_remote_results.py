import importlib.util
import subprocess
from pathlib import Path


def load_module(repo_root: Path):
    script = repo_root / "scripts" / "monitor_remote_results.py"
    spec = importlib.util.spec_from_file_location("monitor_remote_results", script)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def commit_all(repo: Path, message: str):
    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", message], cwd=repo)


def write_result_archive(repo: Path, run_id: str, expected_rows: int):
    archive = repo / "results_archive" / run_id
    archive.mkdir(parents=True, exist_ok=True)
    (archive / f"{run_id}_result_gate.txt").write_text(
        f"result_lines={expected_rows}\nexpected_rows={expected_rows}\n",
        encoding="utf-8",
    )
    (archive / f"{run_id}_summary.csv").write_text("model,accuracy\nmlp,0.51\n", encoding="utf-8")
    (archive / f"{run_id}.jsonl").write_text('{"accuracy": 0.51}\n', encoding="utf-8")


def make_origin_with_result_branches(tmp_path: Path, run_ids: list[tuple[str, int]]) -> Path:
    origin = tmp_path / "origin.git"
    source = tmp_path / "source"
    run(["git", "init", "--bare", str(origin)])
    run(["git", "init", str(source)])
    run(["git", "config", "user.email", "tests@example.invalid"], cwd=source)
    run(["git", "config", "user.name", "Tests"], cwd=source)
    (source / "README.md").write_text("fixture\n", encoding="utf-8")
    commit_all(source, "initial")
    run(["git", "branch", "-M", "main"], cwd=source)
    run(["git", "remote", "add", "origin", str(origin)], cwd=source)
    run(["git", "push", "origin", "main"], cwd=source)

    for run_id, expected_rows in run_ids:
        run(["git", "checkout", "--orphan", f"results/{run_id}"], cwd=source)
        run(["git", "rm", "-rf", "."], cwd=source)
        write_result_archive(source, run_id, expected_rows)
        commit_all(source, f"results: {run_id}")
        run(["git", "push", "origin", f"results/{run_id}"], cwd=source)

    return origin


def make_local_repo(tmp_path: Path, origin: Path) -> Path:
    repo = tmp_path / "local"
    run(["git", "init", str(repo)])
    run(["git", "remote", "add", "origin", str(origin)], cwd=repo)
    return repo


def test_once_waits_when_any_result_branch_is_missing(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)
    origin = make_origin_with_result_branches(tmp_path, [("run-gpu0", 2)])
    local = make_local_repo(tmp_path, origin)

    code = module.main(
        [
            "--repo-root",
            str(local),
            "--remote",
            "origin",
            "--output-dir",
            str(local / "outputs" / "remote_results"),
            "--run-id",
            "run-gpu0=2",
            "--run-id",
            "run-gpu1=3",
            "--once",
        ]
    )

    assert code == 2
    assert not (local / "outputs" / "remote_results" / "run-gpu0").exists()


def test_once_fetches_verified_result_branches_to_outputs(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)
    origin = make_origin_with_result_branches(tmp_path, [("run-gpu0", 2), ("run-gpu1", 3)])
    local = make_local_repo(tmp_path, origin)

    code = module.main(
        [
            "--repo-root",
            str(local),
            "--remote",
            "origin",
            "--output-dir",
            str(local / "outputs" / "remote_results"),
            "--run-id",
            "run-gpu0=2",
            "--run-id",
            "run-gpu1=3",
            "--once",
        ]
    )

    assert code == 0
    for run_id, expected_rows in [("run-gpu0", 2), ("run-gpu1", 3)]:
        output = local / "outputs" / "remote_results" / run_id
        assert (output / f"{run_id}_summary.csv").read_text(encoding="utf-8").startswith("model,accuracy")
        assert f"result_lines={expected_rows}" in (output / f"{run_id}_result_gate.txt").read_text(
            encoding="utf-8"
        )


def test_once_blocks_when_remote_query_fails(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)
    local = tmp_path / "local"
    run(["git", "init", str(local)])
    run(["git", "remote", "add", "origin", str(tmp_path / "missing.git")], cwd=local)

    code = module.main(
        [
            "--repo-root",
            str(local),
            "--remote",
            "origin",
            "--run-id",
            "run-gpu0=2",
            "--once",
        ]
    )

    assert code == 1


def test_once_can_use_explicit_remote_url_without_local_remote(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    module = load_module(repo_root)
    origin = make_origin_with_result_branches(tmp_path, [("run-gpu0", 2)])
    local = tmp_path / "local-no-origin"
    run(["git", "init", str(local)])

    code = module.main(
        [
            "--repo-root",
            str(local),
            "--remote-url",
            str(origin),
            "--output-dir",
            str(local / "outputs" / "remote_results"),
            "--run-id",
            "run-gpu0=2",
            "--once",
        ]
    )

    assert code == 0
    assert (local / "outputs" / "remote_results" / "run-gpu0" / "run-gpu0_summary.csv").exists()
