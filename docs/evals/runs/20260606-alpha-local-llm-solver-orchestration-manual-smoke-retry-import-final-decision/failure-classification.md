# Failure Classification

## Final classification

`MANUAL_LOCAL_ORCHESTRATION_SMOKE_RETRY_FAIL_REQUIRES_FIX`

## Why this is complete rather than blocked/incomplete

The command executed, the preserved artifact files are complete, `manual-smoke-redacted-output.json` is parseable, required provenance is present, exit status is `0`, result count is `5`, repo head and script checksum are recorded, provider key booleans are all false, and the artifact supports prompt-by-prompt interpretation.

## Why this is classified as fail-requires-fix

The retry is classified as fail-requires-fix because not all expected smoke modes or outcomes passed:

- Prompt 2 expected `clarify` but observed `mode=block` and `status=blocked`.
- Prompt 3 expected `answer_with_assumptions` but observed `mode=block` and `status=blocked`.

## Failure class

The failure class is a post-pass-one-gating over-blocking failure for clarify and bounded-assumption paths. Boundary claim enforcement improved and high-risk blocking remained intact, so the next lane should not broaden scope beyond clarify and assumption gating.
