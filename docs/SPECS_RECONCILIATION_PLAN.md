# Specs Reconciliation Plan

> Owner lane: `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001` (2026-06-13).
> Companion to [`SPECS_HEALTH_AUDIT.md`](SPECS_HEALTH_AUDIT.md).
> This plan **routes** reconciliation; it performs **no** spec rewrite, reconstruction,
> or deletion. Those happen (if approved) in the next lane.

## Problem

22 `.specs/*.md` files carry the **MCP-005 Error Taxonomy** body under unrelated titles
(`SPEC_CONTAMINATED`). Their authentic per-feature spec text is therefore missing. This
lane has marked all 22 non-authoritative (banner under title, body preserved) and
indexed them; what remains is to recover the real spec text for each.

## Reconciliation principles (hard rules)

1. **Never reconstruct a spec from memory** and never invent an "original intent".
2. Reconstruct **only** from an authoritative in-repo source: the feature's committed
   **code + tests** (the `## Code Targets`), and/or the originating PR / external doc.
3. **Preserve** contaminated bodies (do not delete); supersede them in place.
4. Keep `MCP-005` (canonical) untouched as the taxonomy source of truth.
5. Filenames are stable identifiers — **do not rename or move** specs (`.specs/README.md`).

## Feasibility (verified)

For all 22, every `## Code Targets` implementation **and** test file is present in the
repo. Reconstruction from committed code+tests is therefore feasible for the whole set;
none is blocked on a missing source. The disposition (reconstruct vs deprecate) is an
operator decision (below).

## Per-spec reconciliation routing (22)

`Reconstruct from` lists the in-repo authoritative source to derive the real spec from.

| Spec | Titled feature | Reconstruct from (impl) | Reconstruct from (tests) |
|------|----------------|-------------------------|--------------------------|
| `MCP-001` | MCP Registry Loader & Wiring (MCP) | `registries/mcp/loader.py`, `service/mcp/wiring.py` | `tests/test_mcp_loader.py` |
| `MCP-002` | Router decision rule (MCP) | `registries/mcp/registry_lookup.py` | `tests/test_mcp_router_rule.py` |
| `MCP-003` | MCP OAuth/Secrets scaffold (auth surface) (MCP) | `service/mcp/policy_auth.py` | `tests/test_mcp_auth.py` |
| `MCP-004` | Sandbox Limits (policy guardrail) (MCP) | `service/mcp/sandbox_limits.py` | `tests/test_mcp_sandbox.py` |
| `MCP-006` | Retry & Backoff (MCP) | `service/mcp/retry_backoff.py` | `tests/test_mcp_retry.py` |
| `MCP-007` | MCP Observability hooks (MCP) | `service/mcp/observability.py` | `tests/test_mcp_observability.py` |
| `NEW-009` | Clarify Templates Pack (RES_02) | `service/clarify/trigger.py`, `service/clarify/templates.yaml`, `service/clarify/render.py` | `tests/test_clarify.py` |
| `NEW-010` | Section-Specific Prompt Decks (RES_01) | `service/prompts/decks.yaml`, `service/prompts/selector.py`, `service/prompts/renderer.py` | `tests/test_prompt_decks.py` |
| `NEW-011` | Weight-Tuning Harness (RES-03 scoring) (RES_03) | `service/scoring/tuning.py`, `config/tuning.yaml` | `tests/test_weight_tuning.py` |
| `NEW-012` | Budget CLI + CI Guard (RES_07) | `service/budget/guard.py`, `service/budget/cli.py` | `tests/test_budget_cli_guard.py` |
| `NEW-013` | Replay CLI + Trace Diff (text viewer) (RES_07) | `service/observability/replay_cli.py`, `service/observability/diff.py` | `tests/test_replay_cli_diff.py` |
| `NEW-014` | Evidence Pack Store (catalog + retrieval) (RES_07) | `service/evidence/store.py`, `service/evidence/index.jsonl`, `service/evidence/api.py` | `tests/test_evidence_store.py` |
| `NEW-015` | Determinism Harness (exact replay & drift detector) (RES_07) | `service/determinism/harness.py`, `service/determinism/report.py`, `config/determinism.yaml` | `tests/test_determinism.py` |
| `NEW-016` | Grafana Dashboards Pack (metrics + sample boards) (RES_07) | `service/metrics/exporter.py`, `dashboards/alpha_observability.json`, `dashboards/cost_budget.json` | `tests/test_metrics_dashboards.py` |
| `NEW-017` | Prompt Quality Pack (rubrics + evaluator) (RES_01) | `service/prompts/quality/rubrics.yaml`, `service/prompts/quality/evaluator.py`, `service/prompts/quality/report.py` | `tests/test_prompt_quality.py` |
| `RES-03` | Decision Rules & Scoring (RES) | `service/scoring/decision_rules.py`, `config/decision_rules.yaml` | `tests/test_decision_rules.py` |
| `RES-04` | Confidence & Budget Gates (RES) | `service/gating/gates.py`, `alpha_solver_cli.py` | `tests/test_gates.py` |
| `RES-05` | Tool Adapters (Playwright, GSheets) — MVP stubs (RES) | `service/adapters/base.py`, `service/adapters/playwright_adapter.py`, `service/adapters/gsheets_adapter.py` | `tests/test_adapters_playwright.py`, `tests/test_adapters_gsheets.py` |
| `RES-06` | Scenario Pack & Showcase (record/replay + rubric) (RES) | `service/scenarios/runner.py`, `service/scenarios/rubric.py`, `scenarios/pack.yaml` | `tests/test_scenarios.py` |
| `RES-07` | Observability (route_explain + JSONL replay) (RES) | `service/observability/logger.py`, `service/observability/replay.py` | `tests/test_observability.py` |
| `RES-08` | Budget Simulator + Evidence Pack (RES) | `service/budget/simulator.py`, `service/evidence/collector.py`, `config/cost_models.yaml` | `tests/test_budget_simulator.py`, `tests/test_evidence_pack.py` |
| `AS-145` | Tool Adapters: Playwright + GSheets (MVP hardening) (RES_05) | `service/adapters/base.py`, `service/adapters/playwright_adapter.py`, `service/adapters/gsheets_adapter.py` | `tests/test_adapters_playwright_hardened.py`, `tests/test_adapters_gsheets_hardened.py` |

## Operator decision required (disposition)

Choose one disposition per spec (or one for the whole set) before the reconstruction lane acts:

- **A. Reconstruct** the real spec from committed code+tests (recommended — sources exist).
- **B. Deprecate/Archive** the spec as historical (if the feature is frozen/retired).
- **C. Delete** as a duplicate (NOT performed by these lanes without explicit operator
  instruction; `.specs/README.md` forbids casual removal).

## Next lane

`ALPHA-SOLVER-SPEC-SOURCE-RECONSTRUCTION-001` — for each spec dispositioned **A**,
draft the real `Goal / Motivation / Acceptance Criteria / Definition of Done /
Code Targets / Test Plan` strictly from its committed code+tests, replacing the
contaminated body while keeping the filename. One spec per reviewable change; cite the
source files in each diff.

## What this lane did NOT do

- Did not rewrite, reconstruct, or delete any spec body.
- Did not modify `MCP-005` or any runtime/product code, test, or CI file.
- Did not call any provider; used no tokens; made no readiness claim.

