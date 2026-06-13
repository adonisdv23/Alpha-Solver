# Claim boundary

This lane is **docs/specs integrity** only. It claims only that it:

- verified live GitHub `main`/PR state read-only,
- detected and confirmed (by body hashing over committed files) that 22 `.specs/`
  files carry the `MCP-005` Error-Taxonomy body under unrelated titles,
- marked those 22 specs non-authoritative without altering their body text,
- updated `docs/SPECS_HEALTH_AUDIT.md`, created `docs/SPECS_RECONCILIATION_PLAN.md`,
  and added a health column to `.specs/INDEX.md`,
- recorded a single selected next lane.

It explicitly does **not** establish provider behavior, runtime behavior,
security/privacy posture, readiness, or value/quality. It does **not** assert that
any contaminated feature is correctly implemented — only that code+test files with
the named paths exist (which makes reconstruction feasible).

Boundary phrasing used throughout: **non-authoritative**, **not implementation
scope**, **preserved unchanged**, **not reconstructed**, **operator decision
required**, **does not claim**.
