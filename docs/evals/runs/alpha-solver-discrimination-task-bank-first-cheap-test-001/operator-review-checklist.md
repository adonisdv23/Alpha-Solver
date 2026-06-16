# Operator-review checklist

Use this checklist to decide whether the cheap-test packet is ready to become a future execution lane.

- [ ] Exactly five task cards are present, one per taxonomy family: `false-premise`, `hidden-constraint`, `should-stop`, `confidence`, and `claim-boundary`.
- [ ] Derivation / no-echo review labels are consistent and include `exact_echo`, `near_echo`, `paraphrase_only_response`, `substantive_derivation`, `acceptable_source_use`, `unsupported_copying`, and `non_answer_safe_out`.
- [ ] `unsupported_copying` is the canonical copying failure label.
- [ ] `unacceptable_output_copying` is not used as a label.
- [ ] Source text is synthetic or approved committed text.
- [ ] No raw Alpha outputs or raw baseline outputs are included.
- [ ] No scoring is performed.
- [ ] No provider, local-model, runtime, API, dashboard, `/v1/solve`, Google Sheets, dependency, or release work is introduced.
- [ ] Evidence boundaries are preserved.
- [ ] Selected-next state is review-only: `OPERATOR_REVIEW_REQUIRED_AFTER_DISCRIMINATION_TASK_BANK_FIRST_CHEAP_TEST_001`.
