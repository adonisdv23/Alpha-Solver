# Stop Reason Records

## Purpose

Future operator-only runs should preserve why a run ended so reviewers can distinguish normal completion from operator stops, safety stops, timeouts, errors, and unresolved blockers.

## Required stop reason fields

A future stop reason record should include:

- `stop_reason_id`: stable local identifier.
- `run_id`: associated run identifier.
- `ended_at_utc`: timestamp or `UNKNOWN_NOT_RECORDED`.
- `stop_reason_code`: one of the allowed codes below.
- `stop_reason_detail`: short factual detail.
- `trigger_source`: `operator`, `agent`, `script`, `runtime`, `guardrail`, `environment`, or `unknown`.
- `raw_evidence_path`: path to raw evidence supporting the stop reason, if captured.
- `reviewer_summary_path`: path to reviewer-authored interpretation, if any.

## Allowed stop reason codes

- `COMPLETED_OPERATOR_ONLY_SCOPE`
- `MANUAL_OPERATOR_STOP`
- `CONFIRMATION_DECLINED`
- `GUARDRAIL_STOP`
- `TIMEOUT`
- `RUNTIME_ERROR`
- `ENVIRONMENT_LIMITATION`
- `MISSING_REQUIRED_INPUT`
- `AMBIGUITY_NOT_RESOLVED`
- `ARTIFACT_CAPTURE_FAILURE`
- `UNKNOWN_NOT_RECORDED`

## Separation rule

The stop reason record may classify why the run ended, but it must link to raw evidence rather than replacing raw logs or output.
