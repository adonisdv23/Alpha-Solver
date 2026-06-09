# Interpretation Engine Summary

The engine accepts a JSON mapping containing task-level import records. It supports `task_records`, `tasks`, `results`, and mapping-shaped `task_results` without requiring the result-import module to exist.

The public API is:
- `AcceptanceInterpretation`
- `AcceptanceTaskInterpretation`
- `AcceptanceDefect`
- `interpret_acceptance_import_summary(import_summary)`
- `write_acceptance_interpretation(interpretation, output_path)`

The output is deterministic JSON with sorted keys and bounded readiness implications.
