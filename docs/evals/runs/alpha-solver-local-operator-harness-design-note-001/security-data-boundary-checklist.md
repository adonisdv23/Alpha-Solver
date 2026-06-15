# Security and Data Boundary Checklist

This checklist is mandatory for interpreting this design note. Every item is a blocked action for this lane.

- No external upload.
- No provider calls.
- No token use.
- No credentials.
- No model calls.
- No hosted model calls.
- No local model calls.
- No model pull or install.
- No dashboard exposure.
- No `/v1/solve` exposure.
- No public API exposure.
- No Google Sheets mutation.
- No Pi.dev install.
- No Pi.dev run.
- No Pi.dev integration.
- No Pi.dev vendoring or code copy.
- No package install.
- No dependency addition.
- No shell feature activation for a future harness.
- No file-operation feature activation for a future harness.
- No MCP feature activation for a future harness.
- No email feature activation.
- No calendar feature activation.
- No memory feature activation.
- No credentials, auth files, env files, billing pages, subscription pages, or private token stores may be inspected for this lane.
