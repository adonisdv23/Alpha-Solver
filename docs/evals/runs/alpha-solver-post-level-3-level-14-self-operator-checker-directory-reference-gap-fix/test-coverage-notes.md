# Test coverage notes

Focused tests added or preserved:

- Missing `alpha-solver-post-*` suffix-less packet directory references are reported.
- Missing legacy local-LLM suffix-less packet directory references are reported.
- A trailing slash does not prevent existence checks, while the original reference text is preserved in findings.
- Existing checked directory references under `tmp_path` do not produce false missing-reference findings, proving root forwarding.
- Glob or shell-like unresolved patterns remain ignored.
- Intentional historical or non-action missing references remain exempt.
- Existing coverage remains for post-Level scan scope, Council bundle scan scope, legacy local-LLM scan scope, forbidden readiness terms, generic non-boundary language, and explicit nearby boundary language.
