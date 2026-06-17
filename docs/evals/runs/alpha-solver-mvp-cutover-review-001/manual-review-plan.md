# Manual review plan

This plan is for a local operator reviewing the MVP candidate manually.

1. Open the local console from the repository root with `python -m uvicorn tools.operator_test_console:app --host 127.0.0.1 --port 8765`. Run this from an environment where project dependencies are installed, for example after activating `.venv` and installing project dependencies.
2. Click or use the route preview path first; do not submit smoke execution first.
3. Enter a non-sensitive test task and request route preview without running smoke.
4. Verify that the preview displays a recommended model path and recommended tool path.
5. Verify that route reasons, warnings, fallback path, and evidence boundary are visible.
6. Verify that execution authorization flags remain false for provider execution, local-model execution, and tool execution in the preview metadata.
7. Verify prompt-too-long behavior by exceeding the documented prompt limit and confirming the console fails closed rather than running smoke.
8. Verify sanitized JSON copy behavior by copying only from the sanitized JSON panel and confirming raw secrets or sensitive content are not copied.
9. Stop immediately if sensitive content appears in preview, result, logs, copied JSON, terminal output, browser UI, or recorded notes.
10. Record only bounded evidence: screenshots or notes showing the local console exists, preview metadata appears, execution flags are false, smoke execution is separate, prompt-too-long fails closed, and sanitized JSON copy is scoped.
11. Do not claim provider quality, local-model quality, tool quality, security/privacy completion, benchmark success, production/public readiness, autonomous execution readiness, or Alpha superiority.
12. Do not execute the routed-vs-plain pilot unless a later separate authorization explicitly permits it.
