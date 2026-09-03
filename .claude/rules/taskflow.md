---
globs: examples/taskflow/**/*
---

# Rules: TaskFlow Sandbox

*Applies when working in `examples/taskflow/`.*

## Architecture

- Database access belongs in the repository layer — **not** in route handlers.
- Domain logic must remain independent of the FastAPI transport layer.
- SQLite is the only permitted database. Do not swap to PostgreSQL or any other engine.

## Testing

- All changes to `src/` must be accompanied by a corresponding test in `tests/`.
- Run `pytest` before claiming a task complete.
- A failing test that existed before your change is **pre-existing** — distinguish it explicitly from failures you introduced.

## Dependencies

- Do not add external dependencies without updating `requirements.txt`.
- Do not pin to a specific sub-patch version unless a known bug requires it.

## Scope

- Do not modify files outside `examples/taskflow/` when working on the sandbox project.
- Do not refactor other modules while fixing a targeted bug.
