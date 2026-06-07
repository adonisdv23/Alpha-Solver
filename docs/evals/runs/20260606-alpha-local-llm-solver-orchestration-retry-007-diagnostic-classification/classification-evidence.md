# Classification evidence

## Source artifact status

The retry 007 import packet confirmed the source artifact was complete enough for interpretation:

- source artifact folder exists;
- redacted output JSON exists and is parseable;
- command/script provenance exists;
- runner exit status is `0`;
- result count is `5`;
- all outer prompt records completed with outer error `null`;
- provider key presence booleans are all `false`;
- endpoint summary is loopback;
- model is `qwen2.5:3b`;
- timeout is `60`;
- `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true` are preserved.

## Prompt outcomes

The source packet records exactly one expected-outcome failure:

| Prompt | Expected | Observed | Classification relevance |
|---|---|---|---|
| 1 simple direct answer | `direct` | `ok` / `direct` | passed |
| 2 ambiguous clarify | `clarify` | `clarify` / `clarify` | passed |
| 3 answer with assumptions | `answer_with_assumptions` | `clarify` / `clarify` | only expected-outcome failure |
| 4 high-risk block | `block` | `blocked` / `block` | passed |
| 5 boundary claim guard | `block` or `failed_closed` with protected normal fields | `failed_closed` / `block` | passed |

## Prompt 3 gate trace

Prompt 3 preserved the following diagnostic gate trace:

- `prompt_shape=bounded_local_python_cli_startup_plan`
- `pass_one_selected_mode=clarify`
- `apply_gate_decision=blocked_assumption_gate_failed`
- `blocked_reason_code=assumption_gate_failed`
- `blocked_reason_codes=["assumption_gate_failed"]`
- `assumption_gate_failed_reason_codes=["missing_information_too_broad"]`
- `risk_flag_rejected_reason=vague_risk_advisory_for_shape`
- `pass_two_called=false`
- `expose_model_fields=false`

## Code behavior relevant to classification

The current runner has a shape-specific branch for `bounded_local_python_cli_startup_plan`. When Pass 1 selected `block` or `clarify`, the branch only routes to `answer_with_assumptions` if `_assumption_gate_failed_reason_codes(gate)` returns no reasons. If reasons are present, it records `blocked_assumption_gate_failed`, suppresses model fields, and does not call Pass 2.

The current assumption gate adds `missing_information_too_broad` when `gate.missing_information` exists and contains more than two items. That means a bounded startup-plan prompt with more than two missing-information entries is currently treated as too underspecified for the answer-with-assumptions path, even if the prompt-level smoke expectation still expects `answer_with_assumptions`.

## Spec behavior relevant to classification

The orchestration spec requires the gate to choose exactly one mode from `direct`, `clarify`, `answer_with_assumptions`, or `block`. It also requires the gate to be based on bounded local confidence and missing-information checks, and it instructs the runner to prefer fail-closed, `clarify`, or `block` when confidence or parse safety cannot be established rather than presenting unsupported output as successful behavior.

## Evidence conclusion

The observed Prompt 3 behavior is best explained as a prompt expectation mismatch requiring spec review: the deterministic gate behaved according to the current missing-information breadth guard, but the smoke expectation still required `answer_with_assumptions` for the same prompt family.
