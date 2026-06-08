# Fallback Policy Overview

## Default posture

Future provider fallback must be treated as forbidden unless a later Level 7-controlled decision explicitly authorizes a bounded fallback path. No hosted fallback is allowed by default.

## Future fallback boundaries

Any future fallback design must remain bounded by all of the following requirements before implementation can be considered:

- Level 7 must control whether and how this packet is used.
- Fallback must never be assumed from provider failure alone.
- Fallback must never be used to bypass local-only, no-network, no-hosted-provider, evidence-boundary, privacy, safety, billing, or operator-review constraints.
- Fallback must identify the original provider path, attempted fallback path, operator authorization state, audit state, blocked state, and safe failure outcome.
- Fallback must distinguish routing eligibility from execution authorization.
- Fallback must fail closed when policy, configuration, consent, auditability, or safety state is missing or contradictory.

## When fallback is forbidden

Fallback is forbidden when the request, environment, operator state, or evidence boundary requires local-only behavior, no hosted providers, no billing activity, no provider calls, no model runs, no `/v1/solve` exposure, no runtime change, no API change, or no dashboard change.

## Safe failure posture

If fallback cannot be proven authorized, bounded, auditable, and safe, the expected policy outcome is to stop and return a blocked or fail-closed state rather than silently retrying, routing to a hosted provider, exposing claims, or promoting evidence.
