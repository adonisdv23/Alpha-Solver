# Failure Handling Plan

A future implementation must fail closed and preserve non-upgraded evidence
labels for all failure cases below.

## Required failure cases

| Failure case | Required handling |
| --- | --- |
| Timeout | Abort the call, return `failed_closed`, record timeout class without claiming output quality. |
| Connection failure | Return `failed_closed`; do not retry indefinitely or fall back to hosted providers. |
| Malformed response | Reject unexpected payloads and return `failed_closed`. |
| Empty output | Return `failed_closed`; do not treat whitespace as output. |
| Prompt echo | Return `failed_closed` when output equals the user prompt or system/contract content after trimming. |
| Missing contract | Return `failed_closed` through the portable contract loader error path. |
| Empty contract | Return `failed_closed` through the portable contract loader error path. |
| Fingerprint mismatch | Return `failed_closed` and do not call the backend. |
| Backend errors | Return `failed_closed` with a safe error class/reason and no provider fallback. |

## Failure metadata

Failure metadata should include safe labels only:

- `provider_mode`;
- backend class;
- prompt-source path;
- prompt-source SHA-256/fingerprint fields when available;
- failure category;
- non-evidence flag;
- no credential values, provider credentials, nonpublic endpoints, or full backend logs.

## Fallback restrictions

A future implementation must not fall back to hosted providers, v91
`_tree_of_thought`, runtime routing, dashboard preview, or `/v1/solve` when a
local backend fails.
