# MetaVibing

**Engineering Agents That Improve Their Own Working Environment**

> *A practical field manual and companion repository for using Claude Code not merely to write software, but to improve the system through which Claude itself works.*

---

## What Is MetaVibing?

Vibe coding means collaborating with an AI to create the artifact.  
**MetaVibing** means collaborating with the AI to improve the intelligence system that creates the artifact.

When Claude does something badly, ask:

> *What artifact would make this correction unnecessary next time?*

That one question contains most of the method.

```
Recurring fact or convention    →  CLAUDE.md
Context-specific convention     →  .claude/rules/
Repeated procedure              →  Skill
Repeated specialist role        →  Subagent
Hard behavioral boundary        →  Permission / Hook
Missing external capability     →  MCP
Reusable bundle of capabilities →  Plugin
Uncertain improvement           →  Evaluation
Repeated meta-maintenance       →  MetaAgent
```

---

## Repository Structure

```
claude-metavibing/
├── README.md
├── LICENSE
├── CLAUDE.md
├── FRICTION_LEDGER.md
│
├── book/                        # The manual (Markdown edition)
│   └── metavibing-manual.md
│
├── examples/
│   └── taskflow/                # Universal sandbox project (FastAPI/SQLite)
│       ├── src/
│       ├── tests/
│       ├── README.md
│       └── requirements.txt
│
├── claude/                      # Meta-code artifacts
│   ├── rules/
│   ├── skills/
│   ├── agents/
│   └── hooks/
│
├── mcp/
│   └── architecture-checker/    # MCP tool: architecture violation scanner
│
├── evals/                       # Evaluation framework
│   ├── baseline/
│   ├── tasks/
│   ├── graders/
│   └── results/
│
├── experiments/                 # Chapter-by-chapter experiments
│   ├── 01-memory/
│   ├── 02-skills/
│   ├── 03-reviewer/
│   ├── 04-hooks/
│   ├── 05-mcp/
│   ├── 06-metaagent/
│   └── 07-multiagent/
│
├── patterns/                    # Reusable MetaVibing patterns
│
└── templates/
    ├── CLAUDE.md
    ├── friction-ledger.md
    ├── meta-skill/
    └── reviewer-agent/
```

---

## Quick Start

### 1. Read the Manual

The manual lives in [`book/metavibing-manual.md`](book/metavibing-manual.md).

### 2. Run the Sandbox Project

```bash
cd examples/taskflow
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Run tests:

```bash
cd examples/taskflow
pytest
```

### 3. Explore the Meta-Stack

- **CLAUDE.md** — persistent project doctrine for Claude
- **claude/rules/** — path-scoped contextual rules
- **claude/skills/** — reusable procedural Skills
- **claude/agents/** — specialist subagent definitions
- **claude/hooks/** — deterministic behavioral guardrails

### 4. Track Friction

Every recurring Claude failure gets logged in [`FRICTION_LEDGER.md`](FRICTION_LEDGER.md).

---

## The Book

*MetaVibing: Engineering Agents That Improve Their Own Working Environment*

**14 parts, 50+ sections:**

| Part | Topic |
|------|-------|
| I | What MetaVibing Actually Is |
| II | The Claude Meta-Stack (7 layers) |
| III | Bootstrapping a MetaVibing Repository |
| IV | The Daily MetaVibing Loop |
| V | Advanced MetaVibing Patterns |
| VI | Agent Teams and the MetaAgents Era |
| VII | The MetaAgent |
| VIII | Recommended Repository Architecture |
| IX | Diagnostic Commands |
| X | Failure Modes of MetaVibing |
| XI | The MetaVibing Maturity Model |
| XII | The Complete MetaVibing Session |
| XIII | The MetaVibing Starter Kit |
| XIV | The Central Discipline |

---

## The Three-Strikes Rule

> **Never suffer the same Claude failure three times.**

- First occurrence — correct it
- Second occurrence — diagnose it  
- Third occurrence — externalize it (create a persistent artifact)

---

## License

MIT — see [LICENSE](LICENSE)

---

*Edition 1.0 — August 2026*
