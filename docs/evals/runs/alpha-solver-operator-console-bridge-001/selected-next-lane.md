# Selected Next Lane

Selected next lane: `ALPHA-SOLVER-OPERATOR-UI-SIDECAR-SECURITY-GATES-001`.

## Rationale

The sidecar feasibility packet now exists, and PR #549 has merged an API-shape compatibility gate into `main`. The bridge must not proceed until the sidecar security/API-shape gate decides the Alpha Solver controlled endpoint or CLI seam, request mapping, response-envelope mapping, authn/authz, tenancy, CORS/CSRF, provider lockdown, cost controls, telemetry/audit identity, retention, replay, and evidence-envelope rendering contract.

## Future implementation lane candidate

`ALPHA-SOLVER-OPERATOR-CONSOLE-BRIDGE-LOCAL-ONLY-IMPLEMENTATION-001`

Required scope after the gate passes:

- local-only;
- default-off;
- authenticated;
- no hosted providers;
- no direct model bypass;
- Alpha Solver controlled endpoint or CLI bridge only;
- Alpha Solver envelope and SAFE-OUT preserved;
- authn/authz, tenancy, CORS/CSRF, cost, telemetry/audit, retention, replay, and evidence-envelope boundaries tested;
- tests for auth denial, loopback-only bind, provider-disabled behavior, request mapping, response-envelope mapping, and non-claim evidence labels.
