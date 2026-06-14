# MVP readiness scorecard

Verdict: `MVP_SCORECARD_CAPTURED_OPERATOR_DECISION_REQUIRED`

Scale used here:

- **Captured / local-only**: committed local or docs evidence exists, but does not prove runtime/provider/public readiness.
- **Blocked**: explicit prerequisite missing.
- **Protocol-only**: a future test plan exists, but no result exists.
- **Not claimable**: evidence does not support an external claim.

## Required scorecard categories

| Category | Current read | Evidence basis | Blocked by | Non-claim |
| --- | --- | --- | --- | --- |
| 1. Core product value evidence | **Blocked / protocol-only** | Value experiment protocol exists and asks a useful A/B question, but is not executed and contains no results. | Successful provider/smoke boundary, no-echo substantive generation evidence, frozen task bank, scored paired outputs. | No value proof, superiority, benchmark validation, or MVP readiness. |
| 2. Provider smoke and billing boundary | **Billing boundary attested; smoke blocked** | PR #512 records redacted project/billing/cost/data-sharing attestation for one tiny synthetic smoke retry. PR #527 consumed retry 002 as blocked with provider calls `0`, tokens `0`, cost `$0.00`. | Explicit model, project boundary, cost cap, token cap, max run count, and exact synthetic fixture authorization. | No OpenAI/provider validation and no API smoke success. |
| 3. No-echo substantive generation gate | **Blocked / absent** | PR #527 produced no smoke output and no provider response. Value protocol requires substantive Alpha-generation/no-echo evidence before execution. | A successful tiny smoke and later controlled value task outputs showing non-echo behavior. | No substantive-generation or no-echo claim. |
| 4. Security and privacy closure | **Review captured; closure not claimable** | DEF-002 review captured open gaps; follow-on hardening packets exist, but central current-state/deferral register still does not support public/security completion claims. | Operator-recognized closure or accepted residual-risk packet after all required gap dispositions, especially exposure-relevant controls. | No DEF-002 resolved, security/privacy completion, or public-safe claim. |
| 5. Runtime entrypoint clarity | **Mapped, not consolidated** | Runtime entrypoint map identifies `/v1/solve`, dashboard, provider, portable, modular/reference, auth, tenancy, and evidence surfaces. | Operator decision on canonical runtime/public surface and security model before exposure. | No `/v1/solve`, dashboard, or consolidated runtime readiness. |
| 6. Public exposure gate | **Blocked** | Public-exposure and runtime-map packets classify product-shaped surfaces as unsafe-to-expose until security, CORS, secrets, provider disclosure, tenancy, and operations are resolved. | DEF-002 closure/acceptance, provider/data-sharing boundary, auth/CORS/secret posture, operator go/no-go. | No public MVP readiness or production readiness. |
| 7. Test and CI health | **Local evidence exists; full health not proven** | Self Operator local evidence chain passed focused local/offline checks; dependency packet recorded full-suite failures in the ambient environment; current lane is docs-only. | Clean focused/full suite under controlled non-provider environment, or explicit issue register for failures. | No CI green, release readiness, or complete test health claim. |
| 8. Documentation and backlog hygiene | **Improved but not finished** | Current-state, evidence index, lane registry, deferral register, issue register, and packets now constrain the evidence narrative. | Ongoing drift control, spec contamination reconciliation, and backlog updates outside repo as operator work. | No claim that all specs/backlog entries are clean or synchronized. |
| 9. Demo readiness | **Internal dry-run only; external demo blocked** | Operator demo/run packets and local Self Operator evidence support local narration of boundaries. | Smoke/no-echo evidence, claim-safe script, security/public-exposure gates if demo touches live/public surfaces. | No external demo readiness, live demo safety, or customer pilot readiness. |
| 10. Investor/incubator narrative readiness | **Narrative must be boundary-heavy** | Evidence supports saying the project has disciplined governance, local execution evidence, and explicit blockers. | Actual value evidence, provider smoke, security/privacy disposition, and claim-approved narrative. | No investor-grade MVP traction, superiority, production, or readiness claim. |

## Opportunity signal scorecard addendum: discrimination-value signal

This addendum asks whether the latest evidence suggests the wedge is worth further investment. It does **not** ask whether Alpha Solver is ready, superior, or productized.

| Signal dimension | Current read | Evidence / missing evidence | Allowed conclusion |
| --- | --- | --- | --- |
| Confidence-envelope usefulness | **Plausible but unmeasured** | Protocol plans calibration and confidence-bound comparisons, but no scored outputs exist. | preserve as Phase G candidate |
| False-premise catch rate | **Unmeasured** | Protocol includes hallucination-bait / false-premise tasks; no run exists. | preserve as Phase G candidate |
| Hidden-constraint catch rate | **Unmeasured** | Protocol can include underspecified/constraint-heavy tasks, but no frozen task bank or results exist. | preserve as Phase G candidate |
| Needs-human escalation usefulness | **Plausible locally; unmeasured in value setting** | Self Operator gates show local approval/stop behavior, but not user-visible escalation quality. | preserve as Phase G candidate |
| Unsupported-claim avoidance | **Governance evidence strong; answer-quality evidence absent** | Packets consistently enforce forbidden claims; no generated-answer comparison exists. | add as immediate follow-up only as rubric/contract refinement, not productization |
| Operator preference versus plain baseline | **Absent** | No paired plain-baseline vs Alpha outputs and no blinded operator preference scores. | defer until more evidence |
| Signal strong enough to justify a future focused lane | **Not yet for productization; yes for protocol/rubric refinement** | Current value read is within noise because no outputs exist. | select task-bank refinement, contract refinement, or wedge-reconsideration; do not open productization lanes |

## Decision rule application

The value read is within noise. Therefore this packet does **not** open productization lanes. The only value-related follow-up that fits the evidence is refinement work: task-bank refinement, contract/rubric refinement, or wedge reconsideration after the provider smoke/no-echo prerequisites are satisfied.
