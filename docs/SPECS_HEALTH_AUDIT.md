# Specs Health Audit

> Owner lane: `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001`.
> Supersedes the initial audit from
> `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Audited `.specs/` against committed file bodies
> (read-only hashing; no spec rewritten from memory; no spec deleted).
>
> Classifications used: `SPEC_OK` · `SPEC_CONTAMINATED` · `SPEC_DUPLICATE_BODY` ·
> `SPEC_STALE` · `SPEC_NEEDS_OPERATOR_DECISION` · `SPEC_NEEDS_SOURCE_RECONSTRUCTION`.

Companion docs: [`SPECS_RECONCILIATION_PLAN.md`](SPECS_RECONCILIATION_PLAN.md) ·
evidence packet [`docs/evals/runs/alpha-solver-spec-contamination-reconciliation-001/`](evals/runs/alpha-solver-spec-contamination-reconciliation-001/).

## Headline finding (CONFIRMED — systemic)

The hypothesis that `.specs/` files carry the **MCP-005 Error Taxonomy** body under
unrelated titles is **CONFIRMED and systemic**. The task's specific question is
answered: **`MCP-002` and `NEW-010` both carry the MCP-005 body** under their own
(unrelated) titles, as do 20 other specs.

- **83** `.md` files in `.specs/` (81 specs + 2 registry/meta files `INDEX.md`, `README.md`).
- **23** files contain the Error-Taxonomy signature `"Create a stable MCP error taxonomy"`.
- **1** is the legitimate source: `MCP-005 · Error Taxonomy (MCP)`.
- **22** carry that same `Goal`/`Acceptance Criteria`/`Design`/`Tests` body under unrelated
  titles — only the `## Code Targets` line differs and matches each file's real feature.

### Method (reproducible, read-only)

For every `.specs/*.md`, the body was normalized by removing (a) the H1 title line,
(b) a leading blockquote block before the first `## ` header — i.e. the
non-authoritative banner or any prior hygiene note — and (c) the `## Code Targets`
section, then SHA-1 hashed and clustered. Excluding the title, banner/note, and
targets isolates the *copied body*, so the hash is stable before and after the
banners were added. Result: **exactly one** multi-file body cluster — the MCP-005
Error Taxonomy body. Under this rule **all 23 taxonomy-bearing specs (canonical
`MCP-005` + 22 contaminated) hash to `a7c9ca95240e`** in the committed state
(`MCP-001` and `NEW-016` included). **No other duplicate or near-duplicate body
cluster exists** among the remaining specs, so cross-contamination is limited to
the Error-Taxonomy body. Reproduce with:

```bash
grep -rl "Create a stable MCP error taxonomy" .specs/   # -> 23 files (MCP-005 + 22)
python docs/evals/runs/alpha-solver-spec-contamination-reconciliation-001/reproduce-body-hash.py
# -> all 23 share normalized body hash a7c9ca95240e; RESULT: PASS
```

The exact normalization rule and a runnable implementation live in the evidence
packet: [`contamination-evidence.md`](evals/runs/alpha-solver-spec-contamination-reconciliation-001/contamination-evidence.md)
and [`reproduce-body-hash.py`](evals/runs/alpha-solver-spec-contamination-reconciliation-001/reproduce-body-hash.py).

### Decisive finding for remediation: the titled features exist in committed code

Every one of the 22 contaminated specs lists `## Code Targets` whose **implementation
and test files are all present in the repo**. The authentic feature each spec was
*supposed* to document therefore exists in committed code+tests — so the real spec can
be **reconstructed from an authoritative in-repo source** (code + tests), not from
memory. This is why the selected follow-up is source reconstruction, not index cleanup.

## Action taken by this lane (non-destructive)

All 22 contaminated specs now carry a standardized non-authoritative banner
immediately under their title:

```text
⚠️ NON-AUTHORITATIVE — CONTAMINATED SPEC (do not implement from this).
```

The contaminated body is **preserved unchanged** beneath the banner for forensic /
reconstruction use. `MCP-005` (canonical) was **not** modified. No spec was deleted.

## Classification summary

