# Spec expectation review

## Current spec contract

The solver orchestration spec requires the local runner gate to choose exactly one mode from:

- `direct`
- `clarify`
- `answer_with_assumptions`
- `block`

The spec says the gate must be based on bounded local confidence and missing-information checks. It also says that if confidence or parse safety cannot be established, the runner must prefer fail-closed, `clarify`, or `block` over presenting unsupported output as successful behavior.

## Current implementation contract expressed by tests

The focused tests preserve two relevant expectations for the bounded startup-plan shape:

1. When Pass 1 has bounded assumptions, sufficient confidence, and acceptable missing information, vague risk labels can route to `answer_with_assumptions` with Pass 2 called.
2. When assumption-gate failures are present, including `missing_information_too_broad`, the runner must not route to `answer_with_assumptions` and must not call Pass 2.

## Retry 007 expectation conflict

The retry 007 smoke expectation for Prompt 3 still required `answer_with_assumptions`, but the preserved Pass 1 output triggered `missing_information_too_broad`. Under the current implementation/test contract, that trigger makes `answer_with_assumptions` unavailable.

## Required spec-review question

The next lane should decide the Prompt 3 contract explicitly:

- Should this smoke prompt continue to require `answer_with_assumptions` even when Pass 1 lists more than two missing-information items?
- Should the smoke expected outcome be changed to accept `clarify` when `missing_information_too_broad` fires?
- Should the deterministic breadth threshold or shape-specific assumption gate be re-specified with a narrower rule?

## Non-decision in this lane

This lane does not alter the spec, update expectations, change tests, or patch code. It only classifies the conflict and selects the next expectation-decision lane.
