# Baseline Failure-Mode Fields

A future task card should also describe likely failure modes so reviewers can identify what the task is meant to expose.

## Proposed fields

- `failure_mode_id`: Stable identifier for the failure pattern.
- `task_id`: Task card associated with the failure mode.
- `failure_family`: False-premise acceptance, constraint miss, over-continuation, overconfidence, or overclaiming.
- `failure_description`: Plain-language description of the failure.
- `observable_marker`: Textual or behavioral marker that suggests the failure occurred.
- `why_it_matters`: Narrow reason the failure is relevant to discrimination behavior.
- `confounders`: Conditions that could make the marker ambiguous.
- `current_fact_freeze_gap`: Whether a current-fact task is missing `as_of_date`, `source_snapshot`, `truth_status_at_freeze`, `staleness_review_required`, or `reuse_rule`.
- `reviewer_caution`: Instruction to avoid converting a single marker into a broad performance claim.
- `non_scoring_note`: Reminder that the field supports review design only until a scoring lane is authorized.
