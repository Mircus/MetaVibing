# Contributing

## Status

MetaVibing is a v0.1.0-alpha.1 research preview, not a finished product. No empirical performance-uplift claim is made yet — see `book/manuscript.md`'s Status & Evidence section. Contributions are welcome, but please read the scope constraints below before opening a pull request.

## What Is Welcome

- Typo fixes and copy edits in the manual (`book/manuscript.md`) or documentation
- Improvements to the TaskFlow sandbox tests (`examples/taskflow/tests/`) that strengthen the test suite
- Clarifications that improve accuracy without weakening any limitation disclosure
- Bug reports filed as GitHub issues

## Pull Request Process

1. Fork the repository and create a branch from `main`.
2. Make the smallest change that addresses the issue. Do not refactor unrelated files.
3. If your change affects `examples/taskflow/`, run `pytest` from `examples/taskflow/` and include the test output in your pull request description.
4. Open a **pull request** against `main` with a clear description of what changed and why.
5. A maintainer will review. Response is best-effort; there is no guaranteed turnaround time.

## Honesty Discipline

If you add or modify a significant artifact, state its origin plainly — do not present reconstructed or imported content as natively produced, and do not claim something is validated when it hasn't been.

Any contribution that removes or weakens a limitation disclosure in `book/manuscript.md`'s Status & Evidence section, or in `FRICTION_LEDGER.md`, will be rejected unless the underlying limitation has genuinely been resolved.

## Tests

The TaskFlow companion (`examples/taskflow/`) has a pytest suite. All existing tests must continue to pass — CI runs this on every push. New features should include new tests. Run locally with:

```bash
cd examples/taskflow
pytest
```

## What Is Not Welcome

- Claims of empirical validation or production readiness that the evidence doesn't support
- Removal or weakening of any limitation disclosure found in this repository
- External dependencies added without updating `requirements.txt`
- Force-pushes or history rewrites on `main`
