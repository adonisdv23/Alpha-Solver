# ALPHA-SOLVER-DEF-002-V1-SOLVE-AUTH-TENANCY-CLOSURE-001

Lane ID: `ALPHA-SOLVER-DEF-002-V1-SOLVE-AUTH-TENANCY-CLOSURE-001`

Verdict: `DEF_002_V1_SOLVE_PARTIAL_REMEDIATION`

## Purpose

Capture local-only evidence for the bundled `/v1/solve` auth, rate-limit, CORS-inherited, logging, and SAFE-OUT boundaries without exposing `/v1/solve`, without calling hosted providers, and without claiming runtime, public, provider, production, or DEF-002 readiness.

## Requirements

- `/v1/solve` remains bundled/local and unexposed as a public runtime surface by this lane.
- Evidence must be local-only and must not call providers, consume tokens, access credentials, deploy, or run provider-backed tests.
- Unauthorized `/v1/solve` requests must fail before solver execution.
- Authorized synthetic local requests with `MODEL_PROVIDER=local` must not construct provider clients or make provider calls.
- Rate limiting evidence must be scoped by API key.
- CORS preflight behavior must inherit the already-merged CORS configuration from `main`; this lane must not modify CORS implementation.
- The packet must state that JWT/key-to-tenant binding, `TenantMiddleware` mounting on `/v1/solve`, and `JWTAuthMiddleware` mounting on `/v1/solve` remain unresolved.
- `/v1/solve` must remain unexposed until an operator/security decision resolves the identity and tenancy model.

## Evidence

See `docs/evals/runs/alpha-solver-def-002-v1-solve-auth-tenancy-closure-001/`.
