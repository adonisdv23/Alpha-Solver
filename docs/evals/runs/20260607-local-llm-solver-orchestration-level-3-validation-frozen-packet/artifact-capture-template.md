# Artifact Capture Template

## Per-test-case required artifacts

For every future execution test case, capture:

- exact repo HEAD;
- exact command or invocation;
- test-case ID;
- prompt source;
- stdout artifact;
- stderr artifact;
- exit code;
- parseable normalized JSON;
- normalized JSON `status`;
- `behavior_evidence` value;
- `no_hosted_fallback` value;
- `no_provider_keys_required` value;
- endpoint locality metadata sufficient to confirm loopback-only use;
- timeout value sufficient to confirm finite-timeout use;
- redaction confirmation;
- operator/environment notes.

## Suggested artifact filenames

For each `test_case_id`, a later execution lane should create an isolated directory and include:

- `repo_head.txt`
- `executed_command.txt`
- `test_case_id.txt`
- `prompt_source.txt`
- `prompt.txt`
- `stdout.json`
- `stderr.txt`
- `exit_code.txt`
- `normalized_status.txt`
- `safety_flags.json`
- `endpoint_locality.txt`
- `timeout.txt`
- `redaction_confirmation.txt`
- `operator_environment_notes.md`
- `review_notes.md`

## Normalized JSON expectations

The stdout artifact must be parseable normalized JSON. The reviewer must record:

- whether JSON parsing succeeded;
- normalized JSON `status`;
- `behavior_evidence` value;
- `no_hosted_fallback` value;
- `no_provider_keys_required` value;
- endpoint locality metadata;
- timeout metadata.

If stdout is malformed or unparseable, the future execution lane must classify it explicitly as malformed or unparseable and then stop for review under the blocker fallback rules.
