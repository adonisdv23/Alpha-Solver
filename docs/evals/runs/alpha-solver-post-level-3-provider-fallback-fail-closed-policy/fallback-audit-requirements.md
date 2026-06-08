# Fallback Audit Requirements

## Audit purpose

Future fallback audit records must make fallback decisions reviewable without requiring providers to be called, models to be run, benchmarks to be executed, billing events to be reproduced, or product surfaces to be exposed.

## Required audit fields

A future fallback audit record should include:

- run ID or explicit statement that no run-scoped packet applies;
- request ID or bounded request reference;
- original provider/local path considered;
- fallback provider/path considered;
- hosted/local classification for each path;
- explicit opt-in reference and scope;
- Level 7 packet-use decision reference;
- blocked fallback state, if any;
- fail-closed reason, if any;
- billing authorization state;
- retention and redaction state;
- safety policy state;
- evidence-boundary state;
- final decision: allowed, blocked, fail-closed, or reviewer-blocked;
- UTC timestamp.

## Audit boundaries

Audit records must not store raw secrets, raw credentials, provider tokens, payment details, unredacted personal data, or raw sensitive payloads. Auditability must not be used as justification to add fallback, call providers, run models, run benchmarks, perform billing work, expose `/v1/solve`, modify runtime/provider/API/dashboard files, or promote evidence.
