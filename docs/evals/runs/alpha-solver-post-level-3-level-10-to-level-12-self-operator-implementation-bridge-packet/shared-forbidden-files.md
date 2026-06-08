# Shared forbidden files and surfaces

Future lanes must explicitly block changes or behavior involving:

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
- runtime behavior before static safety tests;
- missing operator confirmation.

Detection of any forbidden surface is a hard stop, not a partial-implementation opportunity.
