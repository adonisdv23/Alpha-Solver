# Artifact Capture Template

Use this template only for a future approved controlled usage operator-run lane. This packet does not capture run artifacts because no controlled usage run is executed here.

## Required artifact metadata

```text
lane: ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-CONTROLLED-USAGE-OPERATOR-RUN-001
command_identity: python -m alpha.local_llm.operator_cli
exact_command: <copy exact command here>
repo_head: <git rev-parse HEAD>
repo_status: <git status --short output>
cli_version_or_command_identity: python -m alpha.local_llm.operator_cli
stdout_artifact: <path>
stderr_artifact: <path>
exit_code: <integer>
redacted_normalized_json_output: <path>
behavior_evidence: false
no_hosted_fallback: true
no_provider_keys_required: true
operator: <operator initials or handle>
runtime_host: <redacted local host label>
started_at_utc: <timestamp>
completed_at_utc: <timestamp>
```

## Required captured artifacts

- exact command;
- repo HEAD;
- repo status;
- CLI version or command identity;
- stdout;
- stderr;
- exit code;
- redacted normalized JSON output;
- confirmation of `behavior_evidence=false`;
- confirmation of `no_hosted_fallback=true`;
- confirmation of `no_provider_keys_required=true`.

## Redaction rules

Redact before sharing beyond the future lane's approved artifact location:

- secrets or provider keys if present in the shell environment, logs, prompt, stderr, stdout, or copied terminal context;
- raw unsafe diagnostic text;
- local usernames and machine-specific paths where not needed for provenance;
- prompt content if it includes private, sensitive, or unsafe content;
- raw model output if it contains private, sensitive, or unsafe content.

## Invalid artifact states

The future result review must stop if any required artifact is missing, if `repo_head` is not recorded, if `repo_status` is missing, if stdout or stderr is overwritten, if the exit code is absent, or if safety-flag confirmations are absent.
