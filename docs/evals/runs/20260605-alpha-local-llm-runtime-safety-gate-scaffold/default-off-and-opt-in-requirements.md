# Default-Off and Opt-In Requirements

This is a scaffold only. Local LLM runtime integration is not implemented here.

## Default-off rule

Local LLM runtime use must be default-off. No request path may use a local LLM runtime unless a later implementation lane explicitly defines and implements operator opt-in configuration.

## Explicit configuration rule

A future implementation must require explicit local LLM configuration before any local runtime call is attempted. Silent enablement, implicit auto-discovery, opportunistic routing, and environment-dependent activation are prohibited unless a later lane separately authorizes them.

## No exposure by default

Until explicitly authorized by a later lane:

- `/v1/solve` must not be exposed to local LLM mode;
- dashboard preview must not be exposed to local LLM mode;
- hosted-provider routing must not silently switch into or out of local LLM mode.

## Evidence model preservation

`behavior_evidence=false` must remain preserved for local LLM runtime outputs until a later lane explicitly changes the evidence model.
