# Roadmap

> Refreshed **2026-06-15** for the post-#568 blocked Value Read state.
> The old PR #91–#99 list below is **historical** and no longer the current
> roadmap. Source of truth for current state:
> [`CURRENT_STATE.md`](CURRENT_STATE.md). This roadmap makes **no** readiness,
> provider-validation, or benchmark claims.

## Current phase

**Post-#568 blocked Value Read state.** Live GitHub verification on 2026-06-15 confirmed PRs #566, #567, and #568 are merged. PR #568 committed a manual Value Read artifact that stopped before output generation and scoring.

The prior infrastructure records no-echo gating, false-premise / hidden-constraint cases, claim-safety linting, calibrated-confidence vocabulary, needs-human protocol guidance, higher-headroom Value Read cases, prompt-contract simulation methodology, and a local Ollama singlepath scaffold. PR #568 does not add provider/model/value/readiness evidence; it records `VALUE_READ_BLOCKED` with no Alpha outputs, baseline outputs, blind scores, or discrimination-delta.

## Current next lane

**`ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001`** — create an explicitly authorized Value Read execution packet/lane with complete per-case prompts, raw-output preservation, blinding-map storage, output-generation boundary, and explicit operator authorization requirements. This is controlled authorization/design work only until a future authorization supplies execution boundaries; it does not authorize provider calls, token use, credential access, billing inspection, hosted model calls, local model calls, dashboard exposure, `/v1/solve` exposure, public API exposure, Google Sheets mutation, benchmark execution, or value/readiness claims by itself.

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
