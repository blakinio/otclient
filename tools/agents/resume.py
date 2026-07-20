#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import checkpoint


def _task_id(task_path: Path) -> str:
    text = task_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^task_id:\s*[\"']?([^\"'\n]+)", text)
    return match.group(1).strip() if match else task_path.stem


def build_bundle(task_path: Path) -> dict[str, object]:
    parsed = checkpoint.parse_task_checkpoint(task_path)
    if parsed is None:
        return {
            "task_id": _task_id(task_path),
            "checkpoint": str(task_path),
            "warning": "CHECKPOINT_MISSING",
            "next_action": "Reconstruct and write a valid Context checkpoint from current Git, PR, CI and task evidence before substantive implementation.",
        }
    contract = checkpoint.load_contract()
    errors = checkpoint.validate_checkpoint(parsed.data, contract, source=task_path)
    if errors:
        raise checkpoint.CheckpointError("; ".join(errors))
    data = parsed.data
    return {
        "task_id": _task_id(task_path),
        "checkpoint": str(task_path),
        "head": data.get("head", "UNKNOWN"),
        "branch": data.get("branch", "UNKNOWN"),
        "pr": data.get("pr", "none"),
        "status": data.get("status", "UNKNOWN"),
        "context_routes": data.get("context_routes", []),
        "owned_paths": data.get("owned_paths", []),
        "proven": data.get("proven", []),
        "derived": data.get("derived", []),
        "unknown": data.get("unknown", []),
        "conflicts": data.get("conflicts", []),
        "first_failure": data.get("first_failure", {}),
        "changed_paths": data.get("changed_paths", []),
        "validation": data.get("validation", []),
        "blockers": data.get("blockers", []),
        "next_action": data.get("next_action", "UNKNOWN"),
    }


def render_prompt(bundle: dict[str, object]) -> str:
    lines = [
        f"Continue task {bundle.get('task_id', '')} from repository state.",
        "Do not rely on previous chat history.",
        f"CHECKPOINT: {bundle.get('checkpoint', '')}",
    ]
    warning = bundle.get("warning")
    if warning:
        lines.extend([
            f"WARNING: {warning}",
            f"NEXT_ACTION: {bundle.get('next_action', '')}",
            "Verify live repository state before substantive implementation.",
        ])
        return "\n".join(lines)
    lines.extend([
        f"HEAD: {bundle.get('head', 'UNKNOWN')}",
        f"BRANCH: {bundle.get('branch', 'UNKNOWN')}",
        f"PR: {bundle.get('pr', 'none')}",
        f"STATUS: {bundle.get('status', 'UNKNOWN')}",
    ])
    for label, key in [
        ("PROVEN", "proven"), ("DERIVED", "derived"), ("UNKNOWN", "unknown"),
        ("CONFLICTS", "conflicts"), ("CHANGED_PATHS", "changed_paths"), ("BLOCKERS", "blockers"),
    ]:
        lines.append(f"{label}:")
        for item in bundle.get(key, []):
            lines.append(f"- {item}")
    first_failure = bundle.get("first_failure", {})
    if isinstance(first_failure, dict):
        lines.append(f"FIRST_FAILURE_MARKER: {first_failure.get('marker', 'none')}")
        lines.append(f"FIRST_FAILURE_EVIDENCE: {first_failure.get('evidence', 'none')}")
    lines.append("VALIDATION:")
    for item in bundle.get("validation", []):
        if isinstance(item, dict):
            lines.append(f"- {item.get('command', '')}: {item.get('result', '')}; evidence={item.get('evidence', '')}")
    lines.extend([
        f"NEXT_ACTION: {bundle.get('next_action', 'UNKNOWN')}",
        "",
        "OPERATING_RULES:",
        "- Treat current Git state, the checkpoint and the live PR/CI state as source of truth.",
        "- Verify branch/head, PR, CI and ownership only where they can invalidate NEXT_ACTION.",
        "- Do not repeat the full preflight when checkpoint and live state agree.",
        "- Do not rediscover PROVEN facts unless live evidence changed.",
        "- Preserve UNKNOWN and CONFLICT explicitly; never turn them into assumptions.",
        "- Do not paste full logs, diffs, source trees or old chat history.",
        "- Execute NEXT_ACTION autonomously when safe.",
        "- Before ending or handing off, update the checkpoint and leave exactly one concrete next_action.",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a compact continuation prompt from a task checkpoint.")
    parser.add_argument("--task", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    task_path = args.task.resolve()
    bundle = build_bundle(task_path)
    print(json.dumps(bundle, indent=2) if args.json else render_prompt(bundle))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
