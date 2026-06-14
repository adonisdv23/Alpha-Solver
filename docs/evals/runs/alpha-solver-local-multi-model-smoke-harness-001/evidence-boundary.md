# Evidence Boundary

This lane may be cited only as evidence that a local-only multi-model smoke harness exists and that fake-transport tests exercised its safety boundaries.

`connection_failed` means the local loopback adapter path could not connect to
local Ollama or a test fixture simulated that condition. It is not behavior
evidence, not model quality evidence, and not a provider-readiness claim.

It may not be cited as evidence of:

- model quality;
- answer correctness;
- behavioral scoring;
- benchmark validation;
- local routing success;
- production readiness;
- MVP readiness;
- hosted provider integration;
- value evidence;
- Alpha superiority;
- dashboard readiness;
- `/v1/solve` readiness.

The strict evidence label is `local_multi_model_smoke_only_no_behavior_evidence`. Every per-model record must keep `behavior_evidence` set to `false` unless a later approved lane explicitly changes the evidence model.
