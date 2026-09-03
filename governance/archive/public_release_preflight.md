# Public Release Preflight — MetaVibing Governed HyRI v0

**Date:** 2026-08-26
**Stage:** PUBLIC_RELEASE_PREFLIGHT
**Role:** verifier
**Active Object:** governance/public_release_preflight.md
**Overall Readiness Verdict:** CONDITIONAL — human authorization required (see section 7)

---

## Resolved Evaluation Charter

This preflight document is anchored to the resolved decision gate **dec-e84f9216**. Under that gate, MetaVibing is a **proof specimen for Governed HyRI v0**, not the primary intellectual product, and not a finished commercial offering. All deliverables exist to demonstrate that Governed HyRI can produce real artifacts under governance discipline.

---

## Prior Readiness Verdict

A prior structured readiness audit of this repository returned **NO-GO**. That verdict **has not been superseded**. It has been only narrowly offset by one passing `governed_execution` pytest run for the TaskFlow companion (generated_by=governed_executor, exit_code=0). This preflight does not claim blanket verification or full empirical validation.

The 3×3×2 baseline evaluation protocol (3 tasks × 3 trials × 2 conditions) declared in `evals/baseline/README.md` has **not been run**. No empirical uplift claim has been tested or established.

---

## 1. Remote Verification

> *Evidence source: `.hyri/preflight_evidence/remote_verification.txt` — reproduced verbatim.*

```
Intended remote URL (stored on project record, git_remote field): https://github.com/Mircus/MetaVibing.git
No git-level remote is configured yet in this repository (git remote -v returns empty) — it will be added immediately before the seed push, not before.

git ls-remote https://github.com/Mircus/MetaVibing.git (unauthenticated, public repo):
(exit code: 0)
Result: zero refs returned — the remote repository exists and is completely empty.
```

**Interpretation:** The GitHub repository exists and is empty. No prior content will be overwritten by the seed push.

---

## 2. Working Tree Status

> *Evidence source: `.hyri/preflight_evidence/working_tree_status.txt` — reproduced verbatim.*

```
git status --short:
 M .hyri/runs/current_run.yaml

current branch: main
commit to be pushed (HEAD): bff5ac5b86f22fed3c470040af39b895d239fb71
commit subject: Fix SECURITY.md: warn against pasting secrets into public GitHub issues
```

**Interpretation:** One tracked file (`.hyri/runs/current_run.yaml`) has an unstaged modification from the current preflight run. This file is governance-internal and will be committed as part of the final preflight close-out before push. HEAD commit is identified.

---

## 3. Secret Scan

> *Evidence source: `.hyri/preflight_evidence/preflight_scan_evidence.txt` — reproduced verbatim.*

```
Mechanical secret/credential scan performed directly against tracked repository content (git ls-files + content grep), 2026-08-26.

Patterns checked (filenames): .env, .env.*, *token*, *secret*, *credential*, *api[_-]key*, *.pem, *.key, id_rsa, __pycache__, .pytest_cache, node_modules, venv/, .venv/, hyri_runtime
Result: NO MATCHES.

Patterns checked (tracked file contents): GitHub personal-access-token shape (ghp_ prefix), OpenAI/Anthropic secret-key shape (sk- prefix), and assignment lines for the env vars GITHUB TOKEN, OPENAI API KEY, and ANTHROPIC API KEY.
Result: NO MATCHES.

hyri_runtime/ directory (where governed_state.json, run_registry.json, and project_rollup.json actually live) is NOT part of this git repository at all — it lives at the project level, outside repos/Metavibing/, and is not tracked here.

Local absolute path check (e.g. C:\Users\mirco\...): NO MATCHES in tracked file contents or commit messages.

Conclusion: no secrets, credentials, or local machine paths found in any tracked content.
```

**Interpretation:** Secret scan passed. No credentials, tokens, or local machine paths found in any tracked file.

---

## 4. Public-Release Contents

> *Evidence source: `.hyri/preflight_evidence/public_release_contents.txt` — reproduced verbatim.*

