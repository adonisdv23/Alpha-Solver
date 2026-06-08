# Local-vs-Hosted Boundaries

## Boundary labels

A future registry should label each entry with exactly one primary boundary:

| Boundary label | Meaning |
| --- | --- |
| `local_only` | Provider is intended to run only through local runtime boundaries if later authorized. |
| `hosted_only` | Provider requires a hosted service if later authorized. |
| `hybrid_candidate` | Provider may have local and hosted variants, but they must be represented as separate callable paths if later authorized. |
| `unknown_boundary` | Boundary is unresolved and must remain disabled/default-off. |

## Local boundary requirements

A local-labeled entry must preserve local-only safety constraints until a later accepted lane changes them. It must not require, accept, read, validate, forward, or depend on hosted provider credentials for local mode.

## Hosted boundary requirements

A hosted-labeled entry must remain disabled/default-off until a later authorized lane defines credential policy, quota policy, cost controls, operator opt-in, logging limits, provenance requirements, and stop conditions.

## Hybrid boundary requirements

A `hybrid_candidate` label must not blur local and hosted paths. Future design should split local and hosted behavior into separately auditable entries or subentries so hosted fallback cannot be implied by local failure.

## Boundary constraint

This packet does not call providers, configure secrets, enable hosted fallback, enable provider fallback, or authorize any local or hosted model execution.
