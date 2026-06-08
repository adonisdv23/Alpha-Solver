# Command record schema

Proposed local-only fields for dry-run or preflight commands:

- `command_id`
- `command`
- `cwd`
- `started_at_utc`
- `completed_at_utc`
- `exit_code`
- `classification`
- `redacted_stdout_ref`
- `redacted_stderr_ref`

Commands must be local-only and must not include network calls, providers, credentials, browsers, deployment, billing, package installation, remote fetch, or route exposure.
