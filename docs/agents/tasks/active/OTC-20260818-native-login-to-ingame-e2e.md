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
phase: github-secrets-reentry-current-main-inventory
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: 066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
risk: critical
updated: 2026-08-18T12:54:00+02:00
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
github_actions_secret_ingress_authorized_by_owner: true
github_actions_secret_ingress_authorization_source: owner request "To sprawdz to z secrets" on 2026-08-18
github_actions_secret_email_name: TIBIA_TEST_EMAIL
github_actions_secret_password_name: TIBIA_TEST_PASSWORD
github_actions_secret_presence_run: 32128651952
github_actions_secret_presence_job: 95684712657
github_actions_secret_email_present: true
github_actions_secret_password_present: true
github_actions_secret_email_shape_valid: true
github_actions_secret_password_shape_valid: true
github_actions_secret_pair_ready: true
github_actions_secret_values_logged: false
previous_reentry_inventory_run: 32128864303
previous_reentry_inventory_job: 95685348919
previous_reentry_inventory_result: REFUSED_LIVE_MAIN_MOVED_BEFORE_RUNTIME
previous_base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
current_main_rest_reason: docs(track-a) chat inbound static boundaries PR 527 only
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
controller_plane_inventory_run: 32124348434
canonical_bootstrap_run: 32125054251
canonical_bootstrap_result: REGISTERED_GATE_B_PASS
post_bootstrap_inventory_run: 32125504315
canonical_rebind_run: 32125924194
canonical_rebind_result: REBIND_GATE_B_PASS_ACTIVE_GEN10
retained_session_probe_run: 32126937957
retained_session_probe_result: CURRENT_NATIVE_CHARACTER_MODEL_EMPTY
retained_session_available: false
cold_auth_required: true
cold_auth_capability_run: 32127178186
cold_auth_controlling_tty: false
cold_auth_helper_loaded: false
cold_auth_auth_socket_present: false
terminal_release_run: 32127353047
terminal_release_generation: 10
controller_authority_released: true
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — GitHub Secrets re-entry on current main

The owner explicitly requested continuation with repository GitHub Actions Secrets. Secret-presence workflow `32128651952 / 95684712657` proved both `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` are non-empty, UTF-8-bounded for the existing 1..1024-byte memfd contract, and masked by GitHub. No value was printed or returned to ChatGPT.

The first re-entry controller inventory (`32128864303 / 95685348919`) refused before governance/runtime observation because live `main` had advanced from `a518cea...` to `066a5ba8...`. Inspection proved that new main commit is `docs(track-a): promote chat inbound static boundaries (#527)`, a static documentation/evidence promotion that does not mutate the physical runtime. This task was therefore restacked without carrying stale base authority.

## Current secret-bearing boundary

Owner authorization permits this continuation to use the existing Actions secrets only through a one-shot secret producer. It does not permit plaintext files, logging, argv exposure, GUI credential entry, OCR, coordinate automation, auth bypass, challenge fabrication, TLS weakening or server-response spoofing.

Intended secret path after fresh runtime admission:

```text
GitHub Actions secret environment in dedicated one-shot producer
 -> bounded validation
 -> sealed anonymous memfd
 -> SCM_RIGHTS
 -> exact auth-helper socket
 -> exact process/client/peer fence
 -> TGameClient::onRequestLoginWithCredentials(QString,QString)
 -> original Tibia auth state machine
```

No secret may be consumed until current-main-fenced controller inventory, fresh generation authority and an exact auth-helper-enabled runtime are proven.

## Recovery checkpoint

```text
STATUS=validating
BASE_MAIN=066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
BRANCH=runtime/OTC-20260818-native-login-to-ingame-e2e-v3
SECRET_PAIR_READY=true
SECRET_VALUES_LOGGED=false
CURRENT_KNOWN_LEASE_GENERATION=10
CURRENT_KNOWN_LEASE_STATUS=released
CURRENT_KNOWN_REGISTRATION_GENERATION=2
CURRENT_KNOWN_REGISTRATION_LEASE_GENERATION=10
MUTATION_AUTHORIZED=false
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
FIRST_UNRESOLVED_EDGE=fresh controller-plane state on current main after terminal release
NEXT_ACTION=run exactly one current-main-fenced no-client controller-plane inventory on synology-otclient-01; if released generation 10 and registration 2/10 remain unchanged, admit generation-11 rebind before any runtime replacement or secret use
```
