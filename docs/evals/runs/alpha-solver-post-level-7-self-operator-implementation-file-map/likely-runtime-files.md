# Likely runtime files

## May inspect for future Self Operator MVP planning

### Entrypoints and CLI surfaces

- `docs/ENTRYPOINTS.md` — entrypoint role contract and sensitivity guide.
- `alpha_solver_portable.py` — portable standalone behavior contract; inspect only unless explicitly authorized.
- `alpha-solver-v91-python.py` — modular/reference compatibility entrypoint; inspect for compatibility impacts.
- `alpha_solver_entry.py` — import bridge used by import-based callers.
- `alpha_solver_cli.py` — root CLI wrapper over the compatibility entry path.
- `cli/alpha_solver_cli.py` — command-oriented CLI for repo workflows.
- `alpha/cli/__main__.py` and `alpha/cli/main.py` — package CLI entry surfaces.
- `alpha/local_llm/operator_cli.py` — local-only operator wrapper and likely first Self Operator CLI inspection point.

### Local orchestration modules

- `alpha/local_llm/orchestration_runner.py` — local orchestration flow and status normalization.
- `alpha/local_llm/provider_adapter.py` — local runtime config, endpoint validation, transport, parser, fail-closed behavior, and provenance.
- `alpha/local_llm/portable_contract.py` — local LLM proof/contract helper.
- `alpha/local_llm/__init__.py` — package exports and import boundary.

### Solver, routing, and policy surfaces to inspect cautiously

- `alpha/core/orchestrator.py`, `alpha/core/runner.py`, `alpha/core/router.py`, and `alpha/core/plan.py` — core orchestration, runner, router, and plan surfaces.
- `alpha/routing/router_v12.py`, `alpha/router/agents_v12.py`, and `alpha/router/progressive.py` — routing surfaces that may intersect with operator behavior.
- `alpha/policy/safe_out.py`, `alpha/policy/safe_out_sm.py`, `alpha/policy/engine.py`, and `alpha/policy/governance.py` — SAFE-OUT and governance behavior.
- `alpha/core/budgets.py`, `alpha/finops/budget.py`, `service/budget/guard.py`, and `service/budget/simulator.py` — budget and spend guard paths.
- `alpha/core/determinism.py`, `alpha/core/replay.py`, `service/determinism/harness.py`, and `service/replay/*` — determinism and replay paths.
- `alpha/core/observability.py`, `alpha/core/telemetry.py`, `alpha/solver/observability.py`, `service/observability/*`, and `service/metrics/exporter.py` — observability and metrics paths.

### API and dashboard surfaces to inspect only when explicitly in scope

- `service/app.py`, `alpha/api/health.py`, and `service/health.py` — API app and health surfaces.
- `alpha/webapp/routes/*.py` and `alpha/webapp/templates/*.html` — dashboard/web app surfaces.
- `alpha/dashboard/*.json`, `dashboards/*.json`, and `docs/DASHBOARDS.md` — dashboard configuration and documentation.

### Providers and credentials surfaces to inspect only when explicitly in scope

- `alpha/providers/*.py`, `alpha/adapters/*.py`, and `service/adapters/*.py` — hosted/local provider and adapter paths.
- `.env.example`, `scripts/check_env.py`, `service/config/secrets.example.yaml`, and `service/config/*` — environment and credential expectation paths.

## May modify later only with a separate approved implementation scope

- `alpha/local_llm/operator_cli.py` may be a candidate future modification point for a narrow Self Operator command surface, but only if a future spec authorizes behavior changes.
- `alpha/local_llm/orchestration_runner.py` may be a candidate future modification point for local-only Self Operator orchestration behavior, but only with focused tests and preserved evidence boundaries.
- `alpha/local_llm/provider_adapter.py` may be modified later only if endpoint, timeout, local runtime, or provenance behavior is explicitly in scope.
- CLI entrypoints may be modified later only after an entrypoint-specific impact statement explains portable, modular, bridge, and command CLI implications.
- API, dashboard, hosted-provider, credential, budget, SAFE-OUT, routing, determinism, replay, observability, MCP, and SolverEnvelope behavior must not be modified unless a future spec explicitly authorizes that surface.
