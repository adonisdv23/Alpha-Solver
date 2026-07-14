# ACTIONS-COST-CONTAINMENT-ALPHA-001 · GitHub Actions Cost Containment

## Objective

Reduce redundant GitHub-hosted runner use without removing any existing
validation category or changing application behavior.

## Contract

- `.github/workflows/tests.yml` is the sole full-suite `pytest` workflow for
  pull requests and retains the post-merge `main` run.
- `.github/workflows/ci.yml` retains the local LLM orchestration guardrail suite
  under its existing workflow and job status names, without rerunning the full
  test suite.
- `.github/workflows/gates.yml` retains the metrics exporter gate.
- `.github/workflows/reliability-slo.yml` is the sole reliability-suite runner,
  retains its Redis test dependency, invokes the canonical
  `alpha.reliability.slo` enforcer, and preserves its report as an artifact.
- Docker publish builds run only for `v*` tags, matching the publish condition.
- Pull-request workflows cancel superseded runs for the same PR.
- Draft pull requests allocate no runners. A `ready_for_review` event must run
  all applicable checks, and ordinary non-draft PR events must continue to run.
- Existing workflow and job names remain stable so configured status contexts
  are not renamed by this change.

## Non-actions

- No application, provider, routing, scoring, budget, or product behavior
  changes.
- No external service calls, deployment, release, or registry publication.
- No reduction in the full test suite, static guardrail, metrics gate, or
  reliability/SLO validation categories.

## Validation

- Parse every workflow as YAML.
- Run `tests/test_github_actions_cost_controls.py`.
- Run the local LLM orchestration guardrail suite.
- Run the reliability and metrics tests plus the canonical SLO enforcer
  against a generated local report.
