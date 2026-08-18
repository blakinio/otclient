---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: native-login-external-action-required
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v2
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
risk: critical
updated: 2026-08-18T12:35:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - .github/workflows/tibia-official-client-re-native-login-*.yml
modules_touched:
  - track-a-native-login-runtime
policy_version: 2
prompting_standard_version: 2.1
prompt_contract: docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
prompt_alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME
execution_mode: github-orchestrated-synology
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
programme_boundary: native_login_task_and_required_closeout_only
user_communication: terminal_only
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260818-native-login-to-ingame-e2e
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: 10
registration_lease_generation: 10
gate_a: PASS
generation_rebind: PASS
gate_b: PASS
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
client_byte_mutation_authorized: false
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
simultaneous_logged_in_sessions_max: 1
live_runtime_authorization_source: owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18
owner_funded_ai_api_authorized: false
direct_codex_spark_authorized: true
direct_codex_spark_model: gpt-5.3-codex-spark
direct_codex_spark_used: false
exact_client_version: 15.32.df7b29
exact_client_size: 51965216
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
form_ui_used: false
ocr_used: false
image_matching_used: false
coordinate_login_used: false
blind_tab_return_used: false
gui_credential_entry_used: false
password_logged: false
session_secret_persisted: false
auth_bypass_used: false
tls_weakened: false
server_response_spoofed: false
historical_runtime_authority_inherited: false
historical_pid_xid_display_session_inherited: false
historical_login_budget_inherited: false
protected_secret_source_required_if_cold_auth: true
controller_plane_inventory_run: 32124348434
canonical_bootstrap_run: 32125054251
canonical_bootstrap_result: REGISTERED_GATE_B_PASS
post_bootstrap_inventory_run: 32125504315
canonical_rebind_run: 32125924194
canonical_rebind_result: REBIND_GATE_B_PASS_ACTIVE_GEN10
canonical_rebind_registration_generation: 2
canonical_rebind_registration_lease_generation: 10
retained_session_probe_run: 32126937957
retained_session_probe_job: 95679477308
retained_session_probe_result: CURRENT_NATIVE_CHARACTER_MODEL_EMPTY
retained_session_available: false
cold_auth_required: true
cold_auth_capability_run: 32127178186
cold_auth_capability_job: 95680214790
cold_auth_controlling_tty: false
cold_auth_tty_errno: 6
cold_auth_helper_loaded: false
cold_auth_auth_socket_present: false
cold_auth_protected_producer_import: PASS
terminal_release_run: 32127353047
terminal_release_job: 95680752008
terminal_release_generation: 10
controller_authority_released: true
terminal_blocker: EXTERNAL_ACTION_REQUIRED
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — external secret boundary

## Verified progress

Fresh physical execution on `synology-otclient-01` reached and validated the exact official client under the current Track A canonical runtime contract:

```text
CLIENT_VERSION=15.32.df7b29
CLIENT_SIZE=51965216
CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
CANONICAL_BOOTSTRAP=PASS
BOOTSTRAP_GATE_B=PASS
CANONICAL_REBIND=PASS
REBIND_GATE_B=PASS
REGISTRATION_GENERATION=2
LEASE_GENERATION=10
```

The one bounded retained-native-session discriminator then proved exactly one current `TCharacterSelectionController`, but both current native model collections were empty:

```text
NATIVE_LOGIN_RETAINED_CHARSEL_INSTANCE_COUNT=1
NATIVE_LOGIN_RETAINED_CHARSEL_VPTR_PROVEN=true
NATIVE_LOGIN_RETAINED_NATIVE_CHARACTER_LIST_COUNT=0
NATIVE_LOGIN_RETAINED_NATIVE_SELECTED_LOGIN_DATA_COUNT=0
NATIVE_LOGIN_RETAINED_SESSION=NOT_PROVEN_AVAILABLE
NATIVE_LOGIN_RETAINED_DISCRIMINATOR=PASS:CURRENT_NATIVE_CHARACTER_MODEL_EMPTY
```

No direct-to-character-selection shortcut was invoked. Cold authentication is therefore required before native character selection can be legitimately reached.

## Protected cold-auth boundary

The promoted protected credential producer is importable, but the actual GitHub Actions execution context has no real controlling terminal:

```text
NATIVE_LOGIN_COLD_AUTH_PROTECTED_PRODUCER_IMPORT=PASS
NATIVE_LOGIN_COLD_AUTH_CONTROLLING_TTY=false
NATIVE_LOGIN_COLD_AUTH_TTY_ERRNO=6
```

The currently registered client was also launched without the experimental native-auth helper and has no auth socket:

```text
NATIVE_LOGIN_COLD_AUTH_HELPER_LOADED=false
NATIVE_LOGIN_COLD_AUTH_SESSION_AUTH_SOCKET_PRESENT=false
NATIVE_LOGIN_COLD_AUTH_SESSION_AUTH_SOCKET_COUNT=0
```

The repository security contract forbids using GitHub Actions secrets/environment, stdin/getpass, pseudo-TTY, plaintext files, GUI credential entry, OCR or coordinate automation as a replacement for the missing real controlling `/dev/tty`. Credentials and 2FA must never be pasted into chat.

## Terminal release

After proving the external boundary, the task released controller authority cleanly:

```text
NATIVE_LOGIN_TERMINAL_RELEASE_PRECHECK=ACTIVE_GEN10_CURRENT_TASK
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
NATIVE_LOGIN_TERMINAL_RELEASE_RESULT=RELEASED_GEN10
NATIVE_LOGIN_TERMINAL_CLIENT_MUTATION=false
NATIVE_LOGIN_TERMINAL_CREDENTIAL_ACCESS=false
NATIVE_LOGIN_TERMINAL_LOGIN_PERFORMED=false
```

The task-local lease token was deleted. The registered client remains idle, but its PID/display/window and generation-10 registration are historical evidence only; they do not transfer authority to any continuation.

## Durable evidence

- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-controller-plane-admission-inventory.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-canonical-bootstrap-gate-b.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-post-bootstrap-controller-inventory.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-canonical-rebind-gate-b.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-retained-session-discriminator.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-cold-auth-capability.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-terminal-controller-release.md`

## Terminal checkpoint

```text
STATUS=WAITING
RESULT=EXTERNAL_ACTION_REQUIRED
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
FORM_UI_USED=false
OCR_USED=false
IMAGE_MATCHING_USED=false
GUI_CREDENTIAL_ENTRY_USED=false
SECRET_REQUESTED_IN_ACTIONS=false
SECRET_READ_BY_AGENT=false
CONTROLLER_AUTHORITY_RELEASED=true
BLOCKER=Cold auth is required, but the autonomous GitHub Actions context has no real controlling /dev/tty; the current client also lacks the launch-time native-auth helper/socket.
NEXT_ACTION=On continuation, first re-admit from fresh controller-plane evidence and prepare an exact auth-helper-enabled client runtime. Then a human operator must enter account/password only through the protected producer on a real controlling Linux /dev/tty; do not send credentials or OTPs through chat. After successful native account auth, continue semantically through native character selection and prove actual game-server IN_GAME causally.
```
