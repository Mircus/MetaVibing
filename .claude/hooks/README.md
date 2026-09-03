# Hooks

**Status: PLANNED — no hooks are implemented in this repository yet.**

Claude Code hooks allow you to run deterministic checks at specific points in the agent lifecycle. Unlike rules and CLAUDE.md, hooks do not rely on the model's attention or discretion — they run unconditionally, configured in `.claude/settings.json`.

## Available Hook Points

- `PreToolUse` — runs before any tool invocation (file edit, bash command, etc.)
- `PostToolUse` — runs after a tool invocation
- `Notification` — fires when Claude sends a notification
- `Stop` — fires when the agent stops

## Hooks in This Repository

*None yet.* Per the Meta-Stack doctrine, a hook should be built because a Friction Ledger entry names a hard invariant that repeated correction has failed to hold — not to fill out this directory. See the manual (Part III, Step Three — Convert One Rule into a Hook) for the intended first implementation.

## Hook Template

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python mcp/architecture-checker/checker.py examples/taskflow"
          }
        ]
      }
    ]
  }
}
```

## Philosophy

Use hooks for **hard invariants** — behavior that should be deterministic rather than left to model discretion:

```
Preference             →  prompt
Persistent convention  →  CLAUDE.md rule
Procedure              →  Skill
Hard invariant         →  Hook or Permission
```

A hook that rejects writes to `migrations/history/` cannot be talked around. A CLAUDE.md rule that says the same thing can be.
