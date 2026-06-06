# Redaction Rules

## Non-Execution Notice

This scaffold is blocked until a future implementation PR creates a local solver orchestration runner. It is scaffold-only and is not runtime evidence. It does not execute a local LLM, does not call hosted providers, does not import results, and does not close any track.

## Required Redactions

Future artifacts must redact or omit:

- Provider keys.
- Private URLs.
- Private local paths except the repo-root placeholder `<REPO_ROOT>`.
- Full environment dumps.
- Raw credentials.

## Allowed Placeholders

- `<REPO_ROOT>` for the repository root.
- `<LOCAL_ENDPOINT_SUMMARY>` for a non-secret local endpoint summary.
- `<LOCAL_MODEL>` for the local model identifier.
- `<TIMEOUT_SECONDS>` for timeout configuration.
- `<REDACTED>` for any omitted sensitive value.

## Review Checklist

- [ ] No provider keys are present.
- [ ] No private URLs are present.
- [ ] No private local paths appear outside `<REPO_ROOT>`.
- [ ] No full environment dump is present.
- [ ] No raw credentials are present.
