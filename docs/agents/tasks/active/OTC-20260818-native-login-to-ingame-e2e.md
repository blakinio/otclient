---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: ready
agent: null
session_id: null
session_role: handoff_ready
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: resume-package-source-inventory-before-update
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
risk: critical
updated: 2026-08-18T15:30:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
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
  - native-login-prompt-contract
policy_version: 2
prompting_standard_version: 2.1
prompt_contract: docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
prompt_alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME
prompt_contract_target_version: 4.0.0
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
runtime_namespace: native-login-package-source-inventory
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: true
live_runtime_authorization_source: owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18
last_proven_canonical_lease_generation: 16
last_proven_canonical_lease_session: chatgpt-native-login-e2e-20260818-v3-gen16-secrets
canonical_lease_current_status: VERIFY_FRESH_ON_RESUME
canonical_teardown_validation_run: 32141293768
canonical_teardown_validation_result: PASS
canonical_teardown_run: 32141408237
canonical_teardown_job: 95724675001
canonical_teardown_result: PASS
canonical_teardown_registration_absent: true
canonical_teardown_runtime_gone: true
canonical_teardown_lease_retained_at_run_end: true
old_runtime_pid: 30067
old_runtime_display: ':99'
old_runtime_window_identity: x11-window:12582929
old_exact_client_version: 15.32.df7b29
old_exact_client_size: 51965216
old_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
client_version_gate_live_ui_proven: true
client_version_gate_text_sanitized: Your client version is too old. Restart Tibia to update your client.
novnc_raw_xres_repair_run: 32138989357
novnc_raw_xres_repair_job: 95717041668
novnc_raw_xres_repair_result: PASS
novnc_historical_display: ':99'
novnc_historical_xid: 12582929
current_official_probe_run: 32140385842
current_official_probe_job: 95721374178
current_official_probe_result: PASS_READ_ONLY
current_official_packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
current_official_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_official_client_size: 52109920
current_official_version_strings: 15.32,11.25
current_official_exact_build_suffix: UNKNOWN
current_installed_package_client_identity: UNKNOWN_AT_HANDOFF
latest_package_update_run: 32142303624
latest_package_update_job: 95727636509
latest_package_update_result: FAIL_CLOSED_BEFORE_PACKAGE_UPDATE_OLD_EXACT
latest_package_update_governance: PASS
latest_package_update_lease16: PASS
latest_package_update_backup_started: false
latest_package_update_warp_started: false
latest_package_update_xvfb_started: false
latest_package_update_launcher_started: false
latest_package_update_package_mutation_performed: false
latest_package_update_failure_boundary: source_package_client_path_or_size_or_sha_precondition
canonical_update_completed: false
new_exact_auth_contract_reproven: false
new_exact_helper_rebuilt: false
new_exact_runtime_bootstrapped: false
secret_ingress_historical_owner_authorization: true
secret_ingress_requires_current_owner_authority_on_replacement_session: true
secret_retry_before_update: false
native_auth_secret_dispatch_performed_on_old_client: true
old_native_auth_helper_reusable_on_current_official_client: false
old_binary_offsets_reusable_on_current_official_client: false
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
next_action: Freshly verify current main, PR #528/head, current Track A lease/controller-plane state and the exact on-disk source-package bin/client identity; then choose update-required versus already-current without using credentials or starting a canonical client.
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — durable continuation checkpoint

This task is intentionally **READY for a replacement agent**. Do not restart discovery from the login form and do not create a parallel implementation PR while #528 remains the active owner.

## PROVEN durable facts

### 1. noVNC was not the authentication blocker

The user-visible viewer was recovered and raw XRes proved the real Tibia window rather than relying on `xdotool --pid`:

```text
run=32138989357
job=95717041668
DISPLAY=:99
PID=30067
XID=12582929
RAW_XRES_VIEWABLE_1920X1080=true
RFB=PASS
WEBSOCKET=PASS
```

Durable runbook rule: a black `http://synology:6082/` view does not prove the client window is absent. Prove the active DISPLAY/window with raw XRes first, then bind `x11vnc` to that DISPLAY, `websockify` to the RFB backend, and finally the host-facing 6082 presentation layer.

### 2. the old exact client was rejected as too old

