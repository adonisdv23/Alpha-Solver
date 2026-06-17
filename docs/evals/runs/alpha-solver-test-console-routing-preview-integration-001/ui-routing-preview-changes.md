# UI routing preview changes

- Added a route preview card before the bounded smoke-check form.
- Added a separate `Preview route only` action that posts to `/preview`.
- Kept the smoke action as the separate `Run bounded smoke check` form action.
- Displayed task family when available, recommended model path, recommended tool family/tool id, reasons, warnings, fallback path, evidence boundary, provider/local execution authorization, and tool execution authorization.
- Preserved the existing mode/model manual override controls for bounded smoke execution.

The UI states that route preview is metadata-only, tool recommendation is not tool execution, model recommendation is not model validation, and preview does not authorize provider or local model execution.
