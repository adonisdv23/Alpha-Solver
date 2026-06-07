# Failure classification

## Classification input

Artifact integrity is complete, and gate_trace diagnostics are safe and sufficient for interpretation.

## Observed expected-outcome failure

Prompt 3 expected `answer_with_assumptions` but observed `clarify`.

Diagnostic evidence:

- `prompt_shape=bounded_local_python_cli_startup_plan`
- `pass_one_selected_mode=clarify`
- `apply_gate_decision=blocked_assumption_gate_failed`
- `blocked_reason_code=assumption_gate_failed`
- `blocked_reason_codes=["assumption_gate_failed"]`
- `assumption_gate_failed_reason_codes=["missing_information_too_broad"]`
- `pass_two_called=false`
- `expose_model_fields=false`

## Classification decision

This import does not select a direct implementation fix. The artifact identifies a classifiable decision/routing failure, but the narrow fix is not proven by this import alone. The correct decision is therefore:

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_007_FAIL_REQUIRES_CLASSIFICATION`
