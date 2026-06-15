# Lane Registry

> Source-of-truth lane lifecycle registry. Verification date **2026-06-15** after
> live GitHub API verification of **0 open PRs** and merged PRs **#569–#574**.

## Lifecycle classes

`current` · `next ready` · `completed` · `blocked` · `historical` · `superseded` · `do not run again`

## Current

| Lane | State | Evidence |
|------|-------|----------|
| Post-#574 backlog/current-state sync posture | **current control posture** | PRs #569–#574 are merged. The newest evidence is docs/research/gate/helper work: post-#568 source-of-truth sync, founder memo refresh, blocked `/v1/solve` exposure gate, local Ollama helper, failed-closed local Ollama attempt, and Pi.dev no-integration feasibility note. |

## Next ready

| Lane | State | Notes |
|------|-------|-------|
| **`ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001`** | **selected next** | Alpha-native design note only. Borrow useful Pi.dev-style operator-harness patterns without installing Pi.dev, integrating Pi.dev, changing runtime behavior, exposing `/v1/solve`, calling providers/models, or mutating Google Sheets. |

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
- Post-#568 current-state sync (PR #569) — source-of-truth docs and MVP scorecard refresh for `VALUE_READ_BLOCKED`.
- Founder memo refresh (PR #570) — narrative positioning for the blocked Value Read state.
- `14 - V1 Solve Exposure Gate Packet` (PR #571) — `/v1/solve` public exposure is `BLOCKED`.
- Local Ollama singlepath operator helper (PR #572) — local-only helper added; no successful model run implied.
- Local Ollama singlepath blocked attempt (PR #573) — exact `gemma3:4b` model preflight passed, then helper failed closed with timeout/backend error and produced no local answer.
- `18 - PI.DEV-HARNESS-FEASIBILITY` (PR #574) — `BORROW_PATTERNS_ONLY_NO_INTEGRATION` research note.

## Superseded

| Lane / PR | Superseded by | Why |
|-----------|---------------|-----|
| PR #561 — `Add needs-human escalation protocol` | PR #562 | #561 is closed unmerged; #562 merged the docs-only needs-human protocol. |
| Older smoke-authorization selected-next pointers | Post-#568 and post-#574 selected-next lanes in this registry and [`CURRENT_STATE.md`](CURRENT_STATE.md) | The #557–#574 wave changed the active posture to Value Read blocked evidence, exposure/local-lab gates, and an Alpha-native harness design next step. |
| `ALPHA-SOLVER-VALUE-READ-EXECUTION-PACKET-AUTHORIZATION-001` as immediate global next | PR #574's proposed `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001` | Value Read execution remains blocked; the newest merged research note selects a safer docs-only harness design lane. |

## Blocked / not authorized

| Lane / activity | Blocked by | Unblock condition |
|-----------------|-----------|-------------------|
| Provider calls / hosted model runs / token use | Hard boundary for current docs-only sync | Separate explicit operator authorization in a future lane. |
| Local model / Ollama execution | Current evidence includes a failed-closed local attempt, not validation | Separate operator-managed local run authorization and preserved evidence boundaries; do not treat #573 as quality/readiness evidence. |
| Dashboard, `/v1/solve`, public API exposure | PR #571 exposure gate verdict is `BLOCKED` | Separate exposure/readiness/security lane after identity, tenancy, logging, redaction, rate-limit, CORS/ingress, monitoring, incident-response, rollback, and authorization questions are resolved. |
| Pi.dev installation, execution, or integration | PR #574 recommends patterns-only/no-integration | Separate spec, threat model, package/provenance review, sandbox, no-secret workspace, provider/key policy, export policy, and operator authorization. |
| Google Sheets or backlog workbook mutation | Repo task boundary | Operator-managed external ledger process only; this repo PR may include paste-ready sheet updates but must not mutate the Sheet. |
| Value/readiness/provider/security/privacy/local-Ollama/Pi.dev/Alpha-superiority claims | No execution or validation evidence exists; #568 has no outputs/scores and #573 failed closed | Properly scoped future evidence with pre-registered boundaries. |

## Do not run again (as-is)

- PR #561 lane as a standalone needs-human protocol PR — closed unmerged and superseded by PR #562.
- Any merged packet lane verbatim — packets are immutable evidence; create a new lane id instead.
- Any selected-next pointer that predates this post-#574 sync if it conflicts with `ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001`.
- Direct Pi.dev integration from PR #574's research lane — the recorded verdict is patterns-only/no-integration.

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
#569 current-state sync
#570 founder memo refresh
#571 /v1/solve exposure gate ← BLOCKED
#572 local Ollama helper
#573 local Ollama attempt ← FAILED_CLOSED_TIMEOUT / no local answer
#574 Pi.dev harness feasibility ← BORROW_PATTERNS_ONLY_NO_INTEGRATION
        │
        ▼
ALPHA-SOLVER-LOCAL-OPERATOR-HARNESS-DESIGN-NOTE-001 ← selected next; Alpha-native docs-only design lane
```

This registry does not authorize any provider call, local model call, Pi.dev install/run/integration, runtime exposure, public API exposure, Google Sheets mutation, or readiness/value/security/privacy/provider/local-Ollama/Alpha-superiority claim.
