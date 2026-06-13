# Issue Register

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Every issue below was **verified against
> committed repo files** (audit findings treated as hypotheses, not proof).
> Status ∈ {CONFIRMED, PARTIALLY_CONFIRMED}. This is a docs-only register — **no
> runtime/security/code fixes are made here**; each routes to a future lane or
> DEF-002 review. Severity uses P0/P1/P2/P3/Info. No issue is rated P0 because no
> public/runtime surface is currently exposed.
>
> Columns: **smoke** = blocks the next tiny synthetic OpenAI smoke? **public** =
> blocks public/runtime/provider exposure (`/v1/solve`, dashboards)?

| id | sev | title | status | evidence path | owner / next lane | immediate action | smoke | public |
|----|-----|-------|--------|---------------|-------------------|------------------|-------|--------|
| ISS-001 | P2 | Spec contamination (systemic) | CONFIRMED | **22** `.specs/` files (incl. `MCP-002.md`, `NEW-010.md`, and `MCP-001/003/004/006/007`, `NEW-009`–`017`, `RES-03`–`08`, `AS-145`) carry the `.specs/MCP-005.md` Error-Taxonomy body under unrelated titles. See [`SPECS_HEALTH_AUDIT.md`](SPECS_HEALTH_AUDIT.md) | `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001` | Flag all 22 specs; do **not** rewrite from memory; reconcile from authoritative source | No | No |
| ISS-002 | P3 | Stale roadmap | CONFIRMED | `docs/ROADMAP.md` (PRs #91–#99 as "current"; links to `github.com/alpha-solver/alpha-solver` wrong org) | docs maintainer | Refreshed in this lane (history preserved, links marked stale) | No | No |
| ISS-003 | P2 | CORS default risk | CONFIRMED | `alpha/core/config.py` (`origins` default `os.getenv("SERVICE_CORS_ORIGINS","*")`), `service/app.py` (`allow_credentials=True`, `allow_methods=["*"]`) | DEF-002 review | Record as security input; lock down before any exposure | No | Yes |
| ISS-004 | P2 | Plaintext file secrets risk | CONFIRMED | `alpha/webapp/routes/settings.py` `FileSecretsBackend._write` stores raw provider keys as plaintext JSON (masking only on display/audit) | DEF-002 review | Record secrets-at-rest input; not committed to repo (gitignored path) | No | Yes (if dashboard/secrets surface exposed) |
| ISS-005 | P3 | Provider telemetry prompt-content risk | PARTIALLY_CONFIRMED (default-safe) | `alpha/providers/telemetry.py` is allowlist-based and "never inspects provider request/response payloads"; **no prompt-content field**. Residual opt-in/verbose/debug paths not exhaustively reviewed | DEF-002 review | Confirm no opt-in verbose path logs prompts; default path is safe | No | Review before public |
| ISS-006 | P2 | Commit-signing test hermeticity | CONFIRMED | `git config commit.gpgsign=true`, `gpg.ssh.program=/tmp/code-sign`; throwaway-repo tests fail (documented in PR #497): `tests/test_smoke_quickstart.py::test_release_script`, `tests/test_tag_release.py::test_tag_release` | test-hermeticity fix lane (not this lane) | Record; tests must not be edited here | No | No |
| ISS-007 | P3 | Hardcoded pricing | PARTIALLY_CONFIRMED | `service/finops/pricing.py` loads `config/cost_models.yaml` (config-driven) **but** hardcodes `MODEL_SETS` (openai/gpt-4o, gpt-4o-mini); `alpha/core/config.py` `cost_per_token`/`cost_per_ms` defaults | pricing review | Record; consolidate pricing source-of-truth later | No | No |
| ISS-008 | P2 | Duplicate provider/adapter surfaces | CONFIRMED | `alpha/providers/{openai,base,fake,accounting,safeout,telemetry}.py`, `alpha/local_llm/provider_adapter.py`, plus `service/adapters/`, `service/mcp/` | alpha/service architecture map | Map surfaces; pick canonical adapter before public | No | No (adds risk before public) |
| ISS-009 | P2 | Sanitizer Unicode normalization gap | CONFIRMED | `alpha/self_operator/redaction.py` uses regex-only redaction; **no `unicodedata`/NFKC normalization** (homoglyph/escape evasion possible) | DEF-002 review | Record redaction-evasion input | No | Yes |
| ISS-010 | P3 | Orphaned / duplicate MVP docs | PARTIALLY_CONFIRMED | `docs/MVP_READINESS_CHECKPOINT.md` vs `.specs/MVP-READINESS-CHECKPOINT-001.md`; `docs/MVP_TESTER_HANDOFF.md`; `.specs/MVP-CLOSEOUT-001.md` | docs archive/dedup | Route to `ARCHIVE_INDEX.md`; point to source-of-truth | No | No |
| ISS-011 | Info | Stale branches / refs | CONFIRMED | GitHub `list_branches`: 60+ branches incl. merged `codex/*`, `claude/*`, `adonisdv23-patch-{1,2,3}`, `batch-c-artifact-20260605` | operator (branch cleanup) | Operator decision; no docs action deletes branches | No | No |
| ISS-012 | P2 | alpha/service stack overlap | CONFIRMED | Both `alpha/` and `service/` contain providers, finops, observability, determinism, prompts, validation | alpha/service architecture map | Map two stacks; document canonical runtime path | No | No |
| ISS-013 | P3 | Backlog / lane status drift | CONFIRMED | Many per-packet `selected-next-lane.md` snapshots; no single current-state source before this lane | this lane (`LANE_REGISTRY.md`, `CURRENT_STATE.md`) | Maintain the new registries as source-of-truth | No | No |
| ISS-014 | Info | Checker coverage gaps after PR #508 | PARTIALLY_CONFIRMED | `scripts/check_local_llm_*.py` scan only `local_llm_*`, `alpha-solver-post-*`, `openai-*` prefixes; top-level `docs/*.md` governance files and the `alpha-solver-current-state-*` packet are **out of scope by design** | optional checker-scope lane (not this lane) | Record residual scope gap; no checker edit here | No | No |
| ISS-015 | P1 | OpenAI project/billing verification blocker | CONFIRMED | PR #509 `local-openai-token-smoke-capture-retry-001` → `BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED` | **`OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001`** | Operator clarifies project + billing readiness before any call | Yes | n/a (precondition) |

## Severity rationale

- **P1 (ISS-015)** is the only blocker of the current objective (first tiny
  smoke). It is a precondition, not a code defect.
- **P2** items (ISS-001, 003, 004, 006, 008, 009, 012) matter for docs integrity,
  test hermeticity, architecture clarity, or **before any public/provider
  exposure**, but do not block a narrow synthetic smoke.
- **P3 / Info** items are cleanup, drift, or known-by-design scope limits.

## Not overstated

ISS-005 is explicitly **not** rated as a confirmed prompt-content leak: the
default telemetry path is allowlist-safe. ISS-007 and ISS-010 are
**PARTIALLY_CONFIRMED** and scoped narrowly. No issue here asserts DEF-002/DEF-003
resolution, provider/runtime readiness, or any forbidden claim.
