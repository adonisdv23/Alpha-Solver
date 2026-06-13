# ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001

Docs/specs integrity lane. Audits and reconciles `.specs/*.md` files that carry
copied or mismatched content — specifically specs carrying the **MCP-005 Error
Taxonomy** body under unrelated titles.

- **Lane:** `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001`
- **Date:** 2026-06-13
- **Verdict:** **`SPEC_CONTAMINATION_RECONCILIATION_CAPTURED`**
- **Selected next lane:** `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001`
- **Scope:** docs/specs-integrity only. No runtime/product code, tests, or CI
  changed. No provider calls, no tokens. No spec deleted. No spec rewritten from
  memory.

## What this lane produced

Source-of-truth docs (repo root `docs/`):

- [`docs/SPECS_HEALTH_AUDIT.md`](../../../SPECS_HEALTH_AUDIT.md) — updated; full
  83-file health index + contamination evidence.
- [`docs/SPECS_RECONCILIATION_PLAN.md`](../../../SPECS_RECONCILIATION_PLAN.md) —
  new; per-spec reconstruction routing + operator disposition options.

Spec-tree changes:

- 22 contaminated `.specs/*.md` files marked **non-authoritative** with a
  standardized banner (body preserved verbatim).
- [`.specs/INDEX.md`](../../../../.specs/INDEX.md) — added a `Health` column.

## Packet contents

`repo-state-verification.md`, `methodology.md`, `contamination-evidence.md`,
`per-spec-classification.md`, `code-target-existence.md`, `marking-actions.md`,
`reconciliation-summary.md`, `claim-boundary.md`, `forbidden-claims.md`,
`non-actions.md`, `selected-next-lane.md`, `verdict.md`.

## Headline

The hypothesis is **CONFIRMED and systemic**: `MCP-002`, `NEW-010`, and 20 other
specs carry the `MCP-005` Error-Taxonomy body under unrelated titles. `MCP-005`
is the single legitimate source and is left untouched. Every contaminated spec's
titled feature exists in committed code+tests, so reconstruction (next lane) is
feasible from an authoritative in-repo source — never from memory.

## Non-claims

This lane does **not** claim runtime, provider, security/privacy, readiness, or
value/quality outcomes. It is a docs-integrity audit. See `forbidden-claims.md`.
