# Contributing

## Status

MetaVibing is a **proof specimen** for Governed HyRI v0, not a finished product. A prior structured readiness audit of this repository returned **NO-GO**; that verdict has not been superseded. Contributions are welcome, but please read the scope constraints below before opening a pull request.

## What Is Welcome

- Typo fixes and copy edits in the booklet (`book/`) or documentation
- Improvements to the TaskFlow sandbox tests (`examples/taskflow/tests/`) that strengthen the test suite
- Clarifications to governance documents that improve accuracy without weakening any NO-GO or limitation disclosure
- Bug reports filed as GitHub issues

## Pull Request Process

1. Fork the repository and create a branch from `main`.
2. Make the smallest change that addresses the issue. Do not refactor unrelated files.
3. If your change affects `examples/taskflow/`, run `pytest` from `examples/taskflow/` and include the test output in your pull request description.
4. Open a **pull request** against `main` with a clear description of what changed and why.
5. A maintainer will review. Response is best-effort; there is no guaranteed turnaround time.

## Provenance Disclosure

This repository uses Governed HyRI v0 provenance tracking. Artifacts carry explicit provenance labels (e.g., `DELIVERED_IMPORTED_FROM_LEDGER`, `DELIVERED_ADOPTED_EXISTING`). If you add or modify a significant artifact, state its origin plainly — do not present reconstructed or imported content as natively produced.

Any contribution that removes or weakens a **NO-GO**, limitation disclosure, or provenance statement will be rejected. The NO-GO verdict from the prior readiness audit must remain visible and unaltered unless it is formally superseded by a new audit with explicit human sign-off.

## Tests

The TaskFlow companion (`examples/taskflow/`) has a pytest suite. All existing tests must continue to pass. New features should include new tests. Run with:

```bash
cd examples/taskflow
pytest
```

## What Is Not Welcome

- Claims of full empirical validation or production readiness (neither has been established)
- Removal or weakening of any NO-GO or limitation disclosure found in this repository
- External dependencies added without updating `requirements.txt`
- Force-pushes or history rewrites on `main`
