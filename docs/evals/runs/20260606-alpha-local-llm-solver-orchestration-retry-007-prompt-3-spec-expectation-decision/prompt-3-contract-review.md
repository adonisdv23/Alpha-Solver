# Prompt 3 contract review

## Code reviewed

The current runner applies a shape-specific branch for `bounded_local_python_cli_startup_plan` when Pass 1 selects `block` or `clarify`.

That branch routes to `answer_with_assumptions` only when `_assumption_gate_failed_reason_codes(gate)` returns no reasons. When any assumption-gate reason exists, the branch records `blocked_assumption_gate_failed`, keeps or restores a non-answering mode, suppresses model fields, and does not call Pass 2.

The current assumption gate emits `missing_information_too_broad` when parsed `missing_information` contains more than two items.

## Tests reviewed

The existing focused tests encode both sides of the bounded startup-plan shape:

- a bounded startup-plan prompt may route from a vague-risk `block` or `clarify` Pass 1 result to `answer_with_assumptions` when confidence, considerations, assumptions, and missing information remain inside the assumption gate;
- the same shape must not answer with assumptions when an assumption-gate failure reason is present, including `missing_information_too_broad`.

## Spec reviewed

The orchestration spec requires the local runner gate to choose exactly one mode from `direct`, `clarify`, `answer_with_assumptions`, or `block`.

The spec also requires the gate to be based on bounded local confidence and missing-information checks, and it instructs the runner to prefer fail-closed, `clarify`, or `block` when confidence or parse safety cannot be established rather than presenting unsupported output as successful behavior.

The runtime spec's fail-closed contract also preserves the broader safety direction: failed or unsafe local output must not be converted into successful behavior, and no hosted fallback is allowed from local LLM mode.

## Prompt 3 decision question

The question for this lane is whether Prompt 3 should still require `answer_with_assumptions` when the deterministic assumption gate has already emitted `missing_information_too_broad`.

The selected answer is no. Once `missing_information_too_broad` fires, Prompt 3 should not require `answer_with_assumptions`; `clarify` is acceptable for that condition.
