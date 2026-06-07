# Raw-Output Preservation Schema

## raw-output preservation requirement

Future eval packets must preserve raw outputs without mutation. Raw provider responses, local model outputs, runner stdout, runner stderr, command transcripts, API responses, and operator captures must be stored exactly as captured whenever retention is allowed.

## Required preservation fields

| Field | Required | Description |
| --- | --- | --- |
| `raw_output_id` | Yes | Stable ID referenced by reviewer notes and scoring records. |
| `relative_path` | Yes | Path under the future packet, usually `raw-outputs/`. |
| `capture_method` | Yes | CLI redirect, script capture, API transcript, provider export, or operator paste. |
| `captured_at_utc` | Yes | UTC capture timestamp. |
| `captured_by_role` | Yes | Operator, automation, or reviewer role. |
| `bytes` | Yes | File size in bytes. |
| `sha256` | Yes | Hash of the preserved raw file. |
| `encoding` | Yes | UTF-8, binary, JSON, text, or documented alternative. |
| `mutation_state` | Yes | Must be `unmodified_raw` for source-of-record raw outputs. |
| `sensitivity_state` | Yes | `none_detected`, `sensitive_restricted`, or `redacted_derivative_available`. |

## Preservation rules

- Do not edit raw outputs in place.
- Do not normalize whitespace, JSON formatting, timestamps, ordering, or error messages in raw outputs.
- Do not remove failed, partial, invalid, or embarrassing outputs.
- If sensitive content requires restriction, retain the source-of-record path according to the Level 5 retention decision and create a separate redacted derivative rather than mutating the raw file.
- If policy requires raw deletion, the future packet must retain a deletion marker with hash, size, redaction reason, approver role, and deletion timestamp.

## Scored artifact references

Scoring records must refer back to raw outputs by `raw_output_id`, path, and, when practical, line range or JSON pointer. A score cannot stand alone as source evidence; it is an interpretation anchored to preserved raw output.
