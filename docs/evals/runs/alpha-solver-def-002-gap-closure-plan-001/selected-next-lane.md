# Selected next lane

Selected next lane: `ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001`

## Why this lane

RR-02 is High severity and records that dashboard-managed provider API keys are
persisted as plaintext JSON without at-rest protection or explicit restrictive
file modes. This is the highest-risk concrete implementation gap because it
concerns credential material stored on disk. RR-03 is also High severity, but it
is sequenced immediately after RR-02 so credential storage and default credential
semantics can remain narrow, separately testable changes.

## Scope for the selected lane

The selected lane should address only credential storage hardening evidence for
RR-02 unless the operator explicitly expands scope. It should not fix CORS,
default credentials, auth/tenancy, dashboard exposure, provider behavior, model
behavior, or `/v1/solve` exposure in the same lane.

## Required evidence for completion of the selected lane

- Code/config evidence of protected at-rest storage or an explicitly fail-closed
  no-persistence design.
- Restrictive file/directory permission evidence where file storage remains.
- Tests proving masked display and masked audit behavior still do not reveal
  secrets.
- Tests using synthetic placeholder values only.
- Documentation of migration or handling for existing plaintext secret files.

## Non-selection notes

No other lane is selected as next by this packet. Later lanes remain sequenced in
`closure-sequence.md` but are not authorized as parallel next lanes.
