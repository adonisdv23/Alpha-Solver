# Local-Only Runbook

This runbook is for a future implementation lane only. It must not be used as proof that a bridge exists now.

## Preconditions

1. The sidecar security/API-shape gate has selected an Alpha Solver controlled endpoint or CLI seam.
2. Request mapping and response-envelope mapping are explicitly approved and tested.
3. Operator approves a local-only bridge implementation scope.
4. Hosted provider environment variables are unset.
5. No private files, secrets, credentials, customer data, uploads, RAG corpora, memory, workspace data, or embeddings are used as prompts or evidence.
6. Public exposure gate remains no-go unless a later gate explicitly changes it.

## Future smoke shape

```bash
unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY DEEPSEEK_API_KEY
export MODEL_PROVIDER=local
# Start the future bridge on loopback only after implementation exists.
# Submit one synthetic prompt through the bridge and verify Alpha Solver envelope and SAFE-OUT behavior.
```

## Required capture

- command run;
- loopback bind proof;
- auth negative test;
- provider-disabled proof;
- request mapping proof;
- response-envelope mapping proof;
- request ID;
- response envelope shape;
- SAFE-OUT negative case;
- telemetry/audit identity behavior;
- evidence label stating bridge smoke only and no product-readiness claim.
