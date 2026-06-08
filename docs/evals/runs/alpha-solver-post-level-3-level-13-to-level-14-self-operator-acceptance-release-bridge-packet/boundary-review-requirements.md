# Boundary review requirements

Future release boundary review must check for prohibited or unproven scope in these areas:

- provider calls;
- hosted model calls;
- external API calls;
- credentials;
- secret access;
- browser automation;
- deployment;
- billing;
- `/v1/solve` exposure;
- dashboard exposure;
- fallback;
- hosted fallback;
- source-artifact mutation;
- evidence promotion;
- autonomous merge;
- autonomous approval;
- missing operator confirmation.

Any positive finding in these areas must block release claims until resolved by an approved follow-up lane.
