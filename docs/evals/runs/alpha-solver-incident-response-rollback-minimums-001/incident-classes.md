# Incident classes and severity levels

## Severity levels

| Severity | Definition | Minimum escalation | Minimum operator action |
| --- | --- | --- | --- |
| SEV-0 | Confirmed or strongly suspected active public harm, active data disclosure, active credential abuse, uncontrolled provider spend, or externally exposed dashboard/API with unsafe access. | Immediate incident commander plus rollback owner. Page security, infra, and product operator. | Stop exposure or provider spend first, preserve evidence second, communicate status third. |
| SEV-1 | Credible high-risk incident with limited scope or contained blast radius: leaked non-production key, unsafe output reported by a trusted operator, abuse pattern not yet causing runaway spend, or dashboard exposure blocked by auth but misconfigured. | Incident commander and evidence custodian within the same response window. | Contain affected surface, rotate or revoke suspect credentials, capture redacted evidence, decide rollback. |
| SEV-2 | Potential incident, near miss, suspicious telemetry, failed control, or redaction finding without confirmed external disclosure or spend. | Responsible operator plus evidence custodian. | Freeze risky changes, collect redacted evidence, decide whether to escalate. |
| SEV-3 | Documentation gap, drill finding, incomplete owner assignment, or stale runbook that does not indicate active compromise. | Lane owner or docs operator. | Update runbook/evidence; no runtime action unless new facts raise severity. |

If severity is uncertain, classify one level higher until the incident commander records a reasoned downgrade.

## Incident classes

| Class | Examples | Default severity floor | Immediate stop priority |
| --- | --- | --- | --- |
| Leaked credentials | Provider key in logs, screenshots, issue comments, chat, artifact, dashboard response, env dump, or repository content. | SEV-1; SEV-0 if key may be live or abused. | Revoke/rotate key and invalidate sessions/tokens before broader investigation. |
| Runaway provider spend | Unexpected provider billing spike, repeated provider calls, quota exhaustion, abuse-driven prompts, tenant overage, or unknown caller generating costs. | SEV-0 if spend is active or uncapped; otherwise SEV-1. | Disable provider path, revoke provider key, apply provider-side cap, block caller. |
| Unsafe output | Output that could enable harm, disclose private data, bypass SAFE-OUT expectations, or materially mislead an operator. | SEV-1; SEV-0 if public or actively harmful. | Stop the affected surface and preserve minimal redacted prompt/output metadata. |
| Public abuse | Credential stuffing, scraping, prompt flooding, spam, automated `/v1/solve` traffic, tenant abuse, or CORS/browser abuse. | SEV-1; SEV-0 if public traffic is active and controls are insufficient. | Block traffic, disable exposed route, revoke affected sessions/API keys, freeze rollout. |
| Dashboard exposure | Dashboard reachable publicly, default password usable, settings/provider-key route exposed, CSRF/session failure, or role bypass. | SEV-0 when provider keys/settings are reachable; otherwise SEV-1. | Disable dashboard mount or ingress route immediately and rotate dashboard signing secret if session compromise is possible. |
| Data disclosure | Prompt, provider payload, tenant data, audit artifact, trace/span, evidence packet, or log content disclosed beyond policy. | SEV-0 if external or active; SEV-1 if internal but unauthorized. | Stop sharing path, restrict artifact access, preserve redacted evidence, start disclosure assessment. |
| Rollback failure | Rollback cannot be performed, previous known-good version unavailable, or rollback increases exposure. | Same severity as triggering incident; minimum SEV-1. | Freeze deployment and escalate to rollback owner plus incident commander. |

## Cross-cutting escalation rules

- Any incident involving real or suspected live credentials requires credential-leak response minimums.
- Any incident involving provider-backed runtime calls requires provider-spend response minimums, even if the first symptom is not billing.
- Any incident involving public API, dashboard, or `/v1/solve` exposure inherits the public exposure gate no-go posture until a later operator decision changes it.
- Any incident evidence containing prompts, keys, tokens, tenant data, or provider payloads must follow the evidence-boundary redaction rules before being attached to docs or tickets.
