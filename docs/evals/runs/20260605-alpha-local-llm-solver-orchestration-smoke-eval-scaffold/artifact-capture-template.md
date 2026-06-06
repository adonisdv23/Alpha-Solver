# Artifact Capture Template

## Non-Execution Notice

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

## Future Artifact Inventory

For each future smoke run, capture only redacted, non-secret artifacts:

- Runner command summary, not secret-bearing shell history.
- Local endpoint summary, not private URLs.
- Local model identifier.
- Timeout setting.
- Per-prompt request summary.
- Per-prompt response envelope.
- Failure classifications, if any.
- Operator notes.

## Artifact Naming Template

- `artifacts/<future-run-id>/prompt-001-envelope-redacted.json`
- `artifacts/<future-run-id>/prompt-002-envelope-redacted.json`
- `artifacts/<future-run-id>/prompt-003-envelope-redacted.json`
- `artifacts/<future-run-id>/prompt-004-envelope-redacted.json`
- `artifacts/<future-run-id>/prompt-005-envelope-redacted.json`
- `artifacts/<future-run-id>/operator-notes.md`

## Capture Completeness Checklist

- [ ] All five prompt outcomes captured.
- [ ] Expected fields reviewed.
- [ ] Redaction rules applied.
- [ ] No provider keys included.
- [ ] No private URLs included.
- [ ] No full environment dumps included.
- [ ] No runtime-readiness claims added.
