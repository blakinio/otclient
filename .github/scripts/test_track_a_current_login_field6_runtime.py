#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".github/scripts/track_a_current_login_field6_runtime.sh"
SECRET_WRAPPER = ROOT / ".github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh"
WORKFLOW = ROOT / ".github/workflows/track-a-current-login-field6-runtime.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md"


def need(path: Path, needles: tuple[str, ...]) -> str:
    if not path.is_file():
        raise SystemExit(f"FIELD6_RUNTIME_CONTRACT_RED: missing {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise SystemExit(f"FIELD6_RUNTIME_CONTRACT_RED: {path.relative_to(ROOT)} missing {missing}")
    return text


helper = need(
    HELPER,
    (
        "TASK_ID='OTC-20260828-current-login-field6-runtime'",
        "EXPECTED_CLIENT_VERSION='15.32.75d4a0'",
        "EXPECTED_CLIENT_SIZE='52105824'",
        "EXPECTED_CLIENT_SHA256='d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'",
        "PRODUCER_OFFSET='0xe25620'",
        "WGCF_SHA='2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c'",
        "WIREPROXY_TAR_SHA='e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c'",
        'START_OUT="$ROOT/process-start-ticks.txt"',
        "set disable-randomization off",
        "gdb.parse_and_eval('$edx')",
        'start_ticks="$(tr -cd \'0-9\' <"$START_OUT")"',
        "TRACK_A_FIELD6_PROCESS_IDENTITY_SNAPSHOTTED=true",
        "FIELD6_VALUE=",
        "TRACK_A_FIELD6_RUNTIME_CAPTURED=true",
        "TRACK_A_FIELD6_CHARACTER_SELECTION=false",
        "TRACK_A_FIELD6_WORLD_ENTRY=false",
        "cleanup",
    ),
)
for forbidden in (
    "attach ",
    "ptrace_scope=0",
    "kernel.yama.ptrace_scope",
    "TRACK_A_CHARACTER_ACTIVATION_SENT",
    "tcpdump",
    "dump memory",
):
    if forbidden in helper:
        raise SystemExit(f"FIELD6_RUNTIME_CONTRACT_RED: forbidden helper fragment {forbidden!r}")

wrapper = need(
    SECRET_WRAPPER,
    (
        'export -n TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD',
        "env | grep -Eq '^(TIBIA_TEST_EMAIL|TIBIA_TEST_PASSWORD)='",
        'source "$HELPER" "$@"',
        'TRACK_A_FIELD6_SECRET_ENV_SCRUBBED=true',
    ),
)
if "set -x" in wrapper:
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: secret wrapper must never enable xtrace")
if wrapper.index("export -n TIBIA_TEST_EMAIL TIBIA_TEST_PASSWORD") > wrapper.index('source "$HELPER" "$@"'):
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: secret env scrub must occur before sourcing helper")

workflow = need(
    WORKFLOW,
    (
        "name: Track A current login field6 runtime observation",
        "issue_comment:",
        "pull_request:",
        "github.event.comment.user.login == github.repository_owner",
        "AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V1 once=true",
        "ref: main",
        "secrets.TIBIA_TEST_EMAIL",
        "secrets.TIBIA_TEST_PASSWORD",
        "runtime_access: ephemeral_isolated",
        "mutation_authorized: true",
        "login_allowed: true",
        "character_selection_allowed: false",
        "gameplay_allowed: false",
        "physical_action_budget: 1",
        "bash .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh",
        "TRACK_A_FIELD6_RUNTIME_CAPTURED=true",
        "FIELD6_VALUE_PROVEN=true",
    ),
)
if "secrets.TIBIA_TEST_EMAIL" in workflow.split("jobs:\n", 1)[1].split("live-observation:", 1)[0]:
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: contract job must not receive login secrets")

task = need(
    TASK,
    (
        "task_id: OTC-20260828-current-login-field6-runtime",
        "track_id: official-client-re",
        "branch: work/OTC-20260828-current-login-field6-runtime",
        ".github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh",
        "character_selection_allowed: false",
        "gameplay_allowed: false",
        "network_payload_capture_allowed: false",
    ),
)
static = (
    "runtime_access: none" in task
    and "mutation_authorized: false" in task
    and "login_allowed: false" in task
    and "target_uniqueness: NOT_APPLICABLE" in task
)
live = (
    "runtime_access: ephemeral_isolated" in task
    and "mutation_authorized: true" in task
    and "login_allowed: true" in task
    and "target_uniqueness: PROVEN" in task
    and "credentials_allowed: true" in task
    and "physical_action_budget: 1" in task
)
if not (static or live):
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: task admission is neither static-safe nor live-authorized")

if re.search(r"(?im)^\s*(?:password|email|token)\s*:\s*[^<\s].+$", task):
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: task appears to retain secret material")

print("TRACK_A_CURRENT_LOGIN_FIELD6_RUNTIME_CONTRACT=PASS")
