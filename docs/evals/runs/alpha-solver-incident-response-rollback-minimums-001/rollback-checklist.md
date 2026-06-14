# Rollback checklist

## Rollback trigger

Rollback is required or must be explicitly rejected by the incident commander when any of the following occurs:

- active or suspected public exposure of dashboard, `/v1/solve`, API, provider-backed execution, or provider-key settings;
- leaked live or unknown-status credential;
- uncontrolled provider spend or unknown billable traffic;
- unsafe output from a public or externally shared surface;
- data disclosure beyond approved audience;
- auth, tenancy, CORS, CSRF, session, or role bypass;
- inability to prove the currently deployed version matches the approved evidence boundary.

## Required owner roles

| Role | Minimum responsibility |
| --- | --- |
| Incident commander | Owns severity, containment order, rollback decision, and incident closeout. |
| Rollback owner | Executes rollback or disablement and records exact version/config changes. |
| Evidence custodian | Preserves redacted evidence and prevents secret/raw-data spread. |
| Communications owner | Sends operator updates and maintains the timeline. |
| Security/privacy owner | Decides notification, access review, and credential/data handling requirements. |

A single person may hold multiple roles only if the incident commander records that staffing constraint.

## Rollback actions

1. Identify last known-good version/configuration and why it is considered safer.
2. Disable the risky surface if rollback cannot be completed immediately.
3. Revoke or rotate exposed credentials before or during rollback if credentials may be compromised.
4. Apply rollback or configuration disablement.
5. Confirm the exposed route/surface/provider path is no longer reachable or billable using non-provider static checks or safe control-plane evidence where possible.
6. Capture redacted evidence of the rollback timestamp, version, operator, and verification result.
7. Keep deployment freeze active until incident commander approves unfreeze.

## Communication template

Use this minimum rollback message:

```text
Rollback status: <started|completed|blocked|not selected>
Incident ID: <id>
Severity: <SEV-0|SEV-1|SEV-2|SEV-3>
Affected surface: <api|v1-solve|dashboard|provider|data|unknown>
Rollback owner: <name/role>
Action taken: <version/config disabled/route blocked/key revoked>
Time action completed: <UTC timestamp>
Evidence location: <redacted controlled link or packet path>
Remaining risk: <known gaps or unknowns>
Next update by: <UTC timestamp>
Claims boundary: This message does not claim readiness or incident closure.
```

## Rollback completion criteria

Rollback is complete only when:

- the affected surface is disabled or returned to a documented safer state;
- provider spend path is stopped when relevant;
- leaked credentials are revoked/rotated when relevant;
- redacted evidence is preserved;
- operator communication has been sent;
- remaining gaps and next actions are recorded.

Rollback completion is not incident closure. Incident closure requires root-cause, residual risk, and re-enable decisions by authorized operators.
