# Repeatability target

## Selected target

Repeat the same existing evidence packet consistency review pattern used by the
first supervised use, with a fresh run ID and fresh output root.

## Target type

Allowed target type selected:

`same existing evidence packet consistency review as the first supervised use`

## Rationale

This target is similar enough to the first supervised use to support a narrow
repeatability comparison while avoiding any new product surface. It reuses the
same local-only pattern:

1. verify local preconditions;
2. draft operator-approved inputs below a fresh output root;
3. run the dry-run wrapper only to classify the proposed command text;
4. run the deterministic packet consistency checker as the supervised local
   command;
5. verify the repository remains unchanged by the run;
6. preserve artifacts for review.

## Non-execution statement

This packet selects the target only. It does not execute the selected target.
