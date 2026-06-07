# Risk Labels

Risk labels are non-scoring review aids for future design planning. They do not rank tasks, score outputs, establish pass/fail criteria, or claim quality.

## Boundary risk labels

- `CLAIM_BOUNDARY_RISK`: The task may invite unsupported quality, readiness, benchmark, production, or superiority claims.
- `EVIDENCE_PROMOTION_RISK`: The task may treat closed Level 2 or Level 3 evidence as broader evidence than accepted.
- `SELECTED_NEXT_STATE_RISK`: The task may create contradictory selected-next, no-further-lanes, or blocker fallback state.

## Execution risk labels

- `MODEL_EXECUTION_RISK`: The task might be confused with running local model inference, Ollama, hosted providers, or benchmarks.
- `PRODUCT_SURFACE_RISK`: The task might imply dashboard, `/v1/solve`, provider fallback, billing, MVP, or production surface work.
- `FROZEN_TASK_SET_RISK`: The task might be mistaken for a frozen task set or accepted benchmark suite.

## Artifact risk labels

- `SOURCE_ARTIFACT_RISK`: The task may touch preserved source artifacts or closed packets.
- `PATH_SCOPE_RISK`: The task may drift outside approved docs-only paths.
- `TRACEABILITY_RISK`: The task may lack source references, artifact expectations, non-actions, or check records.
