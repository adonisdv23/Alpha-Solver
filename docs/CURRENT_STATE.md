# Alpha Solver — Current State

> Source-of-truth navigation doc. Created by lane
> `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date: **2026-06-13**. Reflects committed `main` state plus
> read-only GitHub PR verification. Docs-only; no provider/runtime claims.

## Current verified phase

**Post-local Self Operator evidence; pre-first real OpenAI smoke; blocked on
OpenAI project/billing attestation retry after PR #511.**

- The Self Operator has a multi-PR local/offline execution-evidence chain
  (PRs #497, #499, #500, #501) that runs its test suite and release-gate CLI
  with **no provider, model, or token**.
- An OpenAI governance/pre-smoke chain (PRs #502–#508) captured the eval/smoke
  plan, data-sharing operator verification, operator pre-smoke attestation, a
  synthetic prompt fixture, and extended the static checkers to OpenAI packets.
- The first narrow real-token smoke attempt (PR #509) **halted before any
  provider call** with verdict `BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED`.
- The project/billing boundary clarification lane (PR #511) remained docs-only
  and blocked because operator confirmation was missing, with verdict
  `BLOCKED_PROJECT_BILLING_OPERATOR_CONFIRMATION_MISSING`.

No OpenAI/provider call has been executed. No value experiment has been run.

## At a glance

| Field | Value |
|-------|-------|
| Last merged PR | **#511** — `docs(openai): add project billing boundary clarification packet` |
| Current controlling lane | `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` (PR #511, **blocked: operator confirmation missing**) |
| Next selected lane | **`OPENAI-PROJECT-BILLING-BOUNDARY-ATTESTATION-RETRY-001`** (operator attestation retry, no provider call) |
| Next provider-call attempt (only after attestation) | `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` |
| Highest-value strategic lane after smoke | `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` |
| Open PRs | none |

## Completed recent lanes (merged, kept as evidence)

| PR | Lane / packet | Verdict |
|----|---------------|---------|
| #497 | Self Operator local execution evidence 001 | `LOCAL_EXECUTION_EVIDENCE_CAPTURED` (DEF-001 partial) |
| #499 | Execution evidence 002 | `PARTIAL_LOCAL_FLOW_CAPTURED_OPERATOR_INPUT_REQUIRED` |
| #500 | Execution evidence 003 (approved) | `APPROVAL_CAPTURED_EXECUTION_BLOCKED_BY_LOCAL_SAFETY_GATE` |
| #501 | Execution evidence 004 (gate-compatible) | `APPROVAL_ACCEPTED_LOCAL_FLOW_CAPTURED` |
| #502 | OpenAI free-token eval/smoke harness plan | `OPENAI_FREE_TOKEN_EVAL_SMOKE_HARNESS_PLAN_CAPTURED` |
| #503 | DEF-002 / DEF-003 evidence boundary | boundary recorded; both DEFs remain open |
| #504 | OpenAI data-sharing operator verification | `OPENAI_DATA_SHARING_OPERATOR_VERIFICATION_PACKET_CAPTURED` |
| #505 | Local OpenAI token smoke capture 001 | `BLOCKED_OPERATOR_ATTESTATION_PACKET_MISSING` |
| #506 | OpenAI synthetic smoke prompt fixture | `OPENAI_SYNTHETIC_SMOKE_PROMPT_FIXTURE_CAPTURED` |
| #507 | OpenAI operator pre-smoke attestation | `OPENAI_OPERATOR_PRE_SMOKE_ATTESTATION_CAPTURED` |
| #508 | OpenAI packet checker-scope hardening | `OPENAI_PACKET_CHECKER_SCOPE_EXTENDED` |
| #509 | Local OpenAI token smoke retry 001 | `BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED` |
| #511 | OpenAI project/billing boundary clarification 001 | `BLOCKED_PROJECT_BILLING_OPERATOR_CONFIRMATION_MISSING` |

See [`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) for full per-PR detail and
[`LANE_REGISTRY.md`](LANE_REGISTRY.md) for lane lifecycle classification.

## Open deferrals (see [`DEFERRAL_REGISTER.md`](DEFERRAL_REGISTER.md))

- **DEF-001** — Self Operator execution evidence: **substantially advanced
  within local-only scope**; does **not** prove provider/runtime readiness.
- **DEF-002** — Product security/privacy review: **open**.
- **DEF-003** — Prior Fable delta-audit custody/replacement: **open**.
- **DEF-004** — Audit custody/provenance: **open** unless repo evidence shows
  otherwise.

## What is blocked

- **First real OpenAI token smoke** — blocked on OpenAI project/billing
  operator confirmation after PR #511. No provider call until the attestation
  retry supplies the required confirmation.
- **DEF-002 closure** — blocked pending security/privacy review (assessment of
  existing machinery, not build-from-scratch).
- **DEF-003 closure** — blocked pending committed audit text or an accepted
  replacement custody path.
- **Public/runtime/provider exposure**, `/v1/solve`, dashboards — out of scope
  and not authorized here.

## What must not be claimed

This phase does **not** support claims of: OpenAI validation, provider
validation, runtime readiness, production readiness, public MVP readiness,
security/privacy completion, DEF-002 resolved, DEF-003 resolved, benchmark
validation, benchmark superiority, broad-user readiness, autonomous readiness,
`/v1/solve` readiness, or dashboard readiness. See
[`EVIDENCE_INDEX.md`](EVIDENCE_INDEX.md) and each packet's `forbidden-claims.md`.
