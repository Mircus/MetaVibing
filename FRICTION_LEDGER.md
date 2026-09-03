# Friction Ledger

> *A public log of recurring Claude failures and the artifacts that resolved them.*
>
> This document is central to MetaVibing. Every entry here represents a human correction that should eventually become unnecessary through persistent meta-code.
>
> **Format:** F-NNN | Failure description | Occurrences | Intervention | Evaluation result

---

## Status vocabulary

A single "closed" status hides a real distinction. Every entry below uses one of three tiers,
weakest to strongest:

- **corrected** — the artifact/text was fixed. Nobody has re-checked it since.
- **mechanically verified** — an automated or structural check confirms the fix holds (a test
  passes, a parser accepts the frontmatter, an arithmetic claim is internally consistent).
- **behaviorally evaluated** — the fix was exercised in the actual real-world path it's meant to
  protect (a real Claude Code session actually loaded the Skill; the metric was actually computed
  from real trial data) and produced the expected outcome.

Do not mark an entry "closed" merely because text changed. Name the tier honestly.

## Active Entries

*(See Closed Entries below — everything opened this session was also closed this session. This
line stays here, not deleted, because the day an entry sits open across a session boundary, this
is where it should already be looked for.)*

---

## Closed Entries

### F-001

**Failure:** README.md and CLAUDE.md described directories, links, and capabilities (`experiments/`, `patterns/`, `templates/`, packaged v2 docx/pdf) that did not exist in the repository.

**Occurrences:** 1 (caught by an external review of the newly-public repo, 2026-09-03).

**Diagnosis:** Missing evaluation criterion — nothing checked README claims against actual repository contents before a governed stage marked documentation DELIVERED.

