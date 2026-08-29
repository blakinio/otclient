#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / ".github/scripts/track_a_current_login_field6_runtime.sh"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md"
WORKFLOW = ROOT / ".github/workflows/track-a-current-login-field6-runtime.yml"


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


task = read(TASK)
for required in (
    "execution_class: synology_physical_runtime",
    "persistent_session_role: canonical_runtime_owner",
    "physical_e2e_required: true",
):
    if required not in task:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: task missing {required!r}")


workflow = read(WORKFLOW)
run_attempt_guard = 'test "${GITHUB_RUN_ATTEMPT:?}" = "1"'
auth_marker = '- name: Consume exact owner authorization once'
secret_marker = 'TIBIA_TEST_EMAIL: ${{ secrets.TIBIA_TEST_EMAIL }}'
if run_attempt_guard not in workflow:
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: live workflow missing GITHUB_RUN_ATTEMPT == 1 guard")
if workflow.index(run_attempt_guard) > workflow.index(auth_marker):
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: rerun guard must precede authorization consumption")
if workflow.index(run_attempt_guard) > workflow.index(secret_marker):
    raise SystemExit("FIELD6_SECURITY_CONTRACT_RED: rerun guard must precede secret exposure")

helper = read(HELPER)
for secret_name in ("email", "password"):
    if re.search(rf"(?m)^\s*xd\s+type\b[^\n]*\$\{{?{secret_name}\}}?", helper):
        raise SystemExit(
            f"FIELD6_SECURITY_CONTRACT_RED: {secret_name} must not be passed to xdotool argv"
        )

for required in (
    "xd_type_stdin()",
    '"$XDO" type --window "$1" --delay 12 --file -',
    'printf \'%s\' "$email" | xd_type_stdin "$win"',
    'printf \'%s\' "$password" | xd_type_stdin "$win"',
):
    if required not in helper:
        raise SystemExit(f"FIELD6_SECURITY_CONTRACT_RED: helper missing {required!r}")

print("TRACK_A_CURRENT_LOGIN_FIELD6_SECURITY_CONTRACT=PASS")
