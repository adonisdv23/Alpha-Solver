# Registry inventory

## Data classification registries

| File | Role | Current content | Runtime reader | Reconciliation status |
| --- | --- | --- | --- | --- |
| `registries/data_classification.yaml` | Canonical registry-loaded data-classification policy. | Versioned registry with `phi -> mask` and `pii -> deny`. | `alpha.core.loader.FILES` maps `data_classification` to this file under the `registries/` root; `alpha.core.policy.PolicyEngine.classify()` consumes loaded `rules`. | Authoritative for registry-loaded policy decisions. |
| `config/data_classification.yaml` | Legacy/runtime governance downgrade input. | Unversioned config with `pii|secret|token -> instructions_only`. | `alpha.core.governance.DataClassifier.load()` defaults to this path and `enforce()` downgrades matching plan steps to `instructions_only`. | Not canonical policy registry; retained as runtime enforcement input until migration. |

## Policy and provider/tool registries

| File | Role | Current content | Runtime reader | Reconciliation status |
| --- | --- | --- | --- | --- |
| `registries/policy.routes.yaml` | Vendor route registry. | JSON-shaped YAML with a `signs365` order endpoint. | Loaded by `alpha.core.loader` as `policy_routes`; no data-classification actions are present. | Not a classification source; route metadata only. |
| `registries/tools.json` | Canonical tool/vendor registry enrichment. | Tool records with nullable `data_handling`, `audit_level`, `risk_flags`, and `compliance_scope` fields. | `alpha.core.registry_provider.RegistryProvider.load()` enriches seed rows from this file and gives canonical rows precedence. | Policy metadata source only unless downstream code explicitly interprets a populated field. |

## Runtime boundary registries and modules reviewed

| Area | Source | Boundary observed |
| --- | --- | --- |
| Provider telemetry | `alpha/providers/telemetry.py` | Allowlist-based event fields; prompt/response content fields are absent. |
| JSONL logs | `alpha/core/jsonl_logger.py` | Generic logger persists caller-provided events; classification depends on caller hygiene. |
| Replay | `alpha/core/replay.py` | Generic event capture/replay; no registry classification or redaction is applied in the harness. |
| Registry snapshots | `alpha/core/registry_provider.py` | Shortlist snapshots include `query`, region, scores, and explanations; no classification policy is applied before writing. |
| Self Operator redaction | `alpha/self_operator/redaction.py` | Deterministic local redaction for secret-like keys and strings; pattern-based limitation remains. |
| Evidence packets | `docs/evals/runs/...` | Evidence docs state boundaries and non-claims; they are policy/evidence constraints, not runtime controls. |

## Conflicts and stale entries

1. `pii` conflicts: `registries/data_classification.yaml` denies it, while
   `config/data_classification.yaml` downgrades matching prompts to
   `instructions_only`.
2. `secret` and `token` exist in `config/data_classification.yaml` but not in the
   canonical registry-loaded policy.
3. `phi` exists in `registries/data_classification.yaml` but not in the runtime
   governance config.
4. `registries/tools.json` contains many nullable data-governance fields. Nulls
   are not policy decisions and must not be treated as allow/deny evidence.
5. `registries/policy.routes.yaml` is route metadata and should not be used to
   infer classification or provider-data-sharing consent.
