#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUTING = ROOT / "docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md"
CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260829-field6-independent-clean-runner.md"
EVIDENCE = ROOT / "docs/agents/evidence/OTC-20260829-field6-clean-runner-host-probe/20260829-terminal.md"
CLASS = "independent_ephemeral_physical_runtime"


def fail(message: str) -> None:
    raise SystemExit(f"INDEPENDENT_PHYSICAL_CONTRACT_RED: {message}")


routing = ROUTING.read_text(encoding="utf-8")
if CLASS not in routing:
    fail(f"routing missing {CLASS}")

if not CONTRACT.is_file():
    fail("independent physical runtime contract missing")
contract = CONTRACT.read_text(encoding="utf-8")

required_contract = (
    "physically separate",
    "runtime_access: ephemeral_isolated",
    "physical_e2e_required: true",
    "persistent_session_role: none",
    "--ephemeral",
    "--disableupdate",
    "--no-default-labels",
    "field6-v4-<comment_id>",
    "queue",
    "Docker socket",
    "root-owned",
    "destroyed",
    "canonical",
    "synology_physical_runtime",
)
missing = [item for item in required_contract if item not in contract]
if missing:
    fail("contract missing invariants: " + ", ".join(missing))

for forbidden in (
    "canonical_bootstrap may use independent_ephemeral_physical_runtime",
    "canonical_reuse_or_mutation may use independent_ephemeral_physical_runtime",
    "canonical_rebind may use independent_ephemeral_physical_runtime",
    "canonical_recovery may use independent_ephemeral_physical_runtime",
):
    if forbidden in contract:
        fail(f"contract weakens canonical routing: {forbidden}")

if not EVIDENCE.is_file():
    fail("terminal Synology disqualification evidence missing")
evidence = EVIDENCE.read_text(encoding="utf-8")
for marker in (
    "RUNNER_PROBE_DOCKER_SOCKET_RW=true",
    "TRACK_A_FIELD6_HOST_PROBE_SECRETS=false",
):
    if marker not in evidence:
        fail(f"terminal evidence missing {marker}")

task = TASK.read_text(encoding="utf-8")
frontmatter = task.split("---", 2)[1]
for marker in (
    "execution_class: github_hosted",
    "runtime_access: none",
    "mutation_authorized: false",
    "credentials_allowed: false",
    "login_allowed: false",
    "physical_action_budget: 0",
    "physical_action_count: 0",
):
    if marker not in frontmatter:
        fail(f"governance task missing no-runtime fence {marker}")

print("TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_CONTRACT=PASS")