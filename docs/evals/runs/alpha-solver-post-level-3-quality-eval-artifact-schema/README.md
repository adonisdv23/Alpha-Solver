# Alpha Solver Post-Level-3 Quality Eval Artifact Schema Packet

Lane: `ALPHA-SOLVER-POST-LEVEL-3-QUALITY-EVAL-ARTIFACT-SCHEMA-PACKET-001`

## Purpose

This packet defines a docs-only artifact schema for future Alpha Solver quality evaluation execution packets. It describes the files, metadata fields, raw-output preservation rules, reviewer notes, scoring records, invalid-result markers, redaction rules, final decision files, and checks-run files that future eval artifact packets should contain.

## Authority and boundary

This schema is a supporting reference only and does not create eval evidence. Level 5 controls whether and how this schema is used in future quality evaluation lanes.

The schema does not execute an eval, score output, call any provider, expose `/v1/solve`, expose dashboards, add fallback behavior, perform billing work, promote evidence, or create real eval result artifacts.

## Required future artifact files

Future quality eval artifact packets that adopt this schema should include the following files or clearly document why a required file is absent:

- `README.md` — packet purpose, evidence boundary, adopted schema version, and file map.
- `run-metadata.md` — required metadata fields for the future evaluation execution.
- `source-evidence-reviewed.md` — source materials reviewed before the future evaluation artifact packet was assembled.
- `artifact-file-inventory.md` — inventory of raw outputs, derived reviewer notes, scoring sheets, final decisions, and checks.
- `raw-output-preservation.md` — preservation hash ledger and immutability notes for captured raw outputs.
- `raw-outputs/` — append-only directory for unmodified raw provider, model, runner, or operator output captures.
- `reviewer-notes.md` — structured reviewer notes that refer back to raw outputs without replacing them.
- `scoring-records.md` — scoring records, rubric references, reviewer identity or role fields, and raw-output anchors.
- `invalid-result-markers.md` — explicit invalid, incomplete, redacted, superseded, and blocked result states.
- `redaction-log.md` — redaction decisions, redacted-field locations, reason codes, and reviewer signoff.
- `final-decision.md` — final decision and claim boundaries derived from reviewed evidence.
- `checks-run.md` — commands and static checks run while assembling the artifact packet.
- `non-actions.md` — explicit confirmation of eval, provider, runtime, dashboard, billing, and evidence-promotion non-actions.

## Packet files in this schema lane

- `README.md`
- `source-evidence-reviewed.md`
- `artifact-file-inventory.md`
- `metadata-fields.md`
- `raw-output-preservation.md`
- `reviewer-notes-schema.md`
- `scoring-record-schema.md`
- `invalid-result-markers.md`
- `redaction-rules.md`
- `final-decision-files.md`
- `non-actions.md`
- `selected-next-action.md`
- `blocker-fallback-lane.md`
- `checks-run.md`

## Required claim-boundary language

Future eval artifacts adopting this schema must use claim-boundary language that separates captured evidence from interpretation. Required phrasing:

- "This artifact records evidence captured during the named evaluation run only."
- "This artifact does not establish production readiness, MVP readiness, benchmark superiority, provider reliability, billing readiness, dashboard readiness, or broad runtime readiness unless a separate Level 5 decision explicitly authorizes that claim."
- "Scored artifacts refer back to preserved raw outputs and do not replace the raw outputs."
- "Redacted derivatives are convenience review artifacts; preserved raw outputs remain the source of record unless Level 5 requires redacted-only retention."
- "Invalid results must remain discoverable and must not be silently deleted or converted into passing evidence."

## Decision state

Selected next action: `NO_FURTHER_QUALITY_EVAL_ARTIFACT_SCHEMA_LANES_SELECTED`

Blocker fallback lane: `ALPHA-SOLVER-POST-LEVEL-3-QUALITY-EVAL-ARTIFACT-SCHEMA-FIX-001`
