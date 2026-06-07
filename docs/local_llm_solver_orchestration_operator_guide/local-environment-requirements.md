# Local Environment Requirements

## Machine assumption

The Level 2 operator path assumes a local Mac or local developer machine. It is not a hosted-provider path and is not a production service path.

## Ollama loopback endpoint assumption

The local runtime endpoint must be localhost or loopback, for example:

```text
http://127.0.0.1:11434/api/chat
```

Remote, hosted, LAN, private-network, malformed, ambiguous, unsupported-scheme, missing-host, or userinfo-bearing endpoints are outside the approved local boundary and should fail closed.

## Model assumption

A typical local model example is:

```text
qwen2.5:3b
```

This is an example model identifier for local operator use. It is not a claim about local model quality.

## Credential and fallback assumptions

- No hosted provider keys are required.
- Hosted provider keys are not part of this local path.
- There is no hosted fallback.
- The result boundary must preserve `behavior_evidence=false`, `no_hosted_fallback=true`, and `no_provider_keys_required=true`.

## Timeout and opt-in assumptions

Every local runtime call must use a finite timeout. Local LLM mode is default-off and requires explicit operator opt-in through the local environment/configuration used by the Python/module entry point.
