# MetaVibing — Project Operating Instructions

This repository contains a practical manual (`book/`) and a runnable example (`examples/taskflow/`) for engineering agents that improve their own working environment. It also uses its own method on itself — the meta-stack below is Claude Code's real, native configuration for this repository, not documentation about a configuration.

---

## Architecture

- **Manual**: `book/manuscript.md` — canonical source; built to `dist/` as PDF/DOCX (`scripts/build_manual.py`)
- **Demo application**: `examples/taskflow/` — FastAPI + SQLite + pytest
- **Meta-code artifacts**: `.claude/` — Rules and Skills, natively loaded; `final-reviewer` Agent, structurally read-only
- **Architecture checker**: `tools/architecture-checker/` — a standalone CLI, not an MCP server (the directory isn't named `mcp/` for exactly that reason)
- **Evaluation pilot**: `evals/` — frozen task prompts, held-out acceptance tests, a grading rubric, and a machine-readable protocol (`evals/protocol.yaml`); the 18-trial run itself has not happened yet

---

## Development

Install and run the sandbox project:
```bash
cd examples/taskflow
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Run sandbox tests:
```bash
cd examples/taskflow
pytest
```

Run the architecture checker (from repo root — pass the project root, not `src/`):
```bash
python tools/architecture-checker/checker.py examples/taskflow
```

Rebuild the manual (from repo root):
```bash
pip install -r requirements-dev.txt
python scripts/build_manual.py
```

---

## Change Discipline

- Make the **smallest change** that solves the requested problem.
- Do **not** refactor unrelated files.
- Do **not** claim success until relevant verification has run.
- Do **not** touch `examples/taskflow/` when working on `tools/` or `.claude/`, and vice versa.

---

## Completion Standard

Before saying a task is complete:

1. Inspect the final diff.
2. Run relevant tests (`pytest` for Python, check imports run cleanly).
3. Report failures explicitly.
4. Distinguish pre-existing failures from newly introduced ones.

---

## Git

- Never force-push.
- Never rewrite shared history.
- Do not commit secrets or local configuration files.
- Commit message format: `<type>(<scope>): <short description>` where type is `feat`, `fix`, `docs`, `refactor`, `test`, or `chore`.

---

## The Friction Ledger

Every recurring failure gets logged in `FRICTION_LEDGER.md`.

When you observe a pattern of repeated mistakes:
1. Log it under a new entry (F-XXX format).
2. Classify the failure type.
3. Propose a candidate intervention.
4. Track the evaluation result after applying the intervention — graded corrected / mechanically verified / behaviorally evaluated, not a single undifferentiated "done."

---

## Meta-Stack Reference

| Artifact | Purpose | Location | Status |
|----------|---------|----------|--------|
| CLAUDE.md | Persistent doctrine | `./CLAUDE.md` | Live |
| Rules | Path-scoped context | `.claude/rules/` | Live |
| Skills | Reusable procedures | `.claude/skills/` | Live |
| Agent | Specialist, read-only review | `.claude/agents/final-reviewer.md` | Live |
| Architecture checker | Deterministic invariant check | `tools/architecture-checker/` | Live (CLI only) |
| Hooks | Hard behavioral boundaries | — | Not present — build one when a Friction Ledger entry demands it, not before |

---

## Skills Available

- `/meta` — run a meta-audit: inspect CLAUDE.md, rules, friction ledger, identify gaps
- `/ship-change` — understand → implement → test → diff → review → report

Invoke with: `/<skill-name> <task description>`

---

## Architectural Constraints (taskflow/)

- Database access belongs in **repositories**, not route handlers.
- Domain logic must remain **independent of transport layers**.
- SQLite is the only permitted database for the sandbox project.
- Do not add external dependencies without updating `requirements.txt`.
