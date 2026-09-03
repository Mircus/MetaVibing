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

## Status

**Implemented now:** the manual draft (Markdown), the TaskFlow sandbox app with a passing pytest suite, `CLAUDE.md` doctrine, path-scoped rules, the architecture-checker (as a standalone CLI), the evaluation charter (design only), and the Friction Ledger template.

**Not implemented yet:** hooks, the MCP server wrapper for the architecture-checker, the `experiments/`/`patterns/`/`templates/` directories described in the book, and — most importantly — the 18-trial baseline evaluation itself. The charter defines what would count as evidence; no trial has been run, and the Friction Ledger has zero entries. Nothing in this repo should be read as an empirical result yet.

This section exists so the structure below and the Quick Start links describe what is actually here, not the eventual destination.

---

## Repository Structure

```
claude-metavibing/
├── README.md
├── LICENSE
├── CLAUDE.md
├── FRICTION_LEDGER.md            # live — template only, no entries yet
│
├── book/                         # live
│   ├── MetaVibing_Provisional_Booklet_v2.md      # current draft (Markdown only)
│   ├── MetaVibing_Provisional_Booklet_v1.{md,docx,pdf}  # prior packaged edition
│   ├── metavibing-manual.md      # direct conversion of the original manuscript
│   └── The Claude MetaVibing Manual.docx         # original manuscript source
│
├── examples/
│   └── taskflow/                 # live — FastAPI/SQLite sandbox
│       ├── src/
│       ├── tests/
│       ├── README.md
│       └── requirements.txt
│
├── claude/                       # meta-code artifacts
│   ├── rules/                    # live
│   ├── skills/                   # live — /meta, /ship-change
│   ├── agents/                   # partial
│   └── hooks/                    # planned — none implemented yet
│
├── mcp/
│   └── architecture-checker/     # live as a standalone CLI; MCP server wrapper planned for v1.1
│
├── evals/
│   └── baseline/                 # live — charter written; 18-trial run planned, not yet executed
│
└── governance/                   # live — Governed HyRI v0 provenance records
```

`experiments/`, `patterns/`, and `templates/` are described in the book as the eventual destination but do not exist in this repository yet — see Status above.

---

## Quick Start

### 1. Read the Manual

The current draft is [`book/MetaVibing_Provisional_Booklet_v2.md`](book/MetaVibing_Provisional_Booklet_v2.md) —
Markdown only; a packaged `.docx`/`.pdf` release for v2 has not been built yet.

The prior packaged edition is still available as
[`.md`](book/MetaVibing_Provisional_Booklet_v1.md), [`.docx`](book/MetaVibing_Provisional_Booklet_v1.docx), and
[`.pdf`](book/MetaVibing_Provisional_Booklet_v1.pdf) — superseded in content by v2, kept here for the packaged format.

The unexpanded, direct conversion of the original manuscript is kept at
[`book/metavibing-manual.md`](book/metavibing-manual.md) for reference, converted from
[`book/The Claude MetaVibing Manual.docx`](<book/The Claude MetaVibing Manual.docx>).

**The examples in the booklet are runnable, not illustrative** — `examples/taskflow/` is a real
FastAPI app you can start, test, and scan with the architecture checker yourself (below).

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

- **CLAUDE.md** — persistent project doctrine for Claude · live
- **claude/rules/** — path-scoped contextual rules · live
- **claude/skills/** — reusable procedural Skills · live
- **claude/agents/** — specialist subagent definitions · partial
- **claude/hooks/** — deterministic behavioral guardrails · planned, none implemented yet

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
