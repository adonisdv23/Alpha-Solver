# Provider and Fallback Confusion Risks

## Provider confusion risks

- Operators may not know whether a future run uses local-only execution, a hosted provider, a fallback provider, a mock, a replay artifact, or no model inference.
- Provider names, model names, and environment variables may be logged or displayed inconsistently.
- A successful local run may be mistaken for hosted provider readiness, and a successful hosted call may be mistaken for general product readiness.

## Fallback confusion risks

- Fallback may silently change model behavior, privacy exposure, cost exposure, latency, or output quality.
- Failure handling may hide provider errors and prevent accurate incident review.
- Budget guard, rate-limit, and data-residency expectations may differ between primary and fallback paths.
- A future UI may display output without clearly labeling provider, fallback, replay, mock, or local-only status.

## Required future clarity

- Any future implementation must make execution mode, provider/fallback status, billing exposure, and data-handling implications explicit.
- Any future evidence must distinguish local, hosted, fallback, mock, replay, and no-inference artifacts.
- Any future stop condition must block silent fallback or unlabeled provider behavior.

## Boundary

This packet does not call providers, configure providers, add fallback, run models, run benchmarks, perform billing work, expose routes, expose dashboards, implement mitigations, or promote evidence.
