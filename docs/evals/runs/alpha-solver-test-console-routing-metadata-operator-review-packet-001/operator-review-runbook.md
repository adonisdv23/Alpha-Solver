# Operator Review Runbook

## Purpose

Guide a human operator through manual inspection of the local-only console route-preview panel for a small representative task set. The operator, not Codex, decides whether the display is understandable and evidence-boundary safe.

## Preconditions

- Review the source-of-truth baseline: `OPERATOR_REVIEW_REQUIRED_AFTER_TEST_CONSOLE_ROUTING_METADATA_DISPLAY_001`.
- Use only local operator-controlled console review.
- Do not treat any catalog entry, route preview, fallback, warning, or tool recommendation as quality evidence.

## Manual steps

1. Open the local console only if authorized by the operator environment.
2. For each task in `review-task-set.md`, inspect the route-preview panel before any smoke execution.
3. Complete `operator-review-checklist.md` for each task.
4. Apply `route-panel-review-rubric.md` to classify readability and boundary-language issues.
5. Record observations in a copy of `manual-result-log-template.md`.
6. Record defects or caveats using `defects-and-caveats.md`.
7. Stop immediately if the panel appears to imply execution occurred, quality was proven, readiness was proven, or provider/local-model/tool superiority was established.

## Stop conditions

Stop the review and record the reason if any of these occur:

- The preview cannot be distinguished from execution.
- Route metadata is missing for recommended mode or recommended model.
- Backend, cost, latency, context, privacy tier, smoke eligibility, no-call evidence, or catalog-not-quality-evidence language is absent or misleading.
- A fail-closed/no-eligible-route case does not present a safe preview state.
- The panel encourages provider, local-model, tool, or web execution beyond explicit operator authorization.
