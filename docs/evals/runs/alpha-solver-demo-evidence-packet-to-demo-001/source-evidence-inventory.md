# Source Evidence Inventory

## Eligible source evidence

A demo narrative may use only evidence that is already committed in the repository and can be cited by path, commit, or packet name. Eligible material includes:

- committed eval run packets under `docs/evals/runs/`;
- committed eval interpretation documents under `docs/evals/`;
- committed operator/demo evidence templates under `docs/`;
- committed specs under `.specs/` when they are described as design contracts, not as measured behavior;
- committed check logs or packet-local `checks-run.md` files when the claim is limited to the check that was actually run.

## Ineligible source evidence

A demo narrative must not rely on:

- uncommitted local files;
- operator memory or chat-only assertions;
- external backlog spreadsheets;
- missing artifact directories;
- absent archives;
- provider dashboards or billing pages;
- Google Sheets;
- runtime observations not captured in committed artifacts;
- screenshots or recordings that are not committed evidence;
- implied behavior from code paths that were not exercised by the packet.

## Inventory fields for each demo source

For every source packet used, record:

| Field | Required content |
| --- | --- |
| Source path | Repository-relative path to the committed source. |
| Evidence type | Design doc, eval packet, interpretation memo, check log, template, or spec. |
| Directly supported observations | Facts directly visible in the source. |
| Explicit non-claims | Claims the source blocks or refuses to support. |
| Missing evidence | Artifacts or runs absent from the source. |
| Demo-safe summary | One or two cautious sentences that preserve the boundary. |

## Minimum source rule

A one-pager may proceed only when each narrative claim maps to at least one committed source and the reviewer can identify the exact source before publication or live narration.
