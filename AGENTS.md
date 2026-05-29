# Agent Instructions

## Purpose

This file gives repo-level operating instructions for AI coding agents working on Alpha Solver, including Codex, Cursor, and future assistants.

## Source of Truth

- `.specs/` contains implementation contracts.
- Existing specs should not be moved or renamed casually.
- New feature or bugfix work should start from or update a spec unless the user explicitly requests exploratory work.
- Backlog spreadsheets are external planning/status ledgers, not repo implementation contracts.
- `data/alpha_solver_master_table_v0_7_0.*` is a registry export/provenance artifact, not a backlog; see `data/README.md` before using or moving it.

## Agent Workflow

- Inspect the repository and relevant specs before implementing.
- Keep PRs narrow and limited to the approved scope.
- Link or create the relevant spec before changing behavior.
- Implement only the approved scope.
- Add or update focused tests for behavior changes.
- Report changed files and the exact tests or checks run.
- Prepare a squash merge extended description for the PR.

## Safety / Do Not Change Casually

- Do not delete or rename confusing legacy/reference files without explicit approval.
- Do not broad-refactor MCP, routing, SAFE-OUT, budget guard, determinism, observability, replay, or SolverEnvelope behavior unless a spec requires it.
- Do not treat placeholder files as deletable until their specs/backlog status are resolved.
- Do not modify backlog workbooks from repo tasks.

## Canonical / Sensitive Files

- `alpha_solver_portable.py` is the portable standalone behavior contract.
- `alpha-solver-v91-python.py` and `alpha_solver_entry.py` are modular/reference entrypoint paths.
- `docs/ENTRYPOINTS.md` documents the portable, modular/reference, bridge, and CLI entrypoint roles.
- `.specs/INDEX.md` should stay synchronized when adding specs.
- `.env.example` and `scripts/check_env.py` define current environment expectations.

## Validation

- Run the most focused relevant tests first.
- Run `python -m pytest -q` when practical.
- For docs-only changes, run relevant smoke, help, or check commands where applicable.
- If tests fail due to pre-existing unrelated issues, report them clearly.