```
Top-level files and directories that will be published (from `git ls-files`, actual tracked content, not a directory listing that could include untracked scratch files):

.gitignore
.hyri/                              (governance contracts: project_contract.yaml, current_run.yaml, decision records, this preflight's own evidence)
.hyri_baseline.json
CLAUDE.md
CONTRIBUTING.md                     (public contribution policy — DELIVERED_REVALIDATED, run_id public_release_files_v1)
Claude MetaVibing — Goals for the Manual and Companion Repository.md
FRICTION_LEDGER.md
LICENSE
README.md
SECURITY.md                         (public security policy — DELIVERED_REVALIDATED, run_id public_release_files_v1)
The Claude MetaVibing Manual.docx
book/                               (v1 raw manual + v2 expanded booklet, md/docx/pdf)
claude/                             (agents, hooks, rules, skills — the MetaVibing meta-stack)
evals/baseline/README.md            (evaluation charter)
examples/taskflow/                  (FastAPI sandbox app: src/, tests/, README, requirements.txt, test_logs/)
governance/                         (decision brief, adoption certificate, project completion report, this preflight report)
mcp/architecture-checker/           (checker.py + one check log)

experiments/, patterns/, templates/ exist as empty local directories but contain no tracked files — git does not track empty directories, so nothing under them will actually be published.
```

**Interpretation:** Contents are as expected for a Governed HyRI v0 proof specimen. `SECURITY.md` and `CONTRIBUTING.md` are present (see section 6 for sha256 hashes and provenance disclosure). Empty directories (experiments/, patterns/, templates/) will not be published.

---

## 5. Provenance Status

> *Evidence source: `.hyri/preflight_evidence/provenance_status.txt` — reproduced verbatim.*

```
Governed HyRI v0 project_rollup.json verdict for this project (proj-703c959f), as of 2026-08-26T13:52:40Z: COMPLETE_PROVENANCE_MIXED.

This means, precisely:
- book/MetaVibing_Provisional_Booklet_v2.md: DELIVERED_IMPORTED_FROM_LEDGER
- evals/baseline/README.md: PASSED_IMPORTED_FROM_LEDGER
- examples/taskflow/README.md: DELIVERED_ADOPTED_EXISTING
- examples/taskflow/test_logs/taskflow_tests.txt: PASSED_IMPORTED_FROM_LEDGER
- examples/taskflow/test_logs/taskflow_tests.meta.json: PASSED_IMPORTED_FROM_LEDGER

Facts that MUST be stated plainly in the preflight report:
1. MetaVibing v0 is COMPLETE_PROVENANCE_MIXED — not natively-produced-only, not fully empirically validated.
2. This is a proof specimen for Governed HyRI v0, not a finished commercial product (per resolved decision gate dec-e84f9216).
3. Artifacts include a mix of provenance: ledger-imported (reconstructed after the fact from progress_ledger.jsonl, with explicit disclosure), and adopted-existing (examples/taskflow/README.md, which predates Governed HyRI entirely).
4. The TaskFlow companion repository is NOT fully readiness-certified — a prior structured readiness audit returned NO-GO, and that verdict has not been superseded; only narrowly offset by one passing governed_execution pytest run.
5. The 3x3x2 baseline evaluation protocol (3 tasks x 3 trials x 2 conditions) declared in evals/baseline/README.md has NOT been run. No empirical uplift claim has been tested.
```

**Interpretation:** Provenance is COMPLETE_PROVENANCE_MIXED. Artifacts are a mix of ledger-imported and adopted-existing provenances. This must be disclosed wherever the repository's outputs are referenced as evidence. Not all artifacts share the same provenance.

### TaskFlow Companion — Explicit Readiness Distinction

The TaskFlow companion (`examples/taskflow/`) is **NOT fully readiness-certified**:

- A prior structured readiness audit returned **NO-GO**.
- That NO-GO verdict has **not been superseded**.
- The one passing `governed_execution` pytest run (generated_by=governed_executor, exit_code=0) provides narrow offset evidence only — it does not constitute blanket verification.
- `examples/taskflow/README.md` predates Governed HyRI entirely; it is `DELIVERED_ADOPTED_EXISTING`.

Any downstream reference to TaskFlow test results must state this distinction explicitly and must not imply that TaskFlow has been fully verified or is production-ready.

---

## 6. Required Public Files

> *Evidence source: `.hyri/preflight_evidence/required_public_files_check.txt` — reproduced verbatim.*

