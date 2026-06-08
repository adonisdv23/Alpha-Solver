# Operator Confirmation Gates

## Required future confirmations

Future Level 7-approved provider orchestration work should require explicit operator confirmation before any of the following actions occur:

- creating, importing, rotating, deleting, or validating a credential;
- adding or changing a secret reference;
- enabling provider calls with a configured credential reference;
- enabling hosted-provider execution;
- enabling fallback behavior that could call a provider;
- running benchmarks or evidence workflows that could consume provider credentials;
- exposing an API or dashboard path that could reveal credential state;
- performing billing-relevant provider work.

## Confirmation content

A safe confirmation should identify the intended action, environment scope, provider scope, billing implication, redaction expectation, and stop condition. It should not display the secret value.

## Default-deny posture

If a future lane cannot prove that confirmation, redaction, and storage rules are satisfied, it should default to no provider call, no credential change, no benchmark execution, no evidence promotion, and no billing work.

## Non-implementation status

This packet does not request operator confirmation, does not validate credentials, does not call providers, and does not modify any confirmation UI or CLI path.
