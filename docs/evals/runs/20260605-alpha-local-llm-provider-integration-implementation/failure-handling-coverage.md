# Failure Handling Coverage

The offline tests cover fail-closed handling for:

- timeout raised by injected transport;
- connection failure raised by injected transport;
- malformed static JSON response shapes;
- empty assistant content;
- user prompt echo;
- system contract echo;
- missing portable contract;
- empty portable contract;
- SHA-256 fingerprint mismatch before backend invocation;
- generic backend exception from injected transport;
- default-off backend construction without a transport.

All covered failures normalize to `failed_closed_result` or the existing
portable-contract exception path before any provider transport is available.
