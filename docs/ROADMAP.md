# Roadmap

> Refreshed **2026-07-08** for `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001`.
> Source of truth for current state: [`CURRENT_STATE.md`](CURRENT_STATE.md).
> This roadmap makes no readiness, provider-validation, benchmark, production, or Alpha-superiority claims.

## Current phase

**Post-#676 north-star roadmap reset.** The current selected next state is `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`.

The post-#663 through post-#676 Operator Console sequence is recorded as adjacent/supporting local-first visibility and operator-status work. It does not automatically select B012, B013, a real-run cockpit, a provider execution lane, or any UI implementation lane.

Alpha Solver remains centered on reasoning/routing plus discrimination/evidence. B012/B013-style cockpit work is deferred pending operator product-direction selection. This roadmap reset authorizes no runtime behavior change, `/v1/solve` exposure, scoring, unblinding, final interpretation, or broad project claims.

## Current next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`** - operator review is required before choosing the next product direction. Candidate directions are recorded in `docs/evals/runs/as-post-676-north-star-roadmap-reset-001/product-direction-options.md`.

## Near-term roadmap after reset

1. Operator chooses one product direction from the post-#676 reset options.
2. If the operator chooses Value Read/discrimination workbench, create a separate scoped design or implementation lane.
3. If the operator chooses route/expert-preview control surface, create a separate scoped design or implementation lane.
4. If the operator chooses bounded smoke-test cockpit, first define execution, budget, receipt, and no-playground boundaries in a separate authorization lane.
5. Keep B012/B013-style cockpit work deferred until the operator explicitly selects that path.
6. Continue open deferrals only through their own scoped lanes.

## Historical near-term roadmap before the post-#676 reset

The prior roadmap item `ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001` is preserved as historical pre-reset context only. It is not the current selected next lane after `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001`.

## Active deferrals

See [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md).

- **DEF-001** - Self Operator execution evidence: advanced within local-only scope; not broad runtime proof.
- **DEF-002** - Security/privacy review: open.
- **DEF-003** - Fable delta-audit custody/replacement: open.
- **DEF-004** - Audit custody/provenance: open.

---

## Historical (pre-#100) - preserved, not current

The entries below reference the old org path `github.com/alpha-solver/alpha-solver` and predate the current evidence chain. Preserved for history only.

### Done (MVP: P0 & P1) - historical

- Metrics exporter and dashboards (PR #99)
- Prompt quality evaluator (PR #98)
- Replay CLI and diff utilities (PR #97)
- Budget guard and CLI (PR #96)
- Deterministic weight tuning harness (PR #95)
- Evidence pack store (PR #93)
- Clarify templates and trigger (PR #92)
- Determinism harness (PR #91)

### Next (P1/P2) - historical wishlist

- Rich MCP adapter library - expand tool coverage with tests.
- Advanced budget modeling - per-route and per-token projections.
- Policy engine v2 - granular gates with audit trail.
- Scenario runner - compose multi-step evaluation flows.
