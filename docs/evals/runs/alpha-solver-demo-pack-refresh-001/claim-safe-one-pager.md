# Claim-Safe One-Pager

## What Alpha Solver is trying to be

Alpha Solver is a discrimination-and-judgment layer that sits before generation. It is intended to infer the deeper task behind a prompt, surface hidden constraints, route the work, and refuse or stop when answering would be unsupported.

## The wedge

- Discrimination: infer the real task behind the prompt.
- Stopping: decline to answer when it should not answer.
- Hidden constraints: surface unstated assumptions before generating.
- Calibrated refusal: refuse or ask for clarification without over-refusing low-risk requests.
- Decision trail: preserve an auditable record of why it answered, refused, routed, or limited a claim.

## What this packet shows

This packet shows five illustrative scenarios for explaining the intended wedge to a founder, technical reviewer, incubator reviewer, or trusted early reviewer. It is a demo narrative and documentation artifact only.

## What this packet does not prove

This packet does not prove value, runtime behavior, provider behavior, benchmark success, public readiness, production readiness, dashboard readiness, `/v1/solve` readiness, security/privacy completion, traction, product-market fit, or Alpha superiority.

## Current evidence posture

Existing evidence is offline, docs, or fixture evidence. Track S simulation was not run and has no scores. Track R runtime/provider execution is blocked. #553 was design-only. #554 records the manual discrimination Value Read as blocked / not executed. Available evidence does not yet show a value-positive, repeatable head-to-head.

## Required next proof

1. Pass the post-#552 successor no-echo / substantive-generation gate or equivalent derivation check.
2. Only after that, consider a local-first generation path to support a value read.
3. Only after that, run a gated head-to-head with preserved artifacts and blind scoring.
4. Keep simulation, runtime, provider, design-only, and docs-only evidence separate.
5. Keep provider work blocked until the post-#552 successor no-echo / substantive-generation gate or equivalent derivation check has passed and the operator explicitly authorizes provider, model, project/billing boundary, cost cap, token cap, max request count, exact synthetic fixture, redaction/data-sharing boundary, and stop conditions.