```
README.md — EXISTS — sha256: cf6a499f4c1b25f195e81eec6b291118eac2fcad7ab4c79f35a04af9416a18d0
LICENSE — EXISTS — sha256: 5f047b0ae203f39b9c8ed5d95721aa90dcab3455ae490cfd295f291900c0ce83
SECURITY.md — EXISTS — sha256: a9b601f758da3958f6a432011c8888f38c547b949a3c8cadfe267635a222244b
CONTRIBUTING.md — EXISTS — sha256: 7ff1b5ad198a85ada428f474ad126ba3dc6a529140b54c8a2726425023bfb143
governance/project_completion_report.md — EXISTS — sha256: fdf31a7f54297db3d57e47f0da316ae81255db9311286133bcd1e8d88b1fab7c
project_rollup.json (raw) — NOT PRESENT in this repo (lives in hyri_runtime/governance/, outside this git repo, by design). The human-readable equivalent, governance/project_completion_report.md, IS present and IS tracked.

All previously-missing required public-release files (SECURITY.md, CONTRIBUTING.md) now exist and are approved: DELIVERED_REVALIDATED, run_id public_release_files_v1, approved by Mirco 2026-08-26.
```

**Interpretation:** All required public-release files are present.

| File | Status | SHA-256 |
|------|--------|---------|
| `README.md` | ✅ EXISTS | `cf6a499f4c1b25f195e81eec6b291118eac2fcad7ab4c79f35a04af9416a18d0` |
| `LICENSE` | ✅ EXISTS | `5f047b0ae203f39b9c8ed5d95721aa90dcab3455ae490cfd295f291900c0ce83` |
| `SECURITY.md` | ✅ EXISTS | `a9b601f758da3958f6a432011c8888f38c547b949a3c8cadfe267635a222244b` |
| `CONTRIBUTING.md` | ✅ EXISTS | `7ff1b5ad198a85ada428f474ad126ba3dc6a529140b54c8a2726425023bfb143` |
| `governance/project_completion_report.md` | ✅ EXISTS | `fdf31a7f54297db3d57e47f0da316ae81255db9311286133bcd1e8d88b1fab7c` |

### SECURITY.md and CONTRIBUTING.md — Provenance Disclosure

`SECURITY.md` and `CONTRIBUTING.md` were not produced in a single clean native governed run. They were initially absent, reported as missing in a prior preflight pass, then authored and committed in a recovery stage (`run_id: public_release_files_v1`), and subsequently revalidated following a validator bug fix in `revalidation.py`. The stage is accurately described as a **revalidated recovery stage**, not a clean native governed run. The sha256 hashes above reflect the files as approved by Mirco on 2026-08-26.

---

## 7. Human Authorization

**Required authorization text (verbatim, per resolved minimum requirement):**

> Mirco authorizes an initial seed push of the Governed HyRI v0 MetaVibing proof specimen to the empty GitHub repository https://github.com/Mircus/MetaVibing, after public-repo safety checks pass. This is not a claim of full empirical validation or production readiness.

**Authorization status:** AWAITING MIRCO'S EXPLICIT SIGN-OFF

This section must be counter-signed by Mirco before the seed push proceeds. The authorization above is the minimum required text; Mirco may augment it if he wishes.

**Instructions for Mirco:**
1. Review this document in full.
2. Confirm the authorization text above by signing with date and name.
3. Once signed, update `governance/public_release_preflight.md` with your signature and the seed push may proceed.

---

## Preflight Summary

| Check | Result |
|-------|--------|
| Remote verification | ✅ PASS — repo exists, empty |
| Working tree status | ⚠ ONE MODIFIED FILE — `.hyri/runs/current_run.yaml` (governance-internal, to be committed before push) |
| Secret scan | ✅ PASS — no secrets found |
| Public-release contents | ✅ PASS — contents as expected |
| Provenance status | ⚠ COMPLETE_PROVENANCE_MIXED — disclosed; not all artifacts share the same provenance |
| Required public files | ✅ PASS — all present; SECURITY.md and CONTRIBUTING.md are DELIVERED_REVALIDATED (revalidated recovery stage, not a clean native governed run) |
| Human authorization | ⏳ AWAITING MIRCO SIGN-OFF |

**Overall:** CONDITIONAL — all file and scan checks pass; push awaits Mirco's explicit authorization.

---

*Generated by: Governed HyRI PUBLIC_RELEASE_PREFLIGHT stage*
*Generation mode: governed_role / LLM writer*
*Validation mode: deterministic validators*
*Status: HUMAN_REVIEW_REQUIRED pending Mirco sign-off*
*Date: 2026-08-26*
*Evidence inputs: all six `.hyri/preflight_evidence/` files read verbatim, not re-run*
*SECURITY.md sha256: a9b601f758da3958f6a432011c8888f38c547b949a3c8cadfe267635a222244b*
*CONTRIBUTING.md sha256: 7ff1b5ad198a85ada428f474ad126ba3dc6a529140b54c8a2726425023bfb143*
