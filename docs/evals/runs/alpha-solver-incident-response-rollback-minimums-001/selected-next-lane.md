# Selected next lane

Recommended incident-response/public-exposure next lane:
`ALPHA-SOLVER-PUBLIC-EXPOSURE-OWNER-ASSIGNMENT-AND-DRILL-PLAN-001`

## Rationale

This packet captures runbook minimums, but it does not assign real environment owners or prove the minimums through tabletop or control-plane drills. Before any public exposure can be reconsidered, operators need named owners and drill evidence for credential revocation, provider spend stop, dashboard disablement, data-disclosure evidence handling, and rollback communication.

## Minimum scope for the next lane

- Assign incident commander, rollback owner, communications owner, evidence custodian, and security/privacy owner roles for the target environment.
- Define contact paths and escalation timing.
- Plan no-provider, no-credential tabletop drills for leaked key, provider spend, dashboard exposure, and data disclosure scenarios.
- Define the evidence store and redaction review process.
- Keep public exposure, provider calls, deployments, and readiness claims out of scope.

## Relationship to DEF-002 lanes

This recommendation does not replace the DEF-002-local remediation sequence. Default credential hardening, CORS hardening, `/v1/solve` auth/tenancy, data classification, and supply-chain gaps remain required or decision-bound before public exposure.
