# Allowed First Code Scope

This file defines the only first code scope that may be considered after a separate implementation lane obtains explicit operator approval. This packet itself does not authorize that implementation.

## Allowed after separate approval

A future first code change may be limited to:

- Local-only Self Operator runtime scaffolding that is disabled by default.
- Deterministic dry-run planning or validation logic that does not execute external actions.
- Local harness entrypoints that require an explicit operator flag and operate only on fixtures, local temporary directories, or fake transports.
- Artifact capture for local dry-run results, including command metadata, timestamps, non-secret configuration summaries, stdout/stderr captures, structured result files, and boundary confirmations.
- Static guardrails that fail closed when provider calls, browser automation, credentials, deployment, billing, product exposure, or evidence promotion are attempted.
- Documentation and tests that prove the above local-only boundary.

## Scope constraints

The first code scope must remain:

- local-only;
- operator-supervised;
- disabled by default;
- fake-transport or dry-run only unless the operator explicitly approves a local harness action;
- non-provider;
- non-browser-automation;
- non-credential;
- non-deployment;
- non-billing;
- non-product-exposed;
- non-promotional for evidence.
