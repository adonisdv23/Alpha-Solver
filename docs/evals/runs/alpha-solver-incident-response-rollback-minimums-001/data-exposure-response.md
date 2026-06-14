# Data exposure, unsafe output, public abuse, and dashboard exposure response

## Trigger conditions

Use this response for suspected or confirmed disclosure of prompts, completions, provider payloads, tenant data, audit events, telemetry, evidence artifacts, dashboard content, provider-key settings, unsafe output, CORS/browser abuse, or public access to an unintended API/dashboard route.

## Immediate stop actions

1. Declare severity using `incident-classes.md`; default to SEV-0 for active public disclosure or reachable dashboard/provider-key settings exposure.
2. Remove public access first:
   - disable ingress, route, deployment, dashboard mount, or public DNS path;
   - disable affected API key/session/JWT path;
   - block abusive principals, tenants, IPs, origins, or user agents where available;
   - disable provider-backed execution if the route can spend money or transmit prompt data.
3. Freeze risky deployments and config changes except incident containment.
4. Preserve redacted evidence: route, method, status, request ID, tenant/principal class, timestamps, deployment version, and minimal description of disclosed data class.
5. Do not copy raw prompt, completion, tenant, provider payload, or credential content into public tickets, PRs, or this packet.

## Unsafe output minimums

For unsafe output incidents, record:

- prompt category, not raw prompt, unless restricted disclosure handling is approved;
- output risk class, not raw output, unless restricted disclosure handling is approved;
- whether SAFE-OUT should have been returned;
- route/model/provider configuration in redacted form;
- whether the output was public, internal, or operator-only;
- containment action and rollback decision.

## Dashboard exposure minimums

For dashboard exposure incidents, record:

- whether default password, missing explicit signing secret, CSRF, session, role, route inventory, or provider-key settings were involved;
- whether provider keys or settings pages were reachable;
- whether sessions, signing secrets, or dashboard passwords were rotated;
- whether the dashboard was disabled at the app, ingress, or deployment layer;
- whether access logs show external access.

## Data disclosure minimums

For data disclosure incidents, record:

- data class and owner, using the data-classification source of truth once reconciled;
- affected tenant/operator population or the reason it is unknown;
- exposure channel and access group;
- containment and artifact removal timestamps;
- notification/legal/privacy owner decision, if applicable.

## Public abuse minimums

For abuse incidents, record:

- abuse vector and affected surface;
- authentication state of abusive traffic;
- rate-limit, quota, CORS, and tenant-control status;
- provider-spend risk and whether provider-spend response was invoked;
- blocks applied and monitoring follow-up.
