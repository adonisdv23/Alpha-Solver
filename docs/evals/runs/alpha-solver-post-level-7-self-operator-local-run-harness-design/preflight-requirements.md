# Preflight Requirements

A future local-only Self Operator harness should fail closed unless all required preflights pass.

## Required preflights

- **Repository location:** confirm the harness is running from the intended repository root.
- **Branch and status capture:** record branch name and `git status --short` before executing a task.
- **Task manifest presence:** require a local manifest or operator-supplied task description that declares allowed command, timeout, artifact path, and expected stop states.
- **Local-only assertion:** require the task manifest to state: no provider calls, no hosted model calls, no local model execution unless a later explicit local-only implementation lane authorizes it, no external API calls, no fallback, no credential use, no billing, no dashboard exposure, no `/v1/solve` exposure, and no evidence promotion.
- **Network boundary check:** require the command plan to avoid network-dependent operations unless a future authorized lane explicitly permits a local-only network-free substitute. The default should be no outbound network use.
- **Credential boundary check:** confirm no environment variable, secret file, token, API key, browser profile, or cloud credential is required.
- **Command allowlist check:** run only bounded local preflights, local artifact capture, and local docs/checker commands explicitly allowed by a future implementation lane.
- **Timeout check:** require a bounded runtime limit before execution starts.
- **Artifact path check:** require artifacts to be written only inside the approved local run artifact directory.
- **Overwrite check:** refuse to overwrite existing artifacts from prior runs.
- **Redaction plan check:** require stdout, stderr, and manifests to be reviewed for secrets before any human-facing summary is generated.

## Preflight stop behavior

If a preflight fails, the future harness should:

1. Stop before task execution.
2. Record a `PREFLIGHT_FAILED` stop state.
3. Capture which preflight failed.
4. Enforce no fallback execution.
5. Avoid external remediation.
6. Avoid evidence promotion.
