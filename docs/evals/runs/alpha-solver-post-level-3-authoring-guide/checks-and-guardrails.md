# Checks and Guardrails

Future post-Level-3 packet authors should run static documentation checks before requesting review.

## Aggregate guardrail command

Run the aggregate guardrail suite from the repository root:

```bash
make check-local-llm-orchestration-guardrails
```

The Makefile target runs:

```bash
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

A pass means the checked documentation satisfied the static guardrails in scope. It does not prove runtime behavior, model quality, provider behavior, dashboard readiness, `/v1/solve` readiness, billing readiness, benchmark results, MVP readiness, or production readiness.

## Packet-specific consistency check by path

If checker discovery has not yet been extended to discover a new `alpha-solver-post-level-3-*` packet automatically, run the packet consistency checker with the packet directory path explicitly:

```bash
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/<packet-directory>
```

Use this path-specific check when:

- the aggregate guardrail target passes but the new packet family may not be in automatic discovery scope;
- a new docs-only packet has selected-next, blocker fallback, or evidence-boundary state that should be checked immediately;
- the packet author needs to confirm one packet without changing checker discovery behavior.

Do not modify checker scripts, tests, CI, or the Makefile merely to satisfy a docs-only authoring packet unless that change is explicitly approved in a separate lane.

## Recommended local checks

For docs-only post-Level-3 authoring packets, record at least:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `make check-local-llm-orchestration-guardrails`
- `python scripts/check_local_llm_evidence_boundaries.py`
- `python scripts/check_local_llm_doc_paths.py`
- `python scripts/check_local_llm_packet_consistency.py`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/<packet-directory>` when discovery may not include the new packet
- `rg` checks for selected-next, blocker fallback, evidence boundary, and guardrail terms in the new packet
- `git diff --name-only -- 'docs/evals/runs/**/source-artifact/**'`
- `git diff --name-only -- scripts tests Makefile .github/workflows/ci.yml`

## Guardrail-compatible fixes

Safe fixes update the packet's own docs to restore required state. Unsafe fixes weaken guardrails, modify closed packets, edit preserved source artifacts, or alter runtime/provider/dashboard/API behavior to make documentation pass.
