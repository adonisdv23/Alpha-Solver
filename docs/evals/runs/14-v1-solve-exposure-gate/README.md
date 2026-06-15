# 14 - V1 Solve Exposure Gate Packet

Executor: `Codex`  
Mode: `gate-only; docs/tests only`  
Date: `2026-06-15`  
Surface: bundled FastAPI `POST /v1/solve`

## TLDR

Verdict: `BLOCKED`.

`/v1/solve` must not be exposed, advertised, deployed as a public endpoint, or treated as public-ready from this packet. Static review found a concrete route and multiple local/provider guardrails, but public exposure remains blocked by unresolved identity/tenancy decisions, incomplete public-exposure risk closure, and required operator/security authorization.

## Scope and hard boundaries honored

This packet is docs-only. It did not expose `/v1/solve`, deploy, publish, open a public endpoint, call providers, use tokens, access credentials, run hosted models, run local models, expose dashboard behavior, mutate Google Sheets, or change runtime routing.

## Gate verdict

`BLOCKED`

### Verdict rationale

The endpoint exists in code and has an API-key/rate-limit dependency, local default behavior, explicit OpenAI opt-in, provider cost-cap checks, structured provider SAFE-OUT behavior, and local-only evidence from an earlier DEF-002 partial-remediation lane. However, exposure is blocked because the existing DEF-002 spec and evidence packet explicitly leave JWT/key-to-tenant binding and middleware mounting decisions unresolved, require `/v1/solve` to remain unexposed until an operator/security decision resolves the identity and tenancy model, and do not constitute runtime/public/provider/security/privacy readiness evidence.

## Evidence reviewed

### Source/spec/docs evidence

- `AGENTS.md` repo instructions and current source-of-truth rules.
- `.specs/ALPHA-SOLVER-DEF-002-V1-SOLVE-AUTH-TENANCY-CLOSURE-001.md`
- `.specs/ALPHA-SOLVER-DEF-002-PROVIDER-COST-CAPS-STOP-CONTROL-001.md`
- `.specs/ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001.md`
- `.specs/PROVIDER-SAFEOUT-001.md`
- `.specs/PROVIDER-BUDGET-001.md`
- `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`
- `docs/evals/runs/alpha-solver-def-002-v1-solve-auth-tenancy-closure-001/README.md`
- `docs/evals/runs/alpha-solver-def-002-v1-solve-auth-tenancy-closure-001/residual-risks.md`
- `docs/evals/runs/alpha-solver-def-002-v1-solve-auth-tenancy-closure-001/v1-solve-boundary-evidence.md`
- `docs/OPPORTUNITY_REGISTER.md`
- `docs/RUNTIME_READINESS.md`
- `service/app.py`
- `service/security.py`
- `service/middleware/tenant_middleware.py`

### Commands used for evidence review

```bash
rg --files -g 'AGENTS.md' -g '.specs/**' -g 'docs/**' -g 'tests/**' -g '*.py'
rg -n "v1/solve|solve endpoint|SAFE-OUT|no-echo|derivation|provider|token|auth|tenan|redact|logging|route" .specs docs alpha alpha_solver_entry.py alpha_solver_portable.py alpha-solver-v91-python.py
rg -n "@app\.|/v1/solve|api_key|TenantMiddleware|JWTAuth|rate|cors|log|provider.cost|MODEL_PROVIDER|SAFE-OUT|safe_out" service tests docs/evals/runs/alpha-solver-def-002-v1-solve-auth-tenancy-closure-001 -g '!**/__pycache__/**'
sed -n '1,220p' service/app.py
sed -n '220,520p' service/app.py
sed -n '860,1360p' service/app.py
sed -n '1,120p' service/security.py
sed -n '1,120p' service/middleware/tenant_middleware.py
```

## Required check matrix

