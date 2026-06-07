# Local LLM Solver Orchestration Operator CLI Wrapper Decision

## Lane completed

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-OPERATOR-CLI-WRAPPER-DECISION-001`

## Purpose

This packet decides the Level 2 operator surface for the existing local LLM solver orchestration path. It is a docs/spec decision packet only. It does not implement a CLI wrapper, change runtime behavior, change tests, run a local model, run hosted providers, expose `/v1/solve`, expose dashboard surfaces, add provider fallback, update Google Sheets, or promote the evidence model.

## Selected decision path

`ADD_STABLE_CLI_WRAPPER`

A stable, local-only, default-off operator CLI wrapper is justified for Level 2 use because the current repository exposes a Python/module function and operator guide templates, but no stable operator-facing command. The future wrapper should reduce copy/paste Python usage while preserving every local-runtime and non-evidence invariant.

## Selected next lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-OPERATOR-CLI-WRAPPER-IMPLEMENTATION-001`

## Packet files

- [source-guide-summary.md](source-guide-summary.md)
- [current-entrypoint-review.md](current-entrypoint-review.md)
- [operator-needs-review.md](operator-needs-review.md)
- [decision-options-reviewed.md](decision-options-reviewed.md)
- [selected-decision.md](selected-decision.md)
- [allowed-cli-boundary.md](allowed-cli-boundary.md)
- [implementation-authorization.md](implementation-authorization.md)
- [safety-invariant-preservation.md](safety-invariant-preservation.md)
- [selected-next-lane.md](selected-next-lane.md)
- [evidence-boundary.md](evidence-boundary.md)
- [checks-run.md](checks-run.md)
