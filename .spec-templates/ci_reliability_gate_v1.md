Encode stricter retry SLO and circuit-breaker timing in CI gates.

### Details
- Tests write retry counts and breaker_open_ms to pytest JSON.
- Gate script parses report and enforces p95 thresholds.

### PR Checklist
- [ ] JSON report generated
- [ ] p95 checks computed
- [ ] Workflow fails on breach
