# Enforcement boundary

## Runtime-enforced today

- `alpha.core.policy.PolicyEngine.classify()` enforces exact-tag `deny` and
  `mask` decisions from the registry-loaded `data_classification` rules supplied
  to the engine.
- `alpha.core.governance.DataClassifier.enforce()` applies the legacy
  `config/data_classification.yaml` regex rules by downgrading matching plan
  steps to `instructions_only` when that classifier is used.
- `alpha.providers.telemetry` emits only explicit allowlisted metadata fields and
  has no prompt or completion content field.
- `alpha.self_operator.redaction` performs deterministic local redaction of
  secret-like fields and strings before Self Operator artifact emission when used
  by callers.

## Policy-only today

- Treating `registries/data_classification.yaml` as canonical for all prompts,
  traces, provider requests, logs, replay artifacts, evidence packets, and
  dashboard data is a precedence decision, not universal runtime enforcement.
- `registries/tools.json` `data_handling`, `audit_level`, `risk_flags`, and
  `compliance_scope` fields are policy metadata unless an explicit caller
  interprets them.
- `registries/policy.routes.yaml` is route metadata and does not itself enforce
  classification, auth, consent, budget, redaction, or provider-call controls.
- Evidence packet non-claims and exposure gates are operator/reviewer constraints,
  not runtime gates.

## Narrow runtime change decision

No runtime enforcement was changed in this lane. The conflict was reconciled by
source-of-truth documentation because changing runtime classification behavior
would alter provider/log/replay semantics beyond this lane's approved boundary.
