# Scorer Preservation Checklist

Lane ID: `ALPHA-BATCH-C-SCORING-RUBRIC-PACKET-001`

Use this checklist to review the packet and to guide a future scorer before scoring is authorized.

## Packet review checklist

- [x] Documentation changes are limited to this scoring-rubric packet folder.
- [x] The packet contains a blank scoring sheet template only.
- [x] The packet does not contain Batch C outputs.
- [x] The packet does not assign task scores.
- [x] Stop-condition rules block scoring when raw artifacts are missing.
- [x] Stop-condition rules block scoring when task prompts are missing.
- [x] Stop-condition rules treat reconstructed raw output as invalid.
- [x] Stop-condition rules block import when scorer-facing sanitized entries are missing.
- [x] Prior-run baseline values are preserved as context only.
- [x] Exactly one selected next lane is recorded.
- [x] No execution, scoring, import, interpretation, readiness, validation, superiority, benchmark, runtime, provider, production, MVP, or billing claim is made.

## Future scorer checklist

- [ ] Confirm raw output exists for the task before scoring.
- [ ] Confirm the frozen task prompt exists before scoring.
- [ ] Confirm the scorer-facing sanitized entry exists before import.
- [ ] Confirm any redaction preserves meaning while removing sensitive details.
- [ ] Confirm blocked tasks have blank score cells.
- [ ] Confirm defect notes use the defect taxonomy without adding interpretation beyond the preserved evidence.
