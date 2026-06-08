# Mode and Surface Compatibility

## Supported mode labels

A future provider registry entry should use explicit mode labels instead of inferring behavior:

| Mode label | Meaning |
| --- | --- |
| `docs_only` | Entry exists only as documentation and cannot be invoked. |
| `local_manual_candidate` | Candidate for manually invoked local workflows if later authorized. |
| `local_operator_candidate` | Candidate for local operator workflows if later authorized. |
| `hosted_candidate` | Candidate for hosted-provider workflows if later authorized. |
| `eval_candidate` | Candidate for future eval-only workflows if later authorized. |
| `production_blocked` | Not eligible for production use. |

## Product surface labels

Surface labels should be separate from mode labels:

| Surface label | Requirement |
| --- | --- |
| `no_surface` | Default label; no product surface may use this provider. |
| `api_candidate` | Candidate for future API design only; does not expose `/v1/solve`. |
| `dashboard_candidate` | Candidate for future dashboard design only; does not expose dashboards. |
| `cli_candidate` | Candidate for future CLI design only; does not modify CLI behavior. |
| `eval_surface_candidate` | Candidate for future evaluation-only workflows. |

## Compatibility rules

- `docs_only` and `no_surface` should be the default state for every registry entry.
- A provider must not become callable because it has an `api_candidate`, `dashboard_candidate`, `cli_candidate`, or `eval_surface_candidate` label.
- Surface compatibility must remain subordinate to accepted Level 6 product-surface gates and Level 7 provider orchestration decisions.
- Missing compatibility labels must fail closed.
