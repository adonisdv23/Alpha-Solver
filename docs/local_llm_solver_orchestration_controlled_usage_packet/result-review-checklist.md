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

## CLI success review

- [ ] Captured `exit_code` is exactly `0` before the controlled usage operator-run artifact review is accepted.
- [ ] Redacted normalized JSON parses successfully before the artifact review is accepted.
- [ ] Accepted normalized JSON `status` is exactly one of `ok`, `clarify`, or `blocked`.
- [ ] No `failed_closed` status appears in the accepted artifact review.

A `failed_closed` result may be preserved as a failed attempt artifact only. It must not be accepted as a successful controlled usage review. Malformed JSON, missing status, missing exit code, or any nonzero exit code must stop review and use the blocker fallback lane or a new approved fix lane.

## Safety flag review

- [ ] Top-level or metadata confirmation shows `behavior_evidence=false`.
- [ ] Top-level or metadata confirmation shows `no_hosted_fallback=true`.
- [ ] Top-level or metadata confirmation shows `no_provider_keys_required=true`.
- [ ] Confirm these safety flags are necessary but not sufficient for acceptance; the CLI success review must also pass.
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

- [ ] If provenance, CLI success, safety flag, surface, and claim checks all pass, record the result as controlled usage operator-run artifact review only.
- [ ] If any check fails, do not promote the result; stop and use the blocker fallback lane or a new approved fix lane.
