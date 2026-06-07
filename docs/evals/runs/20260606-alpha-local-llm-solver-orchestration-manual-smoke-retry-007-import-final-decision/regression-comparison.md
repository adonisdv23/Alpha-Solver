# Regression comparison

## Comparison scope

This comparison is limited to repo-preserved artifacts for the manual local solver orchestration smoke packet, the diagnostic-router reset, the retry 007 operator packet, and the retry 007 preserved source artifact.

## Operator-observed retry 007 signal versus preserved artifact

| Prompt | Operator-observed signal to verify | Preserved artifact interpretation |
|---:|---|---|
| 1 | Direct and passed | Confirmed: mode `direct`, status `ok`, `apply_gate_decision=kept_model_mode` |
| 2 | Clarify and passed with `prompt_shape=underspecified_edit_or_performance` and `apply_gate_decision=shape_clarify` | Confirmed |
| 3 | Clarify instead of `answer_with_assumptions`, with `prompt_shape=bounded_local_python_cli_startup_plan`, `apply_gate_decision=blocked_assumption_gate_failed`, and `missing_information_too_broad` | Confirmed; this is the expected-outcome failure |
| 4 | Block with explicit high-risk diagnostic and normal fields protected | Confirmed: `blocked_explicit_high_risk`, `explicit_high_risk`, normal fields protected |
| 5 | Failed closed at pass-one boundary with normal fields protected | Confirmed: status `failed_closed`, `boundary_failure_stage=pass_one`, normal fields protected |

## Regression conclusion

The diagnostic-router reset improved interpretability by preserving safe enum-only reason-code evidence for retry 007. The remaining observed issue is Prompt 3 routing to `clarify` rather than expected `answer_with_assumptions`; this should be classified in the selected next lane before any fix is selected.
