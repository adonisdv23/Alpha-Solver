# Operator approval template

This template is for a future lane only. It is not completed by this packet.

## Operator decision

- Decision: `GO` / `NO-GO` / `DEFER`
- Operator name/role: `<redacted or named per policy>`
- Date: `<YYYY-MM-DD>`
- Environment/surface: `<API / /v1/solve / dashboard / other>`
- Evidence packet reviewed: `<packet paths>`

## Required checklist

- [ ] DEF-002 closeout or explicit operator deferral packet reviewed.
- [ ] API auth model selected and negative tests passed.
- [ ] `/v1/solve` auth, tenant, rate, CORS, SAFE-OUT, logging, and cost-cap tests passed.
- [ ] Dashboard auth/session/CSRF/default-credential/role/route tests passed.
- [ ] Secret storage and masked display/audit tests passed with synthetic values.
- [ ] Provider billing/project/cost caps and kill switch verified for this environment.
- [ ] Data-sharing and telemetry disclosures approved.
- [ ] Redaction and prompt-content handling reviewed.
- [ ] Dependency lock/hash/provenance checks passed or accepted.
- [ ] Rollback and incident-response runbooks exist and are assigned.
- [ ] Forbidden claims list reviewed and accepted.

## Approval statement

I approve exposure only for the exact surface and environment named above, with the cited evidence packets and residual risks. Any other surface remains no-go.
