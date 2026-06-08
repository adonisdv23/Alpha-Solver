# Confirmation Records

## Purpose

Future operator-only runs should preserve explicit confirmations and non-confirmations so reviewers can see where an operator approved, refused, stopped, or declined to proceed.

## Required confirmation fields

A future confirmation record should include:

- `confirmation_id`: stable local identifier.
- `run_id`: associated run identifier.
- `prompt_or_action_id`: related prompt, command, tool call, or decision.
- `confirmation_type`: `approve`, `decline`, `stop`, `continue`, `manual_override`, `not_requested`, or `unknown`.
- `confirmed_by`: operator identity category, not sensitive personal data.
- `confirmation_text_raw_path`: path to the raw confirmation text when captured.
- `captured_at_utc`: timestamp or `UNKNOWN_NOT_RECORDED`.
- `scope_confirmed`: exact action or boundary confirmed.
- `scope_excluded`: actions not approved by the confirmation.
- `redaction_status`: `none`, `redacted`, or `not_applicable`.

## Preservation rule

Raw confirmation text must be preserved separately from reviewer interpretation. Reviewer comments about whether a confirmation was sufficient must be placed in a reviewer-authored notes file.
