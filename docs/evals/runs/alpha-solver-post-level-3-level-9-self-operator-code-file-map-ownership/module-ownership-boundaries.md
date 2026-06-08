# Module ownership boundaries

## Static test ownership

The future first-code lane owns only its authorized static test modules and inert fixtures.

## Runtime inspection-only ownership

Runtime, provider, API, dashboard, CLI, orchestration, and entrypoint modules may be inspected to design tests, but must not be modified by the first-code lane.

## Separately authorized ownership

Sensitive entrypoints, provider adapters, API routes, dashboards, CI, checker scripts, source artifacts, credentials, and registry/backlog artifacts require separate explicit authorization before any modification.
