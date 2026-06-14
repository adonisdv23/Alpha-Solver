# Auth and Boundary Map

## Current observed boundary

| Surface | Current state | Bridge implication |
| --- | --- | --- |
| Sidecar feasibility packet | Selects `UI sidecar -> Alpha Solver controlled endpoint -> Alpha Solver router/policy/evidence layer -> local or hosted model backend`. | Bridge must use only an Alpha Solver controlled endpoint or CLI seam after the security/API-shape gate defines request mapping and response-envelope mapping. |
| `POST /v1/solve` | Active API route with API-key validation and rate limiting; classified unsafe to expose publicly by existing evidence. | Do not expose or reuse as a sidecar API without a separate API-shape, auth, tenancy, CORS/CSRF, and cost-control decision. |
| Dashboard preview | Mounted only when non-default dashboard password and explicit secret are configured; still classified unsafe to expose publicly. | Do not use dashboard session state as bridge auth. |
| Auth middleware | JWT/API-key components exist but are not proven as the bundled `/v1/solve` public or sidecar boundary. | Future bridge must select one local operator auth model and test negative paths. |
| Tenant middleware | Component exists; bundled `/v1/solve` tenant enforcement is not proven. | Future bridge must either remain single-operator local-only or add mandatory tenant proof before any billable/provider-backed work. |
| CORS | Public gate records CORS as a no-go blocker. | Do not add browser-accessible CORS for a sidecar until the sidecar security gate approves the origin model and CSRF/session constraints. |
| Provider-cost controls | Hosted provider path is explicit opt-in and cost-capped, but public or sidecar traffic cost caps are not proven. | Future bridge must default hosted providers off and must not call hosted providers in this lane. |
| Telemetry/accounting | Provider telemetry/accounting hooks exist for provider paths, and request IDs are emitted by the service. | Future bridge must preserve request IDs and telemetry/audit identity without making UI chat history authoritative evidence. |
| Evidence API router | Router exists but is unsafe if mounted unauthenticated. | Evidence capture should be local artifact writing or explicitly authenticated bridge metadata, not unauthenticated evidence routes. |

## Required future bridge boundary

- Bind only to `127.0.0.1` or equivalent loopback unless a later gate explicitly approves another model.
- Require explicit local operator enablement.
- Use synthetic/local auth for tests; never capture real secrets or credentials.
- Preserve Alpha Solver routing and SAFE-OUT by entering through Alpha Solver-controlled seams.
- Reject direct sidecar model calls as Alpha Solver evidence.
- Deny hosted-provider execution by default.
- Preserve tenant/cost/telemetry metadata as explicit, non-public bridge fields.
- Keep uploads, RAG, memory, tools, web search, and private-file ingestion disabled unless separately approved.
