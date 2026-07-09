# Future-Phase Parking Lot

Future phases are parked, not authorized. A parked phase is not active roadmap work and is not a selected planning or implementation lane.

| Parked phase | What it means | Trigger condition | Explicit non-authorization | Risk if activated too early |
|---|---|---|---|---|
| B016 docs-only correction lane | A narrow correction to B016 static docs if a clarity or source-truth issue is later found. | Operator identifies a concrete B016 clarity/source-truth defect. | Does not authorize runtime, UI, providers, B012, or B013. | Could churn docs without changing the lock posture or could imply implementation readiness. |
| Future implementation-prerequisite planning lane | A planning-only lane to define prerequisites before any implementation decision. | Separate explicit operator authorization. | Does not authorize implementation, providers, routes, or `/v1/solve`. | Could be mistaken for a build lane before boundaries are agreed. |
| B012 implementation | Potential implementation work associated with earlier cockpit concepts. | Separate explicit operator authorization after prerequisite review. | Deferred; not authorized by this packet. | Could create live behavior before source, safety, and claim boundaries are ready. |
| B013 real-run provider work | Potential real-run provider execution work. | Separate explicit operator authorization with cost, safety, and evidence boundaries. | Deferred; no provider calls are authorized. | Could create cost, privacy, evidence, or claim-safety risk. |
| Bounded smoke-test cockpit | A limited operator smoke surface, if later scoped. | Separate planning and operator authorization. | Does not run providers or models here. | Could be confused with provider validation or readiness evidence. |
| Route/expert-preview surface | A possible route/expert context preview surface. | Separate planning and implementation authorization. | No route, POST route, or live UI is authorized here. | Could become a generic playground or expose unsupported behavior. |
| CLI/artifact operator companion | A possible CLI or artifact helper for operator workflows. | Separate operator authorization and source-truth spec. | No CLI/subprocess execution from web UI is authorized. | Could blur local helper boundaries with runtime product behavior. |
| Full real-run Operator Cockpit | A full cockpit for real runs if later justified. | Separate product, safety, privacy, and implementation authorization. | Deferred; not authorized by this packet. | Highest risk of provider, privacy, readiness, and claim drift if premature. |
| Security/privacy review deferrals | Preserved review obligations such as DEF-002. | Separate security/privacy scope and operator authorization. | This packet makes no security/privacy completion claim. | Could imply safety completion without evidence. |
| Audit/provenance deferrals | Preserved audit/provenance obligations such as DEF-003 and DEF-004. | Separate audit/provenance lane authorization. | This packet does not close audit/provenance work. | Could weaken evidence custody if treated as closed. |
