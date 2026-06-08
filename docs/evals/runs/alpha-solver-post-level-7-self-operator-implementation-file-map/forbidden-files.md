# Forbidden files and surfaces without explicit authorization

The following files and surfaces must not change in a future Self Operator MVP lane unless the user or a new approved spec explicitly authorizes that exact surface.

## Canonical and sensitive entrypoints

- `alpha_solver_portable.py`
- `alpha-solver-v91-python.py`
- `alpha_solver_entry.py`
- `alpha_solver_cli.py`
- `cli/alpha_solver_cli.py`
- `docs/ENTRYPOINTS.md`, unless the authorized change is documentation-only entrypoint alignment.

## Runtime behavior surfaces

- `/v1/solve` or any API route behavior in `service/app.py`, `alpha/api/*`, or `alpha/webapp/routes/*`.
- Dashboard preview, dashboard auth, web templates, or dashboard JSON configuration.
- Hosted provider adapters, provider fallback, provider credential handling, provider telemetry, or live provider tests.
- SAFE-OUT, routing, MCP, budget guard, determinism, replay, observability, and SolverEnvelope behavior.
- Authentication, OAuth, API key, JWT, secret store, tenancy, and credential configuration paths.

## Planning, provenance, and generated artifacts

- Backlog workbooks or external planning ledgers.
- `data/alpha_solver_master_table_v0_7_0.*` registry export/provenance artifacts.
- Historical evidence packet source artifacts under `docs/evals/runs/**/source-artifact*/`.
- Runtime output folders such as `artifacts/`, `telemetry/`, and `logs/`, except for explicitly authorized new run artifacts.

## Deletion and rename restrictions

- Do not delete, rename, merge, or consolidate legacy/reference files merely because they appear redundant.
- Do not move existing specs or historical packet files casually.
- Do not treat placeholder files as deletable until their status is resolved by an approved spec or explicit user authorization.
