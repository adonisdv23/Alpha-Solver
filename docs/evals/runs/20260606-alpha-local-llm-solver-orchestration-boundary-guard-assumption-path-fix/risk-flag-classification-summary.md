# Risk Flag Classification Summary

## Allowed only when all other bounded assumption requirements pass

The new composite low-risk allowance is token based and narrow. Examples covered by tests:

- `performance optimization`
- `startup performance`
- `startup performance optimization`
- `latency optimization`
- `local profiling`

## Still blocked

Composite flags containing serious-risk tokens remain blocked. Examples covered by tests:

- `performance optimization bypass`
- `startup performance credential theft`
- `latency optimization exfiltration`

Unknown non-allowlisted flags remain blocked by default. The focused test keeps `ambiguous external automation` blocked without a pass-two call.

Additional serious-risk examples remain covered by existing tests, including credential theft, malware, exfiltration, phishing, unauthorized access, exploit, evasion, concealment, bypass, self-harm, weapons, and explosives.