| Classification | Count | Members |
|----------------|-------|---------|
| `SPEC_OK` | 57 | 56 clean specs + `MCP-005` (canonical, `DO_NOT_TOUCH`) |
| `SPEC_CONTAMINATED` (+ `SPEC_NEEDS_SOURCE_RECONSTRUCTION`) | 22 | see detail table |
| `SPEC_NEEDS_OPERATOR_DECISION` | 2 | `MVP-READINESS-CHECKPOINT-001`, `MVP-CLOSEOUT-001` (doc overlap, ISS-010) |
| `SPEC_DUPLICATE_BODY` | 0 distinct | the 22 are a duplicate-body set, tracked under `SPEC_CONTAMINATED` |
| `SPEC_STALE` | 0 confirmed | not exhaustively assessed beyond contamination scope (see Boundaries) |
| `META` (not a spec) | 2 | `INDEX.md`, `README.md` |

> Note: the 22 contaminated specs are simultaneously `SPEC_DUPLICATE_BODY` (they share
> one body) and `SPEC_CONTAMINATED` (that body is foreign to their title). They are
> filed under `SPEC_CONTAMINATED` as the primary, actionable classification, with
> `SPEC_NEEDS_SOURCE_RECONSTRUCTION` as the remediation path.

## Contaminated specs — detail (22)

| Spec | Titled feature (authentic) | Impl targets present | Test targets present |
|------|----------------------------|----------------------|----------------------|
| `MCP-001` | MCP Registry Loader & Wiring (MCP) | ✅ | ✅ |
| `MCP-002` | Router decision rule (MCP) | ✅ | ✅ |
| `MCP-003` | MCP OAuth/Secrets scaffold (auth surface) (MCP) | ✅ | ✅ |
| `MCP-004` | Sandbox Limits (policy guardrail) (MCP) | ✅ | ✅ |
| `MCP-006` | Retry & Backoff (MCP) | ✅ | ✅ |
| `MCP-007` | MCP Observability hooks (MCP) | ✅ | ✅ |
| `NEW-009` | Clarify Templates Pack (RES_02) | ✅ | ✅ |
| `NEW-010` | Section-Specific Prompt Decks (RES_01) | ✅ | ✅ |
| `NEW-011` | Weight-Tuning Harness (RES-03 scoring) (RES_03) | ✅ | ✅ |
| `NEW-012` | Budget CLI + CI Guard (RES_07) | ✅ | ✅ |
| `NEW-013` | Replay CLI + Trace Diff (text viewer) (RES_07) | ✅ | ✅ |
| `NEW-014` | Evidence Pack Store (catalog + retrieval) (RES_07) | ✅ | ✅ |
| `NEW-015` | Determinism Harness (exact replay & drift detector) (RES_07) | ✅ | ✅ |
| `NEW-016` | Grafana Dashboards Pack (metrics + sample boards) (RES_07) | ✅ | ✅ |
| `NEW-017` | Prompt Quality Pack (rubrics + evaluator) (RES_01) | ✅ | ✅ |
| `RES-03` | Decision Rules & Scoring (RES) | ✅ | ✅ |
| `RES-04` | Confidence & Budget Gates (RES) | ✅ | ✅ |
| `RES-05` | Tool Adapters (Playwright, GSheets) — MVP stubs (RES) | ✅ | ✅ |
| `RES-06` | Scenario Pack & Showcase (record/replay + rubric) (RES) | ✅ | ✅ |
| `RES-07` | Observability (route_explain + JSONL replay) (RES) | ✅ | ✅ |
| `RES-08` | Budget Simulator + Evidence Pack (RES) | ✅ | ✅ |
| `AS-145` | Tool Adapters: Playwright + GSheets (MVP hardening) (RES_05) | ✅ | ✅ |

All 22 → `SPEC_CONTAMINATED` + `SPEC_NEEDS_SOURCE_RECONSTRUCTION`. Per-spec
reconstruction routing is in [`SPECS_RECONCILIATION_PLAN.md`](SPECS_RECONCILIATION_PLAN.md).

## Full specs health index (all 83 files)

This table is the specs health index requested by the lane. `META` rows are the two
registry files, not specs.

