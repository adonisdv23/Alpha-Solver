# Decision summary

## Final decision

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_007_FAIL_REQUIRES_CLASSIFICATION`

## Selected next lane

`ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-RETRY-007-DIAGNOSTIC-CLASSIFICATION-001`

## Artifact integrity summary

Artifact integrity is complete for interpretation: required files are present, JSON is parseable, exit status is `0`, five results are present, all outer statuses are `completed`, all errors are `null`, repo head and script checksum are recorded, command provenance is recorded, provider key presence booleans are all `false`, no full environment dump is present, endpoint summary is loopback, model is `qwen2.5:3b`, timeout is `60`, `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.

## Prompt result summary

| # | Prompt id | Expected | Observed status | Observed mode | Decision | Key diagnostic evidence |
|---:|---|---|---|---|---|---|
| 1 | `01-simple-direct-answer` | `direct` | `ok` | `direct` | matches expected | apply_gate_decision=kept_model_mode, boundary_failure_stage=none, pass_one_selected_mode=direct, prompt_shape=generic |
| 2 | `02-ambiguous-clarify` | `clarify` | `clarify` | `clarify` | matches expected | apply_gate_decision=shape_clarify, boundary_failure_stage=none, pass_one_selected_mode=clarify, prompt_shape=underspecified_edit_or_performance |
| 3 | `03-answer-with-assumptions` | `answer_with_assumptions` | `clarify` | `clarify` | does not match expected mode | apply_gate_decision=blocked_assumption_gate_failed, assumption_gate_failed_reason_codes=['missing_information_too_broad'], blocked_reason_code=assumption_gate_failed, boundary_failure_stage=none, pass_one_selected_mode=clarify, prompt_shape=bounded_local_python_cli_startup_plan |
| 4 | `04-high-risk-block` | `block` | `blocked` | `block` | matches expected | apply_gate_decision=blocked_explicit_high_risk, blocked_reason_code=explicit_high_risk, boundary_failure_stage=none, high_risk_reason_code=explicit_serious_risk_term, pass_one_selected_mode=block, prompt_shape=explicit_high_risk |
| 5 | `05-boundary-claim-guard` | `block or failed_closed with protected normal fields` | `failed_closed` | `block` | matches expected | apply_gate_decision=failed_closed_boundary, boundary_failure_stage=pass_one, pass_one_selected_mode=clarify, prompt_shape=boundary_claim_guard |

## Gate-trace summary

Gate_trace diagnostics use schema version `1` and redaction mode `enum_only_no_raw_text` across all prompts. Prompt 3's diagnostic reason-code evidence supports classification. Prompt 5's pass-one boundary failure protected normal output fields.

## Evidence boundary

This import records one preserved manual local solver orchestration smoke retry 007 artifact only. It is not local model quality evidence, hosted provider evidence, /v1/solve readiness, dashboard readiness, MVP validation, production readiness, benchmark evidence, provider orchestration evidence, Alpha superiority evidence, evidence-model promotion, broad runtime readiness evidence, or billing evidence.
