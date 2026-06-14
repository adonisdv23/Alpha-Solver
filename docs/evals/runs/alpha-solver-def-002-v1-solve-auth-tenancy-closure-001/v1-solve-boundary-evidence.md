# `/v1/solve` Boundary Evidence

Verdict: `DEF_002_V1_SOLVE_PARTIAL_REMEDIATION`

Observed local-only boundary evidence:

1. Unauthorized `/v1/solve` requests fail with SAFE-OUT before solver execution.
2. Authorized synthetic requests with `MODEL_PROVIDER=local` execute local solver seams without constructing provider clients.
3. Rate limiting is scoped by API key, so one synthetic key exhausting its quota does not consume another key's quota.
4. CORS preflight behavior is inherited from the already-merged CORS configuration on `main`; this lane does not modify CORS implementation.
5. No provider call is made.
6. Tests require no real credentials and no live provider access.

This is not `/v1/solve` readiness evidence. `/v1/solve` remains local/unexposed and partial-remediation only.
