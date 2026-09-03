"""Unit tests for the architecture checker CLI (mcp/architecture-checker/checker.py).

Run with: pytest mcp/architecture-checker/test_checker.py
"""
import json
import subprocess
import sys
import textwrap
from pathlib import Path

CHECKER = Path(__file__).parent / "checker.py"


def _write_project(tmp_path: Path, src_files: dict[str, str], test_files: dict[str, str] | None = None) -> Path:
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    for name, content in src_files.items():
        (src_dir / name).write_text(textwrap.dedent(content), encoding="utf-8")

    if test_files:
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        for name, content in test_files.items():
            (tests_dir / name).write_text(textwrap.dedent(content), encoding="utf-8")

    return tmp_path


def _run_checker(project_root: Path) -> tuple[dict, int]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), str(project_root)],
        capture_output=True, text=True,
    )
    return json.loads(proc.stdout), proc.returncode


def test_detects_db_in_route_handler(tmp_path):
    project = _write_project(tmp_path, {
        "routes.py": """
            from fastapi import APIRouter
            router = APIRouter()

            @router.get("/tasks")
            def list_tasks(session):
                return session.exec("select * from tasks")
        """,
    }, {"test_routes.py": "def test_placeholder(): pass"})

    result, code = _run_checker(project)
    assert result["violations"] == 1
    assert result["files"][0]["rule"] == "db-in-handler"
    assert code == 1


def test_clean_repository_layer_is_not_a_violation(tmp_path):
    project = _write_project(tmp_path, {
        "routes.py": """
            from fastapi import APIRouter
            router = APIRouter()

            @router.get("/tasks")
            def list_tasks(repo):
                return repo.list_tasks()
        """,
    }, {"test_routes.py": "def test_placeholder(): pass"})

    result, code = _run_checker(project)
    assert result["violations"] == 0
    assert code == 0


def test_missing_test_file_is_flagged(tmp_path):
    project = _write_project(tmp_path, {"orphan.py": "def f(): pass"}, {"test_other.py": "def test_x(): pass"})

    result, _ = _run_checker(project)
    assert any(v["rule"] == "missing-test" for v in result["files"])


def test_passing_src_dir_directly_does_not_silently_hide_missing_test_violations(tmp_path):
    """Regression: tests_dir used to resolve as <arg>/tests, so calling the
    checker with src/ as the argument (the old documented invocation)
    made tests_dir resolve under src/ (which never exists), and the
    missing-test check silently returned zero violations. This asserts
    the *root* invocation still finds the real tests/ directory and
    genuinely detects a missing test."""
    project = _write_project(tmp_path, {"orphan.py": "def f(): pass"}, {"test_other.py": "def test_x(): pass"})

    result, _ = _run_checker(project)  # project root, not project/src
    assert result["violations"] > 0


def test_syntax_error_is_reported_not_silently_passed(tmp_path):
    project = _write_project(tmp_path, {"broken.py": "def f(:\n    pass"})

    result, code = _run_checker(project)
    assert result["errors"], "a parse failure must be reported, not treated as zero violations"
    assert result["errors"][0]["file"] in ("broken.py", "src/broken.py", "src\\broken.py")
    assert code == 1


def test_exit_code_zero_only_when_clean(tmp_path):
    project = _write_project(tmp_path, {"clean.py": "def f(): pass"}, {"test_clean.py": "def test_f(): pass"})

    _, code = _run_checker(project)
    assert code == 0
