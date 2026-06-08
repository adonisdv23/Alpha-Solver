# Approval flow

Future Self Operator work must require explicit operator approval before any lane begins. The approval flow must:

1. show the lane, scope, allowed files, forbidden files, and hard stops;
2. require operator confirmation text;
3. write an approval record;
4. run local preflight checks;
5. stop if scope is unclear or if approval is missing.

Approval never authorizes provider calls, external API calls, credentials, browser automation, deployment, billing, fallback, route exposure, source-artifact mutation, or evidence promotion.
