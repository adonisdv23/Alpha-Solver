# Required Source Evidence

Lane ID: `ALPHA-LOCAL-LLM-SMOKE-RESULTS-IMPORT-SCAFFOLD-001`

This file defines the required future source evidence for a later sanitized local LLM smoke results import. It is a scaffold only and does not import smoke evidence.

## Mandatory future evidence file

The future import lane must require this evidence file:

`ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md`

If `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` is missing, import must stop.

## Required fields

The future evidence file must include all of the following fields before any import may proceed:

- lane ID
- prerequisite PR link
- exact command executed
- endpoint pattern
- exact model name, if approved for repo disclosure
- timeout seconds
- start timestamp
- end timestamp
- stdout
- stderr
- exit code
- raw artifact preservation notes
- executed / skipped / blocked status
- redaction notes
- evidence boundary
- non-claims

## Required source checks

Before import, the importer must confirm:

- the evidence file is present;
- the lane ID matches the smoke execution lane;
- the prerequisite PR link is present;
- the exact command is recorded rather than reconstructed;
- stdout, stderr, and exit code are sourced from the execution artifact rather than inferred;
- raw artifact preservation notes are present;
- redaction notes are present;
- evidence boundary and non-claims are present.

## Import stop conditions

Import must stop if any of the following is true:

- `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-001.md` is missing;
- required fields are missing;
- the endpoint cannot be sanitized to a localhost or loopback pattern;
- provider keys, secrets, credentials, private URLs, nonpublic endpoints, or raw sensitive environment dumps are present and cannot be removed;
- the source evidence asks the importer to make readiness, validation, superiority, benchmark, billing, provider-orchestration, production, or local-LLM-quality claims.
