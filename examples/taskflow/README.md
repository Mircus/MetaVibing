# TaskFlow — The MetaVibing Sandbox

TaskFlow is a deliberately small FastAPI application used throughout the *MetaVibing* manual as a reproducible laboratory. It is **not** a production template — it is intentionally imperfect in places so readers can watch Claude's behavior improve through progressive meta-code interventions.

## The Intentional Quirks

| Quirk | Introduced | Fixed in |
|-------|-----------|----------|
| Database access in route handlers | Baseline | Part III |
| No pagination on list endpoints | Baseline | Ch. 18 experiment |
| No email uniqueness validation | Baseline | Ch. 20 experiment |
| No `priority` field on tasks | Baseline | Baseline task 3 |
| No `created_at` timestamp | Baseline | Ch. 22 experiment |

## Running

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

API docs at: http://localhost:8000/docs

## Testing

```bash
pytest
```

All 8 baseline tests should pass on a clean checkout.

## Structure

```
taskflow/
├── src/
│   ├── __init__.py
│   ├── main.py       ← FastAPI app + route handlers
│   ├── models.py     ← SQLModel data models (User, Task)
│   └── database.py   ← SQLite engine + session factory
├── tests/
│   ├── __init__.py
│   └── test_tasks.py ← baseline test suite
├── README.md
└── requirements.txt
```

## Baseline Tasks (evals/)

The following tasks are given to vanilla Claude Code before any MetaVibing intervention. Results are recorded in `evals/baseline/`.

1. Add pagination to `GET /tasks/`
2. Fix the failing authentication test (to be added)
3. Add a `priority` field to `Task`
4. Find the concurrency bug (to be introduced)
5. Refactor the notification service (to be added)
6. Add a new endpoint without breaking compatibility
7. Investigate a failing integration test (to be added)
