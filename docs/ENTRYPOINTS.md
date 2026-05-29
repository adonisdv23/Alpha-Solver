# Entrypoint and Reference File Roles

## Purpose

Alpha Solver intentionally keeps several top-level Python entrypoint and reference files because they serve different compatibility, architecture, and runnable CLI purposes. Some of these files can look redundant or legacy at a glance, but they are not interchangeable.

Do not delete, rename, merge, or consolidate these files casually. Any change that affects behavior should be tied to an explicit spec or architecture decision and should explain which entrypoint path is in scope.

## File roles

### `alpha_solver_portable.py`

`alpha_solver_portable.py` is the portable standalone behavior contract and portable spec monolith. It preserves LLM-facing behavior expectations independent of the modular package layout.

Sensitive behavior areas include:

- SAFE-OUT behavior and recovery flow
- routing and route explanation expectations
- confidence scoring and thresholds
- shortlist generation
- budget guard behavior
- deterministic output behavior
- observability and replay expectations
- SolverEnvelope-style response structure

Changes to this file should be intentional and reviewed against the portable behavior expectations. PRs that touch portable behavior should explicitly mention SAFE-OUT, routing, and envelope implications.

### `alpha-solver-v91-python.py`

`alpha-solver-v91-python.py` is the modular/reference compatibility entrypoint. It wraps and imports repository modules and configuration to expose the solver through the modular architecture.

Use this file for architecture grounding and compatibility with the modular implementation. It is not the same as the portable standalone behavior contract in `alpha_solver_portable.py`.

### `alpha_solver_entry.py`

`alpha_solver_entry.py` is an import bridge and compatibility wrapper. It dynamically loads `alpha-solver-v91-python.py` and re-exports `AlphaSolver` while also exposing the shared `_tree_of_thought` path used by other entrypoints.

This file exists so import-based callers can use a Python module name while the reference implementation remains in the historical hyphenated filename.

### `alpha_solver_cli.py`

`alpha_solver_cli.py` is the root CLI wrapper. It uses the compatibility entry/import path from `alpha_solver_entry.py` and provides a runnable top-level command surface for Tree-of-Thought solver execution.

Do not treat this file as the portable behavior contract; it is a CLI surface over the compatibility entry path.

### `cli/alpha_solver_cli.py`

`cli/alpha_solver_cli.py` is the command-oriented CLI surface for repo workflows such as run, replay, gates, finops, and traces. It is useful for local smoke checks and offline command workflows.

Do not conflate this command CLI with `alpha_solver_portable.py` or with the modular/reference compatibility entrypoint.

## Agent guidance

- Do not delete or rename these files just because they look redundant.
- Do not consolidate the portable and modular paths without an explicit spec or architecture decision.
- If a PR changes behavior in one path, state whether the other path should stay unchanged, mirror the behavior, or be intentionally out of scope.
- PRs touching portable behavior should explicitly mention SAFE-OUT, routing, and SolverEnvelope-style response implications.
- Keep documentation-only entrypoint/process PRs narrow: do not fix spec drift, placeholder tests, registry exports, or unrelated CLI behavior while documenting these roles.

## Docs-only validation

For documentation-only changes to these entrypoint contracts, run:

```bash
git diff --check
```

If the docs reference runnable entrypoints or CLI smoke checks, run the directly referenced commands when practical:

```bash
python alpha_solver_cli.py --help
python cli/alpha_solver_cli.py --help
python -m alpha.cli --help
python alpha_solver_portable.py "Summarize Alpha Solver restart state" --json --deterministic
```

If any command cannot run in the current environment, report the command and the reason clearly in the PR.
