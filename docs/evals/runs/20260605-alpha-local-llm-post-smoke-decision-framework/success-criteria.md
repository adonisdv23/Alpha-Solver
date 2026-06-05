# Success Criteria

Lane ID: `ALPHA-LOCAL-LLM-POST-SMOKE-DECISION-FRAMEWORK-001`

Status: narrow success criteria for a future imported smoke result only.

## Required criteria for the `passed cleanly` branch

A future smoke result may be classified as `passed cleanly` only if imported evidence shows all of the following:

1. the smoke command was executed against a localhost or loopback endpoint;
2. no hosted provider fallback occurred;
3. a finite timeout was configured and preserved in the evidence;
4. no provider keys were used, required, exposed, or imported;
5. endpoint locality was validated;
6. the adapter returned a non-failed result under the expected local smoke evidence boundary, with `behavior_evidence=False`; no `failed_closed` status or fail-closed label is present;
7. raw artifacts were preserved; and
8. a sanitized import exists.

## Fail-closed exclusion

Any `failed_closed` status or fail-closed label excludes the `passed cleanly` branch. Fail-closed outcomes must route to their narrow failure branch, including timeout, connection failure, endpoint locality, malformed response, empty output, prompt echo, or system echo when those labels are present in future imported evidence.

## Success non-claims

Even if every criterion above is satisfied, success does not prove:

- local LLM quality;
- runtime readiness;
- production readiness;
- `/v1/solve` readiness;
- benchmark success;
- provider orchestration;
- MVP validation;
- Alpha quality;
- Alpha superiority; or
- broad plain-provider inferiority.

## Evidence dependency

These criteria cannot be evaluated in this lane because no smoke result is imported or interpreted here. They are reserved for a later smoke-results import and decision lane.
