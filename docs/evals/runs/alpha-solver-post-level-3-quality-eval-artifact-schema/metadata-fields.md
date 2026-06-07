# Metadata Fields Schema

## Purpose

Future quality eval artifacts need consistent metadata fields so reviewers can determine what was run, what was captured, what was not run, and which claims are allowed.

## Required metadata fields

| Field | Required | Description |
| --- | --- | --- |
| `schema_packet` | Yes | The schema reference used by the future eval artifact packet. |
| `eval_packet_id` | Yes | Stable identifier for the future evaluation packet. |
| `eval_objective` | Yes | Short objective of the future evaluation execution. |
| `level_5_authorization` | Yes | Link or marker showing whether Level 5 authorized execution and schema use. |
| `operator_role` | Yes | Role of the person or automation that ran the future eval. |
| `reviewer_roles` | Yes | Roles assigned to review, scoring, redaction, and final decision. |
| `started_at_utc` | Conditional | Required if an eval run actually occurred. |
| `completed_at_utc` | Conditional | Required if an eval run actually completed. |
| `repository_commit` | Yes | Git commit used when the future packet was assembled. |
| `working_tree_state` | Yes | Clean, dirty, or documented exception. |
| `runtime_entrypoint` | Conditional | CLI, script, API route, or operator command used if execution occurred. |
| `provider_or_model` | Conditional | Provider, local model, hosted model, or none. |
| `network_state` | Yes | Local-only, hosted-provider, offline, or not applicable. |
| `input_set_id` | Conditional | Frozen or ad hoc input set identifier if execution occurred. |
| `raw_output_ids` | Conditional | IDs of raw outputs captured for the future evaluation. |
| `rubric_id` | Conditional | Rubric or scoring guide used if scoring occurred. |
| `redaction_policy` | Yes | Redaction rule set used by the future artifact packet. |
| `claim_boundary` | Yes | Exact claim-boundary language applied to the packet. |
| `invalid_result_policy` | Yes | Invalid-result marker set used by the packet. |
| `final_decision_state` | Conditional | Final accepted, rejected, blocked, inconclusive, or deferred state. |

## Metadata fields boundary

Metadata fields describe future artifacts and do not themselves prove model quality. Missing conditional fields must be marked `not_applicable` or `not_run`; they must not be inferred from reviewer expectations.
