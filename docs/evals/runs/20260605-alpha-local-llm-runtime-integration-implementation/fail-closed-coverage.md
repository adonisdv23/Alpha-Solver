# Fail-Closed Coverage

Offline tests cover fail-closed behavior for:

- default-off / missing explicit opt-in;
- missing or non-exact model name;
- invalid, missing, non-finite, zero, or negative timeout;
- forbidden provider keys;
- non-local endpoint;
- malformed / ambiguous endpoint;
- unsupported `https` or userinfo-bearing endpoint;
- connection failure;
- timeout;
- generic backend failure;
- malformed response;
- empty output;
- prompt echo;
- system echo;
- no hosted-provider fallback after local failure.

All failure outcomes preserve `behavior_evidence=false` and do not present failed or echoed output as successful behavior.
