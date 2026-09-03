# MetaVibing — Project Operating Instructions

This is the MetaVibing companion repository. It contains a practical manual, runnable examples, experiments, templates, benchmarks, and progressively more sophisticated agent architectures for engineering agents that improve their own working environment.

---

## Architecture

- **Demo application**: `examples/taskflow/` — FastAPI + SQLite + pytest (live)
- **Meta-code artifacts**: `claude/` — rules, skills (live); agents (partial); hooks (planned, none implemented yet)
- **MCP tools**: `mcp/architecture-checker/` — live as a standalone CLI; MCP server wrapper is planned for v1.1
- **Evaluation framework**: `evals/baseline/` — charter written (live); the 18-trial run and `tasks/`/`graders/`/`results/` are planned, not yet executed or created
- **Experiments**: `experiments/` — planned, described in the book, does not exist in this repository yet

---

## Development

Install sandbox project:
```bash
cd examples/taskflow
pip install -r requirements.txt
```

Run sandbox tests:
```bash
cd examples/taskflow
pytest
```

Run architecture checker (from repo root):
```bash
python mcp/architecture-checker/checker.py examples/taskflow/src/
```

---

## Change Discipline

- Make the **smallest change** that solves the requested problem.
- Do **not** refactor unrelated files.
- Do **not** claim success until relevant verification has run.
- Do **not** touch `examples/taskflow/` when working on `mcp/` or `claude/`, and vice versa.

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
4. Track the evaluation result after applying the intervention.

---

## Meta-Stack Reference

| Artifact | Purpose | Location | Status |
|----------|---------|----------|--------|
| CLAUDE.md | Persistent doctrine | `./CLAUDE.md` | Live |
| Rules | Path-scoped context | `claude/rules/` | Live |
| Skills | Reusable procedures | `claude/skills/` | Live |
| Agents | Specialist subagents | `claude/agents/` | Partial |
| Hooks | Hard behavioral boundaries | `claude/hooks/` | Planned — none implemented yet |
| MCP tools | External capabilities | `mcp/` | Partial — architecture-checker is a standalone CLI; MCP wrapper planned for v1.1 |

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
