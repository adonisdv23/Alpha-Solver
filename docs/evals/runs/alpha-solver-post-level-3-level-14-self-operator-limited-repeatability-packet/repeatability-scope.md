# Repeatability scope

## Allowed scope

A future execution lane may run only a local-only, operator-supervised repeat of
the first supervised-use evidence packet consistency review pattern.

Allowed actions for that future lane:

- require exact operator confirmation before execution;
- create a fresh run ID;
- create a fresh output root outside the repository;
- draft `inputs/approval-record.json` and `inputs/proposed-task.json` below the
  fresh output root;
- run local precondition checks;
- run the dry-run wrapper only to classify proposed command text;
- run `python scripts/check_local_llm_packet_consistency.py` as the deterministic
  read-only packet consistency review;
- run local post-run checks;
- preserve raw artifacts below the output root;
- import only redacted review copies into a future execution evidence packet.

## Forbidden surfaces

The future lane must not perform or allow:

- provider calls;
- hosted model calls;
- local model calls;
- external APIs;
- browser automation;
- deployment;
- billing;
- credential access;
- secret access;
- `/v1/solve` exposure;
- dashboard exposure;
- production use;
- autonomous operation;
- source-artifact mutation;
- evidence promotion;
- readiness claims;
- final local status CLI implementation.

## Source-artifact mutation boundary

The future execution lane must not mutate source artifacts, prior evidence
packets, code, tests, specs, or any tracked repository file during execution.
