# Fallback and Fail-Closed Requirements

## Fallback boundary

This packet defines fallback requirements without adding fallback. No hosted fallback, provider fallback, local-to-hosted fallback, hosted-to-hosted fallback, or dashboard/API fallback path is implemented or enabled by this packet.

## Fail-closed requirements

Future provider orchestration must fail closed when:

- no eligible provider is configured;
- provider selection is ambiguous;
- required credentials are missing, invalid, expired, or unsafe to inspect;
- provider capability metadata is missing or contradictory;
- safety gates cannot run or return an unsafe result;
- quota, cost, or budget state is unknown where policy requires a known state;
- timeout, retry, or circuit-breaker limits are exceeded;
- provenance metadata cannot be recorded as required;
- raw provider output is empty, malformed, unsafe, policy-blocked, or not parseable into the required bounded shape;
- local-only policy would be violated by a hosted provider;
- hosted-provider policy would be violated by an unapproved provider.

## Fallback requirements for future lanes

Any future fallback design must require explicit opt-in, deterministic fallback ordering, safety-gate re-evaluation for every fallback attempt, separate provenance for primary and fallback attempts, clear cost/quota accounting per attempt, maximum attempt limits, and operator-visible explanation of why fallback occurred.

Fallback must not hide provider failures, erase primary-attempt provenance, transform failed output into successful quality evidence, or promote local evidence into hosted evidence.
