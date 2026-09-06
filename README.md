# MetaVibing

**Stop correcting your AI. Start evolving the environment it works in.**

Your AI makes a mistake. You correct it. Next week, it makes the same mistake again.

MetaVibing turns a valuable correction into a persistent Rule, Skill, specialist Agent, or deterministic Check — so the *next* session inherits what you learned, instead of you saying it again.

**[→ Try MetaVibing in 10 Minutes](docs/10-minute-metavibe.md)** · [Read the Manual](book/MetaVibing_Provisional_Booklet_v2.md) · [Evaluation Protocol](evals/baseline/README.md)

> **Prompt engineering improves the current conversation. MetaVibing improves the next one.**

---

## What Is MetaVibing?

Vibe coding means collaborating with an AI to create the artifact. **MetaVibing** means collaborating with the AI to improve the intelligence system that creates the artifact — CLAUDE.md, Rules, Skills, specialist Agents, and deterministic Checks, checked into the repository alongside the code they govern.

When Claude does something badly, the question isn't just "how do I fix this" — it's:

> *What artifact would make this correction unnecessary next time?*

That question is most of the method.

## The Core Loop

```
AI makes a mistake
       ↓
You correct it
       ↓
Correction repeats
       ↓
Extract the pattern
       ↓
Rule / Skill / Agent / Check
       ↓
Future work inherits the correction
```

## Why Not Just Prompt Engineering?

A better prompt makes *this* conversation go well. It doesn't survive a new session, a new task, or a teammate who never saw it. MetaVibing takes the same correction and gives it a durable, checked-in form — so it's part of the environment the next session starts from, not something anyone has to remember to repeat.

**[→ Try it yourself in 10 minutes](docs/10-minute-metavibe.md)** — clone the repo, watch a real correction happen, and turn it into a Rule live.

---

## The Meta-Stack

Different kinds of friction call for different kinds of artifact:

```
Recurring fact or convention    →  CLAUDE.md
Context-specific convention     →  .claude/rules/
Repeated procedure              →  Skill
Repeated specialist role        →  Subagent
Hard behavioral boundary        →  Permission / Hook
Missing external capability     →  MCP
Uncertain improvement           →  Evaluation
```

## What Exists Today

- ✓ **Rules** — live, natively loaded from `.claude/rules/`
- ✓ **Skills** — live (`/meta`, `/ship-change`)
- ✓ **A specialist Agent** — live (`final-reviewer`), structurally read-only (`tools: Read, Grep, Glob` — enforced, not just stated)
- ✓ **A deterministic checker** — live, standalone CLI, with its own unit tests and a real committed violation baseline
- ✓ **TaskFlow** — a real, runnable FastAPI/SQLite specimen with a passing 8-test baseline suite
- ✓ **A preregistered evaluation pilot** — frozen tasks, held-out acceptance tests, a grading rubric, and a machine-readable protocol, published *before* any result exists
- ✓ **A Friction Ledger** — [`FRICTION_LEDGER.md`](FRICTION_LEDGER.md), 5 real entries from this repository's own history, including a real activation bug a behavioral test caught and this project fixed on itself

## What Does Not Exist Yet

- ○ **Hooks** — none implemented
- ○ **A real MCP server** — the checker is CLI-only today; an MCP wrapper is a v1.1 item
- ○ **Completed A/B evidence** — the 18-trial pilot is frozen and ready to run, not run
- ○ **Ablations / held-out tasks / multi-practitioner replication** — deliberately deferred until after the first pilot
- ○ **`experiments/`, `patterns/`, `templates/`** — described in the manual as the eventual destination, not created here yet

Nothing above should be read as an empirical result. See [Evidence Status](#evidence-status).

---

## Repository Map

```
MetaVibing/
├── README.md
├── LICENSE
├── CLAUDE.md
├── FRICTION_LEDGER.md            # live — 5 real entries from this repo's own history
│
├── docs/
│   └── 10-minute-metavibe.md     # start here
│
├── book/                         # live
│   └── MetaVibing_Provisional_Booklet_v2.md   # current draft (Markdown only)
│
├── examples/
│   └── taskflow/                 # live — FastAPI/SQLite specimen, 8 passing tests
│
├── .claude/                      # Claude Code's native config — this is what actually loads
│   ├── rules/                    # live
│   ├── skills/                   # live — /meta, /ship-change
│   ├── agents/                   # partial — final-reviewer
│   └── hooks/                    # planned — none implemented yet
│
├── mcp/
│   └── architecture-checker/     # live as a standalone CLI; MCP wrapper planned for v1.1
│
├── evals/                        # live — frozen pilot: tasks, acceptance tests, rubric, protocol.yaml
│
└── governance/                   # provenance records — see governance/ if you care how this repo's artifacts were produced
```

## Evidence Status

MetaVibing's central claim — that this discipline reduces architectural drift, correction turns, and first-try failure rate compared to working without it — is **falsifiable and not yet tested.**

What exists: a frozen, preregistered pilot — [`evals/baseline/README.md`](evals/baseline/README.md) (the charter: core claim, tasks, metrics, protocol) and [`evals/protocol.yaml`](evals/protocol.yaml) (the machine-readable contract: hashes, RNG-generated trial order, formulas). Three tasks, held-out acceptance tests the model never sees, a rubric with atomic rule IDs, 18 trials (3 tasks × 3 trials × 2 conditions).

What doesn't exist: the trial runner, and the trials themselves. This will be reported as a **pilot** — one practitioner, non-held-out tasks — not a confirmatory study, with results published whether or not they're flattering.

## Manual

*MetaVibing: Engineering Agents That Improve Their Own Working Environment* — [`book/MetaVibing_Provisional_Booklet_v2.md`](book/MetaVibing_Provisional_Booklet_v2.md), 16 parts:

| Part | Topic |
|------|-------|
| I | What MetaVibing Actually Is |
| II | The Claude Meta-Stack |
| III | Bootstrapping a MetaVibing Repository |
| IV | The Daily MetaVibing Loop |
| V | Advanced MetaVibing Patterns |
| VI–VII | Agent Teams and the MetaAgent |
| VIII | A Recommended Repository Architecture |
| IX | Diagnostic Commands |
| X | Failure Modes of MetaVibing |
| XI | The MetaVibing Maturity Model |
| XII–XIII | A Complete Session, and the Starter Kit |
| XIV | The Central Discipline |
| XV–XVI | Worked Examples, and MetaVibing as a Proof Specimen |

The prior packaged edition (v1, `.md`/`.docx`/`.pdf`) and the original unexpanded manuscript are kept in `book/` for reference — superseded in content by v2.

**The Three-Strikes Rule**, from Part XIV: never suffer the same Claude failure three times. First occurrence — correct it. Second — diagnose it. Third — externalize it into a Rule, Skill, Agent, or Check.

## Roadmap

Run the frozen pilot → publish the results, including if they're not flattering → then hooks, a real MCP server, and ablations, each built because the evidence calls for it, not to fill out the diagram.

---

## License

MIT — see [LICENSE](LICENSE)

---

*MetaVibing — Provisional Research Preview — September 2026*
