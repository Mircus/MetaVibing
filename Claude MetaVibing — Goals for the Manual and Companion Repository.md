# Claude MetaVibing — Goals for the Manual and Companion Repository

## Ultimate Goal

Produce an expert-level, genuinely hands-on book:

# **MetaVibing**
### *Engineering Agents That Improve Their Own Working Environment*

with a companion open repository containing **runnable examples, experiments, templates, benchmarks, and progressively more sophisticated agent architectures**.

This must **not** be a book of clever prompts.

It should teach AI engineers how to build, evaluate, and govern agent systems that improve the machinery through which they themselves work.

---

## Goal 1 — Build a Universal Sandbox Project

Create one deliberately small application that anyone can understand in minutes.

For example:

```text
TaskFlow
```

A tiny Python/FastAPI application with:

- tasks;
- users;
- API endpoints;
- SQLite;
- tests;
- a few intentionally imperfect architectural choices.

The application itself is not important.

It is the **laboratory rat**.

We use the same project throughout the book so readers can see Claude's operating environment progressively evolve.

### Initial state

```text
examples/taskflow/
├── src/
├── tests/
├── README.md
└── requirements.txt
```

No elaborate Claude configuration.

This becomes our **baseline Claude**.

---

## Goal 2 — Create a Baseline Benchmark

Before improving Claude, measure what ordinary Claude Code does.

Give it perhaps 10–20 reproducible tasks:

```text
Add pagination.

Fix the failing authentication test.

Add a priority field.

Find the concurrency bug.

Refactor the notification service.

Add an endpoint without breaking compatibility.

Investigate a failing integration test.
```

Record:

```text
correctness
tests run
unnecessary files changed
architectural violations
number of human corrections
tokens
time
```

This gives the entire book an empirical backbone.

---

## Goal 3 — Introduce Persistent Intelligence

Add progressively:

```text
CLAUDE.md
↓
.claude/rules/
↓
auto-memory
```

Demonstrate concrete failures before and after.

Example:

### Before

Claude repeatedly puts database access inside API handlers.

### MetaVibing intervention

Create an architectural rule.

### After

Run the same class of task again.

Measure whether behavior changes.

The reader should see:

```text
PROBLEM
→ META-CODE
→ EXPERIMENT
→ RESULT
```

---

## Goal 4 — Turn Repeated Work into Skills

Create a small library of universally useful Skills.

Start with:

```text
/ship-change
/investigate-bug
/review-diff
/add-feature
/refactor-safely
/meta
```

Each chapter should build one Skill from a real recurring problem.

Example:

```text
Repeated behavior:
Claude says "done" too early.

        ↓

Create:
/ship-change

        ↓

Procedure:
understand
→ implement
→ test
→ inspect diff
→ review
→ report

        ↓

Evaluate against baseline.
```

This teaches **procedural agent engineering**.

---

## Goal 5 — Introduce Specialist Agents

Build a small set of reusable agents:

```text
explorer
debugger
final-reviewer
architecture-critic
security-reviewer
meta-engineer
```

Then demonstrate why role separation matters.

Example experiment:

```text
Claude implements + reviews itself

versus

Builder
   ↓
independent Reviewer
```

Measure which catches more defects.

This moves the book from prompting into **cognitive architecture**.

---

## Goal 6 — Demonstrate Failure → Artifact

This should be one of the central ideas of the entire book.

Maintain a public:

```text
FRICTION_LEDGER.md
```

For example:

```text
F-001

Claude modifies unrelated files during small fixes.

Occurrences: 3

Diagnosis:
scope discipline is insufficient.

Candidate mechanisms:
CLAUDE.md
Skill
Reviewer

Chosen intervention:
rule + reviewer

Evaluation:
10 contained bug-fix tasks.
```

Then show how each recurring failure crystallizes into infrastructure:

```text
Mistake       → Rule
Repetition    → Skill
Expert role   → Agent
Invariant     → Hook
Blind spot    → Tool
Reusable set  → Plugin
Uncertainty   → Eval
```

This is **MetaVibing in its purest form**.

---

## Goal 7 — Add Deterministic Guardrails

Build simple examples where prompts are deliberately insufficient.

Example:

```text
protected/
.env.production
migrations/history/
```

First tell Claude:

> Never modify these files.

Show that this is merely an instruction.

Then build a hook.

Now Claude **cannot** perform the forbidden action through the guarded path.

Teach the hierarchy:

```text
Preference
→ prompt

Persistent convention
→ rule

Procedure
→ Skill

Hard invariant
→ hook / permission
```

This is a crucial distinction for expert practitioners.

---

## Goal 8 — Give Claude New Capabilities

Create one deliberately simple external tool.

For example:

```text
architecture_check
```

The tool analyzes the demo repository and returns:

```json
{
  "violations": 2,
  "files": [...]
}
```

First show the primitive workflow:

```text
human runs checker
→ copies output
→ pastes into Claude
```

Then expose it through MCP:

```text
Claude
→ architecture_check()
→ structured result
```

Now the reader experiences the difference between:

**telling an agent more**

and

**giving an agent another capability**.

---

## Goal 9 — Build the MetaAgent

Create:

