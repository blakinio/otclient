from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Optional, Sequence

from .collect_all import build_collect_all, write_collect_all
from .coverage import parse_critical_dependencies, parse_matrix, rank_next, status_counts
from .evidence import DockerRepoReader, LocalRepoReader, RepoReader
from .keepalive import (
    DEFAULT_TRIGGER_SECONDS,
    DockerKeepaliveTransport,
    load_authority,
    run_keepalive_once,
)
from .runtime import DockerRuntimeProbe, EXPECTED_CLIENT_SHA256

MATRIX_PATH = "docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md"
CHECKLIST_PATH = "docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a compact TIBIA-RE evidence bundle")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--repo-container")
    parser.add_argument("--repo-container-root")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--collect-all",
        action="store_true",
        help="emit Surveyor v2 telemetry, all twelve alias views, gap report and manifest",
    )
    parser.add_argument("--runtime-docker", action="store_true")
    parser.add_argument("--runtime-container", default="otclient-track-a-kasmvnc")
    parser.add_argument("--control-container", default="otclient-synology-runner")
    parser.add_argument("--display", default=":1")
    parser.add_argument("--keepalive", action="store_true")
    parser.add_argument("--keepalive-authority", type=Path)
    parser.add_argument("--keepalive-trigger-seconds", type=int, default=DEFAULT_TRIGGER_SECONDS)
    parser.add_argument("--turn-modifier", choices=("ctrl", "shift", "alt"), default="ctrl")
    parser.add_argument("--top-next", type=int, default=20)
    return parser


def _repo_reader(args: argparse.Namespace) -> RepoReader:
    if bool(args.repo_container) != bool(args.repo_container_root):
        raise ValueError("--repo-container and --repo-container-root must be supplied together")
    if args.repo_container:
        return DockerRepoReader(args.repo_container, args.repo_container_root)
    return LocalRepoReader(args.repo_root)


