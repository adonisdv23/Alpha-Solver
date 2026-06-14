# Claim boundary

## Allowed internal statements

- Alpha Solver has a committed evidence chain for local/offline Self Operator execution and governance packets.
- PR #512 records a redacted operator project/billing/cost/data-sharing boundary attestation for one tiny synthetic OpenAI smoke retry.
- PR #527 records that the selected smoke retry was blocked before provider execution because explicit operator authorization fields were missing.
- Provider calls, tokens, and provider cost for PR #527 were all `0`.
- DEF-002 security/privacy review work has identified and routed gaps, but the current scorecard does not claim closure.
- Runtime entrypoints and public-exposure risks have been mapped at documentation level.
- The manual discrimination Value Read exists as a design packet, but Track S simulation was not run and Track R runtime/provider execution is blocked.
- The actual Value Read blocked verdict supports fixing no-echo / derivation first; it does not support value, runtime, provider, or readiness claims.

## Forbidden claims

Do not claim:

- MVP readiness.
- Public readiness.
- Production readiness.
- Alpha superiority.
- OpenAI/provider validation.
- API smoke success.
- Token usage evidence.
- Benchmark validation.
- Core product value proof.
- Value Read simulation or runtime result success.
- No-echo substantive generation success.
- Operator preference versus a plain baseline.
- Security/privacy completion or DEF-002 closure.
- `/v1/solve` readiness.
- Dashboard readiness.
- Broad-user, customer-pilot, autonomous, investor-traction, or incubator-readiness status.

## Narrative-safe wording

Use: "internal readiness scorecard captured; not ready; operator decision required."

Do not use: "MVP ready," "production ready," "validated by OpenAI," "superior to baseline," or "ready for users."
