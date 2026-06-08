# Forbidden commands

Block commands that perform or imply:

- network calls;
- provider calls;
- external API calls;
- credential access;
- browser automation;
- deployment;
- billing;
- package installation;
- remote fetch or remote checkout;
- route exposure;
- model execution;
- evidence promotion;
- source-artifact mutation.

Forbidden examples include `curl`, remote `git fetch`, package installers, browser automation CLIs, deployment CLIs, hosted provider CLIs, and billing/payment tools unless a later explicit lane authorizes them.
