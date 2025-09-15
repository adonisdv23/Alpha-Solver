import argparse
import json
import sys
import uuid
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ObsResult:
    plan: str
    tokens: int
    cost: float
    budget_verdict: str
    confidence: float = 1.0
    trace_id: str | None = None

    def to_card(self) -> str:
        parts = [
            f"plan={self.plan}",
            f"tokens={self.tokens}",
            f"cost={self.cost:.2f}",
            f"budget={self.budget_verdict}",
        ]
        return " | ".join(parts)

    def to_json(self) -> Dict[str, Any]:
        data = {
            "plan": self.plan,
            "tokens": self.tokens,
            "cost": self.cost,
            "budget_verdict": self.budget_verdict,
        }
        if self.trace_id:
            data["trace_id"] = self.trace_id
        return data


def solve(prompt: str, max_tokens: int, min_budget_tokens: int) -> ObsResult:
    tokens = len(prompt.split())
    cost = tokens * 0.01
    budget = "within" if tokens <= min_budget_tokens else "over"
    plan = "direct" if tokens <= max_tokens else "long"
    return ObsResult(plan=plan, tokens=tokens, cost=cost, budget_verdict=budget)


def cmd_run(args: argparse.Namespace) -> int:
    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                prompt = f.read().strip()
        else:
            prompt = sys.stdin.read().strip()
        if not prompt:
            print("error: empty prompt", file=sys.stderr)
            return 2
        result = solve(prompt, args.max_tokens, args.min_budget_tokens)
        if result.budget_verdict == "over":
            exit_code = 3
        else:
            exit_code = 0
        if args.out == "json":
            print(json.dumps(result.to_json()))
        else:
            print(result.to_card())
        return exit_code
    except Exception as exc:  # pragma: no cover
        print(f"internal error: {exc}", file=sys.stderr)
        return 5


def cmd_replay(args: argparse.Namespace) -> int:
    try:
        mismatches = []
        with open(args.file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                rec = json.loads(line)
                expected = rec["expected"]
                prompt = rec["prompt"]
                result = solve(prompt, args.max_tokens, args.min_budget_tokens)
                got = result.to_card()
                if got != expected:
                    mismatches.append((idx, expected, got))
        if mismatches:
            for idx, exp, got in mismatches:
                print(f"line {idx}: expected {exp!r} got {got!r}")
            return 4
        print("replay ok")
        return 0
    except FileNotFoundError:
        print("error: file not found", file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover
        print(f"internal error: {exc}", file=sys.stderr)
        return 5


def cmd_gates(args: argparse.Namespace) -> int:
    print(
        f"thresholds: low={args.low_conf_threshold} clarify={args.clarify_conf_threshold} budget={args.min_budget_tokens}"
    )
    verdict = "pass"
    if args.confidence < args.low_conf_threshold or args.tokens > args.min_budget_tokens:
        verdict = "deny"
    elif args.confidence < args.clarify_conf_threshold:
        verdict = "clarify"
    print(f"verdict: {verdict}")
    return 3 if verdict == "deny" else 0


def cmd_finops(args: argparse.Namespace) -> int:
    tokens = args.tokens
    if tokens is None:
        tokens = len(args.prompt.split())
    cost = tokens * 0.01
    budget_verdict = "within" if tokens <= args.min_budget_tokens else "over"
    print(f"tokens={tokens} cost={cost:.2f} budget={budget_verdict}")
    return 3 if budget_verdict == "over" else 0


def cmd_traces(args: argparse.Namespace) -> int:
    trace_id = "trace-" + uuid.uuid4().hex[:8]
    result = solve(args.prompt, args.max_tokens, args.min_budget_tokens)
    result.trace_id = trace_id
    if args.out == "json":
        print(json.dumps(result.to_json()))
    else:
        print(trace_id)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alpha-solver")
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="solve a prompt")
    run_p.add_argument("--file", type=str, help="prompt file")
    run_p.add_argument("--model", default="stub")
    run_p.add_argument("--max-tokens", type=int, default=100)
    run_p.add_argument("--low-conf-threshold", type=float, default=0.2)
    run_p.add_argument("--clarify-conf-threshold", type=float, default=0.5)
    run_p.add_argument("--min-budget-tokens", type=int, default=20)
    run_p.add_argument("--seed", type=int, default=0)
    run_p.add_argument("--record", action="store_true")
    run_p.add_argument("--replay", action="store_true")
    run_p.add_argument("--metrics", dest="metrics", action="store_true", default=True)
    run_p.add_argument("--no-metrics", dest="metrics", action="store_false")
    run_p.add_argument("--out", choices=["json", "card"], default="card")
    run_p.add_argument("--verbose", action="store_true")
    run_p.add_argument("--dry-run", action="store_true")
    run_p.set_defaults(func=cmd_run)

    replay_p = sub.add_parser("replay", help="replay a record")
    replay_p.add_argument("file", type=str)
    replay_p.add_argument("--max-tokens", type=int, default=100)
    replay_p.add_argument("--min-budget-tokens", type=int, default=20)
    replay_p.set_defaults(func=cmd_replay)

    gates_p = sub.add_parser("gates", help="show gate config")
    gates_p.add_argument("--low-conf-threshold", type=float, default=0.2)
    gates_p.add_argument("--clarify-conf-threshold", type=float, default=0.5)
    gates_p.add_argument("--min-budget-tokens", type=int, default=20)
    gates_p.add_argument("--confidence", type=float, required=True)
    gates_p.add_argument("--tokens", type=int, required=True)
    gates_p.set_defaults(func=cmd_gates)

    finops_p = sub.add_parser("finops", help="estimate tokens/cost")
    finops_p.add_argument("--prompt", type=str, default="")
    finops_p.add_argument("--tokens", type=int)
    finops_p.add_argument("--min-budget-tokens", type=int, default=20)
    finops_p.set_defaults(func=cmd_finops)

    traces_p = sub.add_parser("traces", help="run with tracing")
    traces_p.add_argument("--prompt", required=True)
    traces_p.add_argument("--max-tokens", type=int, default=100)
    traces_p.add_argument("--min-budget-tokens", type=int, default=20)
    traces_p.add_argument("--out", choices=["json", "card"], default="card")
    traces_p.set_defaults(func=cmd_traces)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