| # | Spec file | Classification | Note |
|---|-----------|----------------|------|
| 1 | `ALPHA-ANSWER-STRUCTURE-V2-001` | `SPEC_OK` | Unique body; no contamination detected |
| 2 | `ALPHA-BREVITY-CONTROL-001` | `SPEC_OK` | Unique body; no contamination detected |
| 3 | `ALPHA-CLARIFY-THRESHOLD-001` | `SPEC_OK` | Unique body; no contamination detected |
| 4 | `ALPHA-FORMAT-PRESERVATION-001` | `SPEC_OK` | Unique body; no contamination detected |
| 5 | `ALPHA-LIVE-EXPERT-STEP1-PARSE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 6 | `ALPHA-PRIMARY-ANSWER-EMPTY-001` | `SPEC_OK` | Unique body; no contamination detected |
| 7 | `ALPHA-SIDE-BY-SIDE-EVIDENCE-PACKET-001` | `SPEC_OK` | Unique body; no contamination detected |
| 8 | `AS-145` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 9 | `AS-148` | `SPEC_OK` | Unique body; no contamination detected |
| 10 | `AUTH-SESSION-001` | `SPEC_OK` | Unique body; no contamination detected |
| 11 | `CLARIFY-SURFACE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 12 | `DASHBOARD-LOGIN-REDIRECT-001` | `SPEC_OK` | Unique body; no contamination detected |
| 13 | `DEPLOY-CLOUDRUN-CONFIG-001` | `SPEC_OK` | Unique body; no contamination detected |
| 14 | `DEPLOY-CLOUDRUN-DASHBOARD-SECRET-GUARD-001` | `SPEC_OK` | Unique body; no contamination detected |
| 15 | `DEPLOY-LIVE-SPEND-GUARD-001` | `SPEC_OK` | Unique body; no contamination detected |
| 16 | `DISC-MRG-068` | `SPEC_OK` | Unique body; no contamination detected |
| 17 | `DISC-MRG-069` | `SPEC_OK` | Unique body; no contamination detected |
| 18 | `EPIC_RAG_001` | `SPEC_OK` | Unique body; no contamination detected |
| 19 | `EVAL-ARTIFACT-PRESERVE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 20 | `EVAL-BEHAVIORAL-DEMO-001` | `SPEC_OK` | Unique body; no contamination detected |
| 21 | `EVAL-DEMO-EVIDENCE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 22 | `EVAL-DEMO-FINDINGS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 23 | `EVAL-DEMO-POST-FIX-FINDINGS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 24 | `EVAL-DEMO-POST-FIX-RETEST-001` | `SPEC_OK` | Unique body; no contamination detected |
| 25 | `EVAL-DEMO-RUN-PACKET-001` | `SPEC_OK` | Unique body; no contamination detected |
| 26 | `EVAL-DIFFERENTIATION-RUN-001` | `SPEC_OK` | Unique body; no contamination detected |
| 27 | `FINOPS-BUDGET-001` | `SPEC_OK` | Unique body; no contamination detected |
| 28 | `HIGHER-HEADROOM-EVAL-001` | `SPEC_OK` | Unique body; no contamination detected |
| 29 | `INDEX` | `META` | Registry/index file — not a spec |
| 30 | `LOCAL-LLM-RUNTIME-INTEGRATION-001` | `SPEC_OK` | Unique body; no contamination detected |
| 31 | `LOCAL-LLM-SOLVER-ORCHESTRATION-001` | `SPEC_OK` | Unique body; no contamination detected |
| 32 | `MCP-001` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 33 | `MCP-002` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 34 | `MCP-003` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 35 | `MCP-004` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 36 | `MCP-005` | `SPEC_OK (canonical)` | Legitimate Error Taxonomy source — **DO_NOT_TOUCH** |
| 37 | `MCP-006` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 38 | `MCP-007` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 39 | `MCP-008` | `SPEC_OK` | Unique body; no contamination detected |
| 40 | `MVP-CLOSEOUT-001` | `SPEC_NEEDS_OPERATOR_DECISION` | Spec/doc overlap with `docs/` (ISS-010) |
| 41 | `MVP-READINESS-CHECKPOINT-001` | `SPEC_NEEDS_OPERATOR_DECISION` | Spec/doc overlap with `docs/` (ISS-010) |
| 42 | `NEW-009` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 43 | `NEW-010` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 44 | `NEW-011` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 45 | `NEW-012` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 46 | `NEW-013` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 47 | `NEW-014` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 48 | `NEW-015` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 49 | `NEW-016` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 50 | `NEW-017` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 51 | `NEW-024` | `SPEC_OK` | Unique body; no contamination detected |
| 52 | `NEW-045` | `SPEC_OK` | Unique body; no contamination detected |
| 53 | `NEW-HEALTH-001` | `SPEC_OK` | Unique body; no contamination detected |
| 54 | `NEW-RATE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 55 | `OBS-ALERTS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 56 | `OUTPUT-DIFF-A3-LIVE-CAPTURE-MODELSET-001` | `SPEC_OK` | Unique body; no contamination detected |
| 57 | `OUTPUT-DIFF-B1-LIFT-REPORTING-HARDENING-001` | `SPEC_OK` | Unique body; no contamination detected |
| 58 | `OUTPUT-DIFF-MEASUREMENT-HARDENING-001` | `SPEC_OK` | Unique body; no contamination detected |
| 59 | `PROVIDER-BUDGET-001` | `SPEC_OK` | Unique body; no contamination detected |
| 60 | `PROVIDER-EXPERT-PASS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 61 | `PROVIDER-OPENAI-001` | `SPEC_OK` | Unique body; no contamination detected |
| 62 | `PROVIDER-SAFEOUT-001` | `SPEC_OK` | Unique body; no contamination detected |
| 63 | `README` | `META` | Registry/index file — not a spec |
| 64 | `RES-03` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 65 | `RES-04` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 66 | `RES-05` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 67 | `RES-06` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 68 | `RES-07` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 69 | `RES-08` | `SPEC_CONTAMINATED` | MCP-005 body under wrong title; banner added; → reconstruction |
| 70 | `REVIEW-P0P1` | `SPEC_OK` | Unique body; no contamination detected |
| 71 | `SOLVE-EXPERT-EMPTY-ANSWER-GUARD-001` | `SPEC_OK` | Unique body; no contamination detected |
| 72 | `SOLVE-PROVIDER-FINAL-ANSWER-EMPTY-GUARD-001` | `SPEC_OK` | Unique body; no contamination detected |
| 73 | `SOLVE-SANITIZER-FALSE-POSITIVE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 74 | `UI-JOBS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 75 | `UI-KEYS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 76 | `UI-PREVIEW-001` | `SPEC_OK` | Unique body; no contamination detected |
| 77 | `UI-PREVIEW-LOADING-STATE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 78 | `UI-PREVIEW-LOCAL-SMOKE-001` | `SPEC_OK` | Unique body; no contamination detected |
| 79 | `UI-PREVIEW-REQUEST-METRICS-001` | `SPEC_OK` | Unique body; no contamination detected |
| 80 | `UI-PREVIEW-RESPONSE-LAYOUT-001` | `SPEC_OK` | Unique body; no contamination detected |
| 81 | `UI-REQ-001` | `SPEC_OK` | Unique body; no contamination detected |
| 82 | `UI-RUN-001` | `SPEC_OK` | Unique body; no contamination detected |
| 83 | `alpha-local-llm-provider-integration-spec` | `SPEC_OK` | Unique body; no contamination detected |

## `SPEC_NEEDS_OPERATOR_DECISION`

- **Disposition of the 22 contaminated specs** — reconstruct from code+tests (A),
  deprecate/archive (B), or delete as duplicates (C). This lane performs **no**
  deletion and **no** reconstruction; it only marks + indexes. The decision is the
  gate for `ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001`.
- **MVP spec/doc overlap** — `.specs/MVP-READINESS-CHECKPOINT-001.md` vs
  `docs/MVP_READINESS_CHECKPOINT.md`, and `.specs/MVP-CLOSEOUT-001.md` vs
  `docs/MVP_TESTER_HANDOFF.md` — tracked as ISS-010 in
  [`ARCHIVE_INDEX.md`](ARCHIVE_INDEX.md); not resolved here.

## Boundaries

- No spec was rewritten from memory; no original intended spec was invented.
- No spec was deleted; contaminated bodies are preserved verbatim under a banner.
- `MCP-005` (canonical taxonomy) was not touched.
- No runtime/product code, tests, or CI were modified; no provider calls; no tokens.
- `SPEC_STALE` was not exhaustively assessed beyond the contamination scope; the only
  duplicate-body cluster in `.specs/` is the Error-Taxonomy one (verified by hashing).
- This is a docs-integrity audit; it makes no runtime/provider/readiness claim.

