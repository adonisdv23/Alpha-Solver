# Checks run

Validation record for `ALPHA-SOLVER-ROUTED-VS-PLAIN-PILOT-OUTPUTS-001`.

- `git diff --check` - passed; no whitespace errors reported.
- Narrative claim-safety lint on changed Markdown files - initial local lint was over-strict and flagged existing negated/deferred claim-boundary lines; after adding an explicit `Not authorized:` prefix to one changed source-of-truth line and rerunning the lint, it passed: `PASS narrative claim-safety lint: 27 changed Markdown files checked`.
- Output inventory completeness check - passed: `PASS output inventory completeness: 12/12 collected with task files and plain/routed sections`.
- Route metadata completeness check requiring `route reasons` - passed: `PASS route metadata completeness: 12/12 rows include required metadata and route reasons`.
- Task ID preservation check for `RVP-001` through `RVP-012` - passed: `PASS task ID preservation: RVP-001 through RVP-012 preserved exactly`.
- Source-of-truth consistency check for `OPERATOR_REVIEW_REQUIRED_AFTER_ROUTED_VS_PLAIN_PILOT_OUTPUTS_001` - passed: `PASS source-of-truth consistency: selected next state present in CURRENT_STATE, LANE_REGISTRY, and EVIDENCE_INDEX`.
- Changed-line secret-safety check - passed: `PASS changed-line secret-safety: no secret-like changed lines detected`.
- Packet completeness check - passed: `PASS packet completeness: required 12 top-level files plus 12 task files present`.
