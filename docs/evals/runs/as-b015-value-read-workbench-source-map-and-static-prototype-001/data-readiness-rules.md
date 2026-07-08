# Data Readiness Rules

| Rule | Required inputs | Missing input behavior | Operator-facing label | Blocked claims | Next safe action |
|---|---|---|---|---|---|
| ready for output collection | Case packet present; output collection authorized by selected packet | Show `blocked` if authorization absent | Ready for output collection only if separately authorized | No value/readiness/superiority/provider claim | Review authorization packet or stop/defer |
| ready for scoring | Case, both sides' outputs, blind packet, scoring authorization | Show `scoring blocked` | Ready for scoring only with explicit authorization | No interpretation or superiority claim | Review scoring authorization; do not score in B015 |
| scoring blocked | Missing outputs, missing blind packet, or no scoring authorization | Show blocking reason | Scoring blocked | No score/value/readiness claim | Stop/defer or prepare missing source in a future authorized lane |
| scoring locked | Score output plus lock confirmation | Show `unknown` if lock missing | Scoring locked for packet review | No unblinding or interpretation claim | Review locked score context only |
| ready for interpretation | Locked scores plus source identity review authorization plus interpretation authorization | Show `interpretation blocked` | Ready for interpretation only if separately authorized | No final interpretation claim until completed | Stop/defer in B015 |
| interpretation blocked | No interpretation authorization or missing score/source identity prerequisites | Show blocking reason | Interpretation blocked | No final interpretation, value, readiness, or superiority claim | Operator review or separate authorization |
| source identity hidden | Blind packet/custody posture exists and no reviewed reveal source is selected | Default to hidden | Source identity hidden | No source identity reveal | Preserve blinding; review only |
| source identity reviewed | Committed source identity review/final interpretation packet exists for selected packet | Show `unknown` if not exact | Source identity reviewed in source truth | No new reveal beyond source | Review historical bounded packet only |
| review-only | Source-map/static/design packet selected | Show review-only | Review only | No implementation/runtime/scoring claims | Operator reviews B015 |
| stop/defer | Missing source truth, conflicting states, failed claim safety, or forbidden action required | Show stop/defer with reason | Stop/defer | All broad claims and forbidden actions blocked | Resolve source truth before proceeding |
