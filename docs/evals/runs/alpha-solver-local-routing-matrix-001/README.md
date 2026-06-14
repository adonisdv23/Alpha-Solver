# ALPHA-SOLVER-LOCAL-ROUTING-MATRIX-001

Verdict: `LOCAL_ROUTING_MATRIX_CAPTURED_NOT_EXECUTED`

## TLDR

This packet captures a documentation-only local routing matrix for Alpha Solver task categories, candidate local model roles, evidence requirements, stop conditions, and escalation triggers. It treats routing as explainability: each proposed route must explain why it was selected, why plausible alternatives were rejected, what evidence would be needed, and what must not be claimed.

No local model quality evaluation was run. No hosted provider was called. No API token was used. No private data was sent to any model. This packet is not evidence that local routing works.

## Source context inspected

- `alpha_solver_portable.py` portable pipeline, route explanation, SAFE-OUT, and SolverEnvelope expectations.
- `alpha/local_llm/provider_adapter.py` default-off local adapter, loopback endpoint validation, hosted-key fail-closed behavior, and non-evidence labels.
- `alpha/local_llm/multi_model_smoke_harness.py` local-only smoke statuses and `behavior_evidence=false` result boundary.
- `docs/evals/runs/alpha-solver-local-model-catalog-001/` model family catalog and non-claims.
- `docs/evals/runs/alpha-solver-local-multi-model-smoke-harness-001/` fake-transport-only smoke harness packet.
- `docs/VALUE_EXPERIMENT_PROTOCOL.md` and `docs/evals/runs/alpha-solver-value-experiment-protocol-001/` protocol-only value evidence boundary.
- `docs/ENTRYPOINTS.md` runtime entrypoint map.

## Packet files

- [task-category-map.md](task-category-map.md)
- [model-role-map.md](model-role-map.md)
- [routing-matrix.md](routing-matrix.md)
- [synthetic-routing-task-bank-template.jsonl](synthetic-routing-task-bank-template.jsonl)
- [routing-evidence-plan.md](routing-evidence-plan.md)
- [residual-risks.md](residual-risks.md)
- [selected-next-lane.md](selected-next-lane.md)
- [evidence-boundary.md](evidence-boundary.md)
- [non-actions.md](non-actions.md)

## Allowed verdicts for future use

- `LOCAL_ROUTING_MATRIX_CAPTURED_NOT_EXECUTED`
- `LOCAL_ROUTING_MATRIX_BLOCKED_MODEL_SMOKE_MISSING`
- `STOP_INCONCLUSIVE`
