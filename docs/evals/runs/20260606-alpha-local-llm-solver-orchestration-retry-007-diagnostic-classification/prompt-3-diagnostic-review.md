# Prompt 3 diagnostic review

## Prompt 3 expected and observed outcome

Prompt 3 was the retry 007 `answer_with_assumptions` case.

- Expected mode: `answer_with_assumptions`
- Observed status: `clarify`
- Observed mode: `clarify`
- Observed pass count: `1`
- Observed Pass 2 call: `false`

## Prompt shape

The diagnostic router classified the prompt as:

`bounded_local_python_cli_startup_plan`

This shape is the runner's narrow special case for a concise execution plan to improve a small Python CLI startup time when profiling is only available later and assumptions should be stated.

## Gate trace interpretation

The gate trace shows:

1. Pass 1 selected `clarify`.
2. The prompt shape was recognized as the bounded startup-plan shape.
3. The runner considered whether the shape-specific answer-with-assumptions route was allowed.
4. The assumption gate failed because `missing_information_too_broad` was present.
5. The runner recorded `apply_gate_decision=blocked_assumption_gate_failed`.
6. The runner suppressed model fields with `expose_model_fields=false`.
7. The runner did not call Pass 2.
8. The final user-visible mode remained `clarify`.

## Meaning of `missing_information_too_broad`

In the current code context, `missing_information_too_broad` is a deterministic assumption-gate reason code. It is emitted when Pass 1's parsed `missing_information` list has more than two entries.

In the current spec context, this reason aligns with the requirement that the gate use missing-information checks and prefer `clarify` or `block` over unsupported answer presentation when a bounded answer cannot be safely established.

## Why this points to expectation review

The current implementation and tests already encode two sides of the Prompt 3 contract:

- a bounded startup-plan case can route to `answer_with_assumptions` when the assumption gate passes;
- the same shape must not answer with assumptions when assumption-gate failure reasons, including `missing_information_too_broad`, are present.

Retry 007 produced the second case while the smoke expectation still expected the first. That is a contract/expectation conflict to resolve before implementation changes proceed.
