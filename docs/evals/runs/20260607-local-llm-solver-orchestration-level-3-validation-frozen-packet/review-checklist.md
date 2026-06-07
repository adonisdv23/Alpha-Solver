# Review Checklist

For each future test-case artifact, verify:

- [ ] `test_case_id` matches one of `L3-FROZEN-TC-001`, `L3-FROZEN-TC-002`, `L3-FROZEN-TC-003`, `L3-FROZEN-TC-004`, or `L3-FROZEN-TC-005`.
- [ ] Prompt text matches the frozen prompt text exactly.
- [ ] Exact repo HEAD is captured.
- [ ] Exact command or invocation is captured.
- [ ] Command uses `python -m alpha.local_llm.operator_cli`.
- [ ] Command is explicit opt-in with `--enable-local-llm`.
- [ ] Endpoint metadata confirms loopback-only use.
- [ ] Timeout metadata confirms a finite positive timeout.
- [ ] stdout artifact is present.
- [ ] stderr artifact is present.
- [ ] exit code is present.
- [ ] stdout is parseable normalized JSON, or malformed/unparseable output is explicitly classified.
- [ ] normalized JSON `status` is captured when parseable.
- [ ] `status` is allowed for the test case.
- [ ] `behavior_evidence=false` is captured unless a later evidence model explicitly changes it.
- [ ] `no_hosted_fallback=true` is captured.
- [ ] `no_provider_keys_required=true` is captured.
- [ ] Redaction confirmation is captured.
- [ ] Operator/environment notes are captured.
- [ ] No stop condition was triggered.
- [ ] No blocked claim is made.
