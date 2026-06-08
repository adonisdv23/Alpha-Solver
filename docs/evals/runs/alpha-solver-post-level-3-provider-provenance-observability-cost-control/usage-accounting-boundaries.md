# Usage Accounting Boundaries

## Purpose

This file defines future usage accounting boundaries for provider-related paths. It does not create usage records, normalize provider usage, bill money, or inspect provider billing systems.

## Boundary principles

- Usage accounting must separate design intent, local estimates, provider-reported usage, reconciled usage, billing impact, and budget enforcement.
- A usage record must not be inferred solely from a response existing unless provenance shows a provider path was actually attempted and approved usage data exists.
- Local estimates must be labeled as estimates and must not be presented as provider-reported usage.
- Provider-reported usage must name the usage source label and the provider provenance record it belongs to.
- Reconciled usage must state the reconciliation source and date when approved by a future implementation lane.
- Disputed, partial, stale, redacted, or unavailable usage data must be labeled explicitly.

## Included future usage categories

| Category | Boundary |
| --- | --- |
| Request count | Count of attempted, blocked, succeeded, failed, retried, or safe-out requests, separated by state. |
| Input units | Input units only when sourced and approved; never inferred from raw prompt capture in this packet. |
| Output units | Output units only when sourced and approved; never inferred from raw response capture in this packet. |
| Runtime seconds | Local or provider runtime duration only when measured by approved instrumentation. |
| Tool calls | Tool or provider call counts only when trace records identify approved call boundaries. |
| Cached responses | Cached response usage separated from new provider call usage. |
| Safe-out responses | Safe-out responses counted separately from provider attempts. |

## Exclusions

- This packet does not define a billing ledger.
- This packet does not authorize cost allocation to users, teams, providers, or accounts.
- This packet does not create token counters, metering services, dashboards, alerts, or invoices.
- This packet does not convert local estimates into actual cost claims.
- This packet does not inspect provider invoices, provider consoles, payment systems, or quota dashboards.

## Level 7 control

Level 7 controls whether and how any usage accounting boundary is implemented, replaced, or rejected.
