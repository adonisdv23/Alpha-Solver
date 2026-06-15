# Message Card and Evidence Trail Spec

This is a paper-only UI/spec for an Alpha message card and evidence trail. It does not add runtime UI, dashboard UI, API behavior, public exposure, provider behavior, or model behavior.

## Alpha message card fields

| Field | Purpose | Example bounded values |
| --- | --- | --- |
| `answerability` | State whether the task can be answered under current evidence. | `answerable`, `needs_clarification`, `blocked`, `should_escalate`. |
| `confidence` | Record confidence level with reason. | `low`, `medium`, `high`, plus a short evidence reason. |
| `assumptions` | List assumptions detected in the user task or packet. | `operator wants docs-only design`, `no execution authorized`. |
| `false_premise_flag` | Mark whether the prompt contains an unsupported premise. | `none_detected`, `possible`, `detected`. |
| `hidden_constraints` | Name constraints that must govern the answer. | `no provider calls`, `no runtime changes`, `no Pi.dev integration`. |
| `needs_human` | Indicate whether operator/human review is required before continuation. | `false`, `true: implementation authorization required`. |
| `will_not_claim` | Record claims the answer refuses to make. | `value evidence`, `production readiness`, `Alpha superiority`. |
| `derivation_no_echo_status` | Distinguish substantive synthesis from prompt echo. | `derived_from_sources`, `summary_only`, `blocked_no_derivation`. |
| `route_explanation` | Explain why the answer path was chosen. | `docs-only lane selected by current-state and lane registry`. |
| `evidence_links` | Link to repo evidence paths or local pointers. | `docs/CURRENT_STATE.md`, packet files, raw-output pointer if authorized. |
| `next_safe_action` | Name the next action that stays inside evidence boundaries. | `require operator decision before implementation`. |

## Message card outline

```text
Answerability: <value>
Confidence: <level and reason>
Assumptions: <list>
False-premise flag: <value>
Hidden constraints: <list>
Needs-human: <state and reason>
Will-not-claim: <list>
Derivation/no-echo status: <status>
Route explanation: <bounded route>
Evidence links: <repo paths or local pointers>
Next-safe-action: <one action>
```

## Evidence-trail screen outline

A future local-only evidence-trail screen could display:

1. lane id and branch label;
2. prompt source and named operator action;
3. session-tree steps in chronological order;
4. raw output pointer, if authorized output exists;
5. score pointer, if authorized scoring exists;
6. stop reason and operator decision;
7. non-claims attached to the session;
8. redaction/export status;
9. next-safe-action.

The screen would be local-only by default. It would not upload evidence, expose dashboards, expose `/v1/solve`, call providers, call local models, or mutate external ledgers.

## Blind-compare review outline

If a future authorized lane includes blind comparison, the evidence trail should keep these phases separate:

1. **Case registration:** task id, prompt source, evidence boundary, and non-claims are locked.
2. **Output collection:** raw Output A and Output B pointers are preserved under the authorized mechanism.
3. **Blind scoring:** scores are recorded before unblinding.
4. **Unblind step:** identity mapping is revealed only after score lock.
5. **Interpretation:** conclusions are limited to the case set, scoring rubric, and evidence boundary.
6. **Export review:** redaction and non-claims are checked before any sanitized artifact is committed.

No blind-compare behavior is implemented in this lane.
