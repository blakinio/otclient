#!/usr/bin/env python3
"""Repository-native wave orchestrator CLI with fail-closed executor boundary."""

from __future__ import annotations

import argparse
import dataclasses
import json
from pathlib import Path
import sys
from typing import Any

from orchestrator_core import (
    ContextState,
    OrchestratorError,
    Overlay,
    SHA_RE,
    TaskRecord,
    VALID_GROWTH,
    build_plan,
    context_decision,
    discover_tasks,
    load_config,
    normalize_state,
    path_patterns_overlap,
    pressure_from_score,
    task_from_path,
)
from orchestrator_results import (
    load_result_files,
    run_barrier,
    simulate_worker,
    validate_worker_result,
    write_json,
)
from orchestrator_executor import ExecutorError, execute_plan


def assess_context(args: argparse.Namespace, config: dict[str, Any]) -> dict[str, Any]:
    dimensions = {
        "scope_breadth": args.scope_breadth,
        "evidence_volume": args.evidence_volume,
        "history_dependency": args.history_dependency,
        "iteration_uncertainty": args.iteration_uncertainty,
        "parallel_hypotheses": args.parallel_hypotheses,
    }
    for name, value in dimensions.items():
        if not 0 <= value <= 3:
            raise OrchestratorError(f"{name} must be in 0..3")
    if args.provider_remaining_ratio is not None and not 0.0 <= args.provider_remaining_ratio <= 1.0:
        raise OrchestratorError("provider_remaining_ratio must be in 0..1")
    score = sum(dimensions.values())
    context = ContextState(
        pressure=pressure_from_score(score, config),
        growth=args.growth,
        score=score,
        provider_remaining_ratio=args.provider_remaining_ratio,
    )
    action, reasons = context_decision(context, config)
    return {
        "schema_version": 1,
        "dimensions": dimensions,
        "context": dataclasses.asdict(context),
        "action": action,
        "reasons": reasons,
        "exact_remaining_tokens_known": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("docs/agents/AGENT_ORCHESTRATOR.json"),
        help="Orchestrator policy/config JSON.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="Build the next deterministic worker wave.")
    plan.add_argument("--tasks-root", type=Path, default=Path("docs/agents/tasks/active"))
    plan.add_argument("--lane")
    plan.add_argument("--max-parallel", type=int)
    plan.add_argument("--output", type=Path)

    execute = subparsers.add_parser("execute", help="Run selected workers through the configured executor.")
    execute.add_argument("--tasks-root", type=Path, default=Path("docs/agents/tasks/active"))
    execute.add_argument("--plan", type=Path, required=True)
    execute.add_argument("--results-dir", type=Path, required=True)
    execute.add_argument("--workspace-root", type=Path)
    execute.add_argument("--output", type=Path)

    barrier = subparsers.add_parser("barrier", help="Validate worker results and build the next wave.")
    barrier.add_argument("--tasks-root", type=Path, default=Path("docs/agents/tasks/active"))
    barrier.add_argument("--plan", type=Path, required=True)
    barrier.add_argument("--results-dir", type=Path, required=True)
    barrier.add_argument("--output", type=Path)

    simulate = subparsers.add_parser("simulate-worker", help="Create a deterministic no-AI worker result.")
    simulate.add_argument("--task-id", required=True)
    simulate.add_argument("--branch", required=True)
    simulate.add_argument("--dispatch-head", required=True)
    simulate.add_argument("--output", type=Path, required=True)

    context = subparsers.add_parser("assess-context", help="Score the repository five-dimension context model.")
    for name in (
        "scope-breadth",
        "evidence-volume",
        "history-dependency",
        "iteration-uncertainty",
        "parallel-hypotheses",
    ):
        context.add_argument(f"--{name}", type=int, required=True)
    context.add_argument("--growth", choices=sorted(VALID_GROWTH), default="stable")
    context.add_argument("--provider-remaining-ratio", type=float, default=None)
    context.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.command == "plan":
            tasks = discover_tasks(args.tasks_root, config)
            payload = build_plan(tasks, config, lane=args.lane, max_parallel=args.max_parallel)
            write_json(payload, args.output)
            return 0
        if args.command == "execute":
            plan = json.loads(args.plan.read_text(encoding="utf-8"))
            payload = execute_plan(
                Path.cwd(),
                args.tasks_root,
                plan,
                config,
                args.results_dir,
                workspace_root=args.workspace_root,
            )
            write_json(payload, args.output)
            return 2 if payload["failures"] else 0
        if args.command == "barrier":
            tasks = discover_tasks(args.tasks_root, config)
            plan = json.loads(args.plan.read_text(encoding="utf-8"))
            results = load_result_files(args.results_dir)
            payload = run_barrier(tasks, config, plan, results)
            write_json(payload, args.output)
            return 2 if payload["invalid_results"] else 0
        if args.command == "simulate-worker":
            if not SHA_RE.fullmatch(args.dispatch_head):
                raise OrchestratorError("dispatch_head must be a 40-hex commit id")
            payload = simulate_worker(args)
            write_json(payload, args.output)
            return 0
        if args.command == "assess-context":
            payload = assess_context(args, config)
            write_json(payload, args.output)
            return 0
    except (OSError, json.JSONDecodeError, OrchestratorError, ExecutorError) as exc:
        print(f"orchestrator error: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
