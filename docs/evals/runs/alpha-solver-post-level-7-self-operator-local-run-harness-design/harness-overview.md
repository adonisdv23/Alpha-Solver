# Harness Overview

## Purpose

A future Self Operator local run harness would coordinate a narrow local-only workflow for an operator-approved task. The design goal is to make local preflight checks, bounded local execution, artifact capture, and stop handling explicit before any runner is implemented.

## Future local-only phases

A future local harness should be structured as four local-only phases:

1. **Preflight phase** — validate repository state, packet evidence, operator intent, branch cleanliness, and local command allowlists before any task begins.
2. **Bounded local task phase** — run only explicitly authorized local-only commands or local docs/checker tasks within a declared scope.
3. **Artifact capture phase** — store local logs, command metadata, manifests, and stop-state records without promoting them as evidence.
4. **Closeout phase** — summarize local results, stop states, and unresolved blockers for human review.

## Relationship to accepted prep packets

This packet is a supporting reference for the existing Self Operator prep packets. It relies on their accepted scope, lifecycle, approval, artifact, risk, and runbook concepts while adding a local-only harness design view.

This packet does not supersede those prep packets. If this packet conflicts with a stricter accepted Self Operator prep packet boundary, the stricter boundary should govern future work.

## Explicit non-authorization

This packet does not implement a runner. This packet does not start Level 8. This packet does not authorize provider calls, hosted model calls, local model runs, external API calls, fallback, credential use, billing, dashboard exposure, `/v1/solve` exposure, browser automation, deployment, or evidence promotion.
