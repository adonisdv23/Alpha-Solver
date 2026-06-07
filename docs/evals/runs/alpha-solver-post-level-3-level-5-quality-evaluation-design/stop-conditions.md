# Stop Conditions

A future quality evaluation lane must stop before execution, scoring, or interpretation when any condition below applies.

## Evidence stop conditions

Stop if required evidence is missing, stale, contradictory, overbroad, or non-reproducible. Examples include missing task manifests, changed prompts after execution, absent raw outputs, unavailable environment metadata, undocumented reviewer changes, or score summaries without source score sheets.

## Boundary stop conditions

Stop if the lane attempts to claim benchmark results, model quality, Alpha superiority, MVP readiness, product readiness, production readiness, dashboard readiness, `/v1/solve` readiness, provider fallback readiness, hosted fallback readiness, billing readiness, or evidence promotion beyond the lane's authorization.

## Execution stop conditions

Stop if execution would require unauthorized local model inference, Ollama use, hosted provider calls, `/v1/solve` calls, dashboard route calls, benchmark execution, scoring, billing work, backlog workbook updates, Google Sheets updates, runtime behavior changes, provider behavior changes, checker changes, test changes, `Makefile` changes, CI changes, or preserved source artifact changes.

## Review stop conditions

Stop interpretation if reviewer disagreement exceeds the predeclared threshold and cannot be adjudicated, if reviewers used different rubrics, if raw outputs were edited, if task contamination is discovered, or if material rubric ambiguity prevents reproducible scoring.

## Product stop condition

Stop any product-surface design work until the Level 5 quality evaluation design is accepted. Product surface design depends on accepted evaluation boundaries so it does not imply unsupported quality, readiness, API, dashboard, provider, or billing claims.
