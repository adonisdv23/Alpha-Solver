# Accepted residual candidates

This lane does **not** accept residual risk. It only routes candidate residuals
to a later operator acceptance lane after must-fix items are closed or explicitly
deferred.

| Item | Candidate residual | Acceptance precondition | Why not immediate implementation |
| --- | --- | --- | --- |
| RR-04 | Provider-enabled prompt data sharing | Committed operator/end-user disclosure covering provider identity, what prompt data is sent, opt-in gate, and retention/data-processing boundary | Prompt transmission is intrinsic to provider-backed inference; governance disclosure and operator acceptance are required. |
| RR-A1 | Pattern-based redaction coverage limits | Operator review of deployment secret formats; either accepted limits or expanded regex/keyword coverage with tests | Perfect redaction cannot be proven by this planning lane; risk must be bounded or hardened separately. |
| JWT keystore management | Deployment custody and rotation of RS256 public-key keystore | Deployment runbook or operator attestation describing key custody/rotation without committing secrets | Key custody is operational; repo should not contain private keys. |
| Evidence payload hygiene | Evidence API callers avoid submitting secrets | Operator policy or future validators/redaction guardrails | Caller behavior requires governance and possibly a separate hardening lane. |

## Explicitly not accepted here

RR-01, RR-02, RR-03, RR-05, RR-06, RR-07, RR-08, and RR-09 remain must-fix or
operator-deferral items. They are not accepted residual risks in this packet.
