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
phase: github-secrets-reentry-inventory
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v2
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
risk: critical
updated: 2026-08-18T12:50:00+02:00
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

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — GitHub Secrets re-entry

The owner explicitly requested a continuation using repository GitHub Actions Secrets. This checkpoint records that authorization without treating secret values as repository data.

## Verified secret availability

Hosted workflow `32128651952 / 95684712657` referenced only the canonical secret names already used by historical physical PR #475 and emitted booleans only:

```text
NATIVE_LOGIN_SECRET_EMAIL_PRESENT=true
NATIVE_LOGIN_SECRET_PASSWORD_PRESENT=true
NATIVE_LOGIN_SECRET_EMAIL_SHAPE_VALID=true
NATIVE_LOGIN_SECRET_PASSWORD_SHAPE_VALID=true
NATIVE_LOGIN_SECRET_PAIR_READY=true
```

The secret values were masked by GitHub and were not printed, persisted, committed or returned to ChatGPT.

This owner authorization supersedes the previous task-local assumption that only a human controlling `/dev/tty` may be used for this particular continuation. It does not authorize plaintext files, logs, argv exposure, GUI credential entry, OCR, coordinate automation, auth bypass, 2FA/CAPTCHA fabrication, TLS weakening or server-response spoofing.

## Safety boundary for the next secret-bearing operation

The intended path is:

```text
GitHub Actions secret environment in a dedicated one-shot producer
 -> immediately bounded UTF-8 validation
 -> sealed anonymous memfd
 -> unset secret environment in the producer
 -> SCM_RIGHTS
 -> exact auth-helper socket
 -> exact client/peer identity fence
 -> TGameClient::onRequestLoginWithCredentials(QString,QString)
 -> original Tibia authentication state machine
```

No secret-bearing operation is admitted yet. The prior generation-10 controller lease was deliberately released, so the continuation must first perform a fresh no-client controller-plane inventory, then establish fresh canonical authority. Because the currently registered runtime was launched without the experimental auth helper, it must be replaced or otherwise prepared through a separately admitted exact-client transition before credentials may be consumed.

## Recovery checkpoint

```text
STATUS=validating
RESULT=CONTINUING_WITH_OWNER_AUTHORIZED_GITHUB_SECRETS
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
FIRST_UNRESOLVED_EDGE=fresh controller-plane state after terminal release
NEXT_ACTION=run one fresh no-client controller-plane inventory on synology-otclient-01; if state remains released generation 10 with registration 2/10, admit exactly one generation-11 acquire/rebind/Gate-B transition before any runtime replacement or secret use
```
