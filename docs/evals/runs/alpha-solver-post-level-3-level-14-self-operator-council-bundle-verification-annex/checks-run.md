# Checks run

The following required checks are run for this lane after edits:

- `git status --short`
- `git diff --name-only`
- `git diff --check`
- `python scripts/check_local_llm_doc_paths.py`
- `python scripts/check_local_llm_evidence_boundaries.py`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-bundle-verification-annex`
- `python scripts/check_local_llm_packet_consistency.py docs/evals/runs/alpha-solver-post-level-3-level-14-self-operator-council-audit-evidence-bundle`
- focused scan for finding IDs, PRs #488/#489/#490, Council/manual-review boundaries, routing lanes, checker coverage, directory reference wording, and Fable source-boundary markers
- forbidden-claim scan for disallowed ready/readiness phrases over this annex and the Council bundle

Results are recorded in the PR summary. This file is self-attested prose and should be read with the CI/checker evidence in `ci-evidence.md`.

## Forbidden-claim scan classification

The required forbidden-claim scan was run over this annex and the Council bundle. Hits were limited to pre-existing Council boundary instructions and pre-existing command-record text in the Council bundle. Every hit is classified as `allowed_boundary_reference`; no hit is classified as `forbidden_claim` or `irrelevant_false_positive`.
