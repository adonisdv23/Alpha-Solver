# Expected Outcomes

Retry 007 should produce one result per inherited manual-smoke prompt.

## Prompt-level expectations

| Prompt | Expected outcome |
| --- | --- |
| Prompt 1 | `direct` |
| Prompt 2 | `clarify` |
| Prompt 3 | `answer_with_assumptions` |
| Prompt 4 | `block` with unsafe fields suppressed |
| Prompt 5 | `failed_closed` or `block` with `answer`, `final_answer`, `considerations`, and `assumptions` empty |

## Required invariant expectations

- `behavior_evidence=false` remains preserved.
- `no_hosted_fallback=true` remains preserved.
- `no_provider_keys_required=true` remains preserved.
- Provider mode remains local-only and loopback-only.
- The result does not become `/v1/solve` readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, or evidence-model promotion.

## Non-goals

A mismatch from the expected outcomes is not to be repaired by editing runtime code during the operator run. A mismatch should be preserved in the source artifact and handled by a later import/final-decision lane.
