# UI-REQ-001 · Dashboard Request Submission UI

## Goal
Provide a lightweight web experience that allows operators to submit a prompt to Alpha Solver, receive an acknowledgement immediately, and poll for completion.

## Functional Requirements
- Render an HTML form with a textarea for the prompt, a provider dropdown, and a submit button.
- `POST /requests` enqueues an in-memory job and responds with `{ "id": "<uuid>" }`.
- `GET /requests/<id>` returns `{ "id", "status", "latency_ms", "provider", "cache_hit" }` reflecting the job state.
- Background execution is mocked; no external network calls are performed.

## UX Notes
- Show acknowledgement latency after submit and reveal a status pane that auto-polls until the job completes.
- Surface validation errors inline without reloading the page.

## Testing
- `tests/ui/test_requests.py` performs an end-to-end flow verifying the SLA (ack under 500 ms), the job lifecycle, and the status payload contract.
