# Security Policy

## Status: Alpha

MetaVibing is a v0.1.0-alpha.1 research preview. It is **not a production service**, not a commercial product, and not intended for use in critical or security-sensitive contexts. No SLA, no support commitment.

## No Bug Bounty

There is **no bug bounty program** for this repository. Do not submit security reports expecting compensation.

## Scope

This repository contains:
- A practitioner manual (`book/manuscript.md`, built to PDF/DOCX in `dist/`)
- A companion sandbox application (`examples/taskflow/`) — FastAPI + SQLite, for local development only
- An evaluation pilot design (`evals/`) — not yet run

**TaskFlow** (`examples/taskflow/`) is the companion sandbox application. It is explicitly **not production-ready** — it's a deliberately imperfect specimen built to demonstrate real architectural friction, not a reference implementation. It is intended for local experimentation only — do not expose it to the internet or use it to handle real user data.

## API Keys and Credentials

Do **not** commit API keys, tokens, or credentials to this repository. No API keys are included here; none should be added. If you discover a committed secret, open an issue or contact the maintainer directly.

## Reporting a Vulnerability

If you discover a security issue in the repository content (e.g., accidentally committed credentials, a dangerous script), open a GitHub issue marked **[SECURITY]** or contact the maintainer directly via GitHub.

**Do not paste secrets, tokens, private keys, or exploit details into a public GitHub issue.** A public issue should describe the type and location of the problem (e.g., "a credential-shaped string appears in file X, line Y") without exposing the secret itself. Send the sensitive detail privately to the maintainer via a GitHub direct/contact channel on their profile, or another private channel if one is available.

Response is best-effort; there is no guaranteed SLA.
