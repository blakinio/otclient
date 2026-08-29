#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ROUTING = ROOT / "docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md"
CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md"
WORKFLOW = ROOT / ".github/workflows/track-a-independent-ephemeral-physical-runtime-contract.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260829-field6-independent-clean-runner.md"
CLASS = "independent_ephemeral_physical_runtime"

ALLOWED_PATHS = {
    ".github/scripts/audit_track_a_independent_ephemeral_physical_runtime_contract.py",
    ".github/scripts/test_track_a_independent_ephemeral_physical_runtime_contract.py",
    ".github/workflows/track-a-independent-ephemeral-physical-runtime-contract.yml",
    "docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md",
    "docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md",
    "docs/agents/tasks/active/OTC-20260829-field6-independent-clean-runner.md",
    "docs/superpowers/specs/2026-08-29-track-a-independent-clean-physical-runtime-design.md",
    "docs/superpowers/plans/2026-08-29-track-a-independent-clean-physical-runtime.md",
}


def fail(fid: str, message: str) -> None:
    raise SystemExit(f"{fid}: {message}")


def changed_paths(base: str) -> set[str]:
    raw = subprocess.check_output(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    return {line.strip().replace("\\", "/") for line in raw.splitlines() if line.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()

    changed = changed_paths(args.base)
    unexpected = sorted(changed - ALLOWED_PATHS)
    if unexpected:
        fail("INDEPENDENT-PHYSICAL-AUDIT-F001", "unexpected changed paths: " + ", ".join(unexpected))
    for forbidden in (
        ".github/workflows/track-a-current-login-field6-runtime.yml",
        ".github/scripts/track_a_current_login_field6_runtime.sh",
        ".github/scripts/tibia-official-client-re-canonical-live-transition.py",
    ):
        if forbidden in changed:
            fail("INDEPENDENT-PHYSICAL-AUDIT-F002", f"consumer/canonical path changed in governance PR: {forbidden}")

    routing = ROUTING.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    task = TASK.read_text(encoding="utf-8")

    routing_markers = (
        "routing_contract_version: 1.1.0",
        "EXECUTION_CLASS: github_hosted | synology_physical_runtime | independent_ephemeral_physical_runtime",
        "All `canonical_reuse_or_mutation`, `canonical_bootstrap`, `canonical_rebind`, `canonical_recovery` and `canonical_boot_epoch_recovery` operations remain `synology_physical_runtime`",
        "INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_E2E",
        "TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md",
    )
    missing = [m for m in routing_markers if m not in routing]
    if missing:
        fail("INDEPENDENT-PHYSICAL-AUDIT-F003", "routing missing invariants: " + ", ".join(missing))

    contract_markers = (
        "physically separate",
        "runtime_access: ephemeral_isolated",
        "physical_e2e_required: true",
        "persistent_session_role: none",
        "--ephemeral",
        "--disableupdate",
        "--no-default-labels",
        "field6-v4-<comment_id>",
        "no host Docker socket",
        "root-owned",
        "guest is destroyed",
        "may never route through `independent_ephemeral_physical_runtime`",
    )
    missing = [m for m in contract_markers if m not in contract]
    if missing:
        fail("INDEPENDENT-PHYSICAL-AUDIT-F004", "contract missing invariants: " + ", ".join(missing))

    if "runs-on: [otclient, synology]" in workflow or "runs-on: self-hosted" in workflow:
        fail("INDEPENDENT-PHYSICAL-AUDIT-F005", "governance workflow may not schedule physical self-hosted work")
    if workflow.count("runs-on: ubuntu-24.04") < 2:
        fail("INDEPENDENT-PHYSICAL-AUDIT-F006", "contract and fresh-audit jobs must both be GitHub-hosted")

    header = task.split("---", 2)[1]
    for marker in (
        "execution_class: github_hosted",
        "runtime_access: none",
        "mutation_authorized: false",
        "credentials_allowed: false",
        "login_allowed: false",
        "physical_action_budget: 0",
        "physical_action_count: 0",
    ):
        if marker not in header:
            fail("INDEPENDENT-PHYSICAL-AUDIT-F007", f"governance task authority expanded: missing {marker}")

    print("TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_INDEPENDENT_AUDIT=PASS")
    print("AUDIT_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())