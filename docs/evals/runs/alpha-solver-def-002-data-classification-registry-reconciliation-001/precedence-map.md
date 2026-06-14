# Precedence map

## Source-of-truth order

1. **Runtime code controls first for actual emissions.** Allowlist telemetry,
   SAFE-OUT construction, request logging, redaction, replay writing, and
   dashboard/API handlers determine what can be emitted at runtime.
2. **`registries/data_classification.yaml` is the canonical policy registry for
   data-classification decisions loaded from `registries/`.** It supersedes
   duplicate registry-like classification statements for policy review and future
   provider/tool governance work.
3. **`config/data_classification.yaml` is a compatibility runtime input only.** It
   remains authoritative for the current `DataClassifier.load()` default path and
   its `instructions_only` downgrade behavior, but it is not the source of truth
   for new policy-registry work.
4. **`registries/tools.json` can annotate tools/vendors but cannot override the
   classification registry.** A populated `data_handling`, `risk_flags`, or
   `compliance_scope` field may add constraints; null/empty fields do not grant
   permission.
5. **`registries/policy.routes.yaml` can identify route endpoints but cannot
   authorize provider calls or relax data classification.** Route metadata is
   subordinate to provider opt-in, budget, auth, classification, and redaction
   controls.
6. **Evidence packets and docs constrain claims and operator decisions.** They do
   not change runtime behavior unless a later lane implements code/config changes.

## Prompt, trace, provider, log, replay, evidence, and dashboard mapping

| Data surface | Governing precedence | Current runtime enforcement |
| --- | --- | --- |
| Prompts and user context | Runtime `/v1/solve` provider gate first; canonical classification registry for policy; config classifier only where explicitly invoked. | Default local path does not call providers; current classification enforcement is not proven on every prompt/provider path in this lane. |
| Reasoning traces / session traces | Runtime trace writers first; evidence-boundary docs for claims. | Not proven classification-filtered here. |
| Provider calls | Provider opt-in/config gate, provider client code, provider telemetry allowlist, then canonical classification policy for future gating. | Provider calls were not exercised; no new provider enforcement was added. |
| Request logs and provider telemetry | Logging code and telemetry allowlist first; canonical policy registry for allowed future fields. | Provider telemetry is allowlist-only; generic loggers require caller hygiene. |
| Replay artifacts | Replay harness behavior first; canonical policy registry for future capture decisions. | Replay can persist supplied events; classification/redaction is not automatically enforced by the harness. |
| Evidence packets | Evidence-boundary docs and packet-specific non-actions first. | Policy-only; no runtime effect. |
| Dashboard/API data | Mounted route code, auth/CORS/tenancy controls, exposure-gate docs, then canonical classification policy. | Public-exposure packet still blocks readiness; dashboard data classification was not proven complete. |

## Decision

RR-05 is reconciled at the policy-registry level: new policy work should read
`registries/data_classification.yaml` as canonical and treat
`config/data_classification.yaml` as a legacy runtime compatibility input until a
specific enforcement migration closes the implementation gap.
