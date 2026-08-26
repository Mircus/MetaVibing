# Governance Adoption Certificate
## Artifact: `examples/taskflow/README.md`

---

### Adoption Metadata

| Field | Value |
|-------|-------|
| `artifact_path` | `examples/taskflow/README.md` |
| `artifact_sha256` | `a9fb8e067517b2a3accc8611ca68fc411867f7d13df4a57a8a7e5c1df3dad327` |
| `adoption_date` | 2026-08-26 |
| `adoption_stage` | `ADOPT_EXISTING_ARTIFACT` |
| `governed_hyr_version` | `v0` |
| `generated_by` | `governed_executor` |
| `adoption_status` | `adopted` |
| `prior_readiness_verdict` | `NO-GO` (see Caveats) |

---

### What This Document Is

This is a **governance adoption certificate** for a pre-existing artifact. It records that `examples/taskflow/README.md` has been inventoried under Governed HyRI v0 and that its contents — including its Running and Testing sections — have been verified as present and hash-captured at the time of adoption.

**This document does NOT:**
- Claim that `examples/taskflow/README.md` was natively produced under Governed HyRI governance. It predates Governed HyRI entirely.
- Claim that the companion repository (`examples/taskflow/`) has passed a full readiness validation. A prior audit of that repository returned **NO-GO** — that verdict has not been superseded.
- Imply blanket verification, runability, or production-readiness of the TaskFlow repository as a whole.

The adoption is narrowly scoped: one governed_execution proof (pytest suite passing, `generated_by=governed_executor`, `exit_code=0`) exists. That single passing run does not override the prior NO-GO verdict.

---

### Artifact Declaration

**Target artifact:** `examples/taskflow/README.md`

This artifact is declared a final deliverable within the MetaVibing companion repository. It serves as the entry-point documentation for the TaskFlow sandbox application — a deliberately imperfect FastAPI application used as a reproducible laboratory throughout the *MetaVibing* manual.

The artifact is **not** being rewritten, edited, or improved by this adoption process. Its content is captured as-is.

---

### Artifact Contents Summary

The adopted README covers:

1. **Purpose** — TaskFlow as a MetaVibing sandbox (not a production template)
2. **Intentional Quirks** — documented defects that experiments will address
3. **Running** — how to install and start the application
4. **Testing** — how to run the baseline test suite
5. **Structure** — directory layout
6. **Baseline Tasks** — the eval tasks defined for vanilla Claude Code measurement

---

### Running

As declared in the adopted artifact (`examples/taskflow/README.md`, section "Running"):

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

**Governance note:** The above commands are reproduced from the artifact verbatim for adoption traceability. The ability to execute these commands has not been re-verified under this adoption step. Running instructions were present in the artifact at hash-capture time.

---

### Testing

As declared in the adopted artifact (`examples/taskflow/README.md`, section "Testing"):

```bash
pytest
```

The artifact states: *"All 8 baseline tests pass — real output from an isolated environment (fresh venv, no project-wide config) is recorded in `test_logs/taskflow_tests.txt`, not just claimed here."*

**Governance note:** One governed_execution proof exists: the declared pytest suite was observed passing with `generated_by=governed_executor` and `exit_code=0`. This single passing run is the extent of the governed testing evidence for this repository. It does **not** supersede the prior NO-GO verdict from the full readiness audit.

---

### Hash Verification

At time of adoption, the sha256 digest of the artifact was computed as:

```
a9fb8e067517b2a3accc8611ca68fc411867f7d13df4a57a8a7e5c1df3dad327  examples/taskflow/README.md
```

To re-verify integrity:

```bash
sha256sum examples/taskflow/README.md
```

Any deviation from the hash above indicates the artifact was modified after adoption. If modified, this certificate is invalidated and must be reissued.

---

### Caveats and Explicit Disclaimers

1. **Pre-governance origin.** This artifact predates Governed HyRI v0. It was not produced by a governed executor and was not subject to governance validation at time of creation.

2. **Prior NO-GO verdict.** A readiness review of the TaskFlow companion repository (`examples/taskflow/`) returned **NO-GO**. That verdict covered the repository as a whole and has not been formally superseded. Only one narrow offset exists: a single governed pytest run returning `exit_code=0`.

3. **Narrow adoption scope.** This certificate covers the README only. It does not extend governance adoption to the source code (`src/`), tests (`tests/`), evaluation assets (`evals/`), or any other component of the TaskFlow repository.

4. **No implied readiness.** Adoption under Governed HyRI v0 for inventory and traceability purposes does not constitute a readiness claim. Downstream consumers of this artifact must not interpret this certificate as a "verified and runnable" endorsement.

5. **MetaVibing as proof specimen.** Per resolved decision gate `dec-e84f9216`, MetaVibing itself is a proof specimen for Governed HyRI v0, not the primary intellectual deliverable. This adoption exists to demonstrate that Governed HyRI can inventory and certify real artifacts — not to position MetaVibing or TaskFlow as finished products.

---

### Validators Satisfied

| Validator | Status | Evidence |
|-----------|--------|----------|
| `validate_existing_artifact_exists` | PASS | File read at adoption time; sha256 computed |
| `validate_artifact_is_declared_final_deliverable` | PASS | README declared as entry-point documentation |
| `validate_artifact_hash_captured` | PASS | `a9fb8e067517b2a3accc8611ca68fc411867f7d13df4a57a8a7e5c1df3dad327` |
| `validate_target_file_not_modified` | PASS | Forbidden path — file not touched |
| `validate_required_readme_sections_present` | PASS | Running and Testing sections present in artifact |
| `validate_no_forbidden_paths_touched` | PASS | Only allowed write path used |

---

*Certificate issued under Governed HyRI v0. Stage: ADOPT_EXISTING_ARTIFACT. Role: adoption.*
