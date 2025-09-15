# UI-JOBS-001 · Dashboard Job History & Metrics (RES_Dash)

## Goal
Implement the dashboard job history and metrics view that surfaces the most recent execution records and lightweight observability for operators.

## Functional Requirements
- Provide a server-rendered page at `GET /jobs` that displays the last 100 dashboard jobs (id, provider, status, latency_ms, cache_hit).
- Support sorting the visible jobs by submission time (ascending/descending) and latency (ascending/descending).
- Each table row must link to `/jobs/<id>` for downstream detail and log views.
- Include a status summary component with counts of the displayed jobs grouped by status.

## Performance Notes
- The page should render in under two seconds locally. Keep the implementation in-memory without external I/O.

## UX Notes
- Present the data in a tabular layout with clear headers and action-oriented sort controls.
- Surface the status summary adjacent to the table for quick at-a-glance diagnostics.

## Testing
- `tests/ui/test_jobs.py` validates table shape, limiting to 100 rows, sorting behaviour, status summaries, cache hit rendering, and link construction.
