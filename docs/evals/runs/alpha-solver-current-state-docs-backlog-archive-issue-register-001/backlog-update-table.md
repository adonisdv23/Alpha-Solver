# Backlog update table

Full operating model + paste-ready table:
[`docs/BACKLOG_OPERATING_MODEL.md`](../../../BACKLOG_OPERATING_MODEL.md).

Key rows (state · next lane/owner · blocks smoke · blocks public):

| item | state | next lane / owner | smoke | public |
|------|-------|-------------------|-------|--------|
| PR #508 checker-scope hardening | DONE (merged) | — | No | No |
| PR #509 smoke retry — project/billing blocked | BLOCKED (merged evidence) | `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` | Yes | n/a |
| `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` | **NEXT** | operator + docs (no call) | Yes (unblocks) | No |
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` | BLOCKED (provider setup) | after clarification | Yes | No |
| `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` | BLOCKED (after smoke) | after tiny smoke | No | — |
| DEF-002 security/privacy review | OPEN | DEF-002 lane | No | Yes |
| DEF-003 audit custody/replacement | OPEN | DEF-003 lane | No | No |
| docs/current-state cleanup | DONE (this lane) | maintain registries | No | No |
| spec contamination reconciliation | OPEN | `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001` | No | No |
| roadmap refresh | DONE (this lane) | docs maintainer | No | No |
| test hermeticity fix | OPEN | test-hermeticity lane | No | No |
| evidence ledger / lane registry | DONE (this lane) | maintain registries | No | No |
| CORS / security review input | OPEN | DEF-002 | No | Yes |
| FileSecrets / security review input | OPEN | DEF-002 | No | Yes |
| provider telemetry / security review input | OPEN (default-safe) | DEF-002 | No | Review |
| hardcoded pricing review | OPEN | pricing lane | No | No |
| sanitizer Unicode normalization review | OPEN | DEF-002 | No | Yes |
| alpha/service architecture map | OPEN | architecture-map lane | No | No |
