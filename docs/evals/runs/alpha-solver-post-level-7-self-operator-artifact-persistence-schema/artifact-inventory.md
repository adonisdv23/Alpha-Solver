# Artifact Inventory Schema

## Purpose

Future Self Operator MVP operator-only runs should include an artifact inventory that lists every preserved artifact and identifies whether it is raw evidence or reviewer-authored interpretation.

## Required top-level artifact classes

Each future run packet should preserve these classes when applicable:

| Artifact class | Required path pattern | Raw or reviewer-authored | Preservation requirement |
|---|---|---:|---|
| Run metadata | `run_metadata.*` | Raw/run record | Preserve local run identity, timestamps, environment descriptors, and command context. |
| Prompts | `raw/prompts/*` | Raw | Preserve exact prompt text, prompt files, prompt templates, prompt variables, and operator instructions. |
| Inputs | `raw/inputs/*` | Raw | Preserve source inputs, source evidence, fixtures, config snippets, and operator-provided materials without mutation. |
| Outputs | `raw/outputs/*` | Raw | Preserve stdout, stderr, response bodies, structured outputs, transcripts, and partial outputs exactly as emitted. |
| Logs | `raw/logs/*` | Raw | Preserve terminal logs, application logs, trace snippets, and diagnostic logs exactly as captured. |
| Confirmations | `records/confirmations.*` | Run record | Preserve human/operator confirmations, refusals, approvals, and explicit proceed/stop decisions. |
| Stop reasons | `records/stop_reasons.*` | Run record | Preserve why a run ended, including completion, manual stop, timeout, guardrail stop, error, or ambiguity. |
| Redaction ledger | `records/redactions.*` | Run record | Preserve every redaction marker, reason category, artifact path, and field location. |
| Reviewer summaries | `review/*.md` | Reviewer-authored | Keep interpretations, acceptance notes, risks, caveats, and review notes separate from raw artifacts. |
| Checks run | `checks-run.md` or `review/checks-run.md` | Reviewer-authored/run record | Preserve exact commands and outcomes used to review the packet. |

## Inventory entry fields

Each inventory entry should include:

- `artifact_id`: stable local identifier unique within the run packet.
- `path`: repo-relative or packet-relative path.
- `artifact_class`: one of the required classes above or a documented extension.
- `raw_or_reviewer_authored`: `raw`, `run_record`, or `reviewer_authored`.
- `created_by`: `operator`, `runtime`, `reviewer`, `script`, or `unknown`.
- `capture_time_utc`: ISO-8601 timestamp when available, otherwise `UNKNOWN_NOT_RECORDED`.
- `source_mutated`: must be `false` for raw source evidence.
- `redaction_status`: `none`, `redacted`, or `not_applicable`.
- `notes`: short reviewer note that must not replace the raw artifact.

## Raw versus reviewer separation

Raw artifacts must remain in raw artifact locations. Reviewer summaries must not be stored in the same file as raw prompts, raw inputs, raw outputs, or raw logs.
