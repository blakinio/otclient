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
SECRET_RUNNER_CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md"

ALLOWED_PATHS = {
    ".github/scripts/audit_track_a_current_login_field6_admission.py",
    ".github/scripts/test_track_a_current_login_field6_security_contract.py",
    ".github/scripts/track_a_current_login_field6_runtime.sh",
    ".github/workflows/track-a-current-login-field6-runtime.yml",
    "docs/agents/reports/OTC-20260829-field6-v4-admission-v2.md",
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
        "branch: fix/OTC-20260829-field6-v4-admission-v2",
        "execution_class: synology_physical_runtime",
        "execution_mode: github_actions_ephemeral_isolated",
        "persistent_session_role: canonical_runtime_owner",
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
    )
    missing = [item for item in required if item not in header]
    if missing:
        fail("FIELD6-AUDIT-F002", "task admission fence missing: " + ", ".join(missing))
    for text in (
        "merged PR #795 self-hosted secret-runner boundary and independent audit",
        "If that clean-runner provenance cannot be proven, credentials/login remain forbidden",
        "GITHUB_RUN_ATTEMPT != 1",
        "exact V4 trigger MUST NOT be posted",
    ):
        if text not in task:
            fail("FIELD6-AUDIT-F003", f"task missing clean-runner/rerun invariant: {text}")


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
        "runs-on: [otclient, synology]",
    )
    missing = [item for item in required if item not in live]
    if missing:
        fail("FIELD6-AUDIT-F005", "live trigger/runner fence missing: " + ", ".join(missing))
    if "AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true" in workflow:
        fail("FIELD6-AUDIT-F006", "consumed V3 trigger literal remains executable in workflow")
    return live


def require_order_and_secret_scope(live: str) -> None:
    guard = 'test "${GITHUB_RUN_ATTEMPT:?}" = "1"'
    auth = "- name: Consume exact owner authorization once"
    email = "TIBIA_TEST_EMAIL: ${{ secrets.TIBIA_TEST_EMAIL }}"
    password = "TIBIA_TEST_PASSWORD: ${{ secrets.TIBIA_TEST_PASSWORD }}"
    capture = "- name: Capture field6 with protected login inputs"
    for item, fid in ((guard, "FIELD6-AUDIT-F007"), (auth, "FIELD6-AUDIT-F008"), (capture, "FIELD6-AUDIT-F009"), (email, "FIELD6-AUDIT-F010"), (password, "FIELD6-AUDIT-F011")):
        if item not in live:
            fail(fid, f"live job missing {item}")
    if not live.index(guard) < live.index(auth) < live.index(capture) < live.index(email):
        fail("FIELD6-AUDIT-F012", "required guard -> authorization -> capture/secret ordering is not fail-closed")
    if live.count(email) != 1 or live.count(password) != 1:
        fail("FIELD6-AUDIT-F013", "login secrets are referenced outside the single protected capture step")
    if "TRACK_A_FIELD6_RUN_ATTEMPT=1" not in live:
        fail("FIELD6-AUDIT-F014", "run-attempt proof marker missing")


def require_helper_secret_boundary(helper: str) -> None:
    for secret_name in ("email", "password"):
        if re.search(rf"(?m)^\s*xd\s+type\b[^\n]*\$\{{?{secret_name}\}}?", helper):
            fail("FIELD6-AUDIT-F015", f"{secret_name} is exposed through direct xdotool argv")
    for item in (
        '"$XDO" type --window "$1" --delay 12 --file -',
        'printf \'%s\' "$email" | xd_type_stdin "$win"',
        'printf \'%s\' "$password" | xd_type_stdin "$win"',
    ):
        if item not in helper:
            fail("FIELD6-AUDIT-F016", f"stdin-only credential path missing: {item}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()

    try:
        base_sha = subprocess.check_output(["git", "rev-parse", args.base], cwd=ROOT, text=True, encoding="utf-8").strip()
    except subprocess.CalledProcessError as exc:
        fail("FIELD6-AUDIT-F021", f"cannot resolve base {args.base}: {exc}")

    changed = exact_diff(base_sha)
    unexpected = sorted(changed - ALLOWED_PATHS)
    if unexpected:
        fail("FIELD6-AUDIT-F017", "unexpected changed paths: " + ", ".join(unexpected))
    required_changed = {
        ".github/scripts/test_track_a_current_login_field6_security_contract.py",
        ".github/scripts/track_a_current_login_field6_runtime.sh",
        ".github/workflows/track-a-current-login-field6-runtime.yml",
        "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md",
    }
    missing_changed = sorted(required_changed - changed)
    if missing_changed:
        fail("FIELD6-AUDIT-F018", "expected admission repair path absent from diff: " + ", ".join(missing_changed))

    if not SECRET_RUNNER_CONTRACT.is_file():
        fail("FIELD6-AUDIT-F019", "merged #795 secret-runner contract is absent from trusted tree")
    contract = SECRET_RUNNER_CONTRACT.read_text(encoding="utf-8")
    if "Repository workflow checks are defense in depth only" not in contract or "fresh one-job environment" not in contract:
        fail("FIELD6-AUDIT-F020", "trusted clean-runner contract lacks primary boundary language")

    task = TASK.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    helper = HELPER.read_text(encoding="utf-8")
    require_task_fences(task, base_sha)
    live = require_live_job(workflow)
    require_order_and_secret_scope(live)
    require_helper_secret_boundary(helper)

    print("TRACK_A_CURRENT_LOGIN_FIELD6_ADMISSION_INDEPENDENT_AUDIT=PASS")
    print("AUDIT_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
