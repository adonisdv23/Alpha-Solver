# Provider spend response

## Trigger conditions

Use this response when there is suspected or confirmed provider-cost abuse, provider billing anomaly, unknown provider traffic, unexpected provider enablement, tenant quota bypass, or any public abuse that could call a billable provider.

## Immediate stop actions

1. Declare at least SEV-1; declare SEV-0 if spend is active, uncapped, public, or attributable to unknown callers.
2. Stop billable provider calls by the fastest available operator-controlled mechanism for the environment:
   - disable the provider integration/configuration;
   - remove or revoke the provider key;
   - set provider-side hard budget/cap to zero or the minimum safe value;
   - disable the affected deployment, route, job, tenant, or ingress rule;
   - block abusive caller principals, API keys, IPs, or tenants where known.
3. Freeze deployments and configuration changes except containment changes approved by the incident commander.
4. Preserve billing screenshots, provider dashboard timestamps, request IDs, tenant IDs, deployment versions, and relevant redacted logs. Do not copy real provider keys into evidence.
5. Start an operator update using `operator-communications.md`.

## Minimum evidence to preserve

- Incident start time, detection source, and person declaring the incident.
- Provider name and project/account identifier in redacted form.
- Approximate spend delta, quota impact, and whether the provider-side cap was active.
- Affected route or surface, if known.
- Request IDs, tenant IDs, principal IDs, or IPs only when redacted or policy-approved.
- Exact containment actions and timestamps.

## Do not preserve

- Full provider API keys, dashboard secrets, JWTs, bearer tokens, cookies, session IDs, OAuth client secrets, refresh tokens, or raw environment dumps.
- Raw prompts, completions, provider payloads, or tenant data unless an approved disclosure process requires them in a restricted evidence store.

## Recovery minimums

Provider-backed operation may not resume until an operator records:

- provider key rotation or explicit confirmation that no key was exposed;
- provider-side budget/cap and alert status;
- tenant or principal-level quota and rate-control status;
- abuse source blocked or accepted with documented rationale;
- rollback or forward-fix decision;
- evidence redaction review completed.

This recovery checklist does not authorize public exposure or readiness claims.
