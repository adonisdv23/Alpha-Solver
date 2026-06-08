# Static test overview

The future static test scaffold should be local-only and deterministic. It should inspect repository text, proposed schemas, and inert fixtures without executing Self Operator, models, providers, external APIs, browsers, deployments, billing, dashboards, or `/v1/solve`.

The scaffold should fail closed when a prohibited surface appears in Self Operator first-code changes. It should emit stable finding identifiers from `finding-id-registry.md`.
