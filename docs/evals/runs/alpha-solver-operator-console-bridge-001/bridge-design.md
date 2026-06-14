# Bridge Design

## Goal

Define a narrow local bridge pattern that lets an operator console invoke approved Alpha Solver actions without changing existing solver contracts in this packet.

## Proposed bridge responsibilities

- expose a localhost-only control surface;
- validate operator requests before dispatch;
- translate approved requests into existing commands or functions;
- preserve deterministic inputs where required by existing specs;
- capture structured results for the console;
- redact secrets and sensitive paths from logs;
- return clear fail-closed errors when a request is outside the allowlist.

## Non-goals

- no public web service;
- no hosted provider fallback;
- no new solver behavior;
- no background daemon requirement;
- no credential persistence;
- no changes to portable or modular entrypoint semantics.

## Request lifecycle

1. Operator starts the bridge locally.
2. Bridge emits a short-lived local session token.
3. Console connects to loopback and presents the token.
4. Bridge validates origin, token, operation, and parameters.
5. Bridge dispatches only allowlisted local work.
6. Bridge returns a structured response with redaction applied.
7. Bridge exits or expires credentials according to operator-configured lifetime.

## Allowlist-first model

The bridge should start with no implicit command execution. Each operation must be added deliberately with tests and documentation.
