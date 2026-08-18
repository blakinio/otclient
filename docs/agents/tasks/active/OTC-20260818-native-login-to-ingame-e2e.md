---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v3-update
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: official-package-update-after-canonical-teardown
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: a10df477ce88183718ed855386ef96ba25b66320
risk: critical
updated: 2026-08-18T15:18:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - .github/workflows/tibia-official-client-re-native-login-*.yml
  - .github/scripts/tibia-official-client-re-canonical-live-teardown.py
  - tools/tibia_runtime_bridge/CMakeLists.txt
  - tools/tibia_runtime_bridge/experimental_auth.cpp
  - tools/tibia_runtime_bridge/experimental_auth_client.py
  - tools/tibia_runtime_bridge/experimental_auth_launcher.py
  - tools/tibia_runtime_bridge/experimental_character_confirm.cpp
  - tools/tibia_runtime_bridge/experimental_character_confirm_client.py
modules_touched:
  - track-a-native-login-runtime
  - track-a-official-package-update
  - tibia-runtime-bridge-native-auth
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
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260818-native-login-to-ingame-e2e
runtime_namespace: native-login-official-package-update
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: true
live_runtime_authorization_source: owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18
retained_canonical_lease_generation: 16
retained_canonical_lease_session: chatgpt-native-login-e2e-20260818-v3-gen16-secrets
canonical_teardown_validation_run: 32141293768
canonical_teardown_validation_result: PASS
canonical_teardown_run: 32141408237
canonical_teardown_job: 95724675001
canonical_teardown_result: PASS
canonical_teardown_registration_absent: true
canonical_teardown_runtime_gone: true
canonical_teardown_lease_retained: true
old_runtime_pid: 30067
old_runtime_display: ':99'
old_runtime_window_identity: x11-window:12582929
old_exact_client_version: 15.32.df7b29
old_exact_client_size: 51965216
old_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
client_version_gate_live_ui_proven: true
current_official_probe_run: 32140385842
current_official_probe_job: 95721374178
current_official_packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
current_official_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_official_client_size: 52109920
current_official_version_strings: 15.32,11.25
current_official_exact_build_suffix: UNKNOWN
secret_ingress_authorized_for_later_login: true
secret_retry_before_update: false
native_auth_secret_dispatch_performed_on_old_client: true
old_native_auth_helper_reusable_on_current_official_client: false
canonical_update_completed: false
new_exact_auth_contract_reproven: false
new_exact_helper_rebuilt: false
new_exact_runtime_bootstrapped: false
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
direct_codex_spark_authorized: true
direct_codex_spark_model: gpt-5.3-codex-spark
direct_codex_spark_used: false
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — package update checkpoint

The old exact canonical client was proven obsolete by the live UI and has now been removed through the reviewed cancellation-safe teardown transition.

Exact teardown proof:

```text
run=32141408237
job=95724675001
GEN16_TEARDOWN_PREFLIGHT=PASS_EXACT_REG1_16_PID30067
TRACK_A_CANONICAL_TEARDOWN_COMMIT=true
TRACK_A_CANONICAL_TEARDOWN_RUNTIME_GONE=true
TRACK_A_CANONICAL_TEARDOWN_REGISTRATION_ABSENT=true
TRACK_A_CANONICAL_TEARDOWN_LEASE_RETAINED=true
TRACK_A_CANONICAL_TEARDOWN_SECRET_ACCESS=false
TRACK_A_CANONICAL_TEARDOWN=PASS
GEN16_TEARDOWN_POSTCHECK=PASS_REGISTRATION_ABSENT_LEASE16_RETAINED
```

There is currently no admitted canonical client/Xvfb/VNC session. Temporary black/noVNC output during this phase is expected.

The task is now scoped to one isolated official-package update. No credentials, login or gameplay are authorized in this phase.

Target exact current official binary, independently proven from CipSoft's current Linux package manifest:

```text
packed client.lzma sha256:
1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354

unpacked client sha256:
ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8

unpacked size:
52109920
```

Required continuation:

```text
isolated official CipSoft launcher/update
 -> stop only updater-owned process group
 -> exact installed package SHA/size fence
 -> prove no stray official client process
 -> preserve update evidence
 -> re-prove native auth/character-login boundaries for the new exact SHA
 -> rebuild/revalidate helper
 -> switch admission to canonical bootstrap
 -> bootstrap fresh runtime
 -> restore noVNC
 -> only then re-enable one-shot Secrets auth
```

The old helper and all old binary offsets remain forbidden on the new SHA until re-proven.

```text
STATUS=VALIDATING
RESULT=OFFICIAL_PACKAGE_UPDATE_REQUIRED
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
MUTATION_AUTHORIZED=true
```
