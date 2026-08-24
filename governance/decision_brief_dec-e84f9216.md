# Decision Brief: Evaluation Charter for MetaVibing
**Decision Gate:** dec-e84f9216  
**Status:** OPEN — awaiting human decision by Mirco  
**Produced by:** planner role, DECISION_BRIEF stage  
**Date:** 2026-08-24

---

## Context

This brief was written because **decision gate dec-e84f9216** is open and blocking forward progress. The gate was opened after a NO-GO judgment: writing `evals/baseline/README.md` without an agreed product claim risks locking in the wrong metrics. This brief does NOT resolve the gate — it structures the decision space so Mirco can make an informed choice.

---

## 1. What is the strongest possible core claim for MetaVibing?

**Strongest claim (falsifiable, differentiated, high-value):**

> A developer who applies the MetaVibing techniques in this manual — using CLAUDE.md, Rules, Skills, Agents, Hooks, and MCP tools — will reduce Claude Code's rate of repeated architectural violations by ≥50% and reduce the human correction overhead per feature by ≥30%, measured over a 10-session baseline on the TaskFlow sandbox.

**Why this is the strongest claim:**
- It is quantified and falsifiable against a real codebase (TaskFlow).
- It names the specific mechanism (meta-code artifacts) rather than just "better AI output."
- It anchors the MetaVibing concept to its core thesis: the meta-loop improves the product loop.
- It is achievable — the TaskFlow sandbox already has baseline intentional quirks and 8 passing tests to measure against.
- It differentiates from plain "prompt engineering" by requiring persistent artifacts that survive session restarts.

**Risk:** This claim requires actually running the 10-session baseline. If the uplift is weak (< 20%), the claim collapses and the book needs repositioning.

---

## 2. Alternative weaker/safer core claims

### 2a. Pedagogical claim (safer)
> This manual teaches a systematic, artifact-based approach to improving Claude Code's working behavior, illustrated with runnable examples in the TaskFlow sandbox.

- **Pros:** No quantitative commitment; can ship without running evals.
- **Cons:** No falsifiable value proposition; positions as tutorial, not method. Readers can't tell if it works.
- **Risk:** Reduces perceived value significantly. "Tutorial" competes with blog posts.

### 2b. Behavioral claim (medium)
> Developers who follow the MetaVibing method will observe measurably fewer repeated mistakes from Claude Code in the same project, using artifacts that persist across sessions.

- **Pros:** Falsifiable in spirit without hard numbers; qualitatively testable by any reader.
- **Cons:** "Measurably fewer" is vague; can't be reproduced or compared across practitioners.
- **Risk:** Medium — reviewers may flag it as hand-wavy; press may misrepresent.

### 2c. Conceptual framing claim (weakest)
> MetaVibing is the practice of deliberately improving the agentic system you work in, not just the artifacts it produces — analogous to improving a factory floor, not just running the machines.

- **Pros:** No empirical commitment whatsoever; positions the book as a conceptual contribution.
- **Cons:** Pure framing — no claim about outcomes. Does not justify a "companion repository."
- **Risk:** Low credibility risk but low value signal. Would not justify evals or benchmarks at all.

---

## 3. Primary user options, with consequences

### User Option A: Experienced software engineer moving to AI-assisted development (5–10 yrs experience)
- **Job-to-be-done:** "I want Claude Code to stop making the same mistakes across sessions and across projects."
- **Consequences of choosing this user:**
  - Must include concrete, technical content (code, hook scripts, CLAUDE.md templates).
  - Baseline tasks must be engineering-grade, not toy-level.
  - Metrics must reflect real friction reduction, not just test passage.
  - This user will read the companion repo, run the examples, and judge by behavior change observed.

### User Option B: Team lead or engineering manager evaluating AI coding tools
- **Job-to-be-done:** "I want a methodology for onboarding Claude Code that produces consistent, reviewable behavior across my team."
- **Consequences of choosing this user:**
  - Content must address team-scale: shared CLAUDE.md, rules proliferation, onboarding.
  - Baseline tasks shift toward consistency across developers, not just one session.
  - Harder to instrument; requires multi-user eval setup.
  - This user is less likely to run the companion repo themselves.

### User Option C: AI practitioner / researcher interested in self-improving agent systems
- **Job-to-be-done:** "I want working examples of agents that modify their own operational context and improve over iterations."
- **Consequences of choosing this user:**
  - Content must go beyond Claude Code tips to architectural patterns (the MetaAgents section).
  - Benchmarks must show multi-iteration learning curves, not one-shot performance.
  - Companion repo must include progression experiments, not just a stable example.
  - Hardest to satisfy; most ambitious scope.