**Chosen intervention:** Direct maintenance edit (not a governed run — this corrects the description of reality, not reality itself; see the commit's own rationale).

**Artifact created:** README.md, CLAUDE.md status/structure sections (commit `023efd9`).

**Evaluation:** corrected. Not mechanically verified — no automated doc/reality consistency check exists yet (candidate future Hook or CI check, deferred).

**Status:** corrected

**Closed date:** 2026-09-03

---

### F-002

**Failure:** The M3 evaluation metric was internally contradictory — "≥80% (at least 2 of 3 tasks)" — 2/3 is 66.7%, and no value at 3-task granularity equals 80%.

**Occurrences:** 1 (caught by external review; passed HyRI's own validators and a human approval gate without being caught).

**Diagnosis:** Missing evaluation criterion — validators check structural presence (required sections, artifact hash), not semantic/arithmetic correctness of the content they validate.

**Chosen intervention:** Direct correction, decided outside the governed pipeline (Mirco: "I trust that either you or GPT has better chances" than routing an editorial-judgment call through governance ceremony).

**Artifact created:** `evals/baseline/README.md` M3 section (commit `af937d5`) — redefined at 9-trial granularity, ≥8/9.

**Evaluation:** corrected + mechanically verified (8/9 ≈ 88.9% is a real, internally consistent value; the fix was checked by hand-computing the fraction, not just declared). Not behaviorally evaluated — no real trial has been graded against this threshold yet.

**Status:** corrected, mechanically verified

**Closed date:** 2026-09-03

---

### F-003

**Failure:** The `.claude/`-equivalent meta-stack (Rules, Skills, Agent) lived under `claude/` with no leading dot and no YAML frontmatter — Claude Code could not actually load any of it. The repo, CLAUDE.md, and the book's own "What This Repository Actually Has" section all called these artifacts "live"/"runnable" while they were prose describing a stack, not the stack.

**Occurrences:** 1 (caught by external review, citing current Claude Code conventions — verified independently via web search before acting, since GPT's specific claims about `.claude/rules/` and `.claude/skills/` needed confirming, not assuming).

**Diagnosis:** Missing knowledge of the platform's actual loading convention at the time these files were originally written, compounded by no evaluation criterion that would have caught "this Skill file has no frontmatter" before calling it live.

**Chosen intervention:** Moved every artifact to `.claude/{rules,skills,agents,hooks}/` with the frontmatter Claude Code's documentation specifies (`name`/`description` for Skills, `name`/`description`/`tools` for the Agent, `globs` for Rules — `globs` chosen over the documented-but-currently-buggy `paths` field).

**Artifact created:** `.claude/skills/meta/SKILL.md`, `.claude/skills/ship-change/SKILL.md`, `.claude/agents/final-reviewer.md`, `.claude/rules/taskflow.md`, `.claude/hooks/README.md`; old `claude/` tree removed.

**Evaluation:** corrected + mechanically verified (each file's frontmatter parsed successfully as YAML matching the documented schema; verified as real UTF-8 bytes, not just console output). **Not behaviorally evaluated** — no real fresh-clone Claude Code session has confirmed `/meta`, `/ship-change`, and `final-reviewer` actually appear and load. That specific test is still open work, named here rather than silently assumed.

**Status:** corrected, mechanically verified — behavioral evaluation still open

**Closed date:** 2026-09-03 (mechanical tier only)

---

### F-004

**Failure:** `.hyri/project_contract.yaml` still said the original manuscript lived at repo root and that v2 and the test metadata file were "not yet produced," after both had been delivered weeks earlier and the manuscript had been moved into `book/`. `.hyri/runs/current_run.yaml`'s forbidden-paths list pointed at the pre-move `governance/public_release_preflight.md` path.

**Occurrences:** 1 (caught by external review: "your governance layer is now less truthful than your README").

**Diagnosis:** No mechanism re-syncs governance metadata when a file referenced by path is moved, or when a deliverable is later fixed to remove HyRI's stale prior claim by hand.

**Chosen intervention:** Direct correction of the stale comments and path.

**Artifact created:** `.hyri/project_contract.yaml`, `.hyri/runs/current_run.yaml`.

**Evaluation:** corrected. Verified each corrected claim against `run_registry.json`/the actual filesystem directly (not re-declared from memory). Not mechanically verified — no automated check keeps `.hyri/*.yaml` comments in sync with the filesystem going forward.

**Status:** corrected

**Closed date:** 2026-09-03

---

### F-005

**Failure:** `mcp/architecture-checker/checker.py`'s documented invocation (`checker.py examples/taskflow/src/`) silently disabled its own missing-test check, because `tests_dir` was resolved relative to the passed argument (`src/tests`, which never exists) rather than the project root. The module docstring also called itself an "MCP Tool" and advertised two checks (`domain/transport mixing`, `undeclared dependencies`) that were never implemented. Parse (`SyntaxError`) failures were silently treated as zero violations.

**Occurrences:** 1 named by external review; confirmed directly by running the unfixed checker against the old vs. new invocation and diffing the results (17 vs. 20 violations for the identical codebase).

**Diagnosis:** Missing evaluation criterion — no unit tests existed for the checker itself, so a path-resolution bug that made a whole check silently inert shipped undetected.

**Chosen intervention:** Fixed the path resolution, corrected the docstring (CLI-only, only the two implemented checks advertised), made `SyntaxError` a reported error instead of a silent pass, added a nonzero exit code on any violation or error, and wrote `test_checker.py`.

**Artifact created:** `mcp/architecture-checker/checker.py`, `mcp/architecture-checker/test_checker.py`, `mcp/architecture-checker/check_logs/taskflow_baseline.json`.

**Evaluation:** corrected + mechanically verified (6 new unit tests, all passing, including a regression test reproducing the exact silent-hide bug) + **behaviorally evaluated** — ran the repaired checker against the real `examples/taskflow` code and confirmed it now reports 20 real violations (17 `db-in-handler` + 3 `missing-test`) instead of the old invocation's blind spot.

**Status:** corrected, mechanically verified, behaviorally evaluated

**Closed date:** 2026-09-03

---

## Entry Template

```
## F-XXX

**Failure:** [What Claude did wrong]

**Occurrences:** [Count and context]

**Diagnosis:**
[Was Claude missing knowledge / context / a workflow / a specialist role / a capability / a hard constraint / an evaluation criterion?]

**Candidate interventions:**
- [ ] CLAUDE.md rule
- [ ] .claude/rules/ entry
- [ ] Skill
- [ ] Subagent
- [ ] Hook
- [ ] MCP tool
- [ ] Eval

**Chosen intervention:** [Selected option and rationale]

**Artifact created:** [File path(s)]

**Evaluation:** [Tasks run, pass/fail, before vs after metrics]

**Status:** open | in-progress | closed

**Closed date:** [Date closed, or —]
```

---

## Classification Table

| Failure type | Preferred artifact |
|-------------|-------------------|
| Recurring fact or convention | CLAUDE.md |
| Context-specific rule | .claude/rules/ |
| Repeated procedure | Skill |
| Repeated specialist role | Subagent |
| Hard behavioral boundary | Hook or Permission |
| Missing external capability | MCP tool |
| Reusable bundle | Plugin |
| Uncertain improvement | Evaluation |
| Recurring meta-maintenance | MetaAgent |

---

*The Three-Strikes Rule: never suffer the same Claude failure three times. First — correct it. Second — diagnose it. Third — externalize it.*
