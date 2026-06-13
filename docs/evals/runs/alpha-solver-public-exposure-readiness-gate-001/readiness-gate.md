# Public exposure readiness gate

Verdict: `PUBLIC_EXPOSURE_READINESS_GATE_CAPTURED_NO_GO`

## Overall decision

Public exposure must not proceed. Current source-of-truth docs state that public/runtime/provider exposure, `/v1/solve`, and dashboards are not authorized, and DEF-002 remains open. The DEF-002 gap plan lists must-fix items before closeout. RR-02 credential storage has been hardened by the accepted credential-storage hardening evidence packet, but DEF-002 remains open pending default credentials, CORS defaults, `/v1/solve` auth/tenancy, data classification, supply-chain hardening, and residual-risk decisions.

## Gate matrix

| Area | Pass now | Fail now | Unknown / requires implementation | Accepted residual risk | No-go blocker |
| --- | --- | --- | --- | --- | --- |
| API auth model | API-key dependency exists for `/v1/solve`; JWT/API-key middleware exists as reusable code. | Public exposure model is not selected or proven end-to-end. | Decide API-key-only vs JWT/tenant middleware and prove it with negative tests. | None accepted here. | Yes. |
| `/v1/solve` | Sanitizes query; returns SAFE-OUT on HTTP exceptions; has local default/provider opt-in boundary. | Tenant middleware is not shown mounted for the route; DEF-002 RR-09 remains open. | Per-tenant rate/cost/logging/CORS/provider-budget proof. | None accepted here. | Yes. |
| Dashboard | Service app mounts only login plus supervised expert preview when non-default password and explicit secret are set. | Broader dashboard settings/request routes include provider-secret management and are not approved for public exposure. | Role boundaries and full route inventory tests. | None accepted here. | Yes. |
| Secrets | RR-02 credential storage was hardened by the accepted credential-storage hardening evidence packet; masked display/audit paths and restrictive file modes exist in settings code. | DEF-002 remains open; RR-03 default credential hardening and remaining secret/operator controls are not complete. | Additional secret-manager/encryption/migration evidence may be required by future operator policy. | None accepted here. | Yes. |
| Provider cost | OpenAI provider branch is explicit opt-in; prior attestation covers project/billing boundary only. | No public-exposure cost caps are proven for arbitrary traffic. | Hard caps, quotas, billing guardrails, alerting, rollback. | None accepted here. | Yes. |
| Telemetry/data sharing | Current docs forbid readiness claims and provider validation claims. | Public data-sharing disclosure and telemetry boundary are not complete. | User/operator disclosure, retention policy, prompt logging/redaction tests. | Provider data sharing may later be residual, not accepted here. | Yes. |
| Audit/evidence | Auth middleware records auth denies/logins; settings audit masks secrets. | Exposure-grade immutable audit coverage is not proven. | Define required audit events, retention, redaction, access review. | None accepted here. | Yes. |
| Supply chain | Dependency review packet exists. | Lock/hash and vendored provenance findings remain open. | Close RR-06/RR-07/RR-08 or explicit operator deferral. | None accepted here. | Yes. |
| Rollback/incident response | None sufficient observed for public exposure. | Minimum public incident runbook is absent from this gate evidence. | Rollback, key rotation, abuse shutdown, notification, evidence-capture runbooks. | None accepted here. | Yes. |
| Operator approval | Template created by this packet. | No approval captured. | Operator must complete checklist after no-go blockers close. | Later only. | Yes. |


## Status legend

- **Pass now**: evidence observed in the referenced repo state and sufficient for this gate item.
- **Fail now**: observed repo state violates or does not satisfy the required public-exposure condition.
- **Unknown / requires implementation**: condition needs new implementation, tests, operator evidence, or external process evidence.
- **Accepted residual risk**: may be accepted only by a later explicit operator risk-acceptance packet. None are accepted by this lane.
- **No-go blocker**: exposure must not proceed while this item remains open.