**Recommended primary user:** Option A (experienced software engineer). Option C is a compelling secondary audience and the "MetaAgents Era" framing in the booklet already addresses it — but it should not gate the first release.

---

## 4. Which examples/taskflow baseline tasks should count

The TaskFlow README lists 7 baseline tasks. Three are marked "to be added" and therefore not yet runnable. The decision here is which tasks to designate as **shippability gates** for release v1.

### Runnable now (candidates for v1 gates):
| # | Task | Status | Why it counts |
|---|------|--------|---------------|
| 1 | Add pagination to `GET /tasks/` | Runnable | Tests feature addition with constraint (no breaking change) |
| 3 | Add a `priority` field to `Task` | Runnable | Tests model extension + migration; catches schema errors |
| 6 | Add a new endpoint without breaking compatibility | Runnable | Tests backwards compatibility discipline |

### Not yet runnable (v2 candidates):
| # | Task | Blocker |
|---|------|---------|
| 2 | Fix the failing authentication test | Test doesn't exist yet |
| 4 | Find the concurrency bug | Bug not yet introduced |
| 5 | Refactor the notification service | Service not yet added |
| 7 | Investigate a failing integration test | Test not yet added |

**Recommendation:** Designate Tasks 1, 3, and 6 as the v1 baseline gate. These three are coherent (add feature, extend model, add endpoint), fully runnable, and representative of the claim that MetaVibing reduces architectural violations (pagination belongs in service layer, model extension requires schema discipline, endpoint addition must not break existing callers).

---

## 5. Candidate metrics and numeric thresholds

### Primary metric: Architectural violation rate
- **Definition:** Number of Claude-produced code changes that violate a stated constraint in CLAUDE.md or a path-scoped Rule, per 10 feature requests.
- **Baseline (no MetaVibing):** To be established from evals run.
- **Proposed threshold:** ≤2 violations per 10 requests after MetaVibing artifacts are applied (≥80% reduction from baseline).
- **Why:** This is the direct measure of the meta-loop's value.

### Secondary metric: Human correction turns per task
- **Definition:** Number of follow-up prompts required to correct Claude's output per baseline task.
- **Baseline (no MetaVibing):** To be established.
- **Proposed threshold:** ≤1.5 correction turns per task after MetaVibing (vs. expected baseline of ~3–5 for architecturally constrained tasks).
- **Why:** Proxy for "cognitive overhead saved."

### Tertiary metric: Test passage rate on baseline tasks
- **Definition:** % of baseline tasks where `pytest` passes on first submission.
- **Proposed threshold:** ≥80% (≥2/3 of v1 gate tasks pass on first try without human correction).
- **Why:** Hard, reproducible signal. Currently 8/8 pass with no MetaVibing — but these tests don't yet cover the intentional quirks.

### Warning: metrics 1 and 2 require human-in-the-loop observation
A blind automated eval cannot count "architectural violations" without a grader. Options:
- (a) Human grader scoring transcripts (low cost, low reproducibility)
- (b) A rule-checking agent that reads diffs against CLAUDE.md (medium cost, automatable)
- (c) The existing `mcp/architecture-checker/` tool as grader (low cost, already exists — verify it covers the v1 constraint set)

---

## 6. Measurement protocol

### Acceptable and reproducible protocol for v1:

1. **Environment:** Fresh Python venv, `pip install -r requirements.txt` from `examples/taskflow/`. No external credentials. Seed: fixed random state not applicable (determinism is via task specification, not numeric seed).

2. **Prompts:** Each baseline task is given as a one-shot prompt to Claude Code in a fresh session, with no prior context except what is in CLAUDE.md and the active Rules.

3. **Condition A (Baseline):** CLAUDE.md is empty; no Rules, Skills, Agents, or Hooks active. Claude operates with default behavior only.

4. **Condition B (MetaVibing):** Full MetaVibing artifact stack active: CLAUDE.md populated from the manual's template, all path-scoped Rules, at least one Skill (`/ship-change`), architecture-checker Hook active.

5. **Trials:** Each task run 3 times per condition (n=3×3=9 total task-runs per condition). Report median and worst-case.

6. **Grading:** 
   - Automated: `pytest` result (pass/fail, no partial credit).
   - Human: reviewer counts architectural violations in the diff against the explicit constraints in CLAUDE.md (yes/no per constraint).

7. **Reproducibility requirement:** All prompts, diffs, and `pytest` outputs saved verbatim in `evals/baseline/`. A second experimenter must be able to reproduce the judgment from the artifacts alone.

8. **Exclusion criteria:** Any run where the LLM API returned an error or the session was interrupted is excluded and re-run once. If it fails again, it is recorded as a failure, not excluded.

---

## 7. Shipping gates

