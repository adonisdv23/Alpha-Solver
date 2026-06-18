# Route Panel Review Rubric

This rubric classifies display understandability, not model or tool quality.

| Rating | Meaning | Examples |
|---|---|---|
| Clear | A careful operator can identify the field and boundary without inference. | Field labels separate preview metadata from execution results. |
| Needs clarification | The field is present, but labels or grouping could cause confusion. | Warnings are present but visually buried. |
| Unsafe / blocking | The panel could reasonably be read as execution, quality proof, readiness proof, or authorization to act. | Tool preview appears to be a completed tool run. |

Required rubric dimensions:

- Visibility of recommended mode and recommended model.
- Visibility of backend, cost, latency, context, privacy tier, smoke eligibility, and no-call evidence.
- Visibility of catalog-not-quality-evidence caveat.
- Readability of grouped reasons, grouped warnings, fallback candidates, and tool preview.
- Visibility of tool execution authorization status.
- Fail-closed display when no route is eligible.
- Evidence-boundary language and clear separation between preview and execution.
