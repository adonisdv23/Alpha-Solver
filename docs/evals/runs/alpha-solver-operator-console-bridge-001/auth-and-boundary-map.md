# Auth and Boundary Map

## Current observed boundary

| Surface | Current state | Bridge implication |
| --- | --- | --- |
| `POST /v1/solve` | Active API route with API-key validation and rate limiting; classified unsafe to expose publicly by existing evidence. | Do not expose or reuse as public sidecar API without a separate auth/tenancy decision. |
| Dashboard preview | Mounted only when non-default dashboard password and explicit secret are configured; still classified unsafe to expose publicly. | Do not use dashboard session as bridge auth. |
| Auth middleware | JWT/API-key components exist but are not proven as the bundled `/v1/solve` public boundary. | Future bridge must select one local operator auth model and test negative paths. |
| Tenant middleware | Component exists; bundled `/v1/solve` tenant enforcement is not proven. | Future bridge must either remain single-operator local-only or add mandatory tenant proof before any billable/provider-backed work. |
| CORS | Public gate records CORS as a no-go blocker. | Do not add browser-accessible CORS for a sidecar until the sidecar pattern and origin model are approved. |
| Provider-cost controls | Hosted provider path is explicit opt-in and cost-capped, but public traffic cost caps are not proven. | Future bridge must default hosted providers off and must not call hosted providers in this lane. |
| Evidence API router | Router exists but is unsafe if mounted unauthenticated. | Evidence capture should be local artifact writing or explicitly authenticated bridge metadata, not unauthenticated evidence routes. |

## Required future bridge boundary

- Bind only to `127.0.0.1` or equivalent loopback.
- Require explicit local operator enablement.
- Use synthetic/local auth for tests; never capture real secrets.
- Preserve Alpha Solver routing and SAFE-OUT by entering through Alpha Solver-controlled seams.
- Reject direct sidecar model calls as Alpha Solver evidence.
- Deny hosted-provider execution by default.
- Keep tenant/cost metadata explicit and non-public.
