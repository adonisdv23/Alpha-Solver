# Reviewer Notes Schema

## Purpose

Reviewer notes capture human or automation review observations about future eval artifacts. They are derived artifacts and must not replace raw outputs.

## Required reviewer note fields

| Field | Required | Description |
| --- | --- | --- |
| `review_note_id` | Yes | Stable note identifier. |
| `reviewer_role` | Yes | Reviewer role or automation role. |
| `reviewed_at_utc` | Yes | UTC review timestamp. |
| `source_raw_output_id` | Conditional | Required when a note discusses a raw output. |
| `source_path` | Conditional | Required with `source_raw_output_id`. |
| `source_anchor` | Optional | Line range, JSON pointer, timestamp range, or section marker. |
| `observation_type` | Yes | `format`, `behavior`, `safety`, `correctness`, `latency`, `error`, `redaction`, `validity`, or `other`. |
| `observation` | Yes | Concise reviewer observation. |
| `claim_boundary` | Yes | Boundary statement limiting the observation to the cited source. |
| `requires_scoring` | Yes | `yes`, `no`, or `not_applicable`. |
| `invalid_marker` | Conditional | Required if the observation identifies invalid evidence. |

## Note rules

- Notes must distinguish direct observation from inference.
- Notes must cite preserved raw outputs when discussing outputs.
- Notes must not silently correct or rewrite model responses.
- Notes must not promote an observation into broad Alpha Solver quality evidence without the final decision file and Level 5 authorization.
