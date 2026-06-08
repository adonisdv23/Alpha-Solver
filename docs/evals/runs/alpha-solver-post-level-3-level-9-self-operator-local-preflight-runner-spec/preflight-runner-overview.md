# Preflight runner overview

A future preflight runner should perform local, deterministic checks before any Self Operator lane proceeds. It must fail closed on scope ambiguity, missing docs, missing approval, forbidden commands, or artifact boundary risk.

It must not call networks, providers, external APIs, browsers, deployments, billing systems, package managers, remote fetches, or route exposure paths.