The recovered live screen showed the sanitized server/client gate:

```text
Your client version is too old.
Restart Tibia to update your client.
```

The account identifier visible in the UI is intentionally not persisted in evidence.

The obsolete exact binary was:

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

It must not be used for another login attempt.

### 3. the then-current official CipSoft manifest was resolved read-only

```text
run=32140385842
job=95721374178
packed client.lzma sha256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked client sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size=52109920
version strings=15.32,11.25
```

This is a last-known checkpoint, not permanent truth. A replacement agent must refetch the current official manifest immediately before any package mutation and record a changed target if CipSoft has advanced again.

### 4. obsolete gen16 was removed through a reviewed canonical teardown

```text
run=32141408237
job=95724675001
GEN16_TEARDOWN_PREFLIGHT=PASS_EXACT_REG1_16_PID30067
TRACK_A_CANONICAL_TEARDOWN_RUNTIME_GONE=true
TRACK_A_CANONICAL_TEARDOWN_REGISTRATION_ABSENT=true
TRACK_A_CANONICAL_TEARDOWN_LEASE_RETAINED=true
TRACK_A_CANONICAL_TEARDOWN_SECRET_ACCESS=false
TRACK_A_CANONICAL_TEARDOWN=PASS
```

At teardown completion there was no admitted canonical client/Xvfb/VNC runtime. The gen16 lease was retained at that instant; its status must be freshly checked on resume and must not be guessed from this checkpoint.

### 5. the latest package updater failed before package mutation

Latest attempt:

```text
run=32142303624
job=95727636509
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
PACKAGE_UPDATE_LEASE16=PASS
```

It then failed before `PACKAGE_UPDATE_OLD_EXACT=PASS`. Therefore the exact failed precondition is one of:

```text
source package client path/executable fence
source package client size fence
source package client SHA fence
```

No narrower cause is proven yet.

Because the failure occurred before the updater's backup/WARP/Xvfb/launcher stages, the attempt did **not** update the package and did not use credentials. The first replacement-session action is a read-only inventory of the current on-disk source-package `bin/client` identity.

## UNKNOWN at handoff

Do not silently convert these into assumptions:

```text
current installed source-package client SHA/size/version
current live status/expiry of the last-proven generation-16 lease
the exact current CipSoft manifest at replacement-session time
new exact build suffix
new exact TGameClient/QMeta/auth offsets and instruction fences
new helper compatibility
new character-selection offsets/contracts
```

## Required continuation order

```text
fresh governance/main/PR/task/lease inventory
 -> read-only source-package bin/client identity
 -> refetch current official CipSoft package manifest
 -> if source package is obsolete: legal official launcher/update with backup+rollback
 -> if source package is already current: skip updater
 -> exact installed SHA/size proof, no stray official client
 -> re-prove native auth + character-login contracts for that exact SHA
 -> rebuild/revalidate helpers; old helper/offsets remain forbidden
 -> fresh Track A canonical admission/bootstrap
 -> restore noVNC using active DISPLAY/raw XRes proof
 -> only after all exact-SHA gates: one-shot authorized native Secrets auth
 -> native character selection from the current live model
 -> original game-server login state machine
 -> causal structural IN_GAME proof
```

## Secret authority boundary for a replacement session

Historical owner authorization to use repository Secrets `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` is recorded as a fact, and the old-client one-shot dispatch occurred without exposing values. A task record or prompt cannot by itself create fresh secret authority for a replacement session. The replacement owner invocation must explicitly preserve that authorization before the Secrets are consumed again.

Even when authorized, values must never be printed, returned to ChatGPT, persisted, committed, included in argv, screenshots, artifacts, shell trace, process environment of the persistent client, or diagnostic dumps. Use only the bounded one-shot sealed-memfd/SCM_RIGHTS native-auth ingress after the updated exact-client contract is re-proven.

## Handoff state

```text
STATUS=READY
RESULT=CONTINUE_FROM_PACKAGE_SOURCE_INVENTORY
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
CREDENTIALS_ALLOWED_NOW=false
LOGIN_ALLOWED_NOW=false
MUTATION_AUTHORIZED_NOW=false
```

One concrete next action is recorded in front matter and must be executed immediately after fresh live-state verification.