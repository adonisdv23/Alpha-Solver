# Non-Actions

This packet is docs-only provider registry/capability schema design.

It explicitly does not:

- create a provider registry;
- modify runtime code;
- modify provider code;
- modify API code;
- modify dashboard code;
- modify CLI code;
- modify checker code;
- modify test code;
- modify Makefile or CI behavior;
- modify source-artifact files;
- call providers;
- run models;
- configure secrets or credentials;
- add routing;
- add fallback;
- expose `/v1/solve`;
- expose dashboards;
- run benchmarks;
- perform billing work;
- promote evidence;
- claim provider readiness;
- claim product readiness; or
- start Level 7 provider orchestration design.

This is a supporting reference only. Level 7 controls whether it is used.
