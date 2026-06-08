# Allowed inspection scope

Future first-code work may inspect:

- Level 8 and Level 9 docs packets;
- Level 7 Self Operator design docs;
- candidate runtime surfaces for static pattern discovery only;
- existing tests for style and fixture conventions;
- guardrail checker scripts and Makefile targets for command names only.

Inspection must remain local and static. It must not execute providers, models, services, browsers, deployments, billing tools, or external API calls.
