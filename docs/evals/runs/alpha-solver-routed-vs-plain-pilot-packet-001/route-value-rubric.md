# Route-value rubric

Score each dimension 0-3 after outputs are collected in a separately authorized run. Leave blank until then. This protocol is a pilot scoring protocol, not proof of superiority.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Route correctness | Wrong family/route | Partly relevant route | Mostly correct route | Correct route with clear rationale |
| Model recommendation fit | Mismatched capability/cost | Weak fit | Reasonable fit | Strong fit to task constraints |
| Tool recommendation fit | Missing or unsafe tool advice | Partly useful | Useful with limits | Precise, safe, non-executing recommendation |
| Cost awareness | Ignores cost | Mentions cost vaguely | Balances cost somewhat | Clear cost-sensitive routing |
| Privacy awareness | Misses privacy risk | Generic privacy note | Appropriate privacy handling | Strong privacy boundary and safer alternative |
| Currentness awareness | Misses freshness needs | Generic caveat | Identifies currentness need | Specifies freshness/evidence boundary |
| Capability fit | Capability mismatch | Partial match | Good match | Best available capability match and limits |
| Fallback quality | No fallback | Vague fallback | Plausible fallback | Actionable fallback tied to failure mode |
| Warning quality | Missing warnings | Generic warnings | Relevant warnings | Specific, non-alarmist, actionable warnings |
| Answer usefulness | Not useful | Somewhat useful | Useful | Highly useful within boundaries |
| Failure honesty | Overclaims | Weak caveats | Mostly honest | Clearly states uncertainty/inability |
| Next-action clarity | No next action | Vague next action | Clear next action | Concrete safe next action with stop criteria |

## Protocol boundaries

This packet does not execute the pilot. It does not call providers, run hosted models, run local models, execute tools, browse the web, generate Alpha outputs, generate baseline outputs, score outputs, change scores, unblind, inspect raw Alpha outputs, inspect raw baseline outputs, perform source-map work, mutate Google Sheets, add dependencies, expose `/v1/solve`, or expose dashboard or public API behavior. It makes no readiness, benchmark, production, public, security/privacy, provider, local-model, tool-quality, or Alpha-superiority claims.
