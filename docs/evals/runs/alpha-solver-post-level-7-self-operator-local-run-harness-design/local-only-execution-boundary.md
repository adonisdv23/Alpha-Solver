# Local-Only Execution Boundary

## Boundary statement

A future Self Operator local run harness must be local-only by default and must fail closed when a task requests external action. Local-only means the harness may read repository files, run approved local commands, and write artifacts to an approved local directory. It must not interact with external providers, hosted models, external APIs, dashboards, deployment targets, browsers, credentials, billing systems, `/v1/solve` exposure paths, fallback paths, or evidence promotion systems.

## Allowed future harness actions

The harness may only perform bounded local preflights, local artifact capture, and local docs/checker commands that are explicitly allowed by a future implementation lane.

- Read local repository files needed for the approved task.
- Run allowlisted local docs/checker commands with explicit timeouts.
- Capture stdout, stderr, exit code, elapsed time, and local manifests.
- Write artifacts under the approved local run artifact directory.
- Produce a local operator summary that clearly labels the run as non-promotional.
- Stop safely when the requested task exceeds the local-only boundary.

## Required controls

- Default-deny command policy.
- Explicit allowlist for local commands.
- No implicit shell expansion into external tools.
- No credential discovery.
- No browser automation hooks.
- No service deployment hooks.
- No dashboard publish hooks.
- No provider SDK initialization.
- no provider calls.
- no hosted model calls.
- no local model execution unless a later explicit local-only implementation lane authorizes it.
- no external API calls.
- no fallback.
- no credential use.
- no billing.
- no dashboard exposure.
- no `/v1/solve` exposure.
- No billing or metering calls.
- No evidence-promotion writes.

## Boundary confirmation

The design in this packet is docs-only. It does not create a runner, execute bounded tasks, run models, call providers, modify runtime, or promote evidence.
