# N-1 fix summary

A Fable read-only audit found that F-1 was only partially resolved after #489. Scanner scope included post-Level packets, but missing suffix-less directory references were still dropped before classification.

The remaining N-1 issue was that `extract_local_references` depended on `_is_checkable_reference` before deciding whether a reference looked like a checked local-LLM or `alpha-solver-post-*` packet path. For suffix-less missing directories, that pre-filter used existence as the decision and skipped the reference before `find_missing_path_findings` could report it.

This lane fixes that class by keeping unresolved glob or shell syntax as the first hard skip, then preserving checked local-LLM and post-Level repo-relative references for missing-path reporting even when they are suffix-less directories. Legacy missing-directory detection is restored, and intentional historical or non-action records remain exempt.