| Check | Gate status | Evidence reviewed | Missing prerequisite before exposure |
| --- | --- | --- | --- |
| Auth boundary | `BLOCKED` | `/v1/solve` is declared with `Depends(rate_limiter)`, and `rate_limiter` calls `validate_api_key`. `validate_api_key` enforces configured API keys only when auth is enabled. | Operator/security decision for mandatory public auth posture, configured key/JWT requirements, failure semantics, default-deny deployment settings, and evidence that unauthenticated public traffic cannot execute solver behavior. |
| Tenancy boundary | `BLOCKED` | `TenantMiddleware` exists, but the DEF-002 lane states whether it should mount on `/v1/solve` remains unresolved. `/v1/solve` currently obtains tenant metadata from request context/header only for provider metadata. | Resolve tenant identity source, JWT/key-to-tenant binding, required tenant middleware mounting, tenant-scoped rate limits/quotas, and tenant isolation evidence for `/v1/solve`. |
| Route availability | `INCONCLUSIVE_FOR_PUBLIC_EXPOSURE` | Static code shows `@app.post("/v1/solve")`; runtime readiness docs describe the route as verified local/offline/partial. | Do not translate local route existence into public availability. Require explicit deployment exposure decision, public ingress review, and endpoint advertisement approval. |
| Request/response logging boundary | `BLOCKED` | Request middleware logs request id, path, client, duration, and strategy; provider SAFE-OUT/accounting specs require no raw prompts or raw provider payloads in provider failure/accounting bodies. | Public logging policy for query/body handling, client identifiers, retention, sharing, redaction verification, and incident/audit handling. Evidence must prove no raw sensitive prompts, provider bodies, headers, tokens, cookies, or credentials are logged or shared. |
| Redaction/data-sharing rules | `BLOCKED` | Existing specs require allowlist-built provider SAFE-OUT/accounting records and prohibit raw prompt/provider payload/secret leakage. | Exposure packet must define data classification, redaction responsibilities, evidence-sharing boundaries, retention, deletion, export controls, and operator review of any telemetry/evidence artifacts. |
| Provider cost/token caps if providers are reachable | `BLOCKED_FOR_PUBLIC_EXPOSURE` | OpenAI provider path is explicit opt-in via `MODEL_PROVIDER=openai`; preflight caps are required and emergency stop is checked; post-call usage/cost checks exist. | Operator-approved provider budget policy, per-tenant/request caps, enforcement evidence under public auth/tenant context, billing/quota monitoring, emergency stop runbook, and live-provider validation only in an explicitly authorized lane. |
| Local model path boundaries if local models are reachable | `BLOCKED` | Local LLM spec says local LLM mode is optional/default-off, loopback-only, no silent hosted fallback, and `/v1/solve` remains a blocked surface for local LLM mode unless a later spec authorizes it. | Confirm no public `/v1/solve` path can reach local model runtimes unless a later approved spec implements loopback-only local LLM boundaries and exposure-specific tests. |
| No-echo/derivation evidence | `INCONCLUSIVE_FOR_PUBLIC_EXPOSURE` | A deterministic local-only no-echo/substantive-generation gate spec exists for synthetic fixtures and explicitly does not provide provider/model-quality/public-readiness claims. | Endpoint-specific no-echo/derivation evidence for the exact exposed runtime mode, with allowed evidence sources, fixture policy, false-positive/false-negative limits, and human review thresholds. |
| Error/SAFE-OUT behavior | `INCONCLUSIVE_FOR_PUBLIC_EXPOSURE` | HTTP exceptions return `SAFE-OUT`, internal errors return `SAFE-OUT: internal error`, provider errors return structured provider SAFE-OUT bodies, and provider empty answers SAFE-OUT. | Public error taxonomy, status-code policy, abuse/error-rate monitoring, no-secret negative tests for public responses, and operator-approved user-facing SAFE-OUT copy. |
| Public exposure risk | `BLOCKED` | Opportunity register classifies actual external exposure as deferred and requires public exposure readiness gate, DEF-002 closure, smoke evidence, operator approval, auth/rate-limit/tenant/CORS closure, cost controls, and incident-response minimums. | Complete a dedicated public exposure readiness gate after DEF-002 closure, CORS/ingress review, auth/tenant closure, rate-limit policy, abuse handling, monitoring, incident response, rollback, and evidence-retention rules. |
| Operator authorization requirements | `BLOCKED` | DEF-002 spec/evidence require operator/security decision before `/v1/solve` exposure. | Written operator/security approval with scope, environment, auth/tenant model, provider mode, budget caps, logging/redaction policy, monitoring/incident owner, stop conditions, rollback owner, and allowed claims. |

## Missing prerequisites

