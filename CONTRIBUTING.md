# Contributing

- Use feature branches and squash merge PRs.
- Keep `make test` green.
- Run `ruff check alpha`.
- Add or adjust tests for new code.
- Follow the PR template (summary, tests, docs).

## Observability Workflow

- Use regression tests in `tests/observability` for SAFE-OUT, replay and telemetry.
- Run `pytest tests/observability -q` before committing to validate new regression cases.
- `alpha.core.benchmark.benchmark` can be used locally to generate JSON/Markdown performance reports under `artifacts/benchmarks`.
- The CLI supports `--record`/`--replay` for deterministic session capture and validation.
