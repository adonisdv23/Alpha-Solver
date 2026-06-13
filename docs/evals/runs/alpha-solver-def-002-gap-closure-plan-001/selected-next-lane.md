# DEF-002-local recommended next remediation lane

DEF-002-local recommended next remediation lane:
`ALPHA-SOLVER-DEF-002-CREDENTIAL-STORAGE-HARDENING-001`

## Repo-global selected next lane boundary

This packet does not change the repo-global selected next lane. The repo-global
selected next lane remains controlled by `docs/CURRENT_STATE.md` and
`docs/LANE_REGISTRY.md`, which identify
`LOCAL-OPENAI-TOKEN-SMOKE-CAPTURE-RETRY-002` as the authoritative repo-global
selected next lane.

The credential-storage lane is only the recommended first remediation candidate
within the DEF-002 gap-closure track. It does not authorize parallel runtime or
security implementation unless the operator explicitly chooses the DEF-002 track.

## Why this DEF-002-local lane

RR-02 is High severity and records that dashboard-managed provider API keys are
persisted as plaintext JSON without at-rest protection or explicit restrictive
file modes. This is the highest-risk concrete DEF-002 implementation gap because
it concerns credential material stored on disk. RR-03 is also High severity, but
it is sequenced immediately after RR-02 so credential storage and default
credential semantics can remain narrow, separately testable changes.

## Scope for the DEF-002-local recommended lane

The recommended lane should address only credential storage hardening evidence
for RR-02 unless the operator explicitly expands scope. It should not fix CORS,
default credentials, auth/tenancy, dashboard exposure, provider behavior, model
behavior, or `/v1/solve` exposure in the same lane.

## Required evidence for completion of the DEF-002-local recommended lane

- Code/config evidence of protected at-rest storage or an explicitly fail-closed
  no-persistence design.
- Restrictive file/directory permission evidence where file storage remains.
- Tests proving masked display and masked audit behavior still do not reveal
  secrets.
- Tests using synthetic placeholder values only.
- Documentation of migration or handling for existing plaintext secret files.

## Non-selection notes

No repo-global next lane is selected by this packet. Later DEF-002 lanes remain
sequenced in `closure-sequence.md` but are not authorized as parallel next lanes.
