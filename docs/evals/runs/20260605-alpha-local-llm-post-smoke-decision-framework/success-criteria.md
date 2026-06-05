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
6. the adapter returned a result or failed closed under expected labels;
7. raw artifacts were preserved; and
8. a sanitized import exists.

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
