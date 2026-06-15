# Operator Authorization Template

A future output-generation run requires exact operator authorization text in this form:

```text
I authorize a future Value Read output-generation run for lane <LANE_ID>.

Allowed mechanism: <manual simulation / provider / hosted model / local model / other, with exact scope>.
Allowed models/providers, if any: <names or `none`>.
Provider tokens or credentials authorized: <yes/no; if yes, exact boundary>.
Local model execution authorized: <yes/no; if yes, exact model and no-pull/no-install policy>.
Cost/token/runtime caps: <caps or `none because no provider/local execution is authorized`>.
Data boundary: <committed synthetic packet only / other exact boundary>.
Prompt set: <path>.
Raw Alpha output path: <path>.
Raw baseline output path: <path>.
Blind scorer packet path: <path>.
Operator-only blinding map path: <path>.
Final interpretation path: <path>.
Stop conditions: <explicit list>.
Claim boundaries: no readiness, value, provider, local-model, benchmark, production, public-use, security/privacy, endpoint, dashboard, Google Sheets, or Alpha-superiority claim unless separately supported by preserved evidence.
```

Without this exact future authorization, no output-generation run is authorized.
