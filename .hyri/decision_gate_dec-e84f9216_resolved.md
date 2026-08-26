# Resolved Decision Gate dec-e84f9216

## Status: resolved
Resolved at: 2026-08-24T10:09:26.563130+00:00

## Original Question

Approve the Evaluation Charter: 1) What is the core claim for the MetaVibing repo (one sentence)? 2) Who is the primary user and what job-to-be-done must the first release satisfy? 3) Which two or three baseline tasks from examples/taskflow must the system pass to be shippable? 4) What are the outcome metrics and numeric pass thresholds for each task? 5) What measurement protocol (datasets/prompts/seeds/compute) is acceptable and reproducible? 6) What are the shipping gates (must-pass checks) for PRs and for the initial release?

## Resolution (Mirco's answer)

Provisional resolution to dec-e84f9216, decided by Mirco.

D1 Core claim:
MetaVibing is a governed workflow discipline for using AI agents as bounded workers under explicit context, artifact, validator, and human-gate controls.

D2 Primary user:
Technical creators, researchers, and small lab builders using AI tools for multi-step intellectual/software artifacts.

D3 Baseline tasks:
- expand a source manuscript into a provisional artifact;
- integrate at least one working example;
- verify the companion mini-repo;
- produce declared final files;
- reject raw extraction/scaffold/status as success.

D4 Metrics:
- required artifacts exist;
- final text is at least 20% expanded over source;
- required sections present;
- examples referenced in the artifact;
- companion repo tests pass;
- forbidden paths untouched;
- human gate unresolved prevents DELIVERED.

D5 Measurement protocol:
Every stage has a run contract, context packet, declared output, validator list, artifact registry update, go
