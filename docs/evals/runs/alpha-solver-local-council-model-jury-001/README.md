# ALPHA-SOLVER-LOCAL-COUNCIL-MODEL-JURY-001

## TLDR

Verdict: `LOCAL_COUNCIL_MODEL_JURY_DESIGNED_NOT_EXECUTED`.

This packet designs a local-only council/model-jury lane for Alpha Solver routing and disagreement logic. It begins with fake-model templates and capture rules only. It does not call local models, Ollama, hosted providers, `/v1/solve`, dashboard routes, tokens, Google Sheets, or broad evals.

## Purpose

The lane defines how multiple local roles can produce first-pass, critique, safety/boundary, evidence-audit, and final synthesis outputs while treating disagreement as an uncertainty signal rather than a consensus vote.

## Source context reviewed

- `alpha_solver_portable.py` portable SolverEnvelope, SAFE-OUT, routing, and claim-boundary contract.
- `alpha/local_llm/` adapter, orchestration runner, operator CLI, portable contract, and multi-model smoke harness surfaces.
- `service/models/modelset_registry.py` and `service/models/modelset_resolver.py` model-set metadata surfaces.
- Local LLM guardrail/operator packets under `docs/local_llm_solver_orchestration_*`.
- Level 3 local LLM validation design and execution evidence packets under `docs/evals/runs/20260607-local-llm-solver-orchestration-level-3-validation-*`.
- Value experiment protocol and manual discrimination packets under `docs/evals/runs/alpha-solver-value-experiment-protocol-001/` and `docs/evals/runs/alpha-solver-manual-discrimination-value-read-001/`.
- Existing council audit evidence packets under `docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-*`.

## Packet files

- `council-role-map.md` — local council roles and required role outputs.
- `model-assignment-policy.md` — local/fake model assignment policy and family diversity strategy.
- `disagreement-and-synthesis-rules.md` — disagreement taxonomy, escalation triggers, and finalizer limits.
- `fake-model-test-evidence.md` — fake-model templates and non-executed test evidence plan.
- `operator-local-run-template.md` — operator-only local capture template for a future execution lane.
- `residual-risks.md` — risks that remain after design-only work.
- `selected-next-lane.md` — proposed next lane.
- `evidence-boundary.md` — evidence and claim boundaries.
- `non-actions.md` — explicit non-actions.

## Allowed verdicts for this lane

- `LOCAL_COUNCIL_MODEL_JURY_DESIGNED_NOT_EXECUTED`
- `LOCAL_COUNCIL_FAKE_MODEL_HARNESS_CAPTURED`
- `LOCAL_COUNCIL_BLOCKED_LOCAL_MODEL_EVIDENCE_MISSING`
- `STOP_INCONCLUSIVE`

## Current verdict rationale

The packet defines roles, assignment policy, disagreement capture, safe stop conditions, fake-model templates, and operator-local run template. No executable fake harness was added and no local model run was performed, so the strongest supported verdict is design-only.
