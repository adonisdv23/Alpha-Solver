# Lane Registry

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-14**. Classifies every recent lane by lifecycle.
> The controlling latest packet is PR #527 (`local-openai-token-smoke-capture-retry-002`);
> its `selected-next-lane.md` is the authoritative forward pointer. All
> older `selected-next-lane.md` files are **historical** snapshots.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` | **current control, consumed/blocked** | PR #527 → `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`; provider calls `0`, tokens `0`, cost `$0.00` |

## Next ready

| Lane | State | Notes |
|------|-------|-------|
| **`LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002-AUTHORIZATION-REFRESH`** | **selected next** | Authorization-refresh packet only. It must supply explicit model, project boundary, cost cap, token cap, max run count, and synthetic fixture before any provider call. |

## Blocked

| Lane | Blocked by | Unblock condition |
|------|-----------|-------------------|
| `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` | No real provider smoke yet; no no-echo evidence; protocol designed/canonical packet exists but not executed | After a successful tiny smoke and protocol preconditions, including substantive Alpha generation / no-echo gate and appropriate smoke/provider boundary; highest strategic value |
| `DEF-002` security/privacy review lane | Review not scoped/executed | Operator-scoped security/privacy assessment |
| `DEF-003` audit custody lane | Audit text not committed | Committed audit text or accepted replacement custody |

## Completed (kept as evidence)

- `ALPHA-SOLVER-…-EXECUTION-EVIDENCE-004` (PR #501) — local approved flow captured.
- `OPENAI-FREE-TOKEN-EVAL-SMOKE-HARNESS-PLAN-001` (PR #502).
- `…-DEF-002-DEF-003-EVIDENCE-BOUNDARY-001` (PR #503).
- `OPENAI-DATA-SHARING-OPERATOR-VERIFICATION-001` (PR #504).
- `OPENAI-SYNTHETIC-SMOKE-PROMPT-FIXTURE-001` (PR #506).
- `OPENAI-DATA-SHARING-OPERATOR-ATTESTATION-001` (PR #507).
- `OPENAI-PACKET-CHECKER-SCOPE-001` (PR #508).
- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001` (PR #509) — blocked before provider call.
- `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` (PR #511) — blocked pending operator confirmation, superseded by PR #512.
- `OPENAI-PROJECT-BILLING-BOUNDARY-ATTESTATION-RETRY-001` (PR #512) — redacted operator confirmation recorded; no provider call.
- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` (PR #527) — consumed as a blocked preflight because explicit operator authorization was missing; no provider call, no tokens, no cost.

## Historical (earlier in a still-active chain; superseded as the forward pointer)

- `ALPHA-SOLVER-…-EXECUTION-EVIDENCE-001 / 002 / 003` (PRs #497, #499, #500).
- All `selected-next-lane.md` files in packets older than PR #527.

## Superseded

| Lane | Superseded by | Why |
|------|---------------|-----|
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` (used by PR #505, blocked: attestation missing) | the #507→#508→#509 retry chain | First blocked smoke attempt; attestation since captured (#507). Preserved as evidence. |

## Do not run again (as-is)

- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` — already consumed as a blocked attempt
  (PR #505). Do not re-enter under this id; the live path is the RETRY chain.
- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001` — already consumed as a blocked
  project/billing-verification attempt (PR #509).
- `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` — PR #511 control
  packet; do not re-enter after merge. It was superseded by the PR #512
  attestation retry.
- `OPENAI-PROJECT-BILLING-BOUNDARY-ATTESTATION-RETRY-001` — PR #512 control
  packet; do not re-enter after merge. Its selected next lane was consumed by
  `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002`.
- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` — PR #527 control packet; do
  not re-enter as a provider-call lane because it is consumed/blocked with
  verdict `BLOCKED_OPERATOR_AUTHORIZATION_MISSING`.
- Re-running any merged packet lane verbatim — packets are immutable evidence;
  create a new lane id instead.

## Forward path (single track)

```
LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001 (PR #509, blocked)
        │
        ▼
OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001   ← PR #511 blocked, superseded
        │
        ▼
OPENAI-PROJECT-BILLING-BOUNDARY-ATTESTATION-RETRY-001 ← PR #512 current control, confirmed (no call)
        │
        ▼
LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002          ← consumed/blocked; missing operator authorization; 0 calls/tokens/cost
        │
        ▼
LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002-AUTHORIZATION-REFRESH ← selected next; collect explicit authorization only
        │  (a later successful tiny smoke would prove plumbing only, never value)
        ▼
ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001          ← protocol designed; blocked until smoke + no-echo evidence, not executed
```

This registry does not authorize any provider call, runtime exposure, or
readiness claim.
