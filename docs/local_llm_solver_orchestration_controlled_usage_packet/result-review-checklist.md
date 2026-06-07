# Result Review Checklist

Use this checklist only after a future approved controlled usage operator run.

## Provenance review

- [ ] Exact command is captured.
- [ ] Repo HEAD is captured.
- [ ] Repo status is captured.
- [ ] CLI version or command identity is captured as `python -m alpha.local_llm.operator_cli`.
- [ ] Stdout artifact is captured.
- [ ] Stderr artifact is captured.
- [ ] Exit code is captured.
- [ ] Redacted normalized JSON output is captured.

## Safety flag review

- [ ] Top-level or metadata confirmation shows `behavior_evidence=false`.
- [ ] Top-level or metadata confirmation shows `no_hosted_fallback=true`.
- [ ] Top-level or metadata confirmation shows `no_provider_keys_required=true`.
- [ ] No hosted provider keys appear in artifacts.
- [ ] No hosted provider execution appears in artifacts.
- [ ] No hosted fallback appears in artifacts.
- [ ] No provider fallback appears in artifacts.

## Surface review

- [ ] No `/v1/solve` route is exposed.
- [ ] No `/v1/solve` route is called.
- [ ] No dashboard route is exposed.
- [ ] No dashboard route is called.
- [ ] No billing route, billing claim, or billing artifact is introduced.

## Claim review

- [ ] The result is described only as Level 2 local operator usability output.
- [ ] No production readiness claim is made.
- [ ] No MVP readiness claim is made.
- [ ] No benchmark evidence claim is made.
- [ ] No local model quality claim is made.
- [ ] No provider-orchestration evidence claim is made.
- [ ] No Alpha superiority claim is made.
- [ ] No dashboard readiness claim is made.
- [ ] No `/v1/solve` readiness claim is made.
- [ ] No broad runtime readiness claim is made.
- [ ] No evidence-model promotion claim is made.

## Outcome review

- [ ] If all checks pass, record the result as controlled usage operator-run artifact review only.
- [ ] If any check fails, do not promote the result; stop and use the blocker fallback lane or a new approved fix lane.
