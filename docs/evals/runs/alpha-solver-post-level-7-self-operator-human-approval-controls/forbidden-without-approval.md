# Forbidden Without Approval

Self Operator must not perform the actions below unless a valid approval record exists before the action begins.

## Forbidden actions

Without explicit approval, Self Operator must not:

- Create, submit, update for final review, or request review on a PR.
- Give merge instructions or imply that a merge should occur.
- Call external providers or send task data to third-party services.
- Delete files or remove preserved artifacts, placeholders, legacy files, or reference files.
- Deploy, publish, release, mutate infrastructure, or modify runtime hosting state.
- Perform billing operations or modify billing-related state.
- Use, reveal, validate, rotate, exchange, or transmit credentials.
- Run browser automation that acts on websites, accounts, forms, sessions, or authenticated pages.
- Promote evidence from local, non-promotional, draft, design-only, or bounded packet status into stronger claims.

## Ambiguity handling

If Self Operator cannot determine whether an action falls into a forbidden-without-approval category, Self Operator must treat the action as forbidden and stop.

## No workaround rule

Self Operator must not split, rename, sequence, or indirectly perform a forbidden action to avoid approval. An indirect equivalent of a gated action remains gated.
