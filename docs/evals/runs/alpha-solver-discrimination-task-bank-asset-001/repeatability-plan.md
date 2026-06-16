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

## First cheap test

Draft five task cards, one per taxonomy family, using the proposed fields. The test passes only if a reviewer can explain each card's trap or boundary without running a model, generating outputs, or defining scores.