```text
meta-engineer
```

It should inspect:

```text
CLAUDE.md
rules
skills
agents
hooks
MCP
memory
evals
friction ledger
```

Its job:

```text
OBSERVE
   ↓
IDENTIFY RECURRING FRICTION
   ↓
CLASSIFY
   ↓
PROPOSE META-PATCH
   ↓
EVALUATE
   ↓
HUMAN APPROVAL
   ↓
APPLY
   ↓
RE-EVALUATE
```

Now we have reached the real subject of the book:

> **An agent helping engineer the environment governing future instances of itself.**

---

## Goal 10 — Demonstrate Bounded Self-Improvement

Run an actual experiment.

Give the MetaAgent a history such as:

```text
Claude repeatedly fails to run integration tests.
Claude unnecessarily reads huge directories.
Claude duplicates review instructions.
Claude forgets one project-specific architectural constraint.
```

Ask it to improve the environment.

It may propose:

```text
modify CLAUDE.md
create one Skill
delete duplicated instructions
create one hook
adjust an agent
```

But crucially:

```text
MetaAgent proposes
        ↓
Eval runs
        ↓
Human approves
        ↓
Patch applied
```

Not:

```text
Claude rewrites itself endlessly.
```

The book should develop the concept of:

# **Bounded Recursive Agent Improvement**

---

## Goal 11 — Build Real Meta-Code Evals

Create a dedicated evaluation framework:

```text
evals/
├── tasks/
├── graders/
├── baselines/
├── results/
└── reports/
```

Compare:

```text
A — vanilla Claude

B — Claude + CLAUDE.md

C — Claude + Skills

D — Claude + specialist agents

E — Claude + hooks/tools

F — full MetaVibing environment
```

Measure:

- correctness;
- regression rate;
- scope discipline;
- test coverage;
- architectural compliance;
- human interventions;
- tool-call efficiency;
- tokens;
- latency.

The book then makes **testable engineering claims**, not anecdotes.

---

## Goal 12 — Introduce Multi-Agent MetaVibing

Only after the basic architecture is understood.

Experiment with:

```text
Builder
Reviewer
Debugger
Researcher
Architect
MetaAgent
```

and patterns such as:

```text
Builder
  ↓
Critic
  ↓
Remediator
  ↓
Re-Critic
```

and:

```text
Hypothesis A ─┐
Hypothesis B ─┼→ Judge → Experiment
Hypothesis C ─┘
```

The important question is not:

> How many agents can we spawn?

It is:

> **Which topology produces better cognition for this problem?**

---

## Goal 13 — Create a MetaVibing Pattern Library

Extract reusable patterns independently of Claude or any single demo.

For example:

### Failure → Artifact

Repeated corrections become infrastructure.

### Builder / Critic Separation

Production and judgment use different contexts.

### Progressive Hardening

```text
Prompt
→ Rule
→ Skill
→ Reviewer
→ Hook
```

### Capability Escalation

```text
Manual operation
→ Script
→ Tool
→ MCP
→ Plugin
```

### Context Locality

Load knowledge only where needed.

### Bounded Self-Modification

```text
Propose
→ Evaluate
→ Gate
→ Apply
→ Revert
```

### Friction-Driven Evolution

Agent architecture changes because of observed evidence, not fashion.

These patterns are what make the book valuable beyond Claude Code itself.

---

# Companion Repository

Target structure:

```text
claude-metavibing/
│
├── README.md
│
├── book/
│
├── examples/
│   └── taskflow/
│
├── claude/
│   ├── rules/
│   ├── skills/
│   ├── agents/
│   └── hooks/
│
├── mcp/
│   └── architecture-checker/
│
├── evals/
│   ├── baseline/
│   ├── tasks/
│   ├── graders/
│   └── results/
│
├── experiments/
│   ├── 01-memory/
│   ├── 02-skills/
│   ├── 03-reviewer/
│   ├── 04-hooks/
│   ├── 05-mcp/
│   ├── 06-metaagent/
│   └── 07-multiagent/
│
├── patterns/
│
└── templates/
    ├── CLAUDE.md
    ├── friction-ledger.md
    ├── meta-skill/
    └── reviewer-agent/
```

---

# The Immediate Milestone

Do **not** try to write the entire expert book yet.

Build the experimental spine first:

```text
1. Universal demo repository

2. 10–20 baseline tasks

3. CLAUDE.md + rules

4. /ship-change

5. independent reviewer

6. friction ledger

7. /meta

8. first comparative evaluation
```

Once those work reproducibly, we have something much more valuable than another AI manual.

We have the beginning of an **experimental science of MetaVibing**.

Then the book can grow around actual results.

## Final Standard

Every major chapter should contain:

```text
CONCEPT
   ↓
FAILURE CASE
   ↓
IMPLEMENTATION
   ↓
RUN IT YOURSELF
   ↓
EVALUATION
   ↓
RESULT
   ↓
GENERAL PATTERN
```

That should be the defining character of the project.

**No hidden proprietary project.  
No toy prompt collection.  
No “10 tricks for Claude.”**

A reproducible laboratory and a serious technical manual for people who already understand AI agents and want to engineer the next layer.