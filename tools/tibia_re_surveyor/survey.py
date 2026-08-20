from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import subprocess
from typing import Optional, Sequence

from .collect_all import build_collect_all, write_collect_all
from .coverage import parse_critical_dependencies, parse_matrix, rank_next, status_counts
from .evidence import DockerRepoReader, LocalRepoReader, RepoReader
from .player_state import read_player_state
from .runtime import (
    DockerRuntimeProbe,
    EXPECTED_CLIENT_SHA256,
    EXPECTED_CONTROL_CONTAINER,
    EXPECTED_TARGET_CONTAINER,
)

MATRIX_PATH = "docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md"
CHECKLIST_PATH = "docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md"
BRIDGE_PROFILE_DIR = "tools/tibia_runtime_bridge/profiles"


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
    parser.add_argument(
        "--runtime-container",
        default=EXPECTED_TARGET_CONTAINER,
        help="fixed Track A runtime container; other values fail closed",
    )
    parser.add_argument(
        "--control-container",
        default=EXPECTED_CONTROL_CONTAINER,
        help="fixed OTClient control container; other values fail closed",
    )
    parser.add_argument("--display", default=":1")
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


def _bridge_profile_census(reader: RepoReader) -> dict:
    paths = reader.list_paths(BRIDGE_PROFILE_DIR, ".json")
    profiles = []
    exact_matches = []
    for path in paths:
        try:
            doc = json.loads(reader.read_text(path))
        except (RuntimeError, json.JSONDecodeError):
            profiles.append({"path": path, "state": "MALFORMED_OR_UNREADABLE"})
            continue
        sha = doc.get("binary_sha256") if isinstance(doc, dict) else None
        item = {
            "path": path,
            "client_version": doc.get("client_version") if isinstance(doc, dict) else None,
            "binary_sha256": sha,
            "exact_current_sha_match": sha == EXPECTED_CLIENT_SHA256,
        }
        profiles.append(item)
        if item["exact_current_sha_match"]:
            exact_matches.append(path)
    return {
        "source": BRIDGE_PROFILE_DIR,
        "profile_count": len(paths),
        "profiles": profiles,
        "exact_current_client_sha256": EXPECTED_CLIENT_SHA256,
        "exact_current_profile_count": len(exact_matches),
        "exact_current_profiles": exact_matches,
        "state": "EXACT_PROFILE_AVAILABLE" if len(exact_matches) == 1 else ("AMBIGUOUS_EXACT_PROFILES" if len(exact_matches) > 1 else "NO_EXACT_CURRENT_PROFILE"),
        "semantic_promotion_allowed": False,
    }


def build_bundle(args: argparse.Namespace) -> dict:
    reader = _repo_reader(args)
    matrix_text = reader.read_text(MATRIX_PATH)
    checklist_text = reader.read_text(CHECKLIST_PATH)
    rows = parse_matrix(matrix_text, checklist_text)
    counts = status_counts(rows)
    dependencies = parse_critical_dependencies(matrix_text)
    bridge_profile = _bridge_profile_census(reader)
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
    typed_readers = {}
    if args.runtime_docker:
        probe = DockerRuntimeProbe(
            target_container=args.runtime_container,
            display=args.display,
            control_container=args.control_container,
        )
        runtime = probe.snapshot()
        processes = runtime.get("processes") if isinstance(runtime, dict) else None
        if runtime.get("runtime_access") == "READ_ONLY_ADMITTED" and isinstance(processes, list) and len(processes) == 1:
            proc = processes[0]

            def _runner(command):
                completed = subprocess.run(
                    command,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=45,
                )
                if completed.returncode != 0:
                    raise RuntimeError(completed.stderr.strip() or f"reader command rc={completed.returncode}")
                return completed.stdout

            typed_readers["player_state_typed_reader"] = read_player_state(
                pid=int(proc["pid"]), start_ticks=int(proc["process_start_ticks"]), runner=_runner
            )

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
        "bridge_profile": bridge_profile,
        "typed_readers": typed_readers,
        "guardrails": {
            "surveyor_can_promote_canonical_status": False,
            "evidence_mentions_are_semantic_proof": False,
            "collect_all_runtime_mutation_allowed": False,
            "collector_has_input_path": False,
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
    if bundle.get("collect_all"):
        print(f"TIBIA_RE_SURVEYOR_COLLECT_ALL_ALIASES={bundle['collect_all']['alias_count']}")
        print(f"TIBIA_RE_SURVEYOR_MISSING_READERS={bundle['collect_all']['missing_reader_count']}")
    print(f"TIBIA_RE_SURVEYOR_OUTPUT={args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
