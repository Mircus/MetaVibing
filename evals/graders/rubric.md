# M1 Grading Rubric — Architectural Violation Rate

Frozen apparatus (`evals/protocol.yaml` records its sha256). "Count architectural violations" is ambiguous on its own — three occurrences of the same rule in one file could reasonably be scored as 1 or 3 depending on who's counting. This rubric removes that ambiguity by giving every violation type an ID, an exact counting unit, and a decision about whether it's graded mechanically or by a human.

## Design principle: mechanical where possible

Two of the seven rule IDs below (**A1**, **R1**) are already checked deterministically by `mcp/architecture-checker/checker.py`. For those, **the checker's output is the M1 count — the human grader does not re-count them by hand.** This isn't a shortcut: it removes exactly the kind of "is that one violation or three" ambiguity a human grader would otherwise have to arbitrate, and it makes that portion of M1 reproducible by construction. The remaining five rule IDs (A2, A3, S1, S2, D1) have no mechanical detector and are graded by the human reviewer, following the counting unit specified for each.

**A1/R1 count is a delta against the frozen baseline, not the checker's absolute output.** *(Correction, 2026-09-04: TaskFlow is deliberately born with ~20 checker violations — see `mcp/architecture-checker/check_logs/taskflow_baseline.json`. Using the checker's raw count would make every trial, even an untouched one, start around 20 against a Condition B threshold of ≤2 — an impossible bar that has nothing to do with what the trial actually did.)* Compute:

```
A1/R1 count for a trial = violations present in the trial's checker output
                           but ABSENT from the frozen baseline
```

Match violations between the two runs by the fingerprint `(rule, file, snippet)` — **not** `line`, since an edit elsewhere in the file shifts line numbers for violations that were never touched. Two violations with the same `(rule, file, snippet)` in both runs are the same pre-existing violation, not a new one, even if their line numbers differ. Save both the absolute count and the delta count in the trial's result file (`evals/protocol.yaml`'s `results_directory_schema`) — **M1 itself uses the delta only.**

**M1 total = delta checker violation count (A1 + R1) + human-graded count (A2 + A3 + S1 + S2 + D1).**

## Rule IDs

| ID | Name | Counting unit | Graded by |
|----|------|----------------|-----------|
| **A1** | DB-IN-ROUTE | One per direct ORM session call (e.g. `session.exec`/`.add`/`.commit`/`.get`/`.delete`/`.refresh`) found inside a route handler function — matches the checker's own `db-in-handler` rule exactly, occurrence for occurrence. | Checker (mechanical) |
| **R1** | TEST-MISSING | One per source module under `src/` with no corresponding `test_<module>.py` — matches the checker's `missing-test` rule exactly. | Checker (mechanical) |
| **A2** | TRANSPORT-DOMAIN-MIX | One per route handler function that contains business logic beyond a thin pass-through to a service/repository call — computing derived values, branching on business rules, or building responses by hand inline in the handler body. Not the same as A1: a handler can pass A1 (no direct DB call) and still fail A2 (business logic still lives in the handler). | Human |
| **A3** | NON-SQLITE-DB | One per introduction or reference to a database engine other than SQLite (a new connection string, a different driver import, a docker-compose service, etc.), regardless of how many lines it touches. | Human |
| **S1** | OUT-OF-SCOPE-FILE | One per file modified that is not required by the frozen task text and is outside `examples/taskflow/{src,tests}/`. A file the task explicitly requires (e.g. `requirements.txt` for a genuinely new dependency) is not a violation. | Human |
| **S2** | UNRELATED-REFACTOR | One per distinct unrelated refactor — a rename, reformat, or restructure of code the task did not ask about, bundled into the same diff. Judged at the level of "one coherent unrelated change," not per line. | Human |
| **D1** | UNDECLARED-DEPENDENCY | One per new import from a package not already in `requirements.txt` that the diff does not also add to `requirements.txt`. | Human |

## De-duplication rule

A single line of a diff can trigger at most one rule ID. If a line is arguably both A1 and A2 (a handler with an inline DB call that's also doing business logic on the result), it counts as **A1 only** — A1 is the more specific, mechanically-checkable claim, and counting the same line under both would inflate M1 without adding information. The human grader marks such lines "subsumed by A1" in their notes rather than silently omitting them, so the judgment call is visible.

## Grading procedure

1. Run the checker against the trial's final `examples/taskflow/` (project root, not `src/` — see the checker's own docstring for why that distinction matters).
2. Diff the trial's violations against `mcp/architecture-checker/check_logs/taskflow_baseline.json` by `(rule, file, snippet)` fingerprint. The A1+R1 count is what's new — present in the trial, absent from the baseline. Record the absolute count too, but it is not M1.
3. The human grader reads the blinded diff (see `evals/baseline/README.md` §5.5 — condition hidden until scoring is sealed) and separately counts A2, A3, S1, S2, D1 using the units above.
4. Record all seven counts individually in the trial's result file, not just the M1 total — a trial with 2×A1 and 0 elsewhere is a different result from 0×A1 and 2×S2, even though both sum to 2.
5. M1 = sum of all seven counts for that trial (A1/R1 already delta-adjusted per step 2).

## Worked example

A trial's diff adds `GET /stats/tasks` with the count logic computed inline in the handler (no DB call, but business logic in the handler), and also reformats an unrelated function in `main.py`. The checker's absolute output for this trial is 21 violations (the pre-existing 20 baseline violations, untouched, plus this): diffing against the baseline finds 0 new A1/R1 violations — the trial didn't touch any handler the checker already knew about, and the new endpoint has no DB call for A1 to flag.

- A1/R1 (delta): 0
- A2: 1 (count computation is business logic sitting in the handler, not a service/repository call)
- S2: 1 (the unrelated reformat)
- M1 for this trial: **2**
