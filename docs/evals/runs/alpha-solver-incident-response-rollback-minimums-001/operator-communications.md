# Operator communications

## Communication rules

- Use UTC timestamps.
- State facts, unknowns, owner, next update time, and claims boundary.
- Do not include secrets, raw prompts, raw completions, raw provider payloads, tenant data, cookies, JWTs, dashboard session values, or unrestricted screenshots.
- Mark every public-exposure or provider-backed incident update as no-readiness evidence unless a later operator approval lane says otherwise.

## Incident start template

```text
Incident declared: <UTC timestamp>
Incident ID: <id>
Severity: <SEV-0|SEV-1|SEV-2|SEV-3>
Class: <credential leak|provider spend|unsafe output|public abuse|dashboard exposure|data disclosure|rollback failure|unknown>
Incident commander: <name/role>
Known affected surface: <surface or unknown>
Immediate containment underway: <yes/no/details>
Provider spend risk: <yes/no/unknown>
Credential risk: <yes/no/unknown>
Evidence custodian: <name/role>
Next update by: <UTC timestamp>
Claims boundary: This is an incident notice, not a readiness claim.
```

## Status update template

```text
Incident update: <UTC timestamp>
Incident ID: <id>
Severity: <current severity>
Containment status: <not started|in progress|contained|blocked>
Actions completed: <redacted bullets>
Known impact: <redacted data classes/surfaces, not raw data>
Unknowns: <bullets>
Rollback status: <not evaluated|selected|in progress|complete|blocked|not selected with rationale>
Next decision needed: <operator/security/privacy/infra>
Next update by: <UTC timestamp>
Claims boundary: No public, production, runtime, provider, dashboard, or /v1/solve readiness is claimed.
```

## Closeout template

```text
Incident closeout candidate: <UTC timestamp>
Incident ID: <id>
Final severity: <SEV-0|SEV-1|SEV-2|SEV-3>
Containment completed: <UTC timestamp>
Rollback/recovery decision: <summary>
Credentials rotated/revoked: <yes/no/not applicable, no secret values>
Provider spend stopped/capped: <yes/no/not applicable>
Data disclosure decision owner: <name/role/not applicable>
Evidence packet: <controlled link/path>
Residual risks: <bullets>
Required follow-up lanes: <bullets>
Forbidden claims: This closeout does not claim public readiness, production readiness, runtime readiness, provider readiness, dashboard readiness, /v1/solve readiness, DEF-002 closure, or security/privacy completion.
```

## External notification placeholder

External user, provider, legal, or regulator notification is outside this docs-only lane. If notification may be required, the incident commander must assign a security/privacy owner and avoid unapproved disclosure content in repository artifacts.
