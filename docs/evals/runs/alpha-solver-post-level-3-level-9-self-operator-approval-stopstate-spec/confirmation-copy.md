# Confirmation copy

Future operator confirmation text should be exact and bounded:

```text
I approve this local-only Self Operator lane for the stated scope only. I understand it may not call providers, call external APIs, use credentials, automate browsers, deploy, bill, expose routes, implement fallback, mutate source artifacts, or promote evidence. I understand it must stop if scope is unclear or if changed files exceed the allowed scope.
```

Any missing or altered confirmation must map to `SELF_OPERATOR_OPERATOR_CONFIRMATION_MISSING` or `SELF_OPERATOR_SCOPE_UNCLEAR`.
