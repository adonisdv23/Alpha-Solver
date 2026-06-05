# Outcome Branches

Lane ID: `ALPHA-LOCAL-LLM-POST-SMOKE-DECISION-FRAMEWORK-001`

Status: branch menu only; no smoke result is imported or interpreted here.

## Selection rule

A future actual decision must select exactly one next lane based on imported evidence. Every branch below maps to one and only one next lane.

| Future imported outcome branch | Classification trigger for future evidence | Required next lane |
| --- | --- | --- |
| Passed cleanly | Imported evidence satisfies all narrow success criteria with a non-failed adapter result and without `failed_closed` status, fail-closed labels, skipped execution, blocked execution, timeout, connection failure, malformed response, empty output, prompt echo, system echo, endpoint locality failure, environment setup failure, or model availability failure. | `ALPHA-LOCAL-LLM-RUNTIME-INTEGRATION-PLANNING-001` |
| Failed due to endpoint locality | Imported evidence shows the command was not confined to a localhost or loopback endpoint, or endpoint locality validation failed closed. | `ALPHA-LOCAL-LLM-ENDPOINT-LOCALITY-REPAIR-001` |
| Failed due to environment setup | Imported evidence shows the smoke could not run because required local environment setup was missing, invalid, or inconsistent before model interaction could be evaluated. | `ALPHA-LOCAL-LLM-SMOKE-ENVIRONMENT-RETRY-001` |
| Failed due to model unavailable | Imported evidence shows the endpoint was reachable but the exact operator-supplied local model was unavailable, missing, unloaded, or not selectable. | `ALPHA-LOCAL-LLM-MODEL-AVAILABILITY-RETRY-001` |
| Failed due to timeout | Imported evidence shows execution reached a finite timeout before a valid adapter result could be classified. | `ALPHA-LOCAL-LLM-SMOKE-TIMEOUT-REVIEW-001` |
| Failed due to connection failure | Imported evidence shows localhost or loopback connection setup failed, was refused, reset, or otherwise could not reach the local endpoint. | `ALPHA-LOCAL-LLM-SMOKE-CONNECTION-REVIEW-001` |
| Failed due to malformed response | Imported evidence shows the endpoint returned a response that the adapter/parser could not parse into the expected shape. | `ALPHA-LOCAL-LLM-RESPONSE-PARSER-REPAIR-001` |
| Failed due to empty output | Imported evidence shows the adapter received or produced an empty or whitespace-only output. | `ALPHA-LOCAL-LLM-EMPTY-OUTPUT-REVIEW-001` |
| Failed due to prompt or system echo | Imported evidence shows output consisted of, or materially echoed, the user prompt or system/contract text rather than an assistant response. | `ALPHA-LOCAL-LLM-PROMPT-ECHO-REPAIR-001` |
| Skipped or blocked | Imported evidence shows smoke was not executed, was intentionally skipped, was blocked by missing authorization or artifacts, or lacks enough preserved evidence for classification. | `ALPHA-LOCAL-LLM-SMOKE-TEST-EXECUTION-RETRY-001` |

## Tie handling

If future imported evidence could fit more than one failure branch, the later decision must select exactly one next lane: the narrowest immediate blocker that must be resolved before any broader planning or readiness review.