def _chmod(path: Path, mode: int) -> None:
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def _json_write(path: Path, doc: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    _chmod(path.parent, 0o700)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _chmod(temp, 0o600)
    temp.replace(path)
    _chmod(path, 0o600)


def _summary_markdown(bundle: dict) -> str:
    counts = bundle["coverage_counts"]
    runtime = bundle.get("runtime")
    keepalive = bundle.get("keepalive")
    lines = [
        "# TIBIA-RE Surveyor v1 — compact run summary",
        "",
        "## Canonical coverage",
        "",
        f"- DONE: {counts['DONE']}",
        f"- PARTIAL: {counts['PARTIAL']}",
        f"- NOT_STARTED: {counts['NOT_STARTED']}",
        f"- BLOCKED: {counts['BLOCKED']}",
        f"- TOTAL: {sum(counts.values())}",
        "",
    ]
    if runtime:
        control = runtime.get("canonical_control", {})
        lines += [
            "## Current runtime snapshot",
            "",
            f"- target running: `{runtime.get('target_running')}`",
            f"- target uniqueness: `{runtime.get('target_uniqueness')}`",
            f"- current exact fence match: `{runtime.get('exact_current_fence', {}).get('match')}`",
            f"- runtime access classification: `{runtime.get('runtime_access')}`",
            f"- canonical registration present: `{control.get('registration_present')}`",
            f"- canonical lease expired: `{control.get('lease_expired')}`",
            "",
        ]
    if keepalive:
        lines += [
            "## Anti-idle",
            "",
            f"- result: `{keepalive.get('result')}`",
            f"- heartbeat age seconds: `{keepalive.get('heartbeat_age_seconds')}`",
            f"- authority allowed: `{keepalive.get('authority_allowed')}`",
            "- semantic evidence: `false` (anti-idle is excluded from subsystem proof)",
            "",
        ]
        reasons = keepalive.get("authority_reasons") or []
        if reasons:
            lines.append("Authority/refusal reasons: " + ", ".join(f"`{reason}`" for reason in reasons))
            lines.append("")
    lines += ["## Highest-priority canonical gaps", ""]
    for item in bundle["recommended_next"][:10]:
        deps = item.get("canonical_dependencies") or []
        transition = f" — {deps[0]['required_transition']}" if deps else ""
        lines.append(f"- `{item['row_id']}` {item['status']}: {item['title']}{transition}")
    lines += [
        "",
        "## Interpretation contract",
        "",
        "The Surveyor is an evidence producer/indexer. Repository evidence mentions do not change canonical coverage status. Static presence is not live semantics, and the harness never promotes a row to DONE by itself.",
        "",
    ]
    return "\n".join(lines)


def build_bundle(args: argparse.Namespace) -> dict:
    reader = _repo_reader(args)
    matrix_text = reader.read_text(MATRIX_PATH)
    checklist_text = reader.read_text(CHECKLIST_PATH)
    rows = parse_matrix(matrix_text, checklist_text)
    counts = status_counts(rows)
    dependencies = parse_critical_dependencies(matrix_text)
    evidence = reader.scan_evidence_mentions([row.row_id for row in rows], EXPECTED_CLIENT_SHA256)
    coverage_rows = [
        {
            "row_id": row.row_id,
            "area": row.area,
            "title": row.title,
            "canonical_status": row.status,
            "evidence_index": evidence[row.row_id],
            "status_source": MATRIX_PATH,
        }
        for row in rows
    ]
    runtime = None
    keepalive = None
    if args.runtime_docker:
        probe = DockerRuntimeProbe(
            target_container=args.runtime_container,
            display=args.display,
            control_container=args.control_container,
        )
        runtime = probe.snapshot()
        if args.keepalive:
            authority = load_authority(args.keepalive_authority)
            transport = DockerKeepaliveTransport(args.runtime_container, args.display)
            keepalive = run_keepalive_once(
                runtime,
                authority,
                transport,
                trigger_seconds=args.keepalive_trigger_seconds,
                modifier=args.turn_modifier,
            )
    elif args.keepalive:
        raise ValueError("--keepalive requires --runtime-docker")

    generated_at = datetime.now(timezone.utc).isoformat()
    recommended = rank_next(rows, dependencies, limit=args.top_next)
    bundle = {
        "schema": "otclient.tibia-re-surveyor.agent-bundle.v1",
        "generated_at": generated_at,
        "canonical_sources": {
            "matrix": MATRIX_PATH,
            "checklist": CHECKLIST_PATH,
            "row_count": len(rows),
        },
        "coverage_counts": counts,
        "critical_dependencies": dependencies,
        "recommended_next": recommended,
        "runtime": runtime,
        "keepalive": keepalive,
        "guardrails": {
            "surveyor_can_promote_canonical_status": False,
            "evidence_mentions_are_semantic_proof": False,
            "anti_idle_is_semantic_evidence": False,
            "keepalive_requires_external_canonical_authority": True,
            "collect_all_runtime_mutation_allowed": False,
        },
    }

    root = args.output_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)
    _chmod(root, 0o700)
    surveyor_output = root / "surveyor" if args.collect_all else root
    surveyor_output.mkdir(parents=True, exist_ok=True)
    _chmod(surveyor_output, 0o700)
    _json_write(
        surveyor_output / "coverage.json",
        {
            "schema": "otclient.tibia-re-surveyor.coverage.v1",
            "generated_at": generated_at,
            "counts": counts,
            "rows": coverage_rows,
        },
    )
    _json_write(surveyor_output / "runtime.json", runtime)
    _json_write(surveyor_output / "agent_bundle.json", bundle)
    summary_path = surveyor_output / "summary.md"
    summary_path.write_text(_summary_markdown(bundle), encoding="utf-8")
    _chmod(summary_path, 0o600)

    if args.collect_all:
        collect_all = build_collect_all(bundle, coverage_rows)
        write_collect_all(root, collect_all)
        bundle["collect_all"] = {
            "schema": collect_all["schema"],
            "alias_count": len(collect_all["aliases"]),
            "missing_reader_count": len(collect_all["missing_readers"]["reader_gaps"]),
            "manifest": "manifest.sha256",
            "privacy_scan": "privacy-scan.json",
        }
    return bundle


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parser().parse_args(argv)
    try:
        bundle = build_bundle(args)
    except (ValueError, RuntimeError) as exc:
        print(f"TIBIA_RE_SURVEYOR_ERROR={exc}", file=sys.stderr)
        return 2
    print(f"TIBIA_RE_SURVEYOR_ROWS={sum(bundle['coverage_counts'].values())}")
    if bundle.get("runtime"):
        print(f"TIBIA_RE_SURVEYOR_RUNTIME={bundle['runtime'].get('runtime_access')}")
    if bundle.get("keepalive"):
        print(f"TIBIA_RE_SURVEYOR_KEEPALIVE={bundle['keepalive'].get('result')}")
    if bundle.get("collect_all"):
        print(f"TIBIA_RE_SURVEYOR_COLLECT_ALL_ALIASES={bundle['collect_all']['alias_count']}")
        print(f"TIBIA_RE_SURVEYOR_MISSING_READERS={bundle['collect_all']['missing_reader_count']}")
    print(f"TIBIA_RE_SURVEYOR_OUTPUT={args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
