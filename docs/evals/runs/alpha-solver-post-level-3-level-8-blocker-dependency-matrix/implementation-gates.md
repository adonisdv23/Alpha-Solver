# Implementation Gates

No implementation may begin from this packet. A future approved implementation spec must close all gates below before code changes are in scope.

## Gate 1: Local-only scope

- Provider calls remain blocked.
- Browser automation remains blocked.
- Credentials remain blocked.
- Hosted fallback, provider fallback, and implicit local fallback remain blocked.
- Deployment and billing remain blocked.

## Gate 2: Human approval controls

A future spec must define:

- which actions require approval;
- how approval is requested;
- how approval is denied or timed out;
- how approver identity is recorded without exposing secrets;
- which actions are impossible even with approval, including autonomous merge unless separately authorized by humans.

## Gate 3: Local artifact persistence

A future spec must define:

- local artifact root and path safety rules;
- run manifest schema;
- immutable run identifier requirements;
- redaction and secret exclusion rules;
- retention and cleanup expectations;
- integrity checks for replay/review.

## Gate 4: Local run harness

A future spec must define:

- command shape;
- accepted inputs;
- expected outputs;
- finite timeout behavior;
- stop reason taxonomy;
- no-network or loopback-only behavior;
- exit codes;
- deterministic fixtures for tests.

## Gate 5: Acceptance test plan

A future spec must define focused tests proving:

- no provider calls are made;
- no browser automation is launched;
- no credentials are required or read;
- no fallback executes;
- no deployment or billing behavior executes;
- no autonomous merge occurs;
- artifacts persist locally according to contract;
- human approval controls block unsafe paths;
- branch scope remains clean;
- evidence labels are not promoted.

## Gate 6: Branch and evidence controls

A future spec must define:

- allowed changed-file paths;
- clean `git status --short` expectations before and after work;
- no unrelated branch edits;
- evidence-boundary wording;
- promotion criteria and explicit non-claims.
