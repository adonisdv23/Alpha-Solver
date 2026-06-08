# Future Stop and Recovery

## Use boundary

These instructions are a future fail-closed draft. They do not provide or imply a current Self Operator stop command.

## Stop triggers

A future operator must stop before continuing when any of the following occurs:

- **Missing evidence:** required implementation, spec, provenance, artifact, or safety evidence is absent or stale.
- **Missing approval:** approval is absent, expired, not recorded, or inconsistent with the live run.
- **Unclear task:** the objective, scope, file write set, or completion criteria becomes ambiguous.
- **Provider/fallback ambiguity:** selected provider, model, runtime, hosted fallback, local fallback, or no-fallback state is unclear.
- **Credential risk:** logs, diffs, artifacts, process output, or config may expose secrets.
- **Branch pollution:** unexpected files, unrelated diffs, untracked artifacts, staged changes, deleted files, merge conflicts, or wrong-branch activity appears.

## Future stop procedure

1. Halt the future Self Operator using the approved stop mechanism for that implementation.
2. Do not start a replacement run until the stop reason is reviewed.
3. Preserve logs, command provenance, artifact paths, git status, and timestamps.
4. Redact or quarantine any artifact with possible credential exposure.
5. Record whether the stop was operator-initiated, system-initiated, or safety-gate-initiated.
6. Record the last known approved action and the first observed deviation.
7. Leave the worktree unchanged until a human determines whether to keep, revert, or archive changes.

## Recovery rules

- Prefer fail-closed recovery over task completion.
- Do not retry with a different provider, fallback, credential, branch, or task without new approval.
- Do not merge, deploy, publish, or promote artifacts from a stopped run unless a later review lane explicitly authorizes it.
- If branch pollution occurred, preserve evidence first, then isolate or reset only under explicit human direction.
