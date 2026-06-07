# Accepted outcome matrix

| Prompt id | Prompt shape | Gate condition | Expected / accepted mode | Smoke interpretation |
| --- | --- | --- | --- | --- |
| `03-answer-with-assumptions` | `bounded_local_python_cli_startup_plan` | Assumption gate passes | `answer_with_assumptions` | Expected success path; bounded assumptions path remains the normal positive expectation. |
| `03-answer-with-assumptions` | `bounded_local_python_cli_startup_plan` | `apply_gate_decision=blocked_assumption_gate_failed` and `assumption_gate_failed_reason_codes` includes `missing_information_too_broad` | `clarify` | Accepted guarded outcome; not a smoke failure if pass two is not called, model fields are not exposed, boundary stage is `none`, and safety protections remain intact. |
| `03-answer-with-assumptions` | Any unbounded, unsafe, high-risk, or boundary-violating shape | High-risk, unsafe, boundary, or failed-closed condition | `block`, `clarify`, or fail-closed as dictated by the existing guard | Must remain blocked or fail closed; this packet does not make unsafe or unbounded answers acceptable. |

## Non-accepted outcomes

This packet does not accept:

- `answer_with_assumptions` when high-risk or unsafe conditions require blocking;
- exposed model fields after the assumption gate blocks;
- Pass 2 execution after `missing_information_too_broad` blocks Prompt 3;
- boundary failures being treated as successful normal answers;
- any broadening of the Prompt 3 exception beyond `missing_information_too_broad` for the bounded local Python CLI startup-plan shape.
