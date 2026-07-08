# Roadmap

> Refreshed **2026-07-08** for `AS-POST-676-NORTH-STAR-ROADMAP-RESET-001`.
> The old PR #91–#99 list below is **historical** and no longer the current
> roadmap. Source of truth for current state:
> [`CURRENT_STATE.md`](CURRENT_STATE.md). This roadmap makes **no** readiness,
> provider-validation, or benchmark claims.

## Current phase

**Post-#676 north-star roadmap reset.** The current selected next state is `OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`. The post-#663 through post-#676 Operator Console sequence is recorded as adjacent/supporting local-first visibility and operator-status work. It does not automatically select B012, B013, a real-run cockpit, a provider execution lane, or any UI implementation lane.

Alpha Solver remains centered on reasoning/routing plus discrimination/evidence. B012/B013-style cockpit work is deferred pending operator product-direction selection. No provider calls, hosted/local model runs, `/v1/solve` exposure, scoring, unblinding, final interpretation, readiness/value/superiority claims, provider/local-model validation claims, production/public claims, or security/privacy claims are authorized by this roadmap reset.

## Current next state

**`OPERATOR_REVIEW_REQUIRED_AFTER_POST_676_NORTH_STAR_ROADMAP_RESET_001`** — operator review is required before choosing the next product direction. Candidate directions are recorded in `docs/evals/runs/as-post-676-north-star-roadmap-reset-001/product-direction-options.md`: bounded smoke-test cockpit, Value Read/discrimination workbench, route and expert-preview control surface, CLI/artifact operator companion, full real-run Operator Cockpit, and read-only status checkpoint.

## Active deferrals

See [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md).

- **DEF-001** — Self Operator execution evidence: advanced (local-only); not provider/runtime proof.
- **DEF-002** — Security/privacy review: open.
- **DEF-003** — Fable delta-audit custody/replacement: open.
- **DEF-004** — Audit custody/provenance: open.

## Near-term roadmap (docs-only governance / Value Read packet phase)

1. Create the controlled Value Read execution authorization packet/lane: `ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001`.
2. Keep no-echo, false-premise, hidden-constraint, confidence, needs-human, higher-headroom, and claim-safety boundaries explicit in any later packet.
3. Keep local Ollama work as scaffold/design unless a future operator-managed lane separately authorizes a local run.
4. Keep provider calls, hosted/local model runs, public surfaces, and Google Sheets mutation out of scope until separately authorized.
5. Continue DEF-002/DEF-003/DEF-004 only through their own scoped lanes.

---

## Historical (pre-#100) — preserved, not current

> ⚠️ **Stale links below.** These entries reference an old org path
> `github.com/alpha-solver/alpha-solver` (wrong org; the repo is
> `adonisdv23/Alpha-Solver`) and predate the current evidence chain. Preserved
> for history only (ISS-002).

### Done (MVP: P0 & P1) — historical

- Metrics exporter and dashboards (PR #99) *(stale link)*
- Prompt quality evaluator (PR #98) *(stale link)*
- Replay CLI and diff utilities (PR #97) *(stale link)*
- Budget guard and CLI (PR #96) *(stale link)*
- Deterministic weight tuning harness (PR #95) *(stale link)*
- Evidence pack store (PR #93) *(stale link)*
- Clarify templates and trigger (PR #92) *(stale link)*
- Determinism harness (PR #91) *(stale link)*

### Next (P1/P2) — historical wishlist

- Rich MCP adapter library – expand tool coverage with tests.
- Advanced budget modeling – per-route and per-token projections.
- Policy engine v2 – granular gates with audit trail.
- Scenario runner – compose multi-step evaluation flows.
