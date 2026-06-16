# Ideal Behavior Fields

A future task card should define ideal behavior using structured fields before any execution lane uses it.

## Proposed fields

- `task_id`: Stable identifier for the task card.
- `family`: One taxonomy family from `task-taxonomy.md`.
- `prompt_intent`: The discrimination skill being tested.
- `trap_or_boundary`: The false premise, hidden constraint, stop point, uncertainty driver, or claim boundary.
- `as_of_date`: Date the current-fact premise is frozen, required when the task depends on external or time-changing facts.
- `source_snapshot`: Citation, committed artifact path, or frozen source description used to establish the premise at `as_of_date`.
- `truth_status_at_freeze`: Whether the premise is false, unsupported, contradictory, impossible, or otherwise trap-bearing at freeze time.
- `staleness_review_required`: Whether the task must be reviewed before reuse because it depends on external or current facts.
- `reuse_rule`: Current-fact tasks may not be reused unless the `as_of_date` and `source_snapshot` are preserved, or the task is revised as a new version.
- `ideal_detection`: What the solver should notice.
- `ideal_action`: What the solver should do after detection.
- `ideal_non_action`: What the solver should avoid doing.
- `required_evidence_handling`: How evidence, citations, assumptions, or missing information should be handled.
- `acceptable_uncertainty_language`: Permitted confidence or uncertainty phrasing, when applicable.
- `disallowed_claims`: Claims that would exceed the task evidence.
- `review_notes`: Human-review notes for future maintainers.

These fields are design fields only. They are not a scoring rubric and do not establish pass/fail thresholds.
