# Skill: /ship-change

*Invoke with: `/ship-change <task description>`*

This skill implements a disciplined change procedure. It prevents "Claude says done too early" — the most common MetaVibing failure mode.

---

## Procedure

### 1. Understand

Before writing a single line of code:

- Restate the task in your own words.
- Identify which files are in scope.
- Identify which files are **explicitly out of scope**.
- State any architectural constraints that apply (from CLAUDE.md or relevant rules).
- Ask one clarifying question if the task is ambiguous — only one.

### 2. Implement

- Make the smallest change that satisfies the task.
- Do not refactor unrelated code.
- Do not touch files outside the stated scope.

### 3. Test

- Run the relevant test suite.
- If no tests exist for the changed behavior, write at least one.
- If tests fail, fix them before proceeding.
- Distinguish pre-existing failures from newly introduced ones.

### 4. Inspect diff

Run:
```
git diff
```

Verify:
- No unintended files were modified.
- No debug code, commented-out blocks, or TODO stubs were left in.
- No secrets or local config were included.

### 5. Review

Read through the diff as if you are a critical reviewer who did not write the code. Ask:

- Does this actually solve the task?
- Does it introduce any new bugs or regressions?
- Is it consistent with the project's architectural conventions?

### 6. Report

Write a concise completion report:

```
## Change: <task>
**Files changed:** <list>
**Tests run:** <pass/fail summary>
**Diff size:** +N / -N lines
**Notes:** <anything the human should know>
```

---

## What This Prevents

| Failure | How this skill prevents it |
|---------|--------------------------|
| Claiming done without running tests | Step 3 is explicit and required |
| Touching unrelated files | Step 1 scopes the work; Step 4 inspects for drift |
| Forgetting to report | Step 6 is non-optional |
| Missing architectural violations | Step 5 catches them via explicit review |
