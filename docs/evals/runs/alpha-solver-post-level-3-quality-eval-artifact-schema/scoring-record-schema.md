# Scoring Record Schema

## Purpose

Scoring records document how future eval outputs are scored against an authorized rubric. They are derived artifacts that refer back to raw outputs.

## Required scoring fields

| Field | Required | Description |
| --- | --- | --- |
| `scoring_record_id` | Yes | Stable scoring record identifier. |
| `rubric_id` | Yes | Rubric or scoring guide used. |
| `scorer_role` | Yes | Scorer role or automation role. |
| `scored_at_utc` | Yes | UTC scoring timestamp. |
| `source_raw_output_id` | Yes | Raw output being scored. |
| `source_path` | Yes | Path to the raw output. |
| `source_anchor` | Recommended | Line range, JSON pointer, or transcript turn. |
| `criterion_id` | Yes | Rubric criterion identifier. |
| `score_value` | Conditional | Score if valid scoring was possible. |
| `score_scale` | Conditional | Scale such as `0-2`, `pass_fail`, or rubric-defined labels. |
| `invalid_result_marker` | Conditional | Required when scoring cannot produce a valid result. |
| `rationale` | Yes | Rationale grounded in the cited raw output. |
| `review_status` | Yes | `draft`, `reviewed`, `accepted`, `rejected`, or `blocked`. |
| `claim_boundary` | Yes | Statement that the score applies only to the cited artifact and criterion. |

## Scoring rules

- A scored artifact must refer back to raw output by `source_raw_output_id` and `source_path`.
- A score must not be created from memory, screenshots alone, summaries alone, or reviewer notes alone when raw output exists.
- Invalid outputs should receive an invalid-result marker rather than an invented score.
- Aggregated scores must identify every included scoring record and every excluded invalid record.
