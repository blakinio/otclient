#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHYSICAL = ROOT / ".github/workflows/track-a-field6-clean-runner-host-probe.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260829-field6-clean-runner-host-probe.md"
STALE = ROOT / "docs/agents/tasks/active/OTC-20260816-track-a-isolated-xvfb-startup-discriminator.md"


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"CLEAN_RUNNER_HOST_PROBE_RED: missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")

physical = read(PHYSICAL)
if "pull_request:" in physical:
    raise SystemExit("CLEAN_RUNNER_HOST_PROBE_RED: physical workflow must not be PR-triggerable")
for exact in (
    "workflow_dispatch:",
    "github.actor == github.repository_owner",
    "github.ref == 'refs/heads/main'",
    "runs-on: [otclient, synology]",
    "ref: main",
    "persist-credentials: false",
    'test "${GITHUB_RUN_ATTEMPT:?}" = "1"',
    "RUNNER_PROBE_DOCKER_CLI=",
    "RUNNER_PROBE_DOCKER_SOCKET=",
    "RUNNER_PROBE_DOCKER_SERVER=",
    "RUNNER_PROBE_SUDO_DOCKER=",
    "RUNNER_PROBE_REMOTE_CONTROL_MATCH_COUNT=",
):
    if exact not in physical:
        raise SystemExit(f"CLEAN_RUNNER_HOST_PROBE_RED: physical workflow missing {exact!r}")
for forbidden in ("secrets.", "TIBIA_TEST_EMAIL", "TIBIA_TEST_PASSWORD", "bin/client", "xdotool", "gdb"):
    if forbidden in physical:
        raise SystemExit(f"CLEAN_RUNNER_HOST_PROBE_RED: forbidden runtime/secret surface {forbidden!r}")

task = read(TASK)
for exact in (
    "execution_class: synology_physical_runtime",
    "runtime_access: read_only",
    "mutation_authorized: false",
    "credentials_allowed: false",
    "login_allowed: false",
    "process_control_authorized: false",
    "physical_action_budget: 0",
    "physical_action_count: 0",
):
    if exact not in task.split("---", 2)[1]:
        raise SystemExit(f"CLEAN_RUNNER_HOST_PROBE_RED: probe task missing {exact!r}")

stale = read(STALE)
for exact in ("status: completed", "runtime_access: none", "mutation_authorized: false"):
    if exact not in stale.split("---", 2)[1]:
        raise SystemExit(f"CLEAN_RUNNER_HOST_PROBE_RED: stale runtime authority not revoked: {exact!r}")

print("TRACK_A_FIELD6_CLEAN_RUNNER_HOST_PROBE_CONTRACT=PASS")
