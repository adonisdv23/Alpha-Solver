# Diagnostic Schema

Safe diagnostics are recorded at `metadata.gate_trace`.

Schema version: `1`

Fields are deterministic enum, boolean, number, or list-of-enum values only:

- `diagnostic_schema_version`
- `diagnostic_redaction=enum_only_no_raw_text`
- `prompt_shape`
- `pass_one_selected_mode`
- `apply_gate_decision`
- `blocked_reason_code`
- `blocked_reason_codes`
- `high_risk_reason_code`
- `risk_flag_rejected_reason`
- `assumption_gate_failed_reason_codes`
- `boundary_failure_stage`
- `expose_model_fields`
- `pass_two_called`

The trace does not include raw user prompt text, raw model output, raw risk flag text, raw missing information, raw considerations, raw assumptions, raw answer text, prompt fragments, unsafe content, or boundary-violating content.
