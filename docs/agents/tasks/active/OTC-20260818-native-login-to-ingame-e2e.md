---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v4-update
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: official-package-reinstall-after-source-absent
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
risk: critical
updated: 2026-08-18T16:22:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
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
live_runtime_authorization_source: current owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18 explicitly requesting restart/update and VNC observation
last_proven_canonical_lease_generation: 16
last_proven_canonical_lease_session: chatgpt-native-login-e2e-20260818-v3-gen16-secrets
canonical_lease_current_status: ACTIVE_FRESHLY_VALIDATED_AND_RENEWED
canonical_lease_latest_validation_run: 32147631742
canonical_lease_latest_validation_job: 95745198909
canonical_teardown_validation_run: 32141293768
canonical_teardown_validation_result: PASS
canonical_teardown_run: 32141408237
canonical_teardown_job: 95724675001
canonical_teardown_result: PASS
canonical_teardown_registration_absent: true
canonical_teardown_runtime_gone: true
canonical_teardown_lease_retained_at_run_end: true
current_registration_present: false
current_canonical_session_present: false
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
current_installed_package_probe_run: 32145902488
current_installed_package_probe_job: 95739442673
current_installed_package_client_identity: ABSENT
current_installed_package_directory_identity: ABSENT
current_official_probe_run: 32146091215
current_official_probe_job: 95740074787
current_official_probe_result: PASS_READ_ONLY
current_official_packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
current_official_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_official_client_size: 52109920
current_official_version_strings: 15.32,11.25
current_official_exact_build_suffix: UNKNOWN
current_official_changed_since_previous_probe: false
work_toolroot_probe_run: 32146913847
work_toolroot_probe_job: 95742795369
work_toolroot_complete: true
novnc_backend_contract: websockify_6081_to_host_presentation_6082
latest_vnc_attempt_run: 32147631742
latest_vnc_attempt_job: 95745198909
latest_vnc_attempt_result: FAIL_CLOSED_HOST_PORT_6082_ALREADY_OWNED_BY_PRESENTATION_LAYER
latest_vnc_attempt_package_mutation_performed: false
latest_vnc_attempt_client_started: false
canonical_update_completed: false
new_exact_auth_contract_reproven: false
new_exact_helper_rebuilt: false
new_exact_runtime_bootstrapped: false
secret_ingress_historical_owner_authorization: true
secret_ingress_current_owner_authorization_preserved: true
secret_ingress_scope: bounded_one_shot_native_auth_only_after_updated_exact_sha_gates
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
next_action: Establish updater-owned Xvfb/x11vnc/websockify on backend 6081, prove host-facing http://synology:6082/ reaches that exact observer, then run the official CipSoft Linux launcher reinstall with no credentials and verify the installed bin/client exact SHA and size.
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — active replacement-session checkpoint

Continue PR #528 and this task only. The canonical prompt is v4.0.0 and the objective remains `CHARACTER ACTUALLY LOGGED INTO GAME` through original native client logic below the login-form/UI layer.

## Freshly proven replacement-session facts

Repository/controller plane:

```text
main=ebbb36f50076ff4072c7218e302614c1dfea00b1
PR=#528
branch=runtime/OTC-20260818-native-login-to-ingame-e2e-v3
runner=synology-otclient-01
canonical registration=ABSENT
canonical session=ABSENT
lease generation=16, freshly validate+renew PASS
```

Source package inventory:

```text
run=32145902488
job=95739442673
packages/Tibia/bin/client=ABSENT
packages/Tibia directory=ABSENT at the later updater preflight
```

Therefore there is no current source-package client binary to restart. The legal update path is a clean official-package recovery/reinstall, not another login attempt with the obsolete client.

Fresh current-official manifest proof:

```text
run=32146091215
job=95740074787
packed client.lzma sha256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked client sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size=52109920
changed since previous probe=false
```

The work-side Track A toolroot is complete and contains Xvfb/x11vnc/xdotool, XKB, software GL and proxychains (`32146913847 / 95742795369`).

## noVNC correction

The canonical prompt's durable presentation runbook is:

```text
exact updater/runtime DISPLAY
 -> x11vnc RFB backend
 -> websockify/noVNC backend on runner port 6081
 -> existing host-facing presentation http://synology:6082/
```

The failed replacement-session attempt `32147631742 / 95745198909` proved local Xvfb/VNC construction but incorrectly tried to publish host port 6082 a second time. Docker rejected that bind as already in use. Cleanup removed only the attempt-owned resources; no launcher/client/package mutation occurred.

## Current admission

The source-package inventory has resolved to `ABSENT`, the official target has been freshly revalidated, canonical runtime/registration are absent, target uniqueness is proven, and the current owner explicitly requested restart/update plus VNC observation. The task is therefore re-admitted as task-owned `ephemeral_isolated` package-update work with `mutation_authorized: true` and with credentials/login/gameplay all still forbidden during update.

Secrets remain authorized only for the later bounded one-shot native-auth ingress after the updated exact-client RE/helper/canonical gates are re-proven. No secret may be used by the updater or VNC observer.

## Required continuation order

```text
prove host-facing noVNC against backend 6081
 -> official CipSoft launcher/package reinstall, no credentials
 -> exact installed client SHA/size proof, no stray updater/client
 -> re-prove exact-SHA native auth and character-selection contracts
 -> rebuild/revalidate helpers for that exact SHA
 -> separately reviewed trusted-base exact-client fence update if required
 -> fresh canonical bootstrap/admission
 -> restore noVNC on the admitted runtime
 -> bounded one-shot authorized native Secrets ingress
 -> native character selection from the live model
 -> original game-server progression
 -> structural causal IN_GAME proof
```

## Current result

```text
STATUS=VALIDATING
RESULT=CONTINUE_FROM_OFFICIAL_PACKAGE_REINSTALL
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
CREDENTIALS_ALLOWED_NOW=false
LOGIN_ALLOWED_NOW=false
MUTATION_AUTHORIZED_NOW=true
```
