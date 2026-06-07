# Artifact Capture Requirements

## Future required artifacts

A future frozen validation packet must require capture of the following for each approved test case:

- exact repo HEAD;
- exact command or invocation;
- prompt/test-case ID;
- prompt source reference;
- stdout artifact;
- stderr artifact;
- exit code;
- parseable normalized JSON;
- status;
- safety flags;
- evidence boundary;
- `behavior_evidence` value;
- `no_hosted_fallback` value;
- `no_provider_keys_required` value;
- endpoint locality metadata sufficient to confirm loopback-only use;
- timeout value sufficient to confirm finite-timeout use;
- redaction requirements;
- operator/environment notes.

## Redaction requirements

Future artifacts must not include:

- hosted provider keys;
- secrets or tokens;
- raw unsafe diagnostics beyond approved enum-like safety flags;
- unnecessary full environment dumps;
- private operator data unrelated to provenance;
- dashboard URLs;
- non-loopback endpoints.

## Parseability requirement

Future accepted artifacts must include parseable normalized JSON. Missing, malformed, or unparseable JSON is a stop condition unless a future frozen packet explicitly classifies the case as a blocked malformed-artifact case and preserves that classification without promoting evidence.
