# Authorization Checklist

This checklist is for a later lane. This packet does not grant execution
authority.

## Required before implementation code

- [ ] Lane ID is approved for implementation work.
- [ ] The spec path remains `.specs/alpha-local-llm-provider-integration-spec.md`
  or a later approved spec supersedes it.
- [ ] The selected provider shape remains an Ollama-style local HTTP backend.
- [ ] Proposed source and test files stay inside the approved file boundary.
- [ ] Runtime routing, `/v1/solve`, dashboard preview, hosted providers,
  provider keys, operator evidence, Batch C materials, and backlog workbooks
  remain out of scope.
- [ ] Tests are offline unless a separate smoke gate is approved.

## Required before any local HTTP smoke execution

- [ ] Separate smoke authorization names the lane ID.
- [ ] Host, port, URL path, and transport limits are listed and restricted to an
  approved local endpoint.
- [ ] Timeout is finite and no infinite retry policy is allowed.
- [ ] Opt-in command and environment flag are exact and skip by default.
- [ ] Evidence label distinguishes local smoke output from offline fixtures.
- [ ] Rollback steps are documented before execution.
- [ ] Hosted providers, provider keys, runtime routing, dashboard preview,
  `/v1/solve`, operator evidence edits, Batch C work, readiness claims,
  comparison claims, billing claims, benchmark claims, and provider orchestration
  remain blocked.

## Current packet decision

The current packet leaves every smoke-execution checkbox unchecked. It only
prepares implementation instructions for a future lane.
