# Risk Model Overview

## Protected assets

- User prompts, uploaded context, private operator notes, and any future request metadata.
- Provider credentials, dashboard credentials, cookies, CSRF tokens, session values, API keys, and billing identifiers.
- Solver outputs, traces, score sheets, run packets, evidence artifacts, and decision ledgers.
- Route configuration, provider/fallback configuration, budget limits, and product-readiness status.

## Actors and misuse sources

- Legitimate operators who may misunderstand readiness boundaries.
- External users if a future surface is exposed before authorization.
- Internal reviewers who may over-promote evidence or cite unsupported claims.
- Automated agents that may follow stale docs or infer route/provider/dashboard readiness from packet existence.
- Attackers seeking prompt data, credentials, billing abuse, route enumeration, or dashboard access.

## Trust boundaries

- Local docs versus runtime behavior.
- Internal review packets versus public product claims.
- Operator-only artifacts versus user-facing product surfaces.
- Local model/provider configuration versus hosted provider calls.
- Evidence artifacts versus promoted readiness, quality, or benchmark claims.

## Primary risk themes

- Abuse cases and prompt injection risks if future surfaces accept untrusted input.
- Privacy and data-retention risks if future artifacts include sensitive request content.
- evidence-promotion risks if Level 2 or Level 3 evidence is treated as product readiness.
- Unsupported-claim risks if docs imply benchmark, quality, provider, route, dashboard, billing, MVP, production, or product readiness.
- route exposure risks if `/v1/solve` or related routes are exposed before authentication, authorization, rate limiting, logging, privacy, and stop-condition controls are approved.
- dashboard risks if a dashboard is reachable without strong session, secret, CSRF, and redaction controls.
- Provider and fallback confusion risks if local, hosted, fallback, billing, or model-inference paths are ambiguous.

## Level 6 control

Level 6 controls whether and how this packet is used. This packet is not approval to implement product-surface changes, expose routes, expose dashboards, call providers, add fallback, bill users, run benchmarks, run model inference, or promote evidence.
