# Duplicate and Overlapping Surface Map

| Overlap | Surfaces | Risk |
|---|---|---|
| API auth | `/v1/solve` API-key dependency vs `AuthMiddleware` JWT/API-key stack | Operators may assume JWT/tenant middleware protects `/v1/solve` when it is not mounted there. |
| Rate limiting | `/v1/solve` in-memory limiter, `AuthMiddleware` optional limiter, `TenantLimiter` | Multiple implementations can diverge in semantics and observability. |
| Dashboard routes | Bundled fail-closed auth+preview vs standalone settings/request/run/jobs routers | Standalone routers can look public-ready but are not bundled in the safer mount. |
| Provider entry | `/v1/solve` provider branch, expert preview guard, OpenAI client, local-LLM adapter, fake provider | Provider-capable code exists in several layers with different guard semantics. |
| Solver behavior | `alpha_solver_portable.py` contract, `alpha-solver-v91-python.py`, `alpha_solver_entry.py`, service local fallback | Portable prompt contract and modular runtime may drift if consolidated without tests/spec. |
| Evidence | Eval packet docs vs `service/evidence/api.py` runtime router | Evidence artifacts are documentation; evidence API is mutable runtime storage and needs auth if exposed. |
| Observability | Service logs/metrics, provider telemetry/accounting, Grafana dashboards, CLI replay/record flags | Observability surfaces do not share one explicit runtime authority. |
