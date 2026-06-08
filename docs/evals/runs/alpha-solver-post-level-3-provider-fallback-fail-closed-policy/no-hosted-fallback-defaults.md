# No-Hosted-Fallback Defaults

## Default rule

No hosted fallback is allowed by default. A local provider failure, timeout, missing model, unsupported route, or policy block must not automatically route to a hosted provider.

## Hosted fallback prohibition

Hosted fallback remains prohibited unless all of the following are true in a future approved scope:

- Level 7 has accepted or amended this packet for use.
- A later implementation contract explicitly authorizes hosted fallback.
- The operator has explicitly opted in for the relevant run, request class, provider class, billing class, and retention/audit class.
- Billing, privacy, safety, evidence, and audit boundaries are defined before any provider call.
- The request is not in any blocked fallback state.

## Missing configuration

Missing fallback configuration, missing hosted-provider allowlists, missing credentials policy, missing billing policy, missing audit policy, or missing operator opt-in must produce a blocked or fail-closed result. Missing configuration must not produce best-effort hosted fallback.
