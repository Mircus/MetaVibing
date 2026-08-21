# Skill: /meta

*Invoke with: `/meta` or `/meta <specific concern>`*

This skill runs a meta-audit of the current MetaVibing environment. It surfaces gaps, inconsistencies, and improvement opportunities in the meta-stack.

---

## Procedure

### 1. Inventory the meta-stack

Check what exists:

```
CLAUDE.md              — present / absent / stale?
claude/rules/          — what rules exist? any obvious gaps?
claude/skills/         — what skills exist? any duplicated procedures in CLAUDE.md?
claude/agents/         — what agents exist? any specialist roles missing?
claude/hooks/          — what hooks exist? any hard boundaries unprotected?
mcp/                   — what tools exist? any manual operations that could be automated?
FRICTION_LEDGER.md     — how many open entries? any patterns?
evals/                 — any evaluated experiments? any pending?
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
## Meta-Audit — 2026-08-21

### Stack Health
- CLAUDE.md: ✅ present, 127 lines, reasonable scope
- Rules: ✅ 1 rule (taskflow.md)
- Skills: ⚠️  2 skills — /ship-change and /meta only; no /investigate-bug
- Agents: ❌ 0 agents defined
- Hooks: ❌ 0 hooks defined
- MCP: ⚠️  architecture-checker stub present, not implemented
- Friction Ledger: ✅ 0 open entries (baseline)
- Evals: ❌ 0 baselines recorded

### Proposed Improvements (priority order)
1. Create /investigate-bug skill (high) — repeated diagnostic procedure in ch. 4
2. Create final-reviewer agent (high) — ch. 22 experiment prereq
3. Implement architecture-checker MCP tool (medium) — ch. 25 prereq
4. Record baseline eval results (medium) — needed before any comparison

### Recommended Next Action
Record baseline eval results before implementing any improvements.
```
