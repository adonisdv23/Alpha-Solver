# Abort conditions

Conditions under which the first supervised use must be aborted. Pre-run
aborts mean the run never starts; in-run aborts are stop states handled per
`stop-state-rules.md`. In every case: preserve everything as written,
record the abort in the execution lane's packet, and route per
`blocker-fallback-lane.md`.

## Abort before starting (do not run) if any of:

1. The operator confirmation in `operator-confirmation-required.md` is
   missing, partial, or not recorded for this exact lane and run ID.
2. This packet is not merged on `main`, or `main` has moved in a way that
   contradicts any input artifact.
3. A fresh read-only run of
   `python scripts/check_self_operator_release_gate.py --repo-root .`
   does not exit 0 on the checkout that will be used.
4. The output root cannot be created empty and writable outside the
   repository tree.
5. Any input artifact in `input-artifacts.md` is missing, has been mutated,
   or contains a credential, secret, token, provider/model configuration,
   API endpoint, browser profile, deployment manifest, or billing value.
6. The approval record fails validation for any reason.
7. The supervising operator is not present for the full run, or anything
   material is unclear (unclear means stop).

## Abort during the run if any of:

1. Any stop status in `stop-state-rules.md` is produced.
2. Any process attempts network access, or any forbidden surface in
   `use-scope.md` would be touched.
3. Any write lands outside the output root, or any file inside the
   repository checkout changes.
4. Any checker exits non-zero or produces output inconsistent with
   `expected-artifacts.md`.
5. Any artifact fails the redaction review in `redaction-rules.md`.
6. The wrapper output lacks its non-execution marker text, or there is any
   indication that proposed command text was executed rather than
   classified.
7. The run exceeds one supervised session; the first use is a single
   sitting, not a resumable campaign.

## After an abort

A second attempt is never an in-place retry: it requires the blocker-fix
lane, a recorded defect classification, a fresh approval record, and a
fresh run ID.
