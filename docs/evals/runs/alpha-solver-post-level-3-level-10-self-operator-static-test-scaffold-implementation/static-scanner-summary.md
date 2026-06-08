# Static scanner summary

`tests/helpers/self_operator_static_scan.py` adds a deterministic, offline, test-only scanner.

The scanner:

- Accepts fixture paths or text.
- Reads inert fixture text with Python standard-library file and JSON parsing only.
- Returns stable finding objects with `id`, `path`, `reason`, `blocked_surface`, and `recommended_stop_state`.
- Sorts findings for deterministic output.
- Does not import or execute fixture code.
- Does not call providers, hosted models, local models, external APIs, browser automation, deployment, billing, Google Sheets, dashboard routes, or CLI behavior.
