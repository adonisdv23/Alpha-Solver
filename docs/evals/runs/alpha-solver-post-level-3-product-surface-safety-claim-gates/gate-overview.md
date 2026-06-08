# Gate Overview

## Gate order

Future product-surface work must satisfy these gates before any user-facing implementation or claim is started:

1. **Scope gate**: confirm the future lane is explicitly authorized and is not using this packet as implementation authority.
2. **Evidence gate**: confirm claim-specific evidence exists, is current, is attributable to artifacts, and is bounded to the exact claim.
3. **Blocked-claims gate**: confirm no blocked claim appears in UI copy, API responses, documentation, dashboard text, release notes, or operator-facing copy.
4. **Allowed-claims gate**: confirm any statement is narrow, factual, non-promotional, and tied to the artifact that supports it.
5. **Safety gate**: confirm no user-facing surface is exposed without separate Level 6 authorization.
6. **Non-promotion gate**: confirm Level 2, Level 3, Level 4, Level 5, and this packet are not promoted beyond their accepted evidence boundary.
7. **Stop-condition gate**: stop immediately if any stop condition in `stop-conditions.md` applies.

## Required result

A future lane may proceed only when every applicable gate is satisfied and Level 6 controls whether and how this packet is used for that lane.

## Non-authorizing boundary

These gates are design requirements, not product authority. This packet does not authorize claims, implement UI/API copy, expose `/v1/solve`, expose dashboards, run models, run benchmarks, call providers, perform billing work, or promote evidence.
