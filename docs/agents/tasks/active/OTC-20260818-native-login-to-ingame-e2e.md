---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v3-gen16-secrets
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: client-version-gate-update-required
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: d53eec81bf718b1128fc8e7f9b0a53d991bf30bf
risk: critical
updated: 2026-08-18T15:08:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - .github/workflows/tibia-official-client-re-native-login-*.yml
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - tools/tibia_runtime_bridge/CMakeLists.txt
  - tools/tibia_runtime_bridge/experimental_auth.cpp
  - tools/tibia_runtime_bridge/experimental_auth_client.py
  - tools/tibia_runtime_bridge/experimental_auth_launcher.py
  - tools/tibia_runtime_bridge/experimental_character_confirm.cpp
  - tools/tibia_runtime_bridge/experimental_character_confirm_client.py
modules_touched:
  - track-a-native-login-runtime
  - track-a-canonical-transition
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
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260818-native-login-to-ingame-e2e
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: 16
registration_generation: 1
registration_lease_generation: 16
gate_a: PASS
generation_rebind: PASS
gate_b: PASS
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
runtime_mutation_capability: ACTIVE_GEN16_CURRENT_TASK
client_byte_mutation_authorized: false
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
credentials_allowed: true
login_allowed: true
gameplay_allowed: false
simultaneous_logged_in_sessions_max: 1
live_runtime_authorization_source: owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18
github_actions_secret_ingress_authorized_by_owner: true
github_actions_secret_ingress_authorization_source: owner requests "To sprawdz to z secrets" and "Wykonaj logowanie tymi secrets" on 2026-08-18
github_actions_secret_actual_login_authorized_by_owner: true
github_actions_secret_email_name: TIBIA_TEST_EMAIL
github_actions_secret_password_name: TIBIA_TEST_PASSWORD
github_actions_secret_pair_ready: true
github_actions_secret_values_logged: false
github_actions_secret_values_persisted: false
secret_ingress_scope: one-shot normal account authentication only
secret_retry_before_update: false
exact_client_version: 15.32.df7b29
exact_client_size: 51965216
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
current_runtime_pid: 30067
current_runtime_display: ':99'
current_runtime_window_identity: x11-window:12582929
current_runtime_raw_xres_viewable_1920x1080: true
vnc_observability_restored: true
vnc_user_url: http://synology:6082/
client_version_gate_live_ui_proven: true
client_update_required: true
current_official_probe_run: 32140385842
current_official_probe_job: 95721374178
current_official_packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
current_official_client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
current_official_client_size: 52109920
current_official_version_strings: 15.32,11.25
current_official_exact_build_suffix: UNKNOWN
native_auth_secret_dispatch_performed: true
native_auth_invocation_dispatched: true
native_auth_qmeta_method_id: 17
native_auth_account_success_proven: false
post_auth_character_list_count: 0
post_auth_credential_rejected_hits: 0
post_auth_two_factor_hits: 0
post_auth_device_confirmation_hits: 0
post_auth_captcha_hits: 0
post_auth_tls_hits: 0
post_auth_network_timeout_hits: 0
old_native_auth_helper_reusable_on_current_official_client: false
canonical_teardown_required: true
canonical_teardown_implemented: false
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

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — current checkpoint

The owner authorized a real native login with the existing repository Secrets `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. The values must never be logged, persisted, returned to ChatGPT, committed, placed in argv, or reused outside normal authentication.

## Proven native secret dispatch

The bounded gen16 execution successfully transferred the two GitHub Secrets through the protected one-shot path into a sealed anonymous memfd and SCM_RIGHTS handoff. The native helper accepted the request and dispatched `TGameClient::onRequestLoginWithCredentials(QString,QString)` through QMeta method `17` with `ok=true` and `invocation_dispatched=true`.

That proves secret delivery into the old exact client's native authentication boundary. It does **not** prove successful account authentication.

## Current live runtime

```text
lease generation: 16
registration: 1/16
PID: 30067
DISPLAY: :99
XID: 12582929
Gate B: PASS
raw XRes: exact PID ownership + VIEWABLE 1920x1080
noVNC: restored and operator-confirmed at http://synology:6082/
```

The old exact binary is still:

```text
version=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Proven blocker

After observability recovery, the live client displayed:

```text
Your client version is too old.
Restart Tibia to update your client.
```

Therefore the post-auth `character_list_count=0` is not promoted to a wrong-password or 2FA conclusion. The current exact client is obsolete and must be updated before another credential attempt.

Read-only official-manifest probe `32140385842 / 95721374178` resolved the current Linux client to:

```text
packed client.lzma sha256:
1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354

unpacked client sha256:
ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8

unpacked size:
52109920
```

The probe modified neither the client nor Secrets and ended with same-generation Gate B PASS.

## Required continuation

```text
active old gen16 + Gate B
 -> implement reviewed exact canonical teardown/unregister
 -> execute teardown of only the registered canonical process group
 -> update official package via legitimate CipSoft update path
 -> fence installed new binary by exact SHA/size
 -> re-prove native QMeta/vptr/offset/auth + character-login contracts on the new binary
 -> rebuild/revalidate native-auth helper for that exact binary
 -> bootstrap/re-register fresh canonical runtime
 -> restore noVNC to its active DISPLAY
 -> only then use GitHub Secrets once more
 -> native character selection
 -> game-server login
 -> causal IN_GAME proof
```

The old helper and old offsets are explicitly stale for the new SHA and must not be reused by assumption.

## Durable evidence

- `20260818-vnc-observability-and-client-version-blocker.md`
- `20260818-current-official-client-identity.md`
- prior gen16 native-auth dispatch and post-auth diagnostic evidence in this task directory

```text
STATUS=VALIDATING
RESULT=CLIENT_UPDATE_REQUIRED
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
SECRET_RETRY_BEFORE_UPDATE=false
CLIENT_UPDATE_REQUIRED=true
MUTATION_AUTHORIZED=true
RUNTIME_MUTATION_CAPABILITY=ACTIVE_GEN16_CURRENT_TASK
```
