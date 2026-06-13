# Spec health findings

Full audit: [`docs/SPECS_HEALTH_AUDIT.md`](../../../SPECS_HEALTH_AUDIT.md).

**CONFIRMED and systemic.** The signature phrase `"Create a stable MCP error
taxonomy"` (the MCP-005 Error Taxonomy body) appears in **23** `.specs/` files.
`MCP-005` is the legitimate source; the other **22** carry that body under
unrelated titles (only the `## Code Targets` line differs):

`MCP-001/002/003/004/006/007`, `NEW-009`–`017`, `RES-03`–`08`, `AS-145`.

Classifications:

- `SPEC_CONTAMINATED` + `SPEC_NEEDS_SOURCE_RECONSTRUCTION`: the 22 files (intended
  feature content is missing).
- `SPEC_OK` / `DO_NOT_TOUCH`: `MCP-005` (canonical).
- `SPEC_NEEDS_OPERATOR_DECISION`: disposition of the 22 (reconstruct / deprecate
  / dedup) and MVP doc overlap.

**Recommended follow-up lane:** `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001`.
Contaminated specs were **not** rewritten from memory in this lane.
