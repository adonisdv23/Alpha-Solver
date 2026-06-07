# Gate Trace Guide

`metadata.gate_trace` is diagnostic metadata for operator inspection. It must be redacted and bounded.

## Fields

- `diagnostic_schema_version`: Numeric schema version for the diagnostic shape.
- `diagnostic_redaction`: Redaction label. Expected value indicates enum-only diagnostics with no raw text.
- `prompt_shape`: Enum describing the prompt shape, such as generic, underspecified, high-risk, or boundary-claim categories.
- `pass_one_selected_mode`: Enum describing the Pass 1 selected mode or parse-failure state.
- `apply_gate_decision`: Enum describing the deterministic gate action, such as direct, clarify, block, failed-closed parse, or failed-closed boundary.
- `boundary_failure_stage`: Enum indicating where a boundary failure occurred, such as Pass 1 or Pass 2, when applicable.
- `expose_model_fields`: Boolean indicating whether bounded parsed model fields were safe to expose.
- `pass_two_called`: Boolean indicating whether the second local model pass was called.
- `blocked_reason_code`: Enum reason for a primary blocked outcome when present.
- `blocked_reason_codes`: List of enum reasons for blocked outcomes when present.
- `high_risk_reason_code`: Enum reason for explicit high-risk detection when present.
- `risk_flag_rejected_reason`: Enum reason when model-supplied risk flags were rejected as unsafe or high risk.
- `assumption_gate_failed_reason_codes`: List of enum reasons explaining why assumptions/missing-information checks prevented a direct answer.

## Redaction rule

`gate_trace` must remain enum/boolean/numeric/list-of-enum only. It must not contain:

- raw prompt text;
- raw model output;
- raw risk flags;
- raw missing information;
- raw considerations;
- raw assumptions;
- raw answer text.

Stop and preserve the problematic artifact for review if raw text appears inside `gate_trace`.
