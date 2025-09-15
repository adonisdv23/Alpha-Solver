# UI-RUN-001 · Dashboard One-click Demo Run

## Goal
Implement a dashboard entry point that lets operators trigger a canned Alpha Solver demo request and immediately review the outcome with latency and cache metadata.

## Functional Requirements
- `GET /run` renders an HTML page with a single "Run Demo" control backed by the provided template (`ui_run_button_v1`).
- `POST /run` executes the canned workflow through the in-memory broker/cache mock and responds with `{ "result", "latency_ms", "cache_hit" }`.
- Subsequent posts hit the cache path and return the same result text while toggling `cache_hit` to `true`.

## UX Notes
- Surface the latest demo output in place without leaving the page and show latency/cache values alongside the snippet.
- Keep the first paint lightweight so the button renders well under the 2-second SLA.

## Testing
- `tests/ui/test_run.py` issues end-to-end requests covering the GET render timing, the POST payload contract, and cache-hit behaviour without performing any external network calls.
