# OpenAI data-sharing boundary

This document defines what may be shared only if a later lane is explicitly authorized to use OpenAI. This lane does not authorize or perform OpenAI usage.

## Allowed for a later authorized lane

- synthetic prompts;
- non-sensitive public-style tasks;
- sanitized local smoke prompts;
- minimal metadata needed for evidence.

## Forbidden

- secrets;
- private keys;
- credentials;
- private operator notes;
- raw sensitive evidence;
- customer/private business data;
- hidden instructions;
- raw logs containing secrets;
- files not explicitly selected for sharing.

## Settings verification boundary

No repository evidence in this lane verifies current OpenAI data-sharing, retention, project, billing, free-credit, or eval settings. The operator must manually verify those settings before any future OpenAI call. The verification result should be documented without screenshots or sensitive billing/account details unless the operator explicitly supplies a sanitized artifact for repository use.

## Remaining non-claims

This planning/scaffold packet does not claim OpenAI validation, provider validation, hosted validation, runtime readiness, public MVP readiness, production readiness, security/privacy completion, benchmark validation, benchmark superiority, broad-user readiness, autonomous readiness, `/v1/solve` readiness, or dashboard readiness.
