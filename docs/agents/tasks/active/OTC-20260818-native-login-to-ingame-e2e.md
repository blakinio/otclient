---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v3
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: github-secrets-reentry-helper-build-capability
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: 066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
risk: critical
updated: 2026-08-18T12:59:00+02:00
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
canonical_lease_generation: 11
registration_lease_generation: 11
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
github_actions_secret_ingress_authorized_by_owner: true
github_actions_secret_ingress_authorization_source: owner request "To sprawdz to z secrets" on 2026-08-18
github_actions_secret_email_name: TIBIA_TEST_EMAIL
github_actions_secret_password_name: TIBIA_TEST_PASSWORD
github_actions_secret_presence_run: 32128651952
github_actions_secret_presence_job: 95684712657
github_actions_secret_pair_ready: true
github_actions_secret_values_logged: false
current_main_reentry_inventory_run: 32129188467
current_main_reentry_inventory_job: 95686335148
current_main_reentry_inventory_result: PASS
secret_reentry_rebind_run: 32129321883
secret_reentry_rebind_job: 95686751815
secret_reentry_rebind_result: PASS_ACTIVE_GEN11
secret_reentry_registration_generation: 3
secret_reentry_registration_lease_generation: 11
secret_reentry_registered_pid: 2658
secret_reentry_registered_process_start_ticks: 66643010
secret_reentry_registered_display: ':99'
secret_reentry_registered_window_identity: x11-window:12582929
secret_reentry_remote_view_mapping: PROVEN
secret_reentry_lease_left_active: true
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
retained_session_probe_run: 32126937957
retained_session_probe_result: CURRENT_NATIVE_CHARACTER_MODEL_EMPTY
retained_session_available: false
cold_auth_required: true
cold_auth_helper_loaded: false
cold_auth_auth_socket_present: false
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — active generation 11

Current-main physical re-entry transaction `32129321883 / 95686751815` succeeded:

```text
TRACK_A_CANONICAL_LEASE_GENERATION=11
TRACK_A_CANONICAL_REBIND=PASS
TRACK_A_CANONICAL_GATE_B=PASS
REGISTRATION_GENERATION=3
REGISTRATION_LEASE_GENERATION=11
PID=2658
PROCESS_START_TICKS=66643010
DISPLAY=:99
WINDOW=x11-window:12582929
REMOTE_VIEW_MAPPING=PROVEN
SECRET_ACCESS=false
LOGIN_PERFORMED=false
```

The task now owns active canonical generation 11. No credential has yet been consumed.

## Next discriminator

The running client cannot accept the merged one-shot native-auth socket because it was originally launched without `otclient-tibia-native-auth-experimental.so`. Before replacing that runtime, first establish how the Synology runner can obtain the exact helper binary without touching the client. The next workflow may inspect only build/toolchain availability and build the repository helper in task-local temporary storage. It may not stop, attach to, modify or relaunch the client and may not access GitHub Secrets.

```text
STATUS=validating
RUNTIME_ACCESS=canonical_reuse_or_mutation
LEASE_GENERATION=11
REGISTRATION_GENERATION=3
REGISTRATION_LEASE_GENERATION=11
GATE_A=PASS
GENERATION_REBIND=PASS
GATE_B=PASS
TARGET_UNIQUENESS=PROVEN
MUTATION_AUTHORIZED=false
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
FIRST_UNRESOLVED_EDGE=auth-helper build availability on synology-otclient-01
NEXT_ACTION=build/probe the experimental auth helper without observing or mutating the client; if successful, persist only helper hash/toolchain facts and then separately admit controlled exact-runtime replacement
```
