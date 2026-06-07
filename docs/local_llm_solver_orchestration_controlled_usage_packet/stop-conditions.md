# Stop Conditions

Stop immediately if any condition below appears during a future controlled usage process:

- hosted provider key exposure or use;
- non-loopback endpoint;
- hosted fallback;
- provider fallback;
- `/v1/solve` exposure or call;
- dashboard exposure or call;
- local model quality claims;
- benchmark claims;
- production readiness claims;
- MVP readiness claims;
- evidence-model promotion;
- raw unsafe diagnostic text exposure;
- missing artifact provenance;
- missing exact command artifact;
- missing repo HEAD artifact;
- missing repo status artifact;
- missing stdout artifact;
- missing stderr artifact;
- missing exit code artifact;
- missing redacted normalized JSON output;
- missing `behavior_evidence=false` confirmation;
- missing `no_hosted_fallback=true` confirmation;
- missing `no_provider_keys_required=true` confirmation.

When a stop condition appears, do not retry with fallback, do not call hosted providers, do not call `/v1/solve`, do not call dashboard routes, do not promote evidence, and do not update external planning ledgers from the failed run.
