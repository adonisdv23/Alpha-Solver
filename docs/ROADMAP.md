# Roadmap

> Refreshed **2026-06-13** by lane
> `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> The old PR #91–#99 list below is **historical** and no longer the current
> roadmap. Source of truth for current state:
> [`CURRENT_STATE.md`](CURRENT_STATE.md). This roadmap makes **no** readiness,
> provider-validation, or benchmark claims.

## Current phase

**Post-local Self Operator evidence; pre-first real OpenAI smoke; blocked on
OpenAI project/billing clarification after PR #509.**

- Local/offline Self Operator execution evidence captured (PRs #497, #499, #500,
  #501) — no provider/model/token.
- OpenAI governance/pre-smoke chain captured (PRs #502–#508).
- First real-token smoke retry (PR #509) **halted before any provider call**
  (`BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED`).

## Current next lane

**`OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001`** — docs/operator
clarification of OpenAI project + billing readiness. **No provider call.**

Then (only if clarified): `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` (first real
call attempt; proves plumbing only). Highest strategic value after smoke:
`ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001`.

## Active deferrals

See [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md).

- **DEF-001** — Self Operator execution evidence: advanced (local-only); not
  provider/runtime proof.
- **DEF-002** — Security/privacy review: open.
- **DEF-003** — Fable delta-audit custody/replacement: open.
- **DEF-004** — Audit custody/provenance: open.

## Near-term roadmap (docs-only governance phase)

1. Clarify OpenAI project/billing boundary (next lane).
2. Tiny synthetic OpenAI smoke (plumbing only) once clarified.
3. Design `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` (Alpha vs plain baseline;
   verbosity-controlled; blind-scored). See
   [`VALUE_EXPERIMENT_DIRECTION.md`](VALUE_EXPERIMENT_DIRECTION.md).
4. DEF-002 security/privacy review (assessment + gap closure of existing
   machinery). See [`DEF_002_SECURITY_PRIVACY_INPUTS.md`](DEF_002_SECURITY_PRIVACY_INPUTS.md).
5. `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001` (see
   [`SPECS_HEALTH_AUDIT.md`](SPECS_HEALTH_AUDIT.md)).
6. Technical-debt items (alpha/service map, pricing, redaction hardening, test
   hermeticity). See [`TECHNICAL_DEBT_AND_RUNTIME_NOTES.md`](TECHNICAL_DEBT_AND_RUNTIME_NOTES.md).

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
