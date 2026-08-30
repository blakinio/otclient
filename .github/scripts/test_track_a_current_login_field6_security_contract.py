#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".github/scripts/track_a_current_login_field6_runtime.sh"
ACQUIRE = ROOT / ".github/scripts/track_a_current_client_package_acquire.sh"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md"
WORKFLOW = ROOT / ".github/workflows/track-a-current-login-field6-runtime.yml"
V2_CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V2.md"

EXPECTED_RUNNER = "molehill-otclient-v5-01"
EXPECTED_GUEST = "OTClientV5Clean"
EXPECTED_ROOTFS_SHA = "915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d"
EXPECTED_ADMISSION = "PR_758_COMMENT_5468621219"
EXPECTED_SEED_PATH = "/opt/otclient-v5-seed/seed.tar.gz"
EXPECTED_SEED_SIZE = "412272538"
EXPECTED_SEED_SHA = "64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016"


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


task = read(TASK)
static_required = (
    "execution_class: github_hosted",
    "execution_mode: github_actions_static",
    "persistent_session_role: none",
    "physical_e2e_required: false",
    "runtime_access: none",
    "runtime_owner_task: NOT_APPLICABLE",
    "runtime_namespace: NOT_APPLICABLE",
    "target_uniqueness: NOT_APPLICABLE",
    "mutation_authorized: false",
    "credentials_allowed: false",
    "login_allowed: false",
    "gui_input_authorized: false",
    "process_control_authorized: false",
    "character_selection_allowed: false",
    "gameplay_allowed: false",
    "network_payload_capture_allowed: false",
    "physical_action_count: 0",
)
live_required = (
    "execution_class: independent_ephemeral_physical_runtime",
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
    f"live_runtime_authorization_source: {EXPECTED_ADMISSION}",
    f"independent_guest_name: {EXPECTED_GUEST}",
    f"independent_runner_name: {EXPECTED_RUNNER}",
    f"independent_rootfs_sha256: {EXPECTED_ROOTFS_SHA}",
    f"independent_seed_path: {EXPECTED_SEED_PATH}",
    f"independent_seed_size: {EXPECTED_SEED_SIZE}",
    f"independent_seed_sha256: {EXPECTED_SEED_SHA}",
    "independent_runner_provenance_schema: otclient.track-a.independent-field6-runner.v2",
)
static = all(required in task for required in static_required)
live = all(required in task for required in live_required)
if not (static or live):
    missing_static = [required for required in static_required if required not in task]
    missing_live = [required for required in live_required if required not in task]
    raise SystemExit(
        "FIELD6_SECURITY_CONTRACT_RED: task is neither static-safe nor live-authorized; "
        f"static_missing={missing_static}; live_missing={missing_live}"
    )

workflow = read(WORKFLOW)
run_attempt_guard = 'test "${GITHUB_RUN_ATTEMPT:?}" = "1"'
auth_marker = '- name: Consume exact owner authorization once'
secret_marker = 'TIBIA_TEST_EMAIL: ${{ secrets.TIBIA_TEST_EMAIL }}'
provenance_marker = '- name: Prove independent clean guest provenance'
expected_label = "runs-on: ${{ format('field6-v5-{0}', github.event.comment.id) }}"
for required in (
    expected_label,
    f"EXPECTED_INDEPENDENT_RUNNER_NAME: {EXPECTED_RUNNER}",
    f"EXPECTED_INDEPENDENT_GUEST_NAME: {EXPECTED_GUEST}",
    f"EXPECTED_INDEPENDENT_ROOTFS_SHA: {EXPECTED_ROOTFS_SHA}",
    "PROVENANCE_FILE: /etc/otclient-field6-runner-provenance",
    'test "${RUNNER_NAME:?}" = "$EXPECTED_INDEPENDENT_RUNNER_NAME"',
    "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE_VERIFIED=1",
    "TRACK_A_FIELD6_INDEPENDENT_SEED_VERIFIED=1",
    "TRACK_A_FIELD6_SYSTEM_TOOLROOT=1",
    "otclient.track-a.independent-field6-runner.v2",
    f"EXPECTED_SEED_PATH: {EXPECTED_SEED_PATH}",
    f"EXPECTED_SEED_SIZE: '{EXPECTED_SEED_SIZE}'",
    f"EXPECTED_SEED_SHA: {EXPECTED_SEED_SHA}",
):
    if required not in workflow:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: live workflow missing {required!r}")
for forbidden in ("field6-v4-{0}", "molehill-otclient-v4-01", "OTClientV4Clean", "runs-on: [otclient, synology]"):
    if forbidden in workflow:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: stale physical boundary remains in workflow: {forbidden}")
if run_attempt_guard not in workflow:
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: live workflow missing GITHUB_RUN_ATTEMPT == 1 guard")
if not workflow.index(provenance_marker) < workflow.index(run_attempt_guard) < workflow.index(auth_marker) < workflow.index(secret_marker):
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: provenance step must begin with rerun guard before authorization and secret exposure")

helper = read(HELPER)
for secret_name in ("email", "password"):
    if re.search(rf"(?m)^\s*xd\s+type\b[^\n]*\$\{{?{secret_name}\}}?", helper):
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: {secret_name} must not be passed to xdotool argv")
for required in (
    "xd_type_stdin()",
    '"$XDO" type --window "$1" --delay 12 --file -',
    'printf \'%s\' "$email" | xd_type_stdin "$win"',
    'printf \'%s\' "$password" | xd_type_stdin "$win"',
    "TRACK_A_FIELD6_SYSTEM_TOOLROOT",
    "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE_VERIFIED",
    EXPECTED_RUNNER,
):
    if required not in helper:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: helper missing {required!r}")
if "molehill-otclient-v4-01" in helper:
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: V4 runner remains accepted by helper")

acquire = read(ACQUIRE)
for required in (
    "TRACK_A_FIELD6_INDEPENDENT_PROVENANCE_VERIFIED",
    "TRACK_A_FIELD6_INDEPENDENT_SEED_VERIFIED",
    EXPECTED_RUNNER,
    EXPECTED_SEED_PATH,
    'python3 "$SEED_IMPORTER" "$SEED_ARCHIVE" "$SOURCE" --require-root-owner',
    "TRACK_A_FIELD6_EXACT_PACKAGE_SOURCE=official_launcher_seed",
):
    if required not in acquire:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: package acquisition missing {required!r}")
if "molehill-otclient-v4-01" in acquire:
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: V4 runner remains accepted by package acquisition")

v2 = read(V2_CONTRACT)
for required in (
    "field6-v5-<comment_id>", EXPECTED_RUNNER, EXPECTED_GUEST, "--no-default-labels",
    "no host Docker socket", EXPECTED_SEED_PATH, EXPECTED_SEED_SHA,
):
    if required not in v2:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: V2 independent contract missing {required!r}")

print("TRACK_A_CURRENT_LOGIN_FIELD6_SECURITY_CONTRACT=PASS")
