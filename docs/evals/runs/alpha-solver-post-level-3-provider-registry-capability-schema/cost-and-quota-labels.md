# Cost and Quota Labels

## Cost labels

A future provider registry entry should include a conservative cost label:

| Cost label | Meaning |
| --- | --- |
| `no_cost_docs_only` | Documentation-only entry with no provider calls. |
| `local_resource_cost_candidate` | May consume local compute resources if later authorized. |
| `hosted_billable_candidate` | May create hosted-provider costs if later authorized. |
| `unknown_cost` | Cost is unresolved and must remain disabled/default-off. |

## Quota labels

A future entry should include a quota label:

| Quota label | Meaning |
| --- | --- |
| `no_quota_docs_only` | Documentation-only entry with no quota use. |
| `local_resource_limit_required` | Future local use requires explicit resource limits. |
| `hosted_rate_limit_required` | Future hosted use requires rate-limit policy. |
| `budget_guard_required` | Future use requires budget guard design before invocation. |
| `unknown_quota` | Quota is unresolved and must remain disabled/default-off. |

## Cost and quota constraints

- A provider entry must not be enabled unless cost and quota labels are known and reviewed.
- Hosted billable candidates must remain disabled/default-off without accepted budget, rate-limit, credential, and operator opt-in controls.
- Local resource candidates must remain disabled/default-off without accepted timeout, concurrency, resource-limit, and stop-condition controls.
- Cost labels are not billing evidence and do not perform billing work.
