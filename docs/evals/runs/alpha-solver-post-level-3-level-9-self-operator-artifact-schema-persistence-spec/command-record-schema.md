# Command record schema

Command records are local-only JSON lines with:

- `started_at_utc`
- `command`
- `working_directory`
- `exit_code`
- `stdout_artifact`
- `stderr_artifact`
- `redaction_applied`
- `network_expected: false`

Commands must not include network calls, provider calls, package installation, deployment, billing, browser automation, or credential access.
