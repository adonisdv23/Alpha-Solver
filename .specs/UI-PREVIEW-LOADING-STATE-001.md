# UI-PREVIEW-LOADING-STATE-001 · Expert Preview Loading State

## Purpose

Add a narrow UI-only loading state and duplicate-submit guard for `/dashboard/expert-preview` so a controlled operator preview request cannot be accidentally submitted twice while the first request is still in flight.

This cleanup was discovered during controlled live OpenAI preview testing with a one-request cap. It does not validate the MVP, claim production readiness, or change provider behavior.

## Scope

In scope:

- keep the existing expert-preview form, prompt extraction, prompt preservation, CSRF header behavior, async fetch path, and DOM replacement flow;
- immediately disable the compare submit button after a submit starts;
- change the button label to a running/loading message while the request is in flight;
- ignore duplicate submit events for the currently rendered form while its request is in flight;
- keep the prompt textarea visible and readable while a request is running;
- reinitialize the submit handler after the returned page body is rendered.

Out of scope:

- enabling OpenAI;
- Cloud Run deployment;
- provider behavior changes;
- expert-pass behavior changes;
- dashboard auth/session/CSRF changes;
- live spend guard semantic changes;
- local-provider behavior changes;
- persistent quota storage;
- backlog workbook or Google Sheets updates.

## Acceptance criteria

No-network tests should prove:

- the rendered page includes loading-state and duplicate-submit protection for the preview submit script;
- local-provider preview submit still returns `200` and renders both panes;
- existing browser-style form submits still pass;
- CSRF rejection remains unchanged;
- successful responses preserve the submitted prompt;
- blocked/error responses preserve the submitted prompt;
- live preview cap behavior remains unchanged;
- rendered pages do not expose secrets, raw headers, bearer tokens, API keys, raw request bodies, or provider payloads.

## Backlog impact

`UI-PREVIEW-LOADING-STATE-001` should be marked Done only after the PR implementing this spec is merged. `DEPLOY-CLOUDRUN-LIVE-OPENAI-001` remains inconclusive/held until this fix is merged, deployed, and the one-request live test is repeated. This spec does not validate the MVP and does not claim production readiness.
