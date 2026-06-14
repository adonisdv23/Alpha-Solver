# Local-Only Runbook

This runbook is for a future implementation lane only. It must not be used as proof that a bridge exists now.

## Preconditions

1. Lane 33 sidecar feasibility packet exists and selects a concrete sidecar pattern.
2. Operator approves a local-only bridge implementation scope.
3. Hosted provider environment variables are unset.
4. No private files, secrets, or customer data are used as prompts or evidence.
5. Public exposure gate remains no-go unless a later gate explicitly changes it.

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
- request ID;
- response envelope shape;
- SAFE-OUT negative case;
- evidence label stating bridge smoke only and no product-readiness claim.
