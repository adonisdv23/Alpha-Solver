# Failure modes

The future preflight runner must fail closed when:

- required docs are missing;
- branch state is unclear;
- changed-file proof is unavailable;
- checker scripts are unavailable;
- Python is unavailable;
- a command is not on the allowed list;
- a command may perform network, provider, credential, browser, deployment, billing, route exposure, package installation, or remote fetch behavior.
