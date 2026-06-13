# Specs Health Audit

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Audited `.specs/` against committed file
> bodies. Classifications: `SPEC_OK` · `SPEC_CONTAMINATED` · `SPEC_STALE` ·
> `SPEC_NEEDS_OPERATOR_DECISION` · `SPEC_NEEDS_SOURCE_RECONSTRUCTION`.
> **Contaminated specs are NOT rewritten from memory** here.

## Headline finding (CONFIRMED, broader than the audit input)

The audit hypothesis ("MCP-002 or NEW-010 contain MCP-005 Error Taxonomy content
under unrelated titles") is **CONFIRMED** — and the contamination is **systemic**.

A grep for the Error-Taxonomy signature phrase `"Create a stable MCP error
taxonomy"` matches **23 files** in `.specs/`. `MCP-005` is the legitimate source
(`# CODE SPEC — MCP-005 · Error Taxonomy (MCP)`). The other **22** files carry
the same `Goal` / `Acceptance Criteria` / `Design` / `Tests` body under unrelated
titles; typically only the **`## Code Targets`** line differs and matches each
file's real (titled) feature.

### Verified examples

| File | Title (as written) | Body content | Code Targets (file-specific) |
|------|---------------------|--------------|------------------------------|
| `.specs/MCP-005.md` | Error Taxonomy (MCP) | Error Taxonomy (canonical) | `service/mcp/error_taxonomy.py` |
| `.specs/MCP-002.md` | Router decision rule (MCP) | **Error Taxonomy body** | `registries/mcp/registry_lookup.py` |
| `.specs/NEW-010.md` | Section-Specific Prompt Decks (RES_01) | **Error Taxonomy body** | `service/prompts/decks.yaml; selector.py; renderer.py` |

The mismatch (title + Code Targets describe feature X, but Goal/Design/Tests
describe the Error Taxonomy) means the **intended spec content for the titled
feature is effectively missing** in each contaminated file.

## Classification

### SPEC_CONTAMINATED (22 files — carry the MCP-005 body under unrelated titles)

`MCP-001`, `MCP-002`, `MCP-003`, `MCP-004`, `MCP-006`, `MCP-007`,
`NEW-009`, `NEW-010`, `NEW-011`, `NEW-012`, `NEW-013`, `NEW-014`, `NEW-015`,
`NEW-016`, `NEW-017`, `RES-03`, `RES-04`, `RES-05`, `RES-06`, `RES-07`, `RES-08`,
`AS-145`.

Each of these is also **`SPEC_NEEDS_SOURCE_RECONSTRUCTION`** for its titled
feature: the real feature spec must be recovered from an authoritative source,
not reconstructed from memory.

### SPEC_OK / canonical

`.specs/MCP-005.md` — the legitimate Error Taxonomy spec; its Code Targets
(`service/mcp/error_taxonomy.py`, `tests/test_mcp_errors.py`) exist in the repo.
**DO_NOT_TOUCH** as the taxonomy source of truth.

### SPEC_NEEDS_OPERATOR_DECISION

- Whether the 22 contaminated files should be (a) reconstructed from an external
  authoritative source, (b) marked deprecated/historical, or (c) deleted as
  duplicates — requires an operator decision. (No deletion is performed here.)
- MVP spec/doc overlap (`.specs/MVP-READINESS-CHECKPOINT-001.md` vs
  `docs/MVP_READINESS_CHECKPOINT.md`; `.specs/MVP-CLOSEOUT-001.md`) — see
  [`ARCHIVE_INDEX.md`](ARCHIVE_INDEX.md) (ISS-010).

### SPEC_STALE

Not separately assessed beyond the contamination scope in this lane; the stale
**roadmap** (not a `.specs/` file) is handled in [`ROADMAP.md`](ROADMAP.md) (ISS-002).

## Recommended follow-up lane

Because contamination is confirmed and systemic, recommend:

**`ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001`**

Scope for that lane (not done here):
- Enumerate all 22 contaminated specs and their intended (titled) features.
- For each, recover the real spec from an **authoritative source** (operator /
  original PR / external doc) — never reconstruct from memory.
- Preserve the canonical `MCP-005` taxonomy untouched.
- Record which specs were reconstructed, deprecated, or pending source.

## Boundaries

- This audit **did not** rewrite, delete, or reconstruct any spec.
- No runtime/provider behavior was inspected for correctness; this is a docs
  integrity audit only.
- Finding does not affect smoke or public-exposure gating (ISS-001 is P2 docs
  integrity), but the specs cannot be trusted as feature documentation until
  reconciled.
