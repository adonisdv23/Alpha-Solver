# Likely test files

## May inspect

### Focused local LLM and operator tests

- `tests/test_local_llm_operator_cli.py` — operator CLI argument, opt-in, prompt, and output behavior.
- `tests/test_local_llm_solver_orchestration_runner.py` — local orchestration runner behavior.
- `tests/test_local_llm_provider_adapter.py` — provider adapter validation and fail-closed behavior.
- `tests/test_local_llm_runtime_integration.py` — runtime config, endpoint, timeout, and local runtime integration behavior.
- `tests/test_local_llm_contract_consumption_proof.py` — local LLM contract proof helper behavior.

### Docs and packet guardrail tests

- `tests/test_local_llm_doc_paths.py` — local LLM doc path consistency.
- `tests/test_local_llm_evidence_boundaries.py` — evidence-boundary checker behavior.
- `tests/test_local_llm_packet_consistency.py` — packet continuity and selected-next consistency.

### Adjacent behavior tests to inspect cautiously

- `tests/cli/test_alpha_solver_cli.py`, `tests/test_console_entry.py`, `tests/test_cli_run.py`, `tests/test_cli_gates.py`, and `tests/test_cli_replay.py` — CLI behavior and workflow coverage.
- `tests/test_alpha_minimal_behavior_contract.py` and `tests/fixtures/alpha_minimal_behavior_cases.json` — minimal behavior contracts.
- `tests/policy/test_safe_out.py`, `tests/policy/test_safe_out_sm.py`, `tests/policy/test_safe_out_v12.py`, and `tests/test_governance.py` — SAFE-OUT and governance behavior.
- `tests/test_budget_gate.py`, `tests/test_budget_guard.py`, `tests/finops/test_budget.py`, and `tests/test_budget_cli_guard.py` — budget guard behavior.
- `tests/test_determinism.py`, `tests/test_determinism_cli.py`, `tests/test_determinism_harness.py`, and `tests/test_tot_determinism.py` — determinism expectations.
- `tests/observability/*`, `tests/test_observability.py`, and `tests/test_metrics_smoke.py` — observability and metric expectations.
- `tests/test_api_endpoints.py`, `tests/test_api_auth_ratelimit.py`, and `tests/api/test_health.py` — API boundary tests.
- `tests/dashboard/*` — dashboard configuration tests.
- `tests/providers/*` — provider contract, accounting, telemetry, and live-smoke boundaries.
- `tests/test_mcp_*.py` and `tests/test_mcp_adapter.py` — MCP behavior and guardrail tests.

## May modify later only with a separate approved implementation scope

- Future Self Operator MVP implementation should add or update focused local LLM/operator tests before broad regression work.
- Tests for API, dashboard, hosted-provider fallback, credentials, budget, routing, SAFE-OUT, determinism, replay, observability, MCP, or SolverEnvelope behavior may be modified only when the future implementation spec explicitly includes those behavior surfaces.
- Live provider tests must not be broadened or enabled as part of Self Operator MVP work unless a separate live-service authorization is granted.
