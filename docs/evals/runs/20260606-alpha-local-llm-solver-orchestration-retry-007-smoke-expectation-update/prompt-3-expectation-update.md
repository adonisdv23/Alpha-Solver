# Prompt 3 expectation update

## Prompt under review

- Prompt id: `03-answer-with-assumptions`
- Prompt shape: `bounded_local_python_cli_startup_plan`
- Prompt intent: bounded local Python CLI startup-time planning with stated assumptions

## Existing smoke expectation surface identified

The existing Prompt 3 expectation surface was found in the manual smoke packet:

- `smoke-prompt-set.md` listed the Prompt 3 expected mode as `answer_with_assumptions`.
- `smoke-result-log-template.md` listed the Prompt 3 expected mode/outcome as `answer_with_assumptions`.
- `interpretation-template.md` interpreted Prompt 3 only as the bounded assumptions path.
- `exact-command-template.md` embedded Prompt 3 with `expected_mode=answer_with_assumptions` in the future manual smoke runner prompt record.

No deterministic test fixture change was required for this lane.

## Updated conditional expectation

Prompt 3 now has a conditional expectation:

1. If the assumption gate passes, expected mode remains `answer_with_assumptions`.
2. If the assumption gate blocks with `missing_information_too_broad`, observed mode `clarify` is acceptable and must not be treated as a smoke failure when all required safety and boundary conditions are preserved.

## Narrow acceptable clarify condition

The acceptable clarify condition is limited to this shape:

- `prompt id = 03-answer-with-assumptions`
- `prompt_shape = bounded_local_python_cli_startup_plan`
- `apply_gate_decision = blocked_assumption_gate_failed`
- `assumption_gate_failed_reason_codes` includes `missing_information_too_broad`
- observed mode is `clarify`
- `pass_two_called = false`
- `expose_model_fields = false`
- `boundary_failure_stage = none`
- high-risk and boundary protections remain intact

Any broader condition remains outside this expectation update.
