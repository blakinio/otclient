#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/track-a-current-login-field6-runtime.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md"
HELPER = ROOT / ".github/scripts/track_a_current_login_field6_runtime.sh"
ACQUIRE = ROOT / ".github/scripts/track_a_current_client_package_acquire.sh"
SECRET_RUNNER_CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md"
INDEPENDENT_CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md"

RUNNER = "molehill-otclient-v4-01"
GUEST = "OTClientV4Clean"
ROOTFS_URL = "https://cloud-images.ubuntu.com/releases/noble/release-20260801/ubuntu-24.04-server-cloudimg-amd64-root.tar.xz"
ROOTFS_SHA = "915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d"

ALLOWED_PATHS = {
    ".github/scripts/audit_track_a_current_login_field6_admission.py",
    ".github/scripts/test_track_a_current_login_field6_security_contract.py",
    ".github/scripts/track_a_current_client_package_acquire.sh",
    ".github/scripts/track_a_current_login_field6_runtime.sh",
    ".github/workflows/track-a-current-login-field6-runtime.yml",
    "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md",
}


def fail(fid: str, message: str) -> None:
    raise SystemExit(f"{fid}: {message}")


def exact_diff(base: str) -> set[str]:
    try:
        raw = subprocess.check_output(
            ["git", "diff", "--name-only", base],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as exc:
        fail("FIELD6-AUDIT-F001", f"cannot enumerate exact diff from {base}: {exc}")
    return {line.strip().replace("\\", "/") for line in raw.splitlines() if line.strip()}


def require_task_fences(task: str, base: str) -> None:
    header = task.split("---", 2)[1]
    required = (
        f"base_main: {base}",
        "branch: fix/OTC-20260829-field6-v4-independent-runner",
        "execution_class: independent_ephemeral_physical_runtime",
        "execution_mode: github_actions_independent_ephemeral_physical",
        "persistent_session_role: none",
        "physical_e2e_required: true",
        "runtime_access: ephemeral_isolated",
        "target_uniqueness: PROVEN",
        "mutation_authorized: true",
        "credentials_allowed: true",
        "login_allowed: true",
        "relogin_allowed: false",
        "restart_allowed: false",
        "character_selection_allowed: false",
        "gameplay_allowed: false",
        "network_payload_capture_allowed: false",
        "physical_action_budget: 1",
        "physical_action_count: 0",
        "live_runtime_authorization_source: PR_758_COMMENT_5457904227",
        f"independent_guest_name: {GUEST}",
        f"independent_runner_name: {RUNNER}",
        f"independent_rootfs_url: {ROOTFS_URL}",
        f"independent_rootfs_sha256: {ROOTFS_SHA}",
        "independent_runner_provenance: /etc/otclient-field6-runner-provenance",
    )
    missing = [item for item in required if item not in header]
    if missing:
        fail("FIELD6-AUDIT-F002", "task admission fence missing: " + ", ".join(missing))
    for text in (
        "Trusted-main host probe run `33261106292`, job `99123092884`",
        "Merged PR #804",
        "the one-time label `field6-v4-<comment_id>`",
        "That comment ID becomes the one-time runner label.",
        "The exact V4 trigger remains unposted.",
        "an identical V4 retry is forbidden",
    ):
        if text not in task:
            fail("FIELD6-AUDIT-F003", f"task missing independent-runner invariant: {text}")


def require_live_job(workflow: str) -> str:
    marker = "  live-observation:\n"
    if marker not in workflow:
        fail("FIELD6-AUDIT-F004", "live-observation job missing")
    live = workflow.split(marker, 1)[1]
    required = (
        "github.event_name == 'issue_comment'",
        "github.event.issue.number == 758",
        "github.event.comment.user.login == github.repository_owner",
        "github.event.comment.body == 'AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true'",
        "runs-on: ${{ format('field6-v4-{0}', github.event.comment.id) }}",
        f"EXPECTED_INDEPENDENT_RUNNER_NAME: {RUNNER}",
        f"EXPECTED_INDEPENDENT_GUEST_NAME: {GUEST}",
        f"EXPECTED_INDEPENDENT_ROOTFS_URL: {ROOTFS_URL}",
        f"EXPECTED_INDEPENDENT_ROOTFS_SHA: {ROOTFS_SHA}",
        "PROVENANCE_FILE: /etc/otclient-field6-runner-provenance",
    )
    missing = [item for item in required if item not in workflow]
    if missing:
        fail("FIELD6-AUDIT-F005", "live trigger/runner/provenance fence missing: " + ", ".join(missing))
    if "runs-on: [otclient, synology]" in live:
        fail("FIELD6-AUDIT-F006", "V4 live job still targets Synology")
    if "AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true" in workflow:
        fail("FIELD6-AUDIT-F007", "consumed V3 trigger literal remains executable in workflow")
    return live


def require_order_and_secret_scope(live: str) -> None:
    provenance = "- name: Prove independent clean guest provenance"
    checkout = "- name: Checkout exact trusted main"
    admission = "- name: Prove trusted-main live admission and immutable boundaries"
    materialize = "- name: Materialize exact current package through task-owned WARP"
    auth = "- name: Consume exact owner authorization once"
    capture = "- name: Capture field6 with protected login inputs"
    email = "TIBIA_TEST_EMAIL: ${{ secrets.TIBIA_TEST_EMAIL }}"
    password = "TIBIA_TEST_PASSWORD: ${{ secrets.TIBIA_TEST_PASSWORD }}"
    guard = 'test "${GITHUB_RUN_ATTEMPT:?}" = "1"'
    for item, fid in (
        (provenance, "FIELD6-AUDIT-F008"), (checkout, "FIELD6-AUDIT-F009"),
        (admission, "FIELD6-AUDIT-F010"), (materialize, "FIELD6-AUDIT-F011"),
        (auth, "FIELD6-AUDIT-F012"), (capture, "FIELD6-AUDIT-F013"),
        (email, "FIELD6-AUDIT-F014"), (password, "FIELD6-AUDIT-F015"),
        (guard, "FIELD6-AUDIT-F016"),
    ):
        if item not in live:
            fail(fid, f"live job missing {item}")
    if not live.index(provenance) < live.index(checkout) < live.index(admission) < live.index(materialize) < live.index(auth) < live.index(capture) < live.index(email):
        fail("FIELD6-AUDIT-F017", "provenance -> main -> admission -> package -> authorization -> secret ordering invalid")
    if live.count(email) != 1 or live.count(password) != 1:
        fail("FIELD6-AUDIT-F018", "login secrets are referenced outside the single protected capture step")
    for marker in (
        "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE=PASS",
        "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE_VERIFIED=1",
        "TRACK_A_FIELD6_SYSTEM_TOOLROOT=1",
        "TRACK_A_FIELD6_RUN_ATTEMPT=1",
        'test "${RUNNER_NAME:?}" = "$EXPECTED_INDEPENDENT_RUNNER_NAME"',
        "FIELD6_PROVENANCE_NOT_ROOT_OWNED",
        "FIELD6_PROVENANCE_WRITABLE_BY_NONROOT",
    ):
        if marker not in live:
            fail("FIELD6-AUDIT-F019", f"live provenance proof missing {marker}")


def require_helper_boundary(helper: str, acquire: str) -> None:
    for secret_name in ("email", "password"):
        if re.search(rf"(?m)^\s*xd\s+type\b[^\n]*\$\{{?{secret_name}\}}?", helper):
            fail("FIELD6-AUDIT-F020", f"{secret_name} is exposed through direct xdotool argv")
    for item in (
        '"$XDO" type --window "$1" --delay 12 --file -',
        'printf \'%s\' "$email" | xd_type_stdin "$win"',
        'printf \'%s\' "$password" | xd_type_stdin "$win"',
        "INDEPENDENT_RUNNER_NAME='molehill-otclient-v4-01'",
        "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE_VERIFIED",
        "TRACK_A_FIELD6_SYSTEM_TOOLROOT",
        "toolroot_ok /",
        "resolve_proxychains_library",
    ):
        if item not in helper:
            fail("FIELD6-AUDIT-F021", f"helper boundary missing {item}")
    if "[[ \"${RUNNER_NAME:-}\" == 'synology-otclient-01' ]] || fail wrong_runner" in helper:
        fail("FIELD6-AUDIT-F022", "runtime helper retains Synology-only runner gate")
    for item in (
        "molehill-otclient-v4-01",
        "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE_VERIFIED",
        "runner_allowed || fail wrong_runner",
    ):
        if item not in acquire:
            fail("FIELD6-AUDIT-F023", f"package acquisition boundary missing {item}")
    if "[[ \"${RUNNER_NAME:-}\" == 'synology-otclient-01' ]] || fail wrong_runner" in acquire:
        fail("FIELD6-AUDIT-F024", "package acquisition retains Synology-only runner gate")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    try:
        base_sha = subprocess.check_output(["git", "rev-parse", args.base], cwd=ROOT, text=True, encoding="utf-8").strip()
    except subprocess.CalledProcessError as exc:
        fail("FIELD6-AUDIT-F025", f"cannot resolve base {args.base}: {exc}")

    changed = exact_diff(base_sha)
    unexpected = sorted(changed - ALLOWED_PATHS)
    if unexpected:
        fail("FIELD6-AUDIT-F026", "unexpected changed paths: " + ", ".join(unexpected))
    required_changed = {
        ".github/scripts/test_track_a_current_login_field6_security_contract.py",
        ".github/scripts/audit_track_a_current_login_field6_admission.py",
        ".github/scripts/track_a_current_client_package_acquire.sh",
        ".github/scripts/track_a_current_login_field6_runtime.sh",
        ".github/workflows/track-a-current-login-field6-runtime.yml",
        "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md",
    }
    missing_changed = sorted(required_changed - changed)
    if missing_changed:
        fail("FIELD6-AUDIT-F027", "expected independent runner repair path absent from diff: " + ", ".join(missing_changed))

    if not SECRET_RUNNER_CONTRACT.is_file() or not INDEPENDENT_CONTRACT.is_file():
        fail("FIELD6-AUDIT-F028", "trusted secret/independent runner contract missing")
    independent = INDEPENDENT_CONTRACT.read_text(encoding="utf-8")
    for marker in ("physically separate", "--no-default-labels", "field6-v4-<comment_id>", "no host Docker socket"):
        if marker not in independent:
            fail("FIELD6-AUDIT-F029", f"independent runner contract missing {marker}")

    task = TASK.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    helper = HELPER.read_text(encoding="utf-8")
    acquire = ACQUIRE.read_text(encoding="utf-8")
    require_task_fences(task, base_sha)
    live = require_live_job(workflow)
    require_order_and_secret_scope(live)
    require_helper_boundary(helper, acquire)

    print("TRACK_A_CURRENT_LOGIN_FIELD6_ADMISSION_INDEPENDENT_AUDIT=PASS")
    print("AUDIT_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
