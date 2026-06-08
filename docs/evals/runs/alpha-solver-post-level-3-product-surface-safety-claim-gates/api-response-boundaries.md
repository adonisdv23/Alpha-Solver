# API Response Boundaries

## API response limit

Future API responses must avoid promotional, comparative, readiness, and unsupported quality language. This packet does not implement API response copy and does not authorize `/v1/solve` exposure or any other API exposure.

## Prohibited API response language

Future API responses must not state or imply:

- the answer is validated, correct, reliable, or production-ready;
- the solver outperforms another solver, model, baseline, or workflow;
- a benchmark has passed unless a separately accepted benchmark lane supports that exact response text;
- hosted providers, provider fallback, billing, dashboards, or `/v1/solve` are ready for users;
- local evidence has been promoted to public product evidence.

## Required API response qualifiers

If a later authorized lane permits API response copy, response text must be bounded to the exact runtime, route, environment, and evidence state. It must preserve non-generalization language when evidence is local, internal, experimental, or limited.

## API stop rule

If an API response would imply a blocked claim or require exposing `/v1/solve` before separate authorization, the future lane must stop.
