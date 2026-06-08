# Timeout, Retry, Circuit-Breaker, and Budget Requirements

## Timeout requirements

Future provider orchestration must use finite timeouts for provider selection, connection establishment, request execution, response parsing, and total orchestration. Timeout values must be bounded by policy and must fail closed when exceeded.

## Retry requirements

Retries must be explicitly configured, capped, and eligible only for safe transient failure classes. Retry logic must not retry unsafe payloads, policy-blocked outputs, credential failures, quota failures, budget failures, malformed outputs that indicate provider incompatibility, or requests without idempotency controls where duplicate execution could be unsafe.

## Circuit-breaker requirements

Future orchestration must support provider-level circuit breakers that can mark a provider temporarily ineligible after repeated timeout, network, quota, safety, or parse failures. Circuit-breaker state must be observable, bounded, and reset only by policy.

## Budget requirements

Budgets must be enforced before provider calls where policy requires pre-call blocking, and recorded after provider calls where usage/cost data is available. Unknown usage or cost must not be fabricated. When budget or quota state is required but unavailable, provider orchestration must fail closed.

## Non-action

This packet does not add timeout logic, retry logic, circuit breakers, budget enforcement, or provider calls. It only defines requirements for future implementation.
