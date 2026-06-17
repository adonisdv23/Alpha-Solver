# Task scope

Authorized task set for later output collection: the static 12-card routed-vs-plain pilot task set from `docs/evals/runs/alpha-solver-routed-vs-plain-pilot-packet-001/task-set.md`.

## In scope later, with separate execution authorization or operator-provided outputs

- One plain baseline output per task.
- One routed Alpha output per task.
- Route metadata capture for the routed Alpha side.
- Blinded packaging for later scoring authorization review.

## Out of scope

- New task generation.
- Task substitution.
- Scoring or ranking.
- Unblinding.
- Raw prior-output inspection.
- Runtime, router, provider, local-model, tool, API, dependency, or Google Sheets changes.

## Evidence boundaries

This authorization packet is docs-only. It does not execute pilot tasks, call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha-routed outputs, generate plain baseline outputs, score outputs, unblind outputs, inspect raw prior outputs, mutate Google Sheets, add dependencies, expose `/v1/solve`, or make readiness, benchmark-success, production/public-readiness, provider-quality, local-model-quality, tool-quality, or Alpha-superiority claims.
