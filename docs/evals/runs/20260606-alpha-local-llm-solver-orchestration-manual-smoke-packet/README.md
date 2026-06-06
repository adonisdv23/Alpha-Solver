# Alpha Local LLM Solver Orchestration Manual Smoke Packet

Lane: `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-MANUAL-SMOKE-PACKET-001`

This directory is the manual local orchestration smoke packet for Adonis to use on a Mac after the local LLM solver orchestration implementation review gate authorizes manual smoke.

## Gate status

This packet is **blocked** until the implementation review gate returns exactly:

`AUTHORIZE_MANUAL_LOCAL_ORCHESTRATION_SMOKE`

Until that authorization is recorded, the packet must remain preparation-only.

## What this packet does

This packet prepares:

- operator runbook;
- prompt set;
- exact local command/script template;
- expected result fields;
- smoke result log template;
- artifact capture template;
- redaction rules;
- failure classification;
- interpretation template;
- final decision template;
- evidence boundary;
- preservation checklist;
- selected next lane.

## What this packet does not do

This packet does **not**:

- run smoke;
- call a local model;
- call hosted providers;
- import results;
- update Google Sheets;
- close the track;
- prove local model quality;
- prove `/v1/solve` readiness;
- prove dashboard readiness;
- prove MVP validation;
- prove production readiness;
- create benchmark evidence;
- create provider orchestration evidence;
- prove Alpha superiority;
- promote the evidence model.

## Manual smoke target

Target: `alpha.local_llm.orchestration_runner.run_local_llm_solver_orchestration`

The target is a non-production local orchestration runner for the local expert two-pass path using a local Ollama loopback endpoint only.

## Required invariants

Future manual smoke must preserve:

- `behavior_evidence=false`;
- `no_hosted_fallback=true`;
- `no_provider_keys_required=true`;
- no `/v1/solve` exposure;
- no dashboard exposure;
- no hosted fallback;
- no provider keys.

## Packet index

1. [packet-purpose.md](packet-purpose.md)
2. [prerequisite-gates.md](prerequisite-gates.md)
3. [operator-runbook.md](operator-runbook.md)
4. [exact-command-template.md](exact-command-template.md)
5. [smoke-prompt-set.md](smoke-prompt-set.md)
6. [expected-result-fields.md](expected-result-fields.md)
7. [smoke-result-log-template.md](smoke-result-log-template.md)
8. [artifact-capture-template.md](artifact-capture-template.md)
9. [redaction-rules.md](redaction-rules.md)
10. [failure-classification.md](failure-classification.md)
11. [interpretation-template.md](interpretation-template.md)
12. [final-decision-template.md](final-decision-template.md)
13. [evidence-boundary.md](evidence-boundary.md)
14. [smoke-preservation-checklist.md](smoke-preservation-checklist.md)
15. [selected-next-lane.md](selected-next-lane.md)
