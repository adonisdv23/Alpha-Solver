# UI-PREVIEW-REQUEST-METRICS-001 · Expert Preview Request Metrics Panel

## Status

Implemented for PR review; mark Done in external backlog only after the PR is merged.

## Motivation

The first controlled operator demo identified a need for per-run observability in `/dashboard/expert-preview`. Operators need lightweight latency, usage, and estimated-cost visibility to compare plain same-provider output with the Alpha Solver expert preview responsibly.

## Scope

Add a per-response request metrics panel to `/dashboard/expert-preview` that is visible after a successful preview submit. The panel is not persisted and does not add deployment, OpenAI enablement, Cloud Run, or Google Sheets work.

## Display Contract

The panel should show:

- total wall-clock preview latency;
- provider, model, and mode/route where safely available;
- provider call count where exact response metadata is available;
- input, output, and total tokens where safe usage metadata is available;
- estimated API cost and cost source where cost metadata is available;
- separate rows for plain provider output and Alpha Solver expert preview when both responses are rendered.

Missing call count, token, latency, model, or cost metadata must render as `unknown` or `not estimated` rather than being guessed.

## Safety Boundaries

The panel must be allowlist-rendered. It must not render API keys, bearer tokens, raw provider payloads, raw request bodies, raw headers, cookies, CSRF tokens, session values, provider account identifiers, raw metadata dumps, or secrets.

## Non-Goals

This does not validate the MVP, prove Alpha Solver superiority, prove production readiness, benchmark answer quality, claim exact billing accuracy, change dashboard auth/session/CSRF, weaken live spend guard behavior, enable OpenAI, deploy Cloud Run, add persistent storage, or update Google Sheets.
