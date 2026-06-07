# Operator Safe-Use Checklist

Use this checklist for the approved local-only operator CLI wrapper. It is not a validation checklist and does not authorize evidence promotion.

## 1. Confirm the lane boundary

- Level 3 validation execution is already closed.
- Final accepted decision remains `LEVEL_3_VALIDATION_EXECUTION_ACCEPTED_AS_ARTIFACT_COMPLETE_NON_PROMOTIONAL_LOCAL_ORCHESTRATION_EVIDENCE`.
- Closeout selected next action remains `NO_FURTHER_LEVEL_3_VALIDATION_LANES_SELECTED`.
- This docs consolidation selects `NO_FURTHER_OPERATOR_DOCS_CONSOLIDATION_LANES_SELECTED`.
- Blocker fallback lane is `ALPHA-LOCAL-LLM-SOLVER-ORCHESTRATION-POST-LEVEL-3-OPERATOR-DOCS-CONSOLIDATION-FIX-001`.
- No new validation lane is started by using or reading these docs.

## 2. Confirm the command shape before running locally

Approved command identity:

```text
python -m alpha.local_llm.operator_cli
```

Required safe invocation shape:

```bash
python -m alpha.local_llm.operator_cli \
  --enable-local-llm \
  --prompt "<bounded local prompt>" \
  --endpoint-url "http://127.0.0.1:11434/api/chat" \
  --model "<local-model-id>" \
  --timeout-seconds "60"
```

Before running, confirm:

- `--enable-local-llm` is present.
- Exactly one prompt source is used: `--prompt`, `--prompt-file`, or `--prompt-stdin`.
- `--endpoint-url` is loopback/local, for example `http://127.0.0.1:11434/api/chat` or an equivalent local endpoint accepted by runtime validation.
- `--model` names an exact local model identifier.
- `--timeout-seconds` is finite and positive.
- No hosted provider key is needed or supplied for this path.
- No hosted fallback or provider fallback is expected or accepted.
- The command is not routed through `/v1/solve` or dashboard surfaces.

## 3. Confirm stdout JSON after a local-only run

If a local-only operator run is performed outside validation, inspect stdout JSON only for safe operator understanding. Required boundary fields to confirm are:

- `behavior_evidence=false`;
- `no_hosted_fallback=true`;
- `no_provider_keys_required=true`; and
- bounded diagnostic `metadata.gate_trace` content only.

Do not preserve casual output as validation evidence unless a future approved lane explicitly requires preservation and defines review rules.

## 4. Stop conditions

Stop and do not retry casually if any of these occur:

- missing stdout JSON;
- nonzero exit code that is not already understood as a local boundary or input failure;
- malformed JSON;
- non-loopback endpoint;
- hosted key exposure;
- missing artifact fields needed for a packet review;
- hosted fallback, provider fallback, `/v1/solve`, or dashboard exposure;
- readiness, benchmark, model-quality, provider-orchestration, Alpha-superiority, billing, broad-runtime, dashboard, `/v1/solve`, or evidence-promotion claims.

## 5. Troubleshooting

| Symptom | Safe operator response |
| --- | --- |
| Missing stdout JSON | Stop. Do not infer success from logs, stderr, shell history, or model text. Treat the run as unusable for artifact review unless a future approved lane defines recovery. |
| Nonzero exit code | Stop. Review whether the failure is an input, timeout, endpoint, parser, or boundary failure. Do not convert it into readiness evidence. |
| Malformed JSON | Stop. Do not repair by hand for evidence use. If needed, document the malformed-output condition in a follow-up docs or fix lane. |
| Non-loopback endpoint | Stop before execution if detected. Replace with a loopback/local endpoint or do not run. Never point this operator path at hosted providers. |
| Hosted key exposure | Stop, redact according to repo policy, and do not proceed with local orchestration. This path requires no hosted provider keys. |
| Missing artifact fields | Stop packet review. Do not fill fields from memory or assumptions; cite the missing fields and use an approved fallback lane if needed. |
