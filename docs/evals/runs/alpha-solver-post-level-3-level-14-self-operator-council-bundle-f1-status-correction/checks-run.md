# Checks run

Required commands for this correction lane:

```bash
git status --short
git diff --name-only
git diff --check
python scripts/check_local_llm_doc_paths.py
python scripts/check_local_llm_evidence_boundaries.py
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-f1-status-correction
python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle
rg -n "F-1 remains open|F-1/N-1|Post-#491 F-1 status correction|TARGETED-FABLE-DELTA-RE-AUDIT|Council has not run|manual operator review has not happened|readiness claim" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/README.md docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/current-state-snapshot.md docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-f1-status-correction
rg -n "production ready|runtime ready|provider ready|hosted ready|benchmark superior|benchmark validated|autonomous ready|MVP ready|release ready|broad user ready" docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/README.md docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle/current-state-snapshot.md docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-f1-status-correction
```

The forbidden-claim scan is expected to be classified after execution as either no hits or allowed boundary references only. Any forbidden claim blocks this lane.
