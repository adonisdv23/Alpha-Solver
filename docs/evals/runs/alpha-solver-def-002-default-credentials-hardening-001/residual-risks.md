# Residual risks

- DEF-002 as a whole remains open; this packet addresses RR-03 only.
- Public exposure remains forbidden until CORS defaults, `/v1/solve` auth/tenancy,
  data classification, supply-chain lanes, cost controls, route inventory, and
  operator approval are complete where applicable.
- Explicit operator-provided weak credentials cannot be fully judged by this
  lane; deployments still need credential generation, custody, and rotation
  controls.
- Existing external deployments must set non-default secrets before enabling
  protected surfaces.
