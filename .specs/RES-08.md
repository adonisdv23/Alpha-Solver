# CODE SPEC — RES-08 · Budget Simulator + Evidence Pack (RES)

## Goal
Create a stable MCP error taxonomy with enum, mapper, helpers, and tests. Normalize arbitrary exceptions to deterministic classes.

## Acceptance Criteria
- All taxonomy tests pass.
- Deterministic mapping for timeouts, connectivity, auth, 429, schema validation, sandbox, cancelled, unknown.
- `to_json()` serializes; `to_route_explain()` yields small dict; `is_retryable()` correct.

## Code Targets
service/budget/simulator.py; service/evidence/collector.py; config/cost_models.yaml; tests/test_budget_simulator.py; tests/test_evidence_pack.py

## Design
- ErrorClass enum (TOOL_NOT_FOUND, SCHEMA_VALIDATION, AUTH, RATE_LIMIT, TIMEOUT, CANCELLED,
  CONNECTIVITY, RETRYABLE, NON_RETRYABLE, SANDBOX_VIOLATION, SECURITY, UNKNOWN)
- MCPError dataclass(cls, message, code|None, retryable:bool, root:str, meta:dict|None)
- map_exception(exc) -> MCPError (rules as above); add meta["secondary"]="RETRYABLE" when applicable
- Helpers: to_route_explain(mcp_error), is_retryable(mcp_error)
- No external deps; tests use fake exceptions (no httpx import)

## Tests (must add)
tests/test_mcp_errors.py:
- test_timeout_maps_retryable
- test_connectivity_maps_retryable
- test_rate_limit_429_retryable
- test_auth_nonretryable
- test_schema_validation_nonretryable
- test_sandbox_violation_nonretryable
- test_cancelled_nonretryable
- test_unknown_default
- test_to_route_explain_truncates_message
- test_to_json_is_serializable
