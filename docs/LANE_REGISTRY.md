# Lane Registry

> Source-of-truth lane lifecycle registry. Verification date **2026-06-15** after
> live GitHub verification of PRs #557–#565 and current open PR state.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| Post-#565 consolidation | **current control posture** | PRs #557, #558, #559, #560, #562, #563, #564, and #565 are merged; PR #561 is closed unmerged and superseded by #562; live open PR count was `0` at verification. |

## Next ready

| Lane | State | Notes |
|------|-------|-------|
| **`ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001`** | **selected next** | Docs/eval packet refresh only. Incorporates merged no-echo, false-premise, claim-safety, calibrated-confidence, needs-human, higher-headroom, prompt-contract, and local Ollama scaffold artifacts without running providers or models. |

## Completed (kept as evidence)

- `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001` (PR #557) — no-echo substantive generation gate.
- `ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001` (PR #558) — false-premise and hidden-constraint perturbation case set.
- `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001` (PR #559) — narrative claim-safety linter.
- `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001` (PR #560) — calibrated-confidence output contract.
- `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001` (PR #562) — docs-only needs-human escalation protocol.
- `ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001` (PR #563) — higher-headroom Value Read case set.
- `ALPHA-SOLVER-PROMPT-CONTRACT-SIMULATION-METHODOLOGY-001` (PR #564) — prompt-contract simulation methodology.
- `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001` (PR #565) — local Ollama singlepath lab scaffold.

## Superseded

| Lane / PR | Superseded by | Why |
|-----------|---------------|-----|
| PR #561 — `Add needs-human escalation protocol` | PR #562 | #561 is closed unmerged; #562 merged the docs-only needs-human protocol. |
| Older smoke-authorization selected-next pointers | Post-#565 selected next lane in this registry and [`CURRENT_STATE.md`](CURRENT_STATE.md) | The #557–#565 wave changed the active posture to Value Read infrastructure consolidation. |

## Blocked / not authorized

| Lane / activity | Blocked by | Unblock condition |
|-----------------|-----------|-------------------|
| Provider calls / hosted model runs / token use | Hard boundary for current docs-only consolidation | Separate explicit operator authorization in a future lane. |
| Local model / Ollama execution | Current #565 scaffold is design/local-lab lane only | Separate operator-managed local run authorization and preserved evidence boundaries. |
| Dashboard, `/v1/solve`, public API exposure | Not part of the selected next lane | Separate exposure/readiness/security lane. |
| Google Sheets or backlog workbook mutation | Repo task boundary | Operator-managed external ledger process only. |
| Value/readiness/provider/security/privacy/Alpha-superiority claims | No execution or validation evidence in this lane | Properly scoped future evidence with pre-registered boundaries. |

## Do not run again (as-is)

- PR #561 lane as a standalone needs-human protocol PR — closed unmerged and superseded by PR #562.
- Any merged packet lane verbatim — packets are immutable evidence; create a new lane id instead.
- Any selected-next pointer that predates this post-#565 consolidation if it conflicts with `ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001`.

## Forward path (single track)

```text
#557 no-echo gate
#558 false-premise / hidden-constraint set
#559 claim-safety linter
#560 calibrated-confidence contract
#562 needs-human protocol (supersedes #561)
#563 higher-headroom cases
#564 prompt-contract methodology
#565 local Ollama singlepath scaffold
        │
        ▼
ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001 ← selected next; docs/eval packet refresh only
```

This registry does not authorize any provider call, local model call, runtime exposure, public API exposure, Google Sheets mutation, or readiness/value claim.
