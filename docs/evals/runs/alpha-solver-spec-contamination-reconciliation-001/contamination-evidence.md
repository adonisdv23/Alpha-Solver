# Contamination evidence

`MCP-005` is the canonical Error-Taxonomy spec. The 22 specs below carry that same
`Goal` / `Acceptance Criteria` / `Design` / `Tests` body under unrelated titles;
only the `## Code Targets` line differs (and correctly matches each file's real
feature).

The two specifically named in the lane brief are confirmed:

- **`MCP-002`** — title "Router decision rule (MCP)", body = MCP-005 Error Taxonomy.
- **`NEW-010`** — title "Section-Specific Prompt Decks (RES_01)", body = MCP-005
  Error Taxonomy.

## Normalization rule (Approach B — reproducible against the committed PR state)

The hash below isolates the **copied contaminated body**, so it is identical for
`MCP-005` and for every contaminated copy, and is **stable before and after** the
non-authoritative banners were added. For each `.specs/*.md`, remove — in order:

1. the **H1 title** line (first line starting with `# `);
2. a **leading blockquote block** appearing before the first `## ` section header —
   this excludes the newly added `⚠️ NON-AUTHORITATIVE` banner **and** any prior
   hygiene note, neither of which is part of the copied body;
3. the **`## Code Targets`** section (its header through the line before the next
   `## ` header) — this is the one section that legitimately differs per file.

Then collapse runs of blank lines, strip surrounding whitespace, and take the
SHA-1 (first 12 hex) of the remainder.

Because the rule excludes the title, the banner/hygiene note, and Code Targets,
the surviving text is exactly the `Goal`/`Acceptance Criteria`/`Design`/`Tests`
block that was copied from `MCP-005`. Under this rule **all 23 taxonomy-bearing
specs (canonical `MCP-005` + 22 contaminated) hash to `a7c9ca95240e`** in the
final committed state.

## Reproduce

```bash
# 1. enumerate the taxonomy-bearing specs (23 = MCP-005 + 22 contaminated)
grep -rl "Create a stable MCP error taxonomy" .specs/ | sort

# 2. recompute the normalized contaminated-body hash for all of them
python docs/evals/runs/alpha-solver-spec-contamination-reconciliation-001/reproduce-body-hash.py
# -> distinct normalized body hashes: ['a7c9ca95240e'];  RESULT: PASS
```

The committed helper [`reproduce-body-hash.py`](reproduce-body-hash.py) implements
exactly the rule above (offline; reads only `.specs/`; no providers; no tokens).

## Evidence table

Canonical: `MCP-005` (`service/mcp/error_taxonomy.py`, `tests/test_mcp_errors.py`),
normalized body hash `a7c9ca95240e`.

| Spec | Titled feature (authentic) | Normalized body hash | Relationship to MCP-005 |
|------|----------------------------|----------------------|-------------------------|
| `MCP-001` | MCP Registry Loader & Wiring (MCP) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `MCP-002` | Router decision rule (MCP) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `MCP-003` | MCP OAuth/Secrets scaffold (auth surface) (MCP) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `MCP-004` | Sandbox Limits (policy guardrail) (MCP) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `MCP-006` | Retry & Backoff (MCP) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `MCP-007` | MCP Observability hooks (MCP) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-009` | Clarify Templates Pack (RES_02) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-010` | Section-Specific Prompt Decks (RES_01) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-011` | Weight-Tuning Harness (RES-03 scoring) (RES_03) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-012` | Budget CLI + CI Guard (RES_07) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-013` | Replay CLI + Trace Diff (text viewer) (RES_07) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-014` | Evidence Pack Store (catalog + retrieval) (RES_07) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-015` | Determinism Harness (exact replay & drift detector) (RES_07) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-016` | Grafana Dashboards Pack (metrics + sample boards) (RES_07) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `NEW-017` | Prompt Quality Pack (rubrics + evaluator) (RES_01) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `RES-03` | Decision Rules & Scoring (RES) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `RES-04` | Confidence & Budget Gates (RES) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `RES-05` | Tool Adapters (Playwright, GSheets) — MVP stubs (RES) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `RES-06` | Scenario Pack & Showcase (record/replay + rubric) (RES) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `RES-07` | Observability (route_explain + JSONL replay) (RES) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `RES-08` | Budget Simulator + Evidence Pack (RES) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |
| `AS-145` | Tool Adapters: Playwright + GSheets (MVP hardening) (RES_05) | `a7c9ca95240e` | copy of MCP-005 Error-Taxonomy body |

All 22 contaminated specs and the canonical `MCP-005` share the single normalized
body hash `a7c9ca95240e`. There is **no other** duplicate body cluster anywhere in
`.specs/`.

> Note on `MCP-001` and `NEW-016`: a prior pass (commit `a07d6b0`, #464) had
> already prepended a weaker hygiene note to these two, which is why an earlier
> draft of this packet recorded different raw hashes for them. This lane replaced
> those notes with the standardized banner, and the normalization rule above
> excludes any leading blockquote — so in the committed state both hash to
> `a7c9ca95240e` like the rest. No earlier-stage hashes are relied upon; the only
> authoritative figure is the reproducible `a7c9ca95240e` over the committed files.

## Evidence boundary (unchanged)

- Contaminated specs are marked **non-authoritative**; their bodies are
  **preserved unchanged** (the contaminated body is what the hash is computed over).
- No original intended spec is reconstructed or invented here.
- No spec is deleted. `MCP-005` remains canonical and untouched.
- Source reconstruction (recovering each real spec from committed code+tests)
  remains a **future lane**, `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001`.
