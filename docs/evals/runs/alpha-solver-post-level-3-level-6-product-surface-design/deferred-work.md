# Deferred Work

The following work is deferred and not started by this packet:

- `/v1/solve` implementation, routing, request handling, response handling, or tests;
- dashboard implementation, routes, UI, assets, navigation, or tests;
- provider adapter changes;
- provider fallback or hosted fallback design beyond the selected next lane marker;
- billing, quota, account, metering, or pricing work;
- MVP or production readiness work;
- benchmark execution;
- model inference or Ollama execution;
- output scoring or reviewer scoring execution;
- external ledger updates;
- evidence promotion.

## Why Level 7 provider orchestration design is deferred

Level 7 provider orchestration design depends on accepted Level 6 boundaries for product-surface exposure, operator controls, observability, stop conditions, and claims. Provider orchestration could affect hosted calls, fallback behavior, cost, provenance, and safety. Those topics must remain deferred until this Level 6 packet is accepted, so Level 7 can inherit a clear product-surface boundary instead of inventing one.
