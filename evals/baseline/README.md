# MetaVibing — Baseline Evaluation Charter

**Decision gate:** dec-e84f9216 (resolved 2026-08-24)  
**Charter version:** v1.0  
**Governed by:** Mirco's resolutions D1–D8 (see `.hyri/decision_gate_dec-e84f9216_resolved.md`)

This charter defines what the MetaVibing baseline evaluation covers, how it is run, and what constitutes a passing result. It is a direct consequence of the decisions made in the Evaluation Charter gate — not a speculative design. Every section traces back to a resolved decision.

---

## 1. Core Claim Being Tested

> **MetaVibing is a governed workflow discipline for using AI agents as bounded workers under explicit context, artifact, validator, and human-gate controls.**
> *(D1 — Mirco's resolution)*

In concrete, testable terms: a practitioner who applies the MetaVibing discipline — using CLAUDE.md, path-scoped Rules, reusable Skills, specialist review (an Agent), and deterministic architectural checking — will produce a higher rate of first-try successes on architecturally constrained tasks, commit fewer repeated architectural violations per session, and require fewer human correction turns per feature request, compared to the same practitioner operating without any MetaVibing artifacts.

*(Scope correction, 2026-09-03: the claim previously named Hooks and MCP tools alongside the rest of the stack. Neither exists in this repository yet — see README Status — so a v1 evaluation cannot test them. Narrowed to the five layers that are actually implemented. Hooks and MCP are candidate v1.1+ interventions, to be evaluated separately once built for a reason the Friction Ledger surfaces, not to fill out the diagram.)*

This is a **quantitative, falsifiable claim**. The evals in this directory exist to test it against a controlled sandbox. If the measured uplift is weak, the claim must be revised — the eval does not exist to confirm the claim; it exists to challenge it.

**The companion sandbox:** All measurements use `examples/taskflow/` — a deliberately imperfect FastAPI + SQLite application with intentional quirks (database access in route handlers, no pagination, no `priority` field). See [`examples/taskflow/README.md`](../../examples/taskflow/README.md) for the full list of quirks, the baseline test suite, and the rationale for its deliberate imperfections.

---

## 2. Target User

**Primary:** Technical creators, researchers, and small lab builders using AI tools for multi-step intellectual or software artifacts.  
*(D2 — Mirco's resolution)*

**Operationalised for the eval:** A practitioner with sufficient engineering fluency to run `pytest`, read FastAPI code, and follow a CLAUDE.md prompt. They do not need to know how MetaVibing works at the start of the evaluation — the protocol hands them the artifact stack or withholds it depending on the condition.

**Secondary audience** (not gating v1): Engineering managers evaluating team-scale AI coding discipline; AI/agent researchers interested in self-modifying operational contexts. The TaskFlow sandbox and the eval protocol are designed to be legible to all three, but only the primary user's success criteria gate the v1 release.

---

## 3. Baseline Tasks

Three tasks from [`examples/taskflow/README.md`](../../examples/taskflow/README.md) are the v1 shippability gates (D3). They were selected because they are fully runnable now and collectively cover the core MetaVibing claim: feature addition under layout constraints, model extension requiring schema discipline, and backwards-compatible endpoint addition.

| Task ID | Description | TaskFlow section | Runnable in v1? |
|---------|-------------|-----------------|-----------------|
| **T1** | Add pagination to `GET /tasks/` | Baseline task 1 | ✅ Yes |
| **T3** | Add a `priority` field to `Task` | Baseline task 3 | ✅ Yes |
| **T6** | Add a new endpoint without breaking compatibility | Baseline task 6 | ✅ Yes |

**Why these three:** T1 exercises the service-layer constraint (database access must not live in route handlers); T3 exercises model extension and migration discipline; T6 exercises backwards-compatibility hygiene. Together they are a coherent minimal battery for the core architectural constraints stated in [`CLAUDE.md`](../../CLAUDE.md).

**Tasks not in scope for v1 (D7 — mark as v2):**

| Task ID | Description | Blocker |
|---------|-------------|---------|
| T2 | Fix the failing authentication test | Test does not exist yet |
| T4 | Find the concurrency bug | Bug not yet introduced |
| T5 | Refactor the notification service | Service not yet added |
| T7 | Investigate a failing integration test | Test not yet added |

These tasks are tracked but excluded from the v1 gate. Claiming v1 coverage for them would be hollow. They will be added when the prerequisite code exists.

---

## 4. Metrics and Thresholds

Three metrics are collected per condition, per task (D4):

### M1 — Architectural Violation Rate (primary)

**Definition:** Number of Claude-produced code changes per task that violate a stated constraint in `CLAUDE.md` or a path-scoped Rule, as judged by a human reviewer counting violations in the diff.

**Condition A (no MetaVibing):** baseline to be established from first eval run.  
**Condition B (MetaVibing active):** target **≤ 2 violations total across all 3 tasks** (combined, 3 trials each).

**Threshold rationale:** The MetaVibing claim is that the discipline reduces architectural drift. ≤ 2 combined violations across 9 task-trials is a meaningful bar — it allows for one error without disqualifying the method, but not systematic drift.

### M2 — Human Correction Turns per Task (secondary)

**Definition:** Number of follow-up prompts required to correct Claude's output per task, beyond the initial task prompt.

**Condition A baseline:** expected 3–5 correction turns for architecturally constrained tasks.  
**Condition B threshold:** **mean ≤ 1.5 correction turns per task**, averaged across the 3 trials.

*(Correction, 2026-09-03: "median across 3 trials" was mathematically incoherent — the median of three integers is itself an integer, so "≤1.5" was equivalent to "≤1." Switched to mean, which is what a 1.5 threshold actually expresses.)*

**Why:** Correction turns are a direct cost proxy. They are observable and recordable without additional tooling.

### M3 — Pytest Pass Rate on First Submission (tertiary)

**Definition:** Percentage of Condition B task-trials (3 tasks × 3 trials = 9 total) where `pytest` passes on first Claude submission, with no human correction.

**Threshold:** **≥ 8 of 9 Condition B task-trials (≈88.9%).**

*(Correction, 2026-09-03: the original text — "≥80% (at least 2 of 3 tasks)" — was internally contradictory; 2/3 is 66.7%, not 80%, and no value at 3-task granularity equals 80% at all. Redefined at 9-trial granularity to match how M1 is already counted, and because it's the only reading where "≥80%" is achievable as a distinct value from "all trials pass.")*

**Note:** All 8 baseline tests currently pass with no MetaVibing artifacts active. This rate is expected to drop when task prompts exercise the intentional quirks. The v1 threshold is set for *Condition B performance*, not baseline fidelity.

### What these metrics do NOT measure

- General code quality outside the TaskFlow constraints.
- LLM capability independent of the MetaVibing artifacts (this is not a model benchmark).
- User satisfaction or subjective experience.
- Performance at scale (> 3 tasks, > 2 conditions, > 1 practitioner).

---

## 5. Measurement Protocol

*(D5 — operationalised from the brief)*

### 5.1 Environment

- Fresh Python virtual environment: `python -m venv .venv && source .venv/bin/activate`.
- Install: `pip install -r examples/taskflow/requirements.txt`, then freeze it (`pip freeze`) into the trial's saved metadata — don't just trust the pin in `requirements.txt`, record what was actually installed.
- No external credentials. No project-wide config beyond what is committed.
- Operating system: Linux or macOS (not Windows — path behaviour untested).
- LLM API: Claude (current production model at time of run). Model version recorded in run log.
- **Every task-trial starts from the same frozen commit SHA, in its own disposable git worktree (or clone), destroyed after the trial.** A fresh Claude Code session alone does not guarantee a fresh repository — a previous trial's leftover diff sitting in a shared working tree would contaminate the next one. Record the baseline SHA in `evals/protocol.yaml`; every trial's saved metadata includes the worktree path and the SHA it was created from.

### 5.2 Conditions

**Condition A — Baseline (no MetaVibing):**
- `CLAUDE.md` is empty or absent.
- No Rules, Skills, Agents, or Hooks active.
- Claude operates with default behaviour only.
- Claude is given the frozen task text (`evals/tasks/T*.md`) directly, as the initial prompt — no skill invocation.

**Condition B — MetaVibing active:**
- `CLAUDE.md` populated from the manual's template (full architectural constraints active — see [`CLAUDE.md`](../../CLAUDE.md) for the current canonical version).
- All path-scoped Rules active (sourced from `.claude/rules/`, loaded natively by Claude Code).
- The `/ship-change` Skill and `final-reviewer` subagent (`.claude/skills/ship-change/`, `.claude/agents/final-reviewer.md`) available.
- Architecture-checker active as standalone CLI grader: `python mcp/architecture-checker/checker.py examples/taskflow` (project root, not `src/` — see the checker's own docstring; D6 — relabelled as standalone CLI for v1; MCP server upgrade is a v1.1 item).
- **The initial prompt is standardized, not left to chance:** Claude is given `/ship-change <verbatim frozen task text>`, not the bare task text. "The Skill is available" does not guarantee any given trial actually invokes it — some B trials might and some might not, which would silently turn Condition B into two different conditions. Standardizing the invocation makes the intervention itself the fixed variable between A and B, not "whichever trials happened to reach for the Skill."

### 5.3 Trial Design

- **3 tasks × 3 trials × 2 conditions = 18 task-trials total.**
- Each trial: fresh Claude Code session, task prompt given verbatim (prompts stored in `evals/tasks/`), no prior context except what is in the active CLAUDE.md and Rules.
- Report **mean and worst-case** for M2, and **pass count and worst-case** for M3, across the 3 trials per task. Report **combined count** for M1 across all 9 Condition B trials.
- **Condition order is precommitted and counterbalanced per task, not fixed A-then-B.** Running all of Condition A before any of Condition B lets the practitioner's own task-specific learning (not MetaVibing) explain a B-condition improvement. Each task gets its own fixed 6-run order set before any trial starts, and it is not changed based on how earlier trials went:

  | Task | Trial order (A/B), 6 runs = 3×A + 3×B |
  |------|----------------------------------------|
  | T1 | A, B, B, A, A, B |
  | T3 | B, A, A, B, B, A |
  | T6 | A, B, A, B, A, B |

  This table is now superseded — **`evals/protocol.yaml`** holds the actual generated order (seed `20260904`, `random.Random(seed).shuffle()`, one call per task in T1/T3/T6 order) and is the authoritative sequence. This table stays here only to illustrate the principle inline; if the two ever disagree, `protocol.yaml` wins.

### 5.4 What counts as "first submission" (governs M2 and M3)

*(Added 2026-09-04 — without this, A/B trials are not comparable: nothing else defines when a trial's "first attempt" ends and a human correction begins.)*

**First submission** is the filesystem state at the moment Claude first returns a terminal completion response to the human after receiving the initial frozen task text (`evals/tasks/T*.md`) — the initial invocation, nothing more. Everything before that point counts as part of the same, single first attempt, including: reading files, editing repeatedly, running `pytest` itself, invoking `final-reviewer`, noticing and fixing its own failures, and any other self-directed iteration. Snapshot the diff and run the acceptance tests / checker / baseline pytest independently at that point — do not let Claude's own self-report of success substitute for it.

A human sending any further message intended to repair an unsatisfactory result — starting with the literal text `fix this` or equivalent — begins **correction turn 1**, and each subsequent such message begins the next correction turn. A message that only asks a clarifying question, without asking for a repair, does not count as a correction turn.

### 5.5 Grading

**Automated (M3):**
```bash
cd examples/taskflow
pytest
```
Record full output verbatim in `evals/results/`, snapshotted at first submission (§5.4). Pass = all baseline tests green plus the task's acceptance tests (`evals/acceptance/test_<task-id>.py`) green. Fail = any red.

**Automated (M2):** correction turns are counted from the trial transcript/run log per the §5.4 definition — mechanically, from the record of human messages sent, not judged by a human reading the code diff. This removes M2 from human grading entirely; a grader disagreeing with the code is not the same event as a human having to ask for a fix.

**Human grading (M1 only):** M1 is graded per `evals/graders/rubric.md` — atomic rule IDs (A1, A2, A3, R1, S1, S2, D1), each with an exact counting unit, so "how many violations" doesn't depend on who's counting. Two of the seven rule IDs (A1, R1) are graded by the architecture-checker mechanically, not by the human reviewer, for the same reason. The human grader scores only the remaining five.
- **Grading is blinded where possible.** The diff is presented to the grader as `Trial <n> / Task <id> / Condition: hidden`, without CLAUDE.md/Rules visible in the diff itself and without the grader having run the trial. Condition is revealed only after the rubric's counts are recorded, to keep expectation bias out of the primary metric.

### 5.6 Reproducibility Standard

All of the following are saved verbatim to `evals/results/<task-id>/<condition>/<trial-n>/`:
- The exact prompt text used.
- The full Claude Code session transcript (or diff if full transcript is unavailable).
- The `pytest` output.
- The human grader's violation count and correction turn count.

A second experimenter must be able to reproduce the grading judgment from these artifacts alone without access to the original session.

### 5.7 Exclusion and Error Handling

- Any trial where the LLM API returned an error or the session was interrupted: **re-run once**. If the re-run also fails, record it as a trial failure (not excluded).
- Any trial where the practitioner accidentally provided out-of-condition context (e.g., CLAUDE.md loaded in a Condition A session): discard and re-run.
- Do not exclude trials because the result is bad — a bad result is valid data.

---

## 6. Pass/Fail Gates

### PR-level gates (every PR to `main`)

Before any PR is merged:
- [ ] `pytest` passes — all 8 baseline tests plus any new tests in the PR.
- [ ] `python mcp/architecture-checker/checker.py examples/taskflow` reports **no more violations than the committed baseline** (`mcp/architecture-checker/check_logs/taskflow_baseline.json`, currently 20 — TaskFlow is intentionally born with `db-in-handler` and `missing-test` violations; "zero violations" is not an achievable baseline for this sandbox and was never a meaningful gate). Fail if the PR increases the count, or introduces a violation class absent from the baseline.
- [ ] No new files created under `examples/taskflow/src/` that bypass the repository pattern.
- [ ] `CLAUDE.md` and any modified Rules are internally consistent (no contradictions).

### Release v1 gates (required before public announcement)

Before MetaVibing v1 is announced publicly:
- [ ] **The full 18-trial Condition A vs. Condition B comparison is run and published** in `evals/results/`, including A→B deltas for M1, M2, and M3 — see "Comparative evidence" below. This was previously listed as a v1.1 stretch gate; that was backwards, since the core claim (§1) is explicitly comparative and Condition B results alone cannot confirm it (§7).
- [ ] **Pooled Condition B M3 across T1+T3+T6 is ≥8/9** *(corrected 2026-09-04 — M3 is defined in §4 as pooled across all 9 Condition B task-trials, not 8/9 per individual task, which only has 3 trials each; the previous wording here contradicted the metric's own definition)* — not merely "pass on the mean/median trial." A pooled 6/9 with 3 failures hidden inside an average does not meet the gate.
- [ ] **Condition B produces ≤ 2 architectural violations total** across T1 + T3 + T6 (combined across all trials).
- [ ] Grader rubric (`evals/graders/rubric.md`) is documented and grading was blinded per §5.5.
- [ ] `book/manuscript.md` is human-reviewed and copyedited — not just mechanically extracted.
- [ ] All companion repo examples run end-to-end from a clean `git clone` with documented setup.
- [ ] The architecture-checker is documented clearly as a **standalone CLI only** for v1 (MCP server wrapper is a v1.1 item — see D6).
- [ ] Results are reported and labeled as a **pilot** (one practitioner, 3 tasks) — not broad validation of AI-assisted engineering. See "Pilot, not confirmatory study" below.

### Comparative evidence (why this moved out of "stretch")

§1's core claim is stated as comparative — MetaVibing performs *better than the same practitioner without it*. §7 already said "Condition B run without a verifiable Condition A baseline... cannot confirm uplift." A release gate that didn't require the comparison contradicted the charter's own claim and its own non-success table. Report the comparison as three deltas, not a single pass/fail:
- Δ M1 (Condition A violations − Condition B violations)
- Δ M2 (Condition A mean correction turns − Condition B mean correction turns)
- Δ M3 (Condition A pass rate − Condition B pass rate)

No arbitrary "N% better" threshold is imposed for this first run. Report the effect sizes honestly; use them to set a preregistered threshold for a larger confirmatory study, not to retroactively justify this one.

### Pilot, not confirmatory study

3 tasks × 3 trials × 1 practitioner is enough to find out whether there is signal. It is not enough to support a broad claim about AI-assisted engineering — the tasks are also not held out (the artifacts under test were written with knowledge of exactly what these tasks check). Label the published results a **pilot**. A confirmatory follow-up (more tasks, ideally more than one practitioner, at least one held-out task not named in any MetaVibing artifact) is future work, tracked separately — not a blocker for publishing the pilot honestly.

### Deferred to v1.1

- [ ] T2, T4, T5, T7 are runnable and added to the task battery.
- [ ] Ablations isolating which layer of the stack (CLAUDE.md alone, + a Rule, + a Skill, + the reviewer Agent, + the checker) carries the improvement.
- [ ] Real MCP server for the architecture-checker, and a first protective Hook — built because a Friction Ledger entry demands one, not to fill out the Meta-Stack diagram.

### Gate status accounting

A stage or release is **BLOCKED** if any must-pass gate is unresolved. **DELIVERED** status requires all must-pass gates green AND no unresolved human decision gates. A human gate that is merely *pending* (not yet answered) is sufficient to block DELIVERED — it does not require the gate to have been answered negatively.

---

## 7. What Does Not Count as Success

The following outcomes do **not** satisfy the v1 release criteria, regardless of what other checks pass:

| Non-success outcome | Why it does not count |
|--------------------|-----------------------|
| **Status summary only** | A report describing what the eval will measure, without actually running it, is not an eval result. |
| **Scaffold only** | A directory structure with empty files or placeholder content is not a baseline measurement. |
| **Pytest passing under Condition A alone** | Passing tests with no MetaVibing artifacts proves nothing about the discipline's effect. |
| **M3 threshold met (≥8/9) but M1 violations > 2** | Test passage without architectural discipline is a partial result, not a gate pass. |
| **Condition B run without a verifiable Condition A baseline** | The claim is comparative. Condition B results alone cannot confirm uplift. |
| **Human grading of diffs not saved** | Grading that cannot be reproduced by a second reviewer does not meet the reproducibility standard. |
| **Apparatus paths touched** | Any changes to the *immutable apparatus* — `evals/tasks/`, `evals/graders/`, `evals/protocol.yaml`, `.claude/`, `CLAUDE.md`, `mcp/architecture-checker/checker.py`, `book/`, `.github/`, or `governance/` — during a task-trial invalidate that trial. This does **not** include `examples/taskflow/src/` or `examples/taskflow/tests/` — those are the *mutable experimental target* T1/T3/T6 are supposed to modify; forbidding changes there would make a successful trial invalidate itself. *(Correction, 2026-09-03: the original list included `examples/taskflow/src/`/`tests/`, contradicting the task definitions in §3, which require modifying exactly those paths.)* |
| **Human gate unresolved → DELIVERED claimed** | A stage or release cannot be marked DELIVERED while a decision gate is open, regardless of automated checks. |

---

## Reference Map

| Decision | Location |
|----------|----------|
| Resolved gate (D1–D8) | `.hyri/decision_gate_dec-e84f9216_resolved.md` |
| Full decision brief | `governance/decision_brief_dec-e84f9216.md` |
| TaskFlow sandbox | `examples/taskflow/README.md` |
| Architectural constraints | `CLAUDE.md` (section: Architectural Constraints) |
| Architecture checker CLI | `mcp/architecture-checker/checker.py` |
| Task prompts (frozen) | `evals/tasks/T1.md`, `T3.md`, `T6.md` |
| T3 pre-existing-database fixture | `evals/tasks/fixtures/T3_pre_existing_taskflow.db` |
| Acceptance tests (apparatus, run after first submission) | `evals/acceptance/test_T1.py`, `test_T3.py`, `test_T6.py` |
| Grader rubric | `evals/graders/rubric.md` |
| Machine-readable frozen protocol | `evals/protocol.yaml` |
| Trial results | `evals/results/<task-id>/<condition>/<trial-n>/` |
