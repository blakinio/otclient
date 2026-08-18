---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v4-exact-sha-re
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: exact-sha-native-route-reproof
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
risk: critical
updated: 2026-08-18T17:10:18+02:00
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
modules_touched:
  - track-a-native-login-runtime
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
runtime_namespace: native-login-exact-sha-re
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
live_runtime_authorization_source: current owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18; update/VNC already executed, secret authority preserved only for later bounded one-shot native-auth ingress
last_proven_canonical_lease_generation: 16
last_proven_canonical_lease_session: chatgpt-native-login-e2e-20260818-v3-gen16-secrets
canonical_lease_current_status: ACTIVE_AT_LAST_SUCCESSFUL_UPDATE_VALIDATION
canonical_lease_latest_validation_run: 32151397744
canonical_lease_latest_validation_job: 95758005677
current_registration_present: false
current_canonical_session_present: false
old_exact_client_version: 15.32.df7b29
old_exact_client_size: 51965216
old_exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
old_binary_offsets_reusable_on_current_official_client: false
old_native_auth_helper_reusable_on_current_official_client: false
current_official_probe_run: 32146091215
current_official_probe_job: 95740074787
current_official_packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
current_official_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_official_client_size: 52109920
current_official_version_strings: 15.32,11.25
canonical_update_completed: true
canonical_update_run: 32151397744
canonical_update_job: 95758005677
canonical_update_result: PASS_CURRENT_EXACT
installed_exact_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
installed_exact_client_size: 52109920
update_secret_access: false
update_login: false
update_canonical_runtime_started: false
update_vnc_retained: true
novnc_current_run: 32150057458
novnc_current_job: 95753482037
novnc_current_result: PASS_PERSISTENT_LAN_OBSERVER_READY
novnc_current_display: ':99'
novnc_current_url: http://192.168.1.2:6083/
new_exact_auth_contract_reproven: false
new_exact_character_contract_reproven: false
new_exact_ingame_discriminator_reproven: false
new_exact_helper_rebuilt: false
new_exact_runtime_bootstrapped: false
secret_ingress_historical_owner_authorization: true
secret_ingress_current_owner_authorization_preserved: true
secret_ingress_scope: bounded_one_shot_native_auth_only_after_updated_exact_sha_gates
secret_ingress_used_on_current_exact_client: false
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
next_action: Read-only exact-SHA static RE against the installed current official client. Re-prove TGameClient/native auth route and instruction fence, character-selection/controller route and structural IN_GAME discriminator before any helper rebuild, client bootstrap, credential access or login.
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — exact-SHA RE checkpoint

The official Linux package update is complete. The installed source package now matches the freshly verified official target exactly:

```text
run=32151397744
job=95758005677
bin/client sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
bin/client size=52109920
RESULT=PASS_CURRENT_EXACT
SECRET_ACCESS=false
LOGIN=false
CANONICAL_RUNTIME_STARTED=false
VNC_RETAINED=true
```

The retained observer is:

```text
run=32150057458
job=95753482037
DISPLAY=:99
URL=http://192.168.1.2:6083/
RFB/WebSocket/LAN proof=PASS
```

The obsolete binary and all old absolute/PIE-relative offsets, instruction fences, vptr offsets, QMeta assumptions and helper binaries are historical evidence only. They must not be reused by assumption.

## Current admission

This phase is read-only exact-SHA reverse engineering. Runtime/package mutation, credentials, login and gameplay are all forbidden. Account Secrets remain authorized by the current owner only for the later bounded one-shot native-auth ingress after the updated exact-SHA auth/character/IN_GAME contracts and helper/runtime gates are re-proven.

## Required continuation

1. Assert the installed exact SHA/size again on `synology-otclient-01`.
2. Perform bounded static analysis only; do not upload or persist the proprietary binary as an artifact.
3. Re-prove the native authentication target and instruction fence instead of copying old offsets.
4. Re-prove `TGameClient`/Qt semantic identity and method metadata.
5. Re-prove the native character-selection/controller route and `requestCharacterGameserverLogin` progression surface.
6. Establish a structural IN_GAME discriminator suitable for later causal E2E proof.
7. Only then update/rebuild helper code for the exact SHA and separately re-admit a fresh runtime.
8. Only after those gates may the preserved GitHub Secrets authorization be consumed through the canonical bounded one-shot native-auth ingress.

```text
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
```
