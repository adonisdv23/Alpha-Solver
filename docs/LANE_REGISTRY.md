# Lane Registry

> Source-of-truth lane lifecycle registry. Verification date **2026-06-15** after
> live GitHub verification of PRs #566–#568.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| Post-#568 Value Read blocked state | **current control posture** | PRs #566, #567, and #568 are merged. PR #568 committed a stopped manual Value Read artifact with no output generation and no scoring. |

## Next ready

| Lane | State | Notes |
|------|-------|-------|
| **`ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001`** | **selected next** | Controlled execution authorization packet/lane only. Must include complete per-case prompts, raw-output preservation, blinding-map storage, output-generation boundary, and explicit operator authorization requirements before any outputs are generated. |

## Completed (kept as evidence)

- `ALPHA-SOLVER-NO-ECHO-SUBSTANTIVE-GENERATION-GATE-POST-552-SUCCESSOR-001` (PR #557) — no-echo substantive generation gate.
- `ALPHA-SOLVER-EVAL-FALSE-PREMISE-PERTURBATION-001` (PR #558) — false-premise and hidden-constraint perturbation case set.
- `ALPHA-SOLVER-NARRATIVE-CLAIM-SAFETY-LINTER-001` (PR #559) — narrative claim-safety linter.
- `ALPHA-SOLVER-CALIBRATED-CONFIDENCE-OUTPUT-CONTRACT-001` (PR #560) — calibrated-confidence output contract.
- `ALPHA-SOLVER-ESCALATION-NEEDS-HUMAN-PROTOCOL-001` (PR #562) — docs-only needs-human escalation protocol.
- `ALPHA-SOLVER-EVAL-HIGHER-HEADROOM-CASESET-001` (PR #563) — higher-headroom Value Read case set.
- `ALPHA-SOLVER-PROMPT-CONTRACT-SIMULATION-METHODOLOGY-001` (PR #564) — prompt-contract simulation methodology.
- `ALPHA-SOLVER-LOCAL-MODEL-LAB-OLLAMA-SINGLEPATH-001` (PR #565) — local Ollama singlepath lab scaffold.
- `ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001` (PRs #566–#568) — packet refresh plus blocked manual-run artifact; no Alpha/baseline outputs or scores.

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
| Value/readiness/provider/security/privacy/Alpha-superiority claims | PR #568 generated no outputs and no scores; no execution or validation evidence exists | Properly scoped future evidence with pre-registered boundaries. |

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
ALPHA-SOLVER-VALUE-READ-SIMULATION-PACKET-REFRESH-POST-565-001 / PR #568 artifact ← VALUE_READ_BLOCKED
        │
        ▼
ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001 ← selected next; controlled authorization packet/lane only
```

This registry does not authorize any provider call, local model call, runtime exposure, public API exposure, Google Sheets mutation, or readiness/value claim.
