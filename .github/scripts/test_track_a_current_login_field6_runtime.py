#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".github/scripts/track_a_current_login_field6_runtime.sh"
MATERIALIZER = ROOT / ".github/scripts/track_a_current_client_package_materialize.py"
ACQUIRE = ROOT / ".github/scripts/track_a_current_client_package_acquire.sh"
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


materializer = need(
    MATERIALIZER,
    (
        "EXPECTED_VERSION = '15.32.75d4a0'",
        "EXPECTED_CLIENT_PACKED_SHA256 = '075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f'",
        "EXPECTED_CLIENT_SHA256 = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'",
        "EXPECTED_CLIENT_SIZE = 52105824",
        "CURL = '/usr/bin/curl'",
        "--socks-port",
        "--socks5-hostname",
        "packedhash",
        "unpackedhash",
        "packedsize",
        "unpackedsize",
        "lzma.FORMAT_RAW",
        "PACKED_FILE_HASH_MISMATCH",
        "UNPACKED_FILE_HASH_MISMATCH",
        "TRACK_A_EXACT_CURRENT_PACKAGE_ALL_FILES_VERIFIED=true",
        "TRACK_A_EXACT_CURRENT_PACKAGE_EXECUTED_DOWNLOADED_CONTENT=false",
        "TRACK_A_EXACT_CURRENT_PACKAGE_MATERIALIZED=true",
    ),
)
for forbidden in ("os.system", "shell=True", "shell = True"):
    if forbidden in materializer:
        raise SystemExit(f"FIELD6_RUNTIME_CONTRACT_RED: unsafe materializer execution fragment {forbidden!r}")

acquire = need(
    ACQUIRE,
    (
        "TASK_ID='OTC-20260828-current-login-field6-runtime'",
        "WARP_PORT='25442'",
        "WGCF_SHA='2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c'",
        "WIREPROXY_TAR_SHA='e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c'",
        'MATERIALIZER="${BASH_SOURCE[0]%/*}/track_a_current_client_package_materialize.py"',
        'WIRE_PID_FILE="$ROOT/wireproxy.pid"',
        "read_wire_pid()",
        "process_is_zombie()",
        "https://static.tibia.com/launcher/tibiaclient-linux-current/package.json",
        'SOURCE="$ROOT/current-package"',
        "--socks-port \"$WARP_PORT\"",
        'printf \'%s\\n\' "$WIRE_PID" >"$WIRE_PID_FILE"',
        'if process_is_zombie "$pid"; then',
        'wait "$pid" 2>/dev/null || true',
        'rm -f "$WIRE_PID_FILE"',
        "TRACK_A_FIELD6_EXACT_PACKAGE_SOURCE=materialized",
        "TRACK_A_FIELD6_PACKAGE_PREFLIGHT=PASS",
        "TRACK_A_FIELD6_PACKAGE_EXECUTED=false",
        "TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS",
    ),
)
for forbidden in (
    "set -x",
    "TIBIA_TEST_EMAIL=",
    "TIBIA_TEST_PASSWORD=",
    "exec \"$SOURCE",
    "LEGACY_SOURCE=",
    "legacy_source_collision",
    "cleanup_source_ownership_refused",
    "ln -s \"$SOURCE\"",
):
    if forbidden in acquire:
        raise SystemExit(f"FIELD6_RUNTIME_CONTRACT_RED: forbidden acquisition fragment {forbidden!r}")

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
        'package="$TASK_BASE/package-acquisition/$RUN_ID/current-package"',
        "TRACK_A_FIELD6_DIRECT_PACKAGE_SOURCE=PASS",
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
    '"$BASE/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"',
    '"/work/_otclient_tibia_re_state/home/.local/share/CipSoft GmbH/Tibia/packages/Tibia"',
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
        ".github/scripts/track_a_current_client_package_materialize.py",
        ".github/scripts/track_a_current_client_package_acquire.sh",
        "github.event.comment.user.login == github.repository_owner",
        "AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V6 once=true",
        "ref: main",
        "secrets.TIBIA_TEST_EMAIL",
        "secrets.TIBIA_TEST_PASSWORD",
        "runtime_access: ephemeral_isolated",
        "mutation_authorized: true",
        "login_allowed: true",
        "character_selection_allowed: false",
        "gameplay_allowed: false",
        "physical_action_budget: 1",
        "bash .github/scripts/track_a_current_client_package_acquire.sh prepare",
        "TRACK_A_FIELD6_PACKAGE_PREFLIGHT=PASS",
        "bash .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh",
        "bash .github/scripts/track_a_current_client_package_acquire.sh cleanup",
        "TRACK_A_FIELD6_RUNTIME_CAPTURED=true",
        "FIELD6_VALUE_PROVEN=true",
    ),
)
for consumed_generation in ("V3", "V4", "V5"):
    consumed = f"AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_{consumed_generation} once=true"
    if consumed in workflow:
        raise SystemExit(
            f"FIELD6_RUNTIME_CONTRACT_RED: consumed {consumed_generation} trigger must not remain executable"
        )
if "secrets.TIBIA_TEST_EMAIL" in workflow.split("jobs:\n", 1)[1].split("live-observation:", 1)[0]:
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: contract job must not receive login secrets")
preflight = workflow.index("bash .github/scripts/track_a_current_client_package_acquire.sh prepare")
consume = workflow.index("Consume exact owner authorization once")
capture = workflow.index("bash .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh")
validate = workflow.index("Validate scalar-only evidence")
upload = workflow.index("Upload sanitized field6 evidence")
cleanup = workflow.index("Clean exact current package preflight state")
if not preflight < consume < capture < validate < upload < cleanup:
    raise SystemExit(
        "FIELD6_RUNTIME_CONTRACT_RED: preflight must precede authorization/login and sanitized evidence must be validated/uploaded before final cleanup"
    )

task = need(
    TASK,
    (
        "task_id: OTC-20260828-current-login-field6-runtime",
        "track_id: official-client-re",
        ".github/scripts/track_a_current_client_package_materialize.py",
        ".github/scripts/track_a_current_client_package_acquire.sh",
        ".github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh",
        "AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V6 once=true",
        "character_selection_allowed: false",
        "gameplay_allowed: false",
        "network_payload_capture_allowed: false",
    ),
)
for consumed_generation in ("V3", "V4", "V5"):
    consumed = f"AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_{consumed_generation} once=true"
    if consumed in task:
        raise SystemExit(
            f"FIELD6_RUNTIME_CONTRACT_RED: current task must omit consumed {consumed_generation} trigger literal to block historical reruns"
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
