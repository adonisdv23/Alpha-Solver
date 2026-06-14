# RR-01 closure evidence

RR-01 finding: wildcard CORS origin combined with credentialed requests was an
unsafe default for any externally shared or authenticated runtime surface.

Closure evidence:

- Default `SERVICE_CORS_ORIGINS` now resolves to local-only origins.
- Credentialed CORS remains allowed only with non-wildcard origins.
- `SERVICE_CORS_ALLOW_CREDENTIALS` is evaluated when each `ServiceCorsConfig`
  instance is constructed, so later operator/test opt-outs are not pinned to an
  import-time value.
- Explicit external origins must be supplied through `SERVICE_CORS_ORIGINS`.
- `SERVICE_CORS_ORIGINS=*` with `SERVICE_CORS_ALLOW_CREDENTIALS=false` is
  accepted only as a non-credentialed configuration.
- `SERVICE_CORS_ORIGINS=*` with `SERVICE_CORS_ALLOW_CREDENTIALS=true` or another
  common truthy value fails at config construction.
- Real FastAPI app preflight tests deny an unlisted external origin and allow a
  default local origin.

Closure scope is RR-01 only. It does not close `/v1/solve` auth/tenancy,
provider disclosure, data classification, supply-chain, or public operations
requirements.
