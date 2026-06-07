# Checker Inventory

## Aggregate target

The normal entrypoint is:

```bash
make check-local-llm-orchestration-guardrails
```

That Makefile target runs these checkers in sequence:

```bash
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_packet_consistency.py
```

Direct checker commands are fallback or manual alternatives for isolating a failure after the aggregate target fails.

## Evidence-boundary checker

Command:

```bash
python scripts/check_local_llm_evidence_boundaries.py
```

What it protects:

- Scans local LLM solver orchestration documentation for risky promotional claim phrases.
- Requires nearby boundary language when a risky phrase appears.
- Confirms required final Level 3 closeout boundary phrases are present in authoritative closeout files.
- Excludes preserved source-artifact payload files from the scan.
- Does not validate runtime behavior, run benchmarks, call models, start Ollama, use providers, read secrets, or exercise routes.

Safe interpretation:

- A pass means the scanned docs maintain required static evidence-boundary wording.
- A pass does not prove model quality, readiness, provider behavior, benchmark results, billing readiness, dashboard readiness, or `/v1/solve` readiness.

## Docs path/link checker

Command:

```bash
python scripts/check_local_llm_doc_paths.py
```

What it protects:

- Scans the operator guide, the local LLM solver orchestration evidence index, and selected Level 3 packet docs.
- Verifies repo-relative local LLM documentation paths and key source paths referenced by those docs exist in the checkout.
- Detects simple stale selected-next-lane conflicts inside a single document.
- Excludes preserved source-artifact payload files from scanning while still allowing the source-artifact directory itself to be referenced.
- Does not call GitHub, access the network, run models, start Ollama, expose routes, run benchmarks, or promote evidence.

Safe interpretation:

- A pass means the scanned documentation references resolvable local paths and does not contain the simple stale selected-next conflict patterns checked by the script.
- A pass does not prove that unscanned docs are complete or that any runtime workflow was executed.

## Packet consistency checker

Command:

```bash
python scripts/check_local_llm_packet_consistency.py
```

What it protects:

- Discovers local LLM solver orchestration packet directories under `docs/evals/runs/`.
- Requires selected-next state or an explicit closed/no-further state where applicable.
- Requires blocker fallback lane files when packet patterns indicate they are needed.
- Requires evidence-boundary, blocked-claims, non-actions, or equivalent boundary files when packet patterns indicate they are needed.
- Ensures no-further-lanes decisions are not contradicted by selected implementation lanes.
- Verifies expected decision markers are present in authoritative packet/status files, not only in command logs.
- Excludes source-artifact payload files from packet enforcement.

Safe interpretation:

- A pass means packet metadata and decision markers are internally consistent for the checker scope.
- A pass does not infer missing packet fields from memory and does not promote packet text into runtime evidence.
