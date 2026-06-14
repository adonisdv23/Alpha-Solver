# ALPHA-SOLVER-DEF-002-V1-SOLVE-AUTH-TENANCY-CLOSURE-001

## Purpose

Close local evidence gaps for the bundled `/v1/solve` route boundary without exposing it publicly or claiming production readiness.

## Scope

- Identify the active `/v1/solve` route and mounted dependencies.
- Prove API-key auth, rate limiting, CORS, SAFE-OUT, logging, tenant metadata, and provider-call default behavior with local tests and static evidence.
- Harden credentialed CORS defaults so wildcard origins are not the bundled default.
- Record residual tenant/JWT/public-exposure design gaps rather than inventing a broader auth/tenancy model.

## Non-goals

- Public exposure, deployment, live provider calls, credentials, tokens, JWT keystore rollout, or production-readiness claims.
- Broad routing, SolverEnvelope, MCP, SAFE-OUT, budget guard, or dashboard refactors.
- Backlog workbook updates.

## Acceptance

- Unauthorized `/v1/solve` requests fail before solver/provider execution.
- Authorized synthetic local requests succeed without provider construction by default.
- Rate-limit behavior is covered and documented as API-key scoped, not tenant-middleware scoped.
- CORS allows configured localhost origins with credentials and rejects unconfigured origins.
- Evidence packet records tested path, verdict, remaining unknowns, non-actions, and non-claims.
