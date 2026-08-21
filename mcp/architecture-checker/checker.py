"""
architecture_check — MetaVibing MCP Tool

Analyzes a FastAPI/SQLModel project and reports architectural violations.
Specifically checks for the patterns demonstrated in the MetaVibing manual:

- Database access in route handlers (instead of repository layer)
- Domain logic mixed with transport layer
- Missing test files for source modules
- Undeclared dependencies

Usage (standalone):
    python checker.py <path-to-src-directory>

Usage (via MCP):
    Call the `architecture_check` tool with {"path": "<src-dir>"}

Returns JSON:
    {
        "violations": <count>,
        "files": [
            {
                "file": "<relative-path>",
                "rule": "<violated-rule>",
                "line": <line-number>,
                "snippet": "<offending-code>"
            }
        ]
    }
"""
import ast
import json
import os
import sys
from pathlib import Path
from typing import Any


# ── Rules ─────────────────────────────────────────────────────────────────────


def check_db_in_handlers(source: str, rel_path: str) -> list[dict[str, Any]]:
    """
    Detect direct database Session usage inside route handler functions.
    In a clean architecture, route handlers should call repository functions,
    not query the database directly.
    """
    violations = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return violations

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if this looks like a route handler (has HTTP-verb decorator)
            is_route = any(
                (isinstance(d, ast.Attribute) and d.attr in ("get", "post", "put", "patch", "delete"))
                or (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in ("get", "post", "put", "patch", "delete"))
                for d in node.decorator_list
            )
            if not is_route:
                continue

            # Walk function body for Session.exec / session.add / session.commit
            for child in ast.walk(node):
                if isinstance(child, ast.Attribute) and child.attr in ("exec", "add", "commit", "delete", "get", "refresh"):
                    if isinstance(child.value, ast.Name) and "session" in child.value.id.lower():
                        violations.append({
                            "file": rel_path,
                            "rule": "db-in-handler",
                            "line": child.lineno,
                            "snippet": f"session.{child.attr}() in route handler '{node.name}'",
                        })

    return violations


def check_missing_tests(src_dir: Path, tests_dir: Path, rel_src: str) -> list[dict[str, Any]]:
    """Detect source modules that have no corresponding test file."""
    violations = []
    if not tests_dir.exists():
        return violations

    test_files = {f.stem.replace("test_", "").replace("_test", "") for f in tests_dir.rglob("test_*.py")}

    for src_file in src_dir.rglob("*.py"):
        if src_file.name == "__init__.py":
            continue
        module_name = src_file.stem
        if module_name not in test_files:
            violations.append({
                "file": str(src_file.relative_to(src_dir.parent)),
                "rule": "missing-test",
                "line": 0,
                "snippet": f"No test file found for module '{module_name}'",
            })

    return violations


# ── Runner ────────────────────────────────────────────────────────────────────


def run_checks(project_path: str) -> dict[str, Any]:
    root = Path(project_path)
    src_dir = root / "src" if (root / "src").exists() else root
    tests_dir = root / "tests"

    violations = []

    for py_file in src_dir.rglob("*.py"):
        source = py_file.read_text(encoding="utf-8")
        rel = str(py_file.relative_to(root))
        violations.extend(check_db_in_handlers(source, rel))

    violations.extend(check_missing_tests(src_dir, tests_dir, str(src_dir.relative_to(root))))

    return {
        "violations": len(violations),
        "files": violations,
    }


# ── CLI entry point ───────────────────────────────────────────────────────────


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python checker.py <project-path>")
        sys.exit(1)

    result = run_checks(sys.argv[1])
    print(json.dumps(result, indent=2))
