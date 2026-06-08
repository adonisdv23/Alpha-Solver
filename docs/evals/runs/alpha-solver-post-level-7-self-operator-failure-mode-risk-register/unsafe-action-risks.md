# Unsafe Action Risks

## Unsafe action classes

- Runtime behavior changes without a linked implementation contract.
- Provider, fallback, local model, or hosted model calls outside explicit approval.
- Credential reads, writes, printing, screenshots, copying, rotation, or storage.
- Deployment, preview, dashboard, API, route, health, metrics, or public exposure.
- Auto-merge, self-merge, branch-protection changes, force-push, release, or tag creation.
- CI, dependency, environment, billing, budget, observability, replay, SAFE-OUT, routing, MCP, or SolverEnvelope changes outside scope.
- Evidence promotion, ledger updates, readiness claims, or benchmark claims not backed by accepted evidence.

## Stop conditions

- Stop if a command can modify runtime, deploy, call a provider, alter credentials, expose a route, or merge a branch outside the authorized scope.
- Stop if a tool output includes secrets, private URLs, non-redacted artifacts, or unreviewed provider output.
- Stop if the operator must infer permission rather than rely on an explicit lane, spec, or human approval.

## Required future review

Before any Self Operator can execute actions, a future design must classify actions by risk tier, define default-deny behavior, require human approval for sensitive actions, and document deterministic checks for allowed actions.
