# Fail-Closed Requirements

## Required fail-closed behavior

Future provider fallback policy must fail closed when authorization, configuration, locality, provider identity, billing scope, auditability, evidence boundary, or safety state is absent, stale, contradictory, or unreviewed.

## Safe failure requirements

A safe failure must:

- avoid calling providers when provider calls are not explicitly authorized;
- avoid hosted fallback when no-hosted-fallback defaults apply;
- avoid billing activity unless explicitly authorized by a later governing packet;
- avoid exposing `/v1/solve` or changing API/dashboard behavior;
- avoid running models or benchmarks;
- return or record a blocked/fail-closed state rather than silently degrading;
- preserve enough bounded metadata for review without storing secrets, credentials, payment data, or raw sensitive payloads;
- avoid converting a failure into product readiness, provider readiness, benchmark, billing, or promotional evidence.

## Ambiguity handling

Ambiguous fallback eligibility must be treated as ineligible. Ambiguous operator opt-in must be treated as absent. Ambiguous hosted-provider status must be treated as hosted and blocked unless a later Level 7-controlled policy proves otherwise.
