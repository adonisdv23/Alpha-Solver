# Contamination evidence

`MCP-005` is the canonical Error-Taxonomy spec. The 22 specs below carry that same
`Goal`/`Acceptance Criteria`/`Design`/`Tests` body under unrelated titles; only the
`## Code Targets` line differs (and correctly matches each file's real feature).

Canonical: `MCP-005` body hash = `a7c9ca95240e` (`service/mcp/error_taxonomy.py`,
`tests/test_mcp_errors.py`).

The two specifically named in the lane brief are confirmed:

- **`MCP-002`** — title "Router decision rule (MCP)", body = MCP-005 Error Taxonomy.
- **`NEW-010`** — title "Section-Specific Prompt Decks (RES_01)", body = MCP-005
  Error Taxonomy.

| Spec | Titled feature (authentic) | Normalized body hash | Relationship to MCP-005 |
|------|----------------------------|----------------------|-------------------------|
| `MCP-001` | MCP Registry Loader & Wiring (MCP) | `d8f98b83401a` | + prior hygiene note |
| `MCP-002` | Router decision rule (MCP) | `a7c9ca95240e` | body == MCP-005 |
| `MCP-003` | MCP OAuth/Secrets scaffold (auth surface) (MCP) | `a7c9ca95240e` | body == MCP-005 |
| `MCP-004` | Sandbox Limits (policy guardrail) (MCP) | `a7c9ca95240e` | body == MCP-005 |
| `MCP-006` | Retry & Backoff (MCP) | `a7c9ca95240e` | body == MCP-005 |
| `MCP-007` | MCP Observability hooks (MCP) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-009` | Clarify Templates Pack (RES_02) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-010` | Section-Specific Prompt Decks (RES_01) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-011` | Weight-Tuning Harness (RES-03 scoring) (RES_03) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-012` | Budget CLI + CI Guard (RES_07) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-013` | Replay CLI + Trace Diff (text viewer) (RES_07) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-014` | Evidence Pack Store (catalog + retrieval) (RES_07) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-015` | Determinism Harness (exact replay & drift detector) (RES_07) | `a7c9ca95240e` | body == MCP-005 |
| `NEW-016` | Grafana Dashboards Pack (metrics + sample boards) (RES_07) | `e51b49782566` | + prior hygiene note |
| `NEW-017` | Prompt Quality Pack (rubrics + evaluator) (RES_01) | `a7c9ca95240e` | body == MCP-005 |
| `RES-03` | Decision Rules & Scoring (RES) | `a7c9ca95240e` | body == MCP-005 |
| `RES-04` | Confidence & Budget Gates (RES) | `a7c9ca95240e` | body == MCP-005 |
| `RES-05` | Tool Adapters (Playwright, GSheets) — MVP stubs (RES) | `a7c9ca95240e` | body == MCP-005 |
| `RES-06` | Scenario Pack & Showcase (record/replay + rubric) (RES) | `a7c9ca95240e` | body == MCP-005 |
| `RES-07` | Observability (route_explain + JSONL replay) (RES) | `a7c9ca95240e` | body == MCP-005 |
| `RES-08` | Budget Simulator + Evidence Pack (RES) | `a7c9ca95240e` | body == MCP-005 |
| `AS-145` | Tool Adapters: Playwright + GSheets (MVP hardening) (RES_05) | `a7c9ca95240e` | body == MCP-005 |

21 files (canonical `MCP-005` plus 20 contaminated specs) share body hash
`a7c9ca95240e` byte-for-byte. `MCP-001` and `NEW-016` carry the same Error-Taxonomy
body but hash differently only because a prior pass already prepended a hygiene
note. No other duplicate body cluster exists anywhere in `.specs/`.
