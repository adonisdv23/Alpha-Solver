# Selected next lane

```text
ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001
```

Exactly one next lane is selected. Per the lane brief's branching:

- Contaminated specs **are confirmed** → select source reconstruction
  (`ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001`), **not** the documentation-only
  `ALPHA-SOLVER-SPECS-INDEX-CLEANUP-001`.
- Feasibility is established here: every contaminated spec's titled feature exists
  in committed code+tests, so reconstruction can use an authoritative in-repo
  source rather than memory.

## Scope handed to the next lane

- For each of the 22 specs, draft the real
  `Goal / Motivation / Acceptance Criteria / Definition of Done / Code Targets /
  Test Plan` strictly from its committed code+tests; replace the contaminated body
  in place; keep the filename.
- Resolve the operator disposition first (reconstruct **A** / deprecate **B** /
  delete **C**). Default recommendation: **A**.
- Keep `MCP-005` untouched.

This selection authorizes no provider call, runtime exposure, or readiness claim.
