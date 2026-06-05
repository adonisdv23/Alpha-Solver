# Operator Runbook Template

Do not execute this runbook in the scaffold lane. This is a template for a later authorized smoke lane only.

## Pre-Run Gate

Record each item before execution:

- [ ] Future implementation PR merged.
- [ ] Future review gate authorizes runtime smoke.
- [ ] Endpoint is localhost or loopback only.
- [ ] Exact local model name is known.
- [ ] Finite timeout is configured.
- [ ] Hosted provider fallback is disabled.
- [ ] No hosted provider keys are required for local mode.
- [ ] Raw artifact capture path is ready.
- [ ] Sanitized import path is ready.
- [ ] `behavior_evidence=false` remains preserved unless a later lane explicitly changes the evidence model.

## Endpoint Locality Requirement

Allowed endpoint forms are localhost or loopback only, such as:

- `http://localhost:<port>`
- `http://127.0.0.1:<port>`
- `http://[::1]:<port>`

Any externally routable hostname, private network host, public IP, hosted provider URL, or proxy endpoint fails the locality gate.

## Execution Placeholder

Execution command must be copied from `local-runtime-smoke-command-template.md` only after a future implementation lane replaces placeholders with reviewed implementation details.

## Post-Run Placeholder

After a future authorized execution:

1. Preserve raw artifacts without destructive edits.
2. Apply redaction rules.
3. Import sanitized results only in a future import lane or authorized import step.
4. Preserve failure classification and evidence boundary language.
