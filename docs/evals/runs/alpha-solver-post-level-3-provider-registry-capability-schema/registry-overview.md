# Registry Overview

## Purpose

A future provider registry, if Level 7 chooses to use one, should be a declarative inventory of candidate provider integrations and capabilities. The registry should help future orchestration code answer narrowly scoped questions such as:

- What provider identity is being described?
- Is the provider local or hosted?
- Which capability labels are declared?
- Which modes and product surfaces are compatible?
- Which safety, provenance, cost, and quota constraints apply?
- Is the provider disabled by default?

## Reference-only schema shape

This packet recommends the following conceptual record sections:

1. `identity`: stable provider identity fields.
2. `location`: local-vs-hosted boundary labels.
3. `capabilities`: capability labels and evidence limitations.
4. `modes`: supported execution modes.
5. `surfaces`: allowed future surfaces, if separately authorized.
6. `safety`: safety constraints and stop conditions.
7. `provenance`: required evidence and attribution metadata.
8. `cost_quota`: cost, quota, budget, and rate-limit labels.
9. `state`: disabled/default-off requirements.

## Required defaults

Every future provider registry entry should default to disabled unless a later accepted Level 7 or implementation lane explicitly enables it. Missing fields should fail closed, not enable implicit provider routing.

## Evidence boundary

This reference does not create a registry, modify provider code, add routing, add fallback, call providers, configure credentials, run models, run benchmarks, expose `/v1/solve`, expose dashboards, perform billing work, or promote evidence.
