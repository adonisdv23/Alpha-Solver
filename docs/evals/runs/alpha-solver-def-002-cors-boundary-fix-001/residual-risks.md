# Residual risks

- Public exposure remains blocked until remaining DEF-002 lanes close or receive
  explicit recorded decisions.
- `/v1/solve` auth/tenancy and per-tenant enforcement remain separate blockers.
- Dashboard exposure remains unauthorized unless an operator intentionally
  configures and validates the full surface.
- Provider execution, data-sharing, telemetry, redaction, and supply-chain
  controls remain outside this RR-01-only fix.
- Operators must choose and maintain any external CORS allowlist; this lane does
  not bless a production origin.
