#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.tibia_re_control_center.current_client_fence import (  # noqa: E402
    CURRENT_CLIENT_FENCE_MANIFEST,
    approved_historical_fences,
    current_client_fence,
    load_current_client_fence_manifest,
)

MANIFEST_REL = CURRENT_CLIENT_FENCE_MANIFEST.relative_to(ROOT).as_posix()
MANIFEST_REF = f"docs/agents/contracts/{CURRENT_CLIENT_FENCE_MANIFEST.name}"
MIGRATED_CONSUMERS = (
    ROOT / "tools/tibia_re_control_center/agent_runtime_admission.py",
    ROOT / ".github/scripts/tibia-official-client-re-canonical-live-session.sh",
    ROOT / ".github/scripts/tibia-official-client-re-canonical-live-transition.py",
    ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py",
    ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py",
    ROOT / ".github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py",
    ROOT / ".github/scripts/test_track_a_agent_runtime_governance.py",
    ROOT / ".github/workflows/track-a-canonical-live-governance.yml",
    ROOT / ".github/workflows/track-a-canonical-current-client-fence.yml",
    ROOT / ".github/workflows/track-a-kasm-canonical-bootstrap.yml",
    ROOT / ".github/workflows/track-a-surveyor-v2-readonly.yml",
    ROOT / ".github/workflows/track-a-canonical-client-fence-reconciliation.yml",
)

CURRENT_CONTRACT_DOCS = (
    ROOT / "docs/agents/TIBIA_RESEARCH_TRACKS.md",
    ROOT / "docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md",
    ROOT / "docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md",
    ROOT / "docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md",
)

def _provenance_matches_current() -> None:
    manifest = load_current_client_fence_manifest()
    path = ROOT / manifest.current_provenance
    document = json.loads(path.read_text(encoding="utf-8"))
    exact = document.get("exact_client")
    if not isinstance(exact, dict):
        raise SystemExit("CURRENT_FENCE_PROVENANCE_EXACT_CLIENT_MISSING")
    observed = (exact.get("version"), exact.get("size"), exact.get("sha256"))
    if observed != manifest.current.as_tuple():
        raise SystemExit("CURRENT_FENCE_PROVENANCE_MISMATCH")
    if not str(document.get("decision", "")).startswith("PASS_"):
        raise SystemExit("CURRENT_FENCE_PROVENANCE_NOT_PASS")


def _consumers_are_manifest_driven() -> None:
    current = current_client_fence()
    historical = tuple(item.sha256 for item in approved_historical_fences())
    for path in MIGRATED_CONSUMERS:
        text = path.read_text(encoding="utf-8")
        if "current_client_fence" not in text:
            raise SystemExit(f"CURRENT_FENCE_LOADER_MISSING:{path}")
        if current.version in text or current.sha256 in text:
            raise SystemExit(f"CURRENT_FENCE_LITERAL_REINTRODUCED:{path}")
        if any(sha in text for sha in historical):
            raise SystemExit(f"HISTORICAL_FENCE_ACTIVE_IN_CONSUMER:{path}")

def _contracts_reference_manifest() -> None:
    for path in CURRENT_CONTRACT_DOCS:
        text = path.read_text(encoding="utf-8")
        if MANIFEST_REF not in text:
            raise SystemExit(f"CURRENT_FENCE_MANIFEST_REF_MISSING:{path}")


def _base_current(base_ref: str) -> tuple[str, int, str] | None:
    completed = subprocess.run(
        ["git", "show", f"{base_ref}:{MANIFEST_REL}"],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        return None
    raw = json.loads(completed.stdout)
    current = raw.get("current")
    if not isinstance(current, dict):
        raise SystemExit("BASE_CURRENT_FENCE_INVALID")
    value = (current.get("version"), current.get("size"), current.get("sha256"))
    if not isinstance(value[0], str) or not isinstance(value[1], int) or not isinstance(value[2], str):
        raise SystemExit("BASE_CURRENT_FENCE_INVALID")
    return value

def _promotion_retains_previous_current(base_ref: str | None) -> None:
    if not base_ref:
        return
    previous = _base_current(base_ref)
    if previous is None:
        print("TRACK_A_CURRENT_FENCE_BASE_MANIFEST=ABSENT_INITIAL_INTRODUCTION")
        return
    manifest = load_current_client_fence_manifest()
    if previous == manifest.current.as_tuple():
        return
    history = {item.as_tuple() for item in manifest.approved_history}
    if previous not in history:
        raise SystemExit("PREVIOUS_CURRENT_FENCE_MISSING_FROM_HISTORY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref")
    args = parser.parse_args()
    load_current_client_fence_manifest()
    _provenance_matches_current()
    _consumers_are_manifest_driven()
    _contracts_reference_manifest()
    _promotion_retains_previous_current(args.base_ref)
    print("TRACK_A_CANONICAL_CURRENT_CLIENT_FENCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
