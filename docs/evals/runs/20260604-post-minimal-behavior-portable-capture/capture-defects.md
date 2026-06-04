# Capture Defects

Lane ID: `OUTPUT-DIFF-POST-IMPROVEMENT-PORTABLE-CAPTURE-001`

Status: capture-only defect record.

## Technical failures

None observed.

## Retries

No retries occurred.

## Empty or malformed outputs

No empty outputs were observed. No malformed outputs were observed.

## Truncation

No truncation was observed in preserved raw outputs.

## Sanitizer failures

No sanitizer failures were observed. Sanitized scorer-facing material could be created without substantive rewriting.

## Parity concerns

No task-visible parity mismatch was observed: both conditions used the same Codex conversation model surface, no browsing, no generation-time tools, no repository runtime provider adapters, no provider orchestration, and no `/v1/solve`.

The exact underlying provider/model sampling configuration was not exposed by the repository or shell environment, and this limitation is recorded in `source-packet.md`; capture proceeded because the same task surface and policy were used for both conditions.

## Legacy-audit gate failures

No legacy-audit gate failure was observed.

## Stop conditions triggered

No stop condition was triggered.