### PR-level gates (every PR to main):
- [ ] `pytest` passes (all 8 baseline tests, plus any new tests added by the PR).
- [ ] `mcp/architecture-checker` reports zero violations against current `examples/taskflow/src/`.
- [ ] No new files created under `examples/taskflow/src/` that bypass the repository pattern.
- [ ] CLAUDE.md and any modified Rules are consistent (no contradictions introduced).

### Release v1 gates (required before public announcement):
- [ ] Baseline tasks 1, 3, 6 each pass `pytest` under Condition B (MetaVibing active).
- [ ] Condition B produces ≤2 architectural violations across the 3 tasks (combined).
- [ ] `book/metavibing-manual.md` is human-reviewed and copyedited (not just mechanically extracted from .docx).
- [ ] All companion repo examples run end-to-end from a clean `git clone` with documented setup.
- [ ] The MCP architecture-checker is either (a) documented as a standalone CLI only, or (b) wrapped as a real MCP server — not in an ambiguous hybrid state.

### Stretch gate (v1.1):
- [ ] Condition A vs. Condition B comparison data is recorded in `evals/baseline/` with full methodology documented.

---

## 8. Risks / open decisions for Mirco

### Risk R1: The quantitative claim may not survive measurement
If the 3-task baseline shows <30% reduction in architectural violations, the book's core claim collapses. Mitigation: run a single-task pilot (Task 1 only, 3 trials) before committing the claim to the book.

### Risk R2: "MetaVibing" is a coined term with no prior literature
The book cannot be validated against external benchmarks. All comparisons are internal. Mitigation: frame the contribution as a practitioner method, not a scientific result; cite Claude's documented capabilities (hooks, rules, MCP) as evidence of mechanism.

### Risk R3: The companion repo's MCP architecture-checker is in an ambiguous state
CLAUDE.md documents it as runnable (`python mcp/architecture-checker/checker.py`), but whether it is actually an MCP server or just a CLI is unresolved. If it is used as the grader in the measurement protocol, this ambiguity undermines reproducibility. **Mirco must decide: MCP server or standalone CLI.**

### Risk R4: Baseline tasks 2, 4, 5, 7 are not yet runnable
If v1 ships before these exist, the taskflow README's promise ("results recorded in evals/baseline/") is hollow. Mitigation: either add the missing tasks before release, or explicitly mark them as v2 in the README.

### Open decision OD1: Primary user
Which of the three user options (A/B/C) is primary? This affects content prioritization in Parts IV–XIV of the book (the MetaAgents sections).

### Open decision OD2: Claim strength
Is the book claiming a quantitative uplift (strongest claim) or a pedagogical contribution (safest claim)? This must be settled before the evals charter is written, because the measurement protocol is only needed for the quantitative claim.

### Open decision OD3: Evaluation staffing
Running the eval requires ~2–4 hours of human grading time to score diffs. Is Mirco willing to commit to this before v1 ships, or should the evals be scoped to automated metrics only (pytest pass/fail)?

---

## 9. Recommended decision set

The following is the planner's recommendation. Mirco must approve, reject, or modify before work continues.

| # | Decision | Recommended choice | Rationale |
|---|----------|--------------------|-----------|
| D1 | Primary user | Option A (experienced software engineer) | Most direct audience for the content; most testable claim |
| D2 | Core claim strength | Strongest claim (quantitative uplift) | Differentiates the book; enables falsifiable evals |
| D3 | Baseline tasks for v1 gate | Tasks 1, 3, 6 | All runnable now; coherent coverage of the core constraints |
| D4 | Primary metric | Architectural violation rate + pytest pass rate | Directly measures what MetaVibing claims to improve |
| D5 | Eval protocol | 3 trials × 3 tasks × 2 conditions; human grading of diffs | Minimum reproducible standard |
| D6 | MCP checker | Relabel as standalone CLI for v1 | Removes ambiguity; can be upgraded to MCP server in v1.1 |
| D7 | Unrunnable tasks (2,4,5,7) | Mark as v2 in taskflow README | Honest scoping; avoids hollow promises |
| D8 | Evals charter production | Write evals/baseline/README.md after D1–D5 approved | Prevents optimize-the-wrong-objective |

---

## Human Gate Required

**This brief is an input to a human decision, not a resolved decision.**

Decision gate **dec-e84f9216** remains OPEN. Work on `evals/baseline/README.md` and the CI workflow is blocked until Mirco approves the recommended decisions (or a modified set) above.

Once Mirco provides decisions on D1–D8, the next action is: write `evals/baseline/README.md` anchored to the approved claim, tasks, metrics, and protocol — making the evals charter a direct consequence of the decisions, not a guess.
