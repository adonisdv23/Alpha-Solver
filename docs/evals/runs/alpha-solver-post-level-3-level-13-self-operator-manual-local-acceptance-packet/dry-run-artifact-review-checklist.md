# Dry-Run Artifact Review Checklist

For each future acceptance task, review generated artifacts only after operator execution.

- [ ] `dry-run-result.json` exists when expected.
- [ ] `execution-gate-result.json` exists when expected.
- [ ] `stop-state.json` exists when blocked.
- [ ] Schema version is present and expected.
- [ ] Lane ID matches the execution lane.
- [ ] Run ID is present and consistent across artifacts.
- [ ] Approval summary is present and redacted.
- [ ] Preflight summary is present and redacted.
- [ ] Gate summary is present and redacted.
- [ ] Stop-state summary is present when blocked.
- [ ] Artifact paths are inside the temporary output root.
- [ ] Redaction status is safe.
- [ ] Evidence boundary is present.
- [ ] Non-execution confirmation is present.
- [ ] Selected next lane is recorded.
