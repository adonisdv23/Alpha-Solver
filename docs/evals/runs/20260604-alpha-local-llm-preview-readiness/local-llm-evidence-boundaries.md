# Local LLM Evidence Boundaries

Lane ID: `ALPHA-LOCAL-LLM-PREVIEW-READINESS-001`

Status: evidence-boundary memo only; no outputs or results.

## Allowed claims from this readiness spike

- Local LLM preview feasibility was reviewed.
- A future local LLM path would require explicit provider/adapter wiring.
- Current local smoke behavior should remain separate from local LLM evidence.
- Current runtime/preview paths do not prove `alpha_solver_portable.py` consumption.
- Local LLM evidence would be specific to backend/model/configuration/prompt source/environment.
- Ollama or an OpenAI-compatible local endpoint may be plausible future backend options, subject to implementation and tests.

## Forbidden claims from this readiness spike

- Alpha is validated.
- Alpha is superior.
- Alpha is production-ready.
- Alpha is runtime-ready.
- `/v1/solve` behavior is proven.
- `/dashboard/expert-preview` proves portable-contract execution today.
- OpenAI behavior is proven.
- Claude behavior is proven.
- Broad plain-provider inferiority is proven.
- Batch C is ready.
- Exact billing is proven.
- Provider orchestration works.
- Self-healing, adaptive learning, self-optimization, or autonomous optimization works.
- Local LLM quality, latency, reliability, or hardware portability is established.

## Future local LLM evidence labels

Future evidence should be labeled with at least:

- lane ID;
- surface used;
- backend, such as Ollama native or local OpenAI-compatible endpoint;
- model name and exact local tag/version when available;
- endpoint class, such as localhost/private-network only;
- prompt source path;
- prompt source hash or version;
- whether the prompt source was direct file content or an approved transformation;
- route/mode, such as plain, expert, or API;
- environment notes, including hardware class when relevant;
- timeout/context/output limits;
- fake-client vs real-local-backend distinction;
- explicit statement that evidence is not OpenAI/Claude/provider-orchestration evidence.

## Boundary rule

If model outputs are generated in a future lane, they must not be imported as operator-test results, scored, treated as Batch C, or used for validation unless a separate approved lane defines that scope, surface, artifact handling, scoring policy, and claim boundaries.
