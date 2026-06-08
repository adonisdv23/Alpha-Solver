# Capability Labels

## Capability label goals

Capability labels should describe declared provider abilities without claiming runtime readiness. They are planning metadata for Level 7 provider orchestration design only.

## Recommended capability labels

| Label | Meaning |
| --- | --- |
| `text_generation` | Provider is intended to produce natural-language output. |
| `structured_output_candidate` | Provider may support structured output in a future authorized implementation. |
| `tool_use_candidate` | Provider may support tool-use patterns, but this packet does not authorize tool use. |
| `local_runtime_candidate` | Provider may run through a local runtime boundary. |
| `hosted_api_candidate` | Provider may require a hosted API boundary. |
| `streaming_candidate` | Provider may support streamed output in future design. |
| `batch_candidate` | Provider may support batch execution in future design. |
| `eval_only_candidate` | Provider may be limited to evaluation contexts if later authorized. |
| `operator_review_required` | Operator review is required before use. |
| `evidence_restricted` | Output must not be promoted beyond its accepted evidence boundary. |

## Capability constraints

- Capability labels are not proof that a provider works.
- Capability labels are not permission to call providers.
- Capability labels do not authorize routing, fallback, hosted calls, local model execution, benchmarks, billing work, API exposure, dashboard exposure, or evidence promotion.
- Capability labels must be auditable and tied to provenance requirements.

## Unknown capabilities

Unknown, missing, stale, or contradictory capability labels should fail closed. A future registry should treat unknown capability data as disabled/default-off until Level 7 or a later authorized lane resolves it.
