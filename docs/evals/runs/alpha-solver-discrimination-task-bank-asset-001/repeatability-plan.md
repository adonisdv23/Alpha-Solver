# Repeatability Plan

## Goal

The task bank should be reusable without becoming an accidental benchmark, hidden source of claims, or mutable evidence artifact.

## Controls

- Assign stable task IDs before any future execution.
- Keep task prompts, ideal fields, and failure-mode fields versioned together.
- Record any wording change as a new revision rather than silently editing an existing task.
- Maintain family labels separately from scoring labels.
- Preserve docs-only boundaries until a separate authorized execution lane exists.
- Require reviewer notes for ambiguous task interpretations.
- Keep generated outputs outside this feasibility packet.
- Avoid provider-specific assumptions in task wording.
- Freeze current-fact tasks at draft time with `as_of_date`, `source_snapshot`, `truth_status_at_freeze`, `staleness_review_required`, and `reuse_rule`.
- If the current fact changes later, do not silently edit the existing task.
- Create a new task revision instead of mutating the frozen current-fact task.
- A current-fact task with missing `as_of_date` or missing `source_snapshot` must not be used in a scoring or execution lane.
- Current-fact tasks may not be reused unless the as-of date and source snapshot are preserved, or the task is revised as a new version.

## First cheap test

Draft five task cards, one per taxonomy family, using the proposed fields. The test passes only if a reviewer can explain each card's trap or boundary without running a model, generating outputs, or defining scores. Any card that depends on current facts must also include an `as_of_date`, `source_snapshot`, `truth_status_at_freeze`, `staleness_review_required`, and `reuse_rule` before it can pass the manual review.
