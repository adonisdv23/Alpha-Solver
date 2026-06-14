# Authentication and Boundary Map

## Actors

- **Local operator**: a human using the console on a trusted workstation.
- **Operator console**: a future UI or CLI surface that requests local bridge actions.
- **Local bridge**: a future localhost-only adapter that may translate console requests into approved Alpha Solver commands.
- **Alpha Solver runtime**: existing solver entrypoints and supporting scripts.

## Boundary principles

1. The bridge should bind to loopback only by default.
2. The bridge should fail closed when authentication or origin checks are absent.
3. The bridge should not accept remote network traffic unless a later spec explicitly authorizes it.
4. The bridge should not embed long-lived secrets in repo files, logs, docs, or examples.
5. The console should request only allowlisted operations with bounded inputs.

## Authentication shape

A future implementation should prefer short-lived local session credentials or an explicit operator start token. The token should be generated at bridge startup, displayed only to the local operator, and never persisted by default.

## Authorization shape

Authorization should be command-scoped. Each callable bridge operation should declare:

- operation name;
- accepted parameters;
- validation rules;
- side-effect class;
- expected output envelope;
- redaction requirements;
- stop conditions.

## Evidence boundary

This file is a design map only. It does not prove that current code enforces these controls.
