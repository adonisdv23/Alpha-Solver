# Not-now items

The following are intentionally out of scope for this gap-closure planning lane
and for the DEF-002-local recommended next remediation lane.

| Item | Reason |
| --- | --- |
| CORS implementation | Planned as RR-01 lane, not implemented here and not selected first. |
| Default credential implementation | Planned as RR-03 lane, not implemented here; sequenced immediately after storage hardening. |
| Auth/tenancy wiring for `/v1/solve` | Planned as RR-09 lane after credential and CORS hardening. |
| Provider calls or OpenAI smoke/eval execution | Hard boundary: no providers, tokens, billing, smoke, eval, or runtime validation in this lane. |
| Dashboard or `/v1/solve` exposure | Hard boundary: do not expose public API, dashboard, or `/v1/solve`. |
| Production/runtime/provider/public readiness claims | Unsupported by this evidence; explicitly forbidden. |
| Broad auth, tenancy, dashboard, provider, model, or API redesign | Only narrow, finding-bound lanes are authorized by this plan. |
| DEF-002 closeout | Blocked until must-fix evidence and operator residual acceptance exist. |
| Backlog workbook updates | Repo instructions prohibit modifying backlog workbooks from repo tasks. |
