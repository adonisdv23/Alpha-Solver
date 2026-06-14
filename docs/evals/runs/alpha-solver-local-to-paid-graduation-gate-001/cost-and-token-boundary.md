# Cost and token boundary

## Required boundary before any paid smoke

A paid hosted-provider smoke must define all limits before execution:

- Maximum number of runs.
- Maximum number of provider requests.
- Maximum input tokens.
- Maximum output tokens.
- Maximum total tokens.
- Maximum estimated provider cost.
- A local kill/stop procedure if accounting is unclear.
- A rule that any retry requires a new authorization unless explicitly included in the max run count.

## Current boundary assessment

Provider cost caps and stop controls have partial fake-provider evidence only. They do not prove exact provider billing accuracy, exact hosted-provider accounting, or safety under public traffic.

The blocked `local-openai-token-smoke-capture-retry-002` authorization did not supply explicit cost cap, token cap, model, project boundary, max run count, or exact synthetic fixture in the execution prompt. Therefore, this gate cannot authorize a paid call.

## Minimum first-smoke recommendation

If a later authorization-refresh lane is completed, the first paid action should be a single synthetic connectivity/no-echo smoke with the smallest practical token budget. It must stop after one response or first error, whichever occurs first, unless the refreshed authorization explicitly permits a bounded retry.