1. Written operator/security decision resolving identity and tenancy model for `/v1/solve`.
2. JWT/key-to-tenant binding decision and implementation/evidence if required.
3. Decision on mounting `TenantMiddleware` and/or JWT middleware on `/v1/solve`.
4. Public auth posture and proof that unauthenticated requests cannot execute solver behavior.
5. Tenant-scoped rate limit/quota design and exposure-mode evidence.
6. Public CORS/ingress policy and evidence for only approved origins/headers/methods.
7. Request/response logging and telemetry redaction policy, including prompt/body handling.
8. Data sharing, evidence retention, deletion, and incident-response rules.
9. Provider cost/token/request caps bound to public auth/tenant context if any hosted provider is reachable.
10. Emergency stop and rollback runbook with named owner.
11. Confirmation that local model runtimes are unreachable from public `/v1/solve` unless separately authorized and loopback-constrained.
12. Endpoint-mode no-echo/derivation evidence for the actual runtime configuration.
13. Public SAFE-OUT/error response review and no-secret negative tests.
14. Explicit non-claims/marketing boundary approval before any advertisement.

## Authorization fields required before any future exposure lane

A future operator-approved exposure lane must record:

- `operator_approval_id`: required, non-empty.
- `security_reviewer`: required, named person/team.
- `approved_environment`: required, exact environment and ingress path.
- `approved_surface`: required, exact route(s); default must be only `POST /v1/solve` if approved.
- `auth_model`: required, e.g. API key, JWT, dashboard session, service-to-service, or other.
- `tenant_model`: required, including tenant source and binding rule.
- `cors_policy`: required, exact origins/headers/methods.
- `provider_mode`: required, e.g. local/offline only or explicit provider mode.
- `provider_caps`: required if hosted providers are reachable.
- `local_model_policy`: required if any local model path exists.
- `logging_policy`: required, including prompt/body retention and redaction.
- `data_sharing_policy`: required, including evidence artifacts and external sharing.
- `monitoring_owner`: required.
- `incident_response_owner`: required.
- `emergency_stop_owner`: required.
- `rollback_plan`: required.
- `allowed_claims`: required and bounded.
- `stop_conditions`: required and enforceable.

## Stop conditions

Stop immediately and do not expose or advertise `/v1/solve` if any of the following is true:

- Operator/security approval is absent, ambiguous, expired, or outside scope.
- Auth is disabled, optional, misconfigured, or dependent on known/default credentials.
- Tenant identity is absent, spoofable, unbound from credentials, or unverified.
- Rate limits/quotas are not tenant/key scoped for the exposure mode.
- CORS/ingress policy is broad, unknown, or unreviewed.
- Logs, telemetry, evidence, or error bodies can include raw prompts, provider payloads, headers, cookies, tokens, credentials, environment dumps, tracebacks with secrets, or tenant-sensitive data.
- Hosted provider execution can occur without explicit caps, request-count limits, token limits, cost limits, emergency stop, and rollback owner.
- Local model execution can reach non-loopback endpoints or can silently fall back to hosted providers.
- No-echo/derivation evidence is missing for the actual exposed runtime mode.
- SAFE-OUT/error behavior leaks secrets, raw payloads, or unsupported readiness/value/security claims.
- Monitoring, incident response, evidence retention, or deletion responsibilities are undefined.
- Any person attempts to use this packet as readiness, production, security/privacy completion, public readiness, value, or Alpha-superiority evidence.

## Non-claims

This packet does not claim:

- `/v1/solve` readiness.
- Runtime readiness.
- Provider validation.
- Live provider usability.
- Local model readiness.
- Production readiness.
- Public readiness.
- Security/privacy completion.
- Value validation.
- Benchmark success.
- Alpha superiority.
- Endpoint safety for public users.
- That auth, tenancy, CORS, logging, redaction, incident response, provider caps, or no-echo/derivation are complete for public exposure.

## Checks run for this packet

- Static file/spec/doc review only.
- No hosted endpoint tests.
- No live provider tests.
- No local model execution.
- No credential access.
- No Google Sheets mutation.
- No deployment or public ingress checks.

Validation command run after creating this packet:

```bash
python -m pytest -q tests/test_v1_solve_auth_tenancy_boundary.py tests/test_api_auth_ratelimit.py tests/providers/test_safeout.py
```
