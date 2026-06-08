# Provider and external API gates

The future static scaffold must block any Self Operator first-code change that appears to call providers or external APIs.

## Blocked surfaces

- Hosted model provider clients or SDK calls.
- HTTP clients aimed at external services.
- Network-enabled command execution.
- Remote fetch or package installation.

Expected finding IDs: `SELF_OPERATOR_PROVIDER_CALL_BLOCKED` and `SELF_OPERATOR_EXTERNAL_API_BLOCKED`.
