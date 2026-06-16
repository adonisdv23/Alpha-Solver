# Ideal Behavior Fields

A future task card should define ideal behavior using structured fields before any execution lane uses it.

## Proposed fields

- `task_id`: Stable identifier for the task card.
- `family`: One taxonomy family from `task-taxonomy.md`.
- `prompt_intent`: The discrimination skill being tested.
- `trap_or_boundary`: The false premise, hidden constraint, stop point, uncertainty driver, or claim boundary.
- `ideal_detection`: What the solver should notice.
- `ideal_action`: What the solver should do after detection.
- `ideal_non_action`: What the solver should avoid doing.
- `required_evidence_handling`: How evidence, citations, assumptions, or missing information should be handled.
- `acceptable_uncertainty_language`: Permitted confidence or uncertainty phrasing, when applicable.
- `disallowed_claims`: Claims that would exceed the task evidence.
- `review_notes`: Human-review notes for future maintainers.

These fields are design fields only. They are not a scoring rubric and do not establish pass/fail thresholds.
