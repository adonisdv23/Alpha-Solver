# Lane Registry

> Created by lane `ALPHA-SOLVER-CURRENT-STATE-DOCS-BACKLOG-ARCHIVE-ISSUE-REGISTER-001`.
> Verification date **2026-06-13**. Classifies every recent lane by lifecycle.
> The controlling latest packet is PR #509 (`local-openai-token-smoke-capture-retry-001`);
> its `selected-next-lane.md` is the only authoritative forward pointer. All
> older `selected-next-lane.md` files are **historical** snapshots.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001` | **current control, blocked before provider call** | PR #509 → `BLOCKED_OPENAI_PROJECT_OR_BILLING_NOT_VERIFIED` |

## Next ready

| Lane | State | Notes |
|------|-------|-------|
| **`OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001`** | **selected next** | Docs/operator clarification of OpenAI project + billing readiness. **No provider call.** This is the single selected next lane. |

## Blocked

| Lane | Blocked by | Unblock condition |
|------|-----------|-------------------|
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` | OpenAI project/billing not yet clarified | Completion of `OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001` |
| `ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001` | No real provider smoke yet; protocol not designed | After a successful tiny smoke; highest strategic value |
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

## Historical (earlier in a still-active chain; superseded as the forward pointer)

- `ALPHA-SOLVER-…-EXECUTION-EVIDENCE-001 / 002 / 003` (PRs #497, #499, #500).
- All `selected-next-lane.md` files in packets older than PR #509.

## Superseded

| Lane | Superseded by | Why |
|------|---------------|-----|
| `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` (used by PR #505, blocked: attestation missing) | the #507→#508→#509 retry chain | First blocked smoke attempt; attestation since captured (#507). Preserved as evidence. |

## Do not run again (as-is)

- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-001` — already consumed as a blocked attempt
  (PR #505). Do not re-enter under this id; the live path is the RETRY chain.
- `LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001` — already consumed as a blocked
  project/billing-verification attempt (PR #509). The next provider-call attempt
  is `…-RETRY-002`, and only after billing/project clarification.
- Re-running any merged packet lane verbatim — packets are immutable evidence;
  create a new lane id instead.

## Forward path (single track)

```
LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-001 (PR #509, blocked)
        │
        ▼
OPENAI-PROJECT-BILLING-BOUNDARY-CLARIFICATION-001   ← selected next (docs/operator, no call)
        │  (only if project + billing safely clarified)
        ▼
LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002          ← first real provider-call attempt
        │  (proves plumbing only, never value)
        ▼
ALPHA-SOLVER-VALUE-EXPERIMENT-PROTOCOL-001          ← highest strategic value
```

This registry does not authorize any provider call, runtime exposure, or
readiness claim.
