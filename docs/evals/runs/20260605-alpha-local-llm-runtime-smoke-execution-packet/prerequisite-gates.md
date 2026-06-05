# Prerequisite Gates

Lane ID: `ALPHA-LOCAL-LLM-RUNTIME-SMOKE-EXECUTION-PACKET-001`

## Required before future execution

The future operator must confirm all prerequisites before executing smoke:

1. PR #315 is squashed, merged, closed, and recorded in GS.
2. PR #316 is squashed, merged, closed, and recorded in GS.
3. PR #318 is squashed, merged, closed, and recorded in GS.
4. PR #319 is squashed, merged, closed, and recorded in GS.
5. Canonical implementation spec exists at `.specs/LOCAL-LLM-RUNTIME-INTEGRATION-001.md`.
6. The merged implementation surface exists in `alpha/local_llm/provider_adapter.py`.
7. `scripts/check_env.py` recognizes `MODEL_PROVIDER=local_llm` and the required local runtime fields.
8. `service/config/validators.py` recognizes `local_llm` as a user-facing provider value for configuration validation.
9. `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-REVIEW-GATE-001` explicitly authorizes runtime smoke.

## Hard block

Runtime smoke remains blocked unless the review gate explicitly approves smoke. Do not infer authorization from implementation merge, docs merge, operator availability, or local service availability.

## Gate record template

```text
Review gate lane:
Review gate artifact path:
Review gate status:
Does the gate explicitly authorize runtime smoke? yes/no
Gate reviewer or approver:
Gate decision timestamp:
Notes:
```

If the answer is not exactly `yes`, stop.
