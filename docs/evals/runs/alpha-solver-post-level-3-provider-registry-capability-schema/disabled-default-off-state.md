# Disabled and Default-Off State

## Required default

Every future provider registry entry must be disabled/default-off unless a later accepted Level 7 or implementation lane explicitly authorizes a narrower state.

## State labels

| State label | Meaning |
| --- | --- |
| `disabled_default_off` | Required default for all entries. |
| `docs_reference_only` | Entry is reference material only. |
| `blocked_pending_level_7` | Entry cannot be used until Level 7 decides whether it is in scope. |
| `blocked_pending_credentials_policy` | Hosted candidate cannot be used without credential policy. |
| `blocked_pending_cost_policy` | Candidate cannot be used without cost and quota policy. |
| `blocked_pending_safety_review` | Candidate cannot be used without safety review. |

## Fail-closed requirements

A future registry should fail closed when:

- a required identity field is missing;
- a capability label is unknown or contradictory;
- local-vs-hosted boundary is unknown;
- cost or quota labels are unknown;
- provenance is missing;
- safety constraints are missing;
- a provider is not explicitly enabled by an accepted lane; or
- operator opt-in is absent.

## No implicit enablement

No label in this packet authorizes provider calls. No future registry entry should become callable through default configuration, environment variables, installed dependencies, discovered local runtimes, available provider keys, dashboard selection, API request fields, CLI flags, or fallback behavior unless later accepted work explicitly authorizes that behavior.
