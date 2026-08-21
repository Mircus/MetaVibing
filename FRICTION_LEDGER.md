# Friction Ledger

> *A public log of recurring Claude failures and the artifacts that resolved them.*
>
> This document is central to MetaVibing. Every entry here represents a human correction that should eventually become unnecessary through persistent meta-code.
>
> **Format:** F-NNN | Failure description | Occurrences | Intervention | Evaluation result

---

## Active Entries

*(No entries yet — this is the baseline state.)*

---

## Closed Entries

*(None — no interventions have been evaluated yet.)*

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
