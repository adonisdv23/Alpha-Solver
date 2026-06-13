# Archive Index

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**.
>
> **Archive = remove from the active backlog/queue, NOT delete.** No evidence
> packet is ever deleted, and historical evidence content is never mutated.
> Statuses: `KEEP_ACTIVE` · `CURRENT_CONTROL_SOURCE` · `COMPLETED_KEEP_AS_EVIDENCE`
> · `ARCHIVE_HISTORICAL` · `SUPERSEDED_BY_NEWER_EVIDENCE` ·
> `REMOVE_FROM_ACTIVE_BACKLOG` · `NEEDS_OPERATOR_DECISION` · `DO_NOT_TOUCH`.

## Current control source

| Item | Status |
|------|--------|
| `docs/evals/runs/local-openai-token-smoke-capture-retry-001/` (PR #509) and its `selected-next-lane.md` | **CURRENT_CONTROL_SOURCE** |
| `docs/CURRENT_STATE.md`, `EVIDENCE_INDEX.md`, `LANE_REGISTRY.md`, `DEFERRAL_REGISTER.md`, `ISSUE_REGISTER.md` (this lane) | **KEEP_ACTIVE** |

## Completed evidence packets (keep, off active queue)

| Item | Status |
|------|--------|
| `…execution-evidence-004` (PR #501) | COMPLETED_KEEP_AS_EVIDENCE |
| `alpha-solver-openai-free-token-eval-smoke-harness-plan-001` (PR #502) | COMPLETED_KEEP_AS_EVIDENCE |
| `…def-002-def-003-evidence-boundary-001` (PR #503) | COMPLETED_KEEP_AS_EVIDENCE |
| `openai-data-sharing-operator-verification-001` (PR #504) | COMPLETED_KEEP_AS_EVIDENCE |
| `openai-synthetic-smoke-prompt-fixture-001` (PR #506) | COMPLETED_KEEP_AS_EVIDENCE |
| `openai-data-sharing-operator-attestation-001` (PR #507) | COMPLETED_KEEP_AS_EVIDENCE |
| `openai-packet-checker-scope-001` (PR #508) | COMPLETED_KEEP_AS_EVIDENCE |

## Historical / superseded (preserved)

| Item | Status |
|------|--------|
| `…execution-evidence-001 / 002 / 003` (PRs #497, #499, #500) | ARCHIVE_HISTORICAL (earlier links in a completed local chain) |
| `local-openai-token-smoke-capture-001` (PR #505, blocked: attestation missing) | SUPERSEDED_BY_NEWER_EVIDENCE (by #507→#508→#509) — keep as evidence |
| All `selected-next-lane.md` files in packets **older than PR #509** | ARCHIVE_HISTORICAL (non-controlling snapshots; only #509's is current) |
| Local qwen manual-smoke retry chain `docs/evals/runs/20260606-alpha-local-llm-…-manual-smoke-retry-{002..007}-…` | DO_NOT_TOUCH (preserved source artifacts; non-promotional Level-3 evidence) |
| Older OpenAI planning packets (#502) relative to attestation/checker packets (#507/#508) | SUPERSEDED_BY_NEWER_EVIDENCE (planning superseded by governance; keep as evidence) |

## Stale docs / sections

| Item | Status |
|------|--------|
| `docs/ROADMAP.md` "Done (MVP P0 & P1)" + #91–#99 links | ARCHIVE_HISTORICAL (refreshed in place this lane; old content kept under a "Historical" heading, broken org links marked stale) |
| `docs/MVP_READINESS_CHECKPOINT.md` ↔ `.specs/MVP-READINESS-CHECKPOINT-001.md` overlap (ISS-010) | NEEDS_OPERATOR_DECISION (which is source-of-truth?) |
| `docs/MVP_TESTER_HANDOFF.md`, `.specs/MVP-CLOSEOUT-001.md` | NEEDS_OPERATOR_DECISION (dedup vs keep both) |

## Specs

| Item | Status |
|------|--------|
| `.specs/MCP-002.md`, `.specs/NEW-010.md` (contaminated with MCP-005 body, ISS-001) | NEEDS_OPERATOR_DECISION → reconcile via `ALPHA-SOLVER-SPEC-CONTAMINATION-RECONCILIATION-001` (do **not** delete or rewrite from memory) |
| `.specs/MCP-005.md` (canonical Error Taxonomy) | DO_NOT_TOUCH (source of truth for the taxonomy body) |

## Branches / refs

| Item | Status |
|------|--------|
| 60+ remote branches incl. merged `codex/*`, `claude/*`, `adonisdv23-patch-*`, `batch-c-artifact-*` (ISS-011) | NEEDS_OPERATOR_DECISION / REMOVE_FROM_ACTIVE_BACKLOG (branch cleanup is an operator action; this docs lane does not delete branches) |

## Rules

- Nothing in this index is a deletion recommendation for any evidence packet.
- `DO_NOT_TOUCH` items are preserved source artifacts or canonical sources.
- `NEEDS_OPERATOR_DECISION` items require a human choice before any change.
