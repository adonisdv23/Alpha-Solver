# Selected next lane

Selected next lane: `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002-AUTHORIZATION-REFRESH`

## Scope

This selected lane is documentation/authorization only. It should collect the exact provider, model, project/account boundary, synthetic fixture, max run count, request cap, token cap, cost cap, data-sharing acknowledgement, redaction confirmation, and stop-condition approval for a possible subsequent tiny synthetic smoke.

## Not selected

- Paid hosted-provider smoke execution — not selected because authorization fields are missing.
- Value experiment execution — not selected because the no-echo precondition is failing and paid-provider authorization is missing.
- Public exposure, dashboard exposure, or `/v1/solve` exposure — not selected because the public exposure gate is no-go.
- Google Sheets/backlog update lane — not selected and not authorized.
