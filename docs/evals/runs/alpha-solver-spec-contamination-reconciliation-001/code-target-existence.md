# Code-target existence (reconstruction feasibility)

For every contaminated spec, all `## Code Targets` — implementation **and** test
files — are present in the repository. The authentic feature each spec was meant
to document therefore exists in committed code+tests, so its real spec can be
**reconstructed from an authoritative in-repo source** (next lane), not from memory.

| Spec | # Code Targets | On disk |
|------|----------------|---------|
| `MCP-001` | 3 | ✅ all present |
| `MCP-002` | 2 | ✅ all present |
| `MCP-003` | 2 | ✅ all present |
| `MCP-004` | 2 | ✅ all present |
| `MCP-006` | 2 | ✅ all present |
| `MCP-007` | 2 | ✅ all present |
| `NEW-009` | 4 | ✅ all present |
| `NEW-010` | 4 | ✅ all present |
| `NEW-011` | 3 | ✅ all present |
| `NEW-012` | 3 | ✅ all present |
| `NEW-013` | 3 | ✅ all present |
| `NEW-014` | 4 | ✅ all present |
| `NEW-015` | 4 | ✅ all present |
| `NEW-016` | 4 | ✅ all present |
| `NEW-017` | 4 | ✅ all present |
| `RES-03` | 3 | ✅ all present |
| `RES-04` | 3 | ✅ all present |
| `RES-05` | 5 | ✅ all present |
| `RES-06` | 4 | ✅ all present |
| `RES-07` | 3 | ✅ all present |
| `RES-08` | 5 | ✅ all present |
| `AS-145` | 5 | ✅ all present |

**Conclusion:** reconstruction is feasible for all 22 → selected next lane is
`ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` (source reconstruction), not the
documentation-only `ALPHA-SOLVER-SPECS-INDEX-CLEANUP-001`.
