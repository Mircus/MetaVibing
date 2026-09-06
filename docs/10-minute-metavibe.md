# MetaVibing in 10 Minutes

**Stop correcting the AI. Change the environment it works in.**

You are going to give an AI coding assistant a small engineering task, watch it make a recurring class of mistake, and then turn the correction into persistent project intelligence — something the *next* task inherits automatically, not something you have to say again.

This is a hands-on walkthrough, not a reading assignment. Have a terminal open.

---

## 0. The idea — 30 seconds

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

**Prompt engineering improves the current conversation. MetaVibing improves the next one.**

That's the whole idea. Everything below is one concrete pass through that loop.

---

## 1. Clone and enter TaskFlow — 1 minute

```bash
git clone https://github.com/Mircus/MetaVibing.git
cd MetaVibing/examples/taskflow
pip install -r requirements.txt
pytest
```

You should see 8 tests pass. TaskFlow is a controlled sandbox: a small, real FastAPI + SQLite app that works, but contains architectural friction preserved on purpose — it exists specifically so MetaVibing has something concrete to demonstrate against.

Now go back to the repository root and start Claude Code there — everything from here on (the Rule, the Skills, the checker) is referenced relative to the repo root, not `examples/taskflow/`:

```bash
cd ../..
claude
```

---

## 2. Meet the problem — 1 minute

Open `src/main.py`. Here's one of its route handlers, unmodified:

```python
@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

Database access sits directly in the route handler. It works — the tests pass — but it's exactly the kind of decision a project might not want repeated as it grows: harder to test in isolation, harder to swap persistence later, logic and transport tangled together.

Now there's something to improve.

---

## 3. The ordinary AI workflow — 1 minute

This is the familiar part, and it's worth naming plainly: you ask a coding assistant to add a feature. It produces something that works — tests pass, the endpoint responds correctly — while quietly repeating the same pattern above in a new handler. You notice, and you say something like:

> "Don't put database access in the route handler. Keep that in the repository/service layer."

The assistant fixes it. The conversation ends.

**Normally, that correction dies with the conversation.** Open a new session next week, ask for the next feature, and you're saying it again.

---

## 4. The MetaVibing move — 2 minutes

Instead of only repeating the correction, look at what's already sitting in this repository:

```
.claude/
├── rules/
│   └── taskflow.md
├── skills/
│   ├── meta/
│   └── ship-change/
└── agents/
    └── final-reviewer.md
```

Open `.claude/rules/taskflow.md`. The correction from Section 3 is already there, as the first line under Architecture:

```
Database access belongs in the repository layer — not in route handlers.
```

This file isn't documentation about a convention — it's loaded natively by Claude Code. Its frontmatter (`paths: ["examples/taskflow/**/*"]`) scopes it: when Claude works with a file matching that pattern, Claude Code loads the Rule automatically. You don't have to restate the architectural correction in the prompt — the correction from a past conversation is now part of *this* conversation's environment the moment you touch TaskFlow.

That's the first "aha."

---

## 5. Escalate from rule to procedure — 1 minute

A Rule says what must stay true. A Skill encodes *how* a recurring class of work should be done — understand, implement, test, inspect the diff, review, report, every time, not left to memory.

Try it on a real, small task:

```
/ship-change Add an endpoint: POST /users/{user_id}/complete-all-tasks — marks every task belonging to that user as done, and returns the count of tasks updated.
```

Watch it work through the six steps `.claude/skills/ship-change/SKILL.md` documents. Then inspect the diff yourself: does the new handler keep database access out of the route, without you repeating the instruction from Section 3 at all? If yes, the persistent Rule influenced the work without you restating it. If not, you've just discovered new friction — which is exactly what MetaVibing is designed to capture and escalate, not something to paper over.

For a wider inventory of what's accumulated in the project's meta-stack, and what friction hasn't been turned into structure yet:

```
/meta
```

**Rule → constraint. Skill → reusable procedure.**

---

## 6. Add independent judgment — 1 minute

`/ship-change`'s final step is documented to delegate review of non-trivial changes to `final-reviewer` — a separate subagent — rather than grading its own work. Check whether it did. If it didn't (its own judgment call on "non-trivial"), invoke the reviewer directly:

```
Use the final-reviewer subagent to review the diff from Section 5.
```

Sometimes the missing capability isn't another instruction — it's a different role: someone who didn't write the code, reviewing it. `final-reviewer` is **structurally** read-only — its own frontmatter restricts it to `Read, Grep, Glob`, no `Edit`, `Write`, or `Bash` — so it cannot fix what it finds, only report it. That's enforced by Claude Code's tool permissions, not by the reviewer choosing to behave.

```
Correction
   ↓
Rule
   ↓
Skill
   ↓
Specialist Agent
   ↓
Deterministic Check   ← next
```

---

## 7. Move beyond model judgment — 1 minute

One rung further down the ladder, stop asking any model — reviewer included — whether a constraint was obeyed, and check it mechanically instead:

```bash
python mcp/architecture-checker/checker.py examples/taskflow
```

This walks the actual AST of `src/`, looking for direct database calls inside route handlers, and reports every one it finds — the same rule from Section 4, now enforced by code instead of judgment.

**Once a constraint can be checked deterministically, stop asking the model whether it obeyed it.** That's one of MetaVibing's strongest principles: AI judgment, converted into executable infrastructure.

---

## 8. The whole thing — final minute

```
FRICTION
   │
   ├── forgotten context      →  CLAUDE.md
   ├── path-specific mistake  →  Rule
   ├── repeated procedure     →  Skill
   ├── specialist judgment    →  Agent
   ├── objective invariant    →  Checker
   ├── must-never-happen      →  Hook
   └── external capability    →  Tool / MCP
```

Don't keep writing better prompts forever. When a correction proves valuable, give it a durable computational form — one your next session inherits without being told.

**You have just MetaVibed the project.**

---

## Want to know whether this actually improves anything?

Everything above is the *method*. Whether it measurably reduces architectural drift, correction turns, or first-try failures compared to working without it is a separate, open, honest question — one MetaVibing hasn't answered yet.

See the [preregistered evaluation charter](../evals/baseline/README.md) and its [machine-readable protocol](../evals/protocol.yaml): frozen tasks, held-out acceptance tests, a grading rubric, and a real 18-trial A/B design — published before the results, not after.
