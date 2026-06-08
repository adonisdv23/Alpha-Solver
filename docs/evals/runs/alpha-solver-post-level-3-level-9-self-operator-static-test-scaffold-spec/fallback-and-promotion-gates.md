# Fallback and promotion gates

Static tests must fail with:

- `SELF_OPERATOR_ROUTE_EXPOSURE_BLOCKED` for `/v1/solve`, dashboard, API, or route exposure.
- `SELF_OPERATOR_FALLBACK_BLOCKED` for fallback logic.
- `SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED` for hosted fallback or silent provider fallback.
- `SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED` for evidence promotion, behavior-evidence upgrades, source-artifact mutation, or MVP-readiness claims beyond the accepted boundary.

These finding IDs must map to the approval stop-state registry entries for `SELF_OPERATOR_ROUTE_EXPOSURE_BLOCKED`, `SELF_OPERATOR_FALLBACK_BLOCKED`, `SELF_OPERATOR_HOSTED_FALLBACK_BLOCKED`, and `SELF_OPERATOR_EVIDENCE_PROMOTION_BLOCKED`.
