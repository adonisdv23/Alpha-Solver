# Per-spec classification

Full classification of all 83 `.specs/*.md` files is the index table in
[`docs/SPECS_HEALTH_AUDIT.md`](../../../SPECS_HEALTH_AUDIT.md#full-specs-health-index-all-83-files).

Summary:

| Classification | Count |
|----------------|-------|
| `SPEC_OK` (incl. `MCP-005` canonical) | 57 |
| `SPEC_CONTAMINATED` (+ `SPEC_NEEDS_SOURCE_RECONSTRUCTION`) | 22 |
| `SPEC_NEEDS_OPERATOR_DECISION` | 2 |
| `META` (registry files, not specs) | 2 |

- `SPEC_CONTAMINATED` = the 22 listed in `contamination-evidence.md`.
- `SPEC_NEEDS_SOURCE_RECONSTRUCTION` = the same 22 (remediation path; code+tests exist).
- `SPEC_DUPLICATE_BODY` = the same 22 form one duplicate-body set; filed under
  `SPEC_CONTAMINATED` as the primary actionable label.
- `SPEC_NEEDS_OPERATOR_DECISION` = `MVP-READINESS-CHECKPOINT-001`,
  `MVP-CLOSEOUT-001` (spec/doc overlap, ISS-010).
- `SPEC_STALE` = none confirmed; staleness was not exhaustively assessed beyond
  the contamination scope (the only duplicate-body cluster is the taxonomy one).
