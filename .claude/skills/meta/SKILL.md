---
name: meta
description: Run a meta-audit of the MetaVibing environment — inventory the stack (CLAUDE.md, Rules, Skills, Agents, Hooks, MCP), review the Friction Ledger, and propose improvements for human approval. Use when asked to audit, review, or check the health of the MetaVibing meta-stack itself, or when invoked directly as /meta.
---

# /meta — MetaVibing Meta-Audit

*Invoke with: `/meta` or `/meta <specific concern>`*

This skill runs a meta-audit of the current MetaVibing environment. It surfaces gaps, inconsistencies, and improvement opportunities in the meta-stack.

---

## Procedure

### 1. Inventory the meta-stack

Check what exists:

```
CLAUDE.md              — present / absent / stale?
.claude/rules/          — what rules exist? any obvious gaps?
.claude/skills/         — what skills exist? any duplicated procedures in CLAUDE.md?
.claude/agents/         — what agents exist? any specialist roles missing?
.claude/hooks/          — what hooks exist? any hard boundaries unprotected?
mcp/                    — what tools exist? any manual operations that could be automated?
FRICTION_LEDGER.md      — how many open entries? any patterns?
evals/                  — any evaluated experiments? any pending?
```

### 2. Read the friction ledger

For each open entry in FRICTION_LEDGER.md:

- Is the diagnosis complete?
- Has an artifact been created?
- Has an evaluation been run?
- Is it ready to close?

### 3. Identify gaps

Based on the inventory, identify:

- Procedures described in CLAUDE.md that should be Skills.
- Behavioral rules that are advisory but should be hooks.
- Manual operations repeated more than twice that should be MCP tools.
- Classes of failure in the ledger with no corresponding artifact.

### 4. Propose improvements

For each gap, propose:

```
Gap: [description]
Proposed artifact: [type and path]
Priority: high / medium / low
Rationale: [one sentence]
```

Sort by priority. Do not implement — propose for human approval.

### 5. Summarize

Report:
- Stack health (green / amber / red per layer)
- Open friction entries: N
- Proposed improvements: N
- Recommended next action

---

## Example output

```
## Meta-Audit — 2026-09-03

### Stack Health
- CLAUDE.md: [OK] present, reasonable scope
- Rules: [OK] 1 rule (taskflow.md), natively loaded from .claude/rules/
- Skills: [OK] 2 skills — /ship-change and /meta, natively loaded from .claude/skills/
- Agents: [OK] 1 agent — final-reviewer, read-only tools enforced via frontmatter
- Hooks: [PLANNED] 0 hooks defined — none implemented yet
- MCP: [PARTIAL] architecture-checker present as a standalone CLI; MCP wrapper is a v1.1 item
- Friction Ledger: [OPEN] N open entries — see FRICTION_LEDGER.md
- Evals: [DESIGNED] baseline charter frozen; 18-trial run not yet executed

### Proposed Improvements (priority order)
1. Run the frozen 18-trial baseline (high) — the central untested claim
2. Build the real MCP wrapper (low) — only once a Friction Ledger entry demands it

### Recommended Next Action
Whatever the Friction Ledger's oldest open entry names, or the 18-trial run if the ledger is clear.
```
