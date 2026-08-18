---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: waiting
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v3
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: github-secrets-reentry-lost-generation11-capability
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: 066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
risk: critical
updated: 2026-08-18T13:12:00+02:00
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
auth_helper_local_build_run: 32129514948
auth_helper_local_build_job: 95687339670
auth_helper_local_build_result: CMAKE_UNAVAILABLE
auth_helper_hosted_build_run: 32129906446
auth_helper_hosted_build_job: 95688521351
auth_helper_hosted_build_result: PASS
auth_helper_sha256: e5cd3f4c42c35000dce7ed5736bdf646fdb179119817f726a86f9e9637a82777
auth_helper_size: 63728
auth_helper_artifact_id: 9321784436
auth_helper_artifact_zip_sha256: cb87d6f0ee1b5e4eb4c096c368ea53d55274f479be5fdaedbf5c1f24bde76608
auth_helper_synology_stage_run: 32129906446
auth_helper_synology_stage_job: 95688788481
auth_helper_synology_stage_result: BLOCKED_TOKEN_FILE_MISSING
auth_helper_staged_on_synology: false
canonical_lease_token_present: false
canonical_lease_capability_usable: false
canonical_lease_status_probe_run: 32130384212
canonical_lease_status_probe_job: 95690011684
canonical_lease_status: active
canonical_lease_expired: false
canonical_lease_expires_at_epoch: 1787053385
canonical_lease_expires_at_utc: 2026-08-18T11:43:05Z
canonical_lease_expires_at_local: 2026-08-18T13:43:05+02:00
canonical_lease_recovery: WAIT_FOR_EXPIRY_THEN_STALE_TAKEOVER
lost_token_cause_run: 32129514869
lost_token_cause_job: 95687604400
lost_token_cause: superseded_rebind_workflow_unlinked_token_before_fail_closed_precheck
lost_token_manual_state_override_used: false
lost_token_fabricated_token_used: false
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
retained_session_probe_result: CURRENT_NATIVE_CHARACTER_MODEL_EMPTY
retained_session_available: false
cold_auth_required: true
cold_auth_helper_loaded: false
cold_auth_auth_socket_present: false
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — generation-11 capability recovery checkpoint

## Verified progress

The owner-authorized GitHub Actions secret pair is present and shape-valid. No secret value has been printed or returned to ChatGPT.

Fresh current-main admission produced canonical generation `11`, registration `3/11`, immediate Gate B PASS, with the exact physical client identity preserved. No secret was consumed during admission.

The repository experimental native-auth helper was successfully built on GitHub-hosted Ubuntu from current source:

```text
SHA256=e5cd3f4c42c35000dce7ed5736bdf646fdb179119817f726a86f9e9637a82777
SIZE=63728
ARTIFACT_ID=9321784436
```

## Current fail-closed blocker

A superseded rebind workflow `32129514869 / 95687604400` deleted the task-local `canonical-lease-token` before its own state precheck. That run then failed closed and did not change lease/registration/client state, but the random raw capability for generation `11` was lost.

Direct status `32130384212 / 95690011684` proved:

```text
TOKEN_PATH_PRESENT=false
LEASE_STATUS=active
LEASE_GENERATION=11
CONTROLLER_TASK=OTC-20260818-native-login-to-ingame-e2e
CONTROLLER_SESSION=chatgpt-native-login-e2e-20260818-v3
EXPIRED=false
EXPIRES_AT=2026-08-18T13:43:05+02:00
CLIENT_OBSERVATION=false
SECRET_ACCESS=false
```

The durable lease contains only the hash of the raw token. The token is not reconstructable and will not be fabricated. Manual lease-state editing is forbidden.

Durable evidence:

`docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-github-secrets-reentry-gen11-capability-loss.md`

## Next legal transition

After the generation-11 lease is expired, re-evaluate current `main`, task/PR state and public lease state. If and only if generation `11` is expired, the token remains absent, and registration remains `3/11`, perform exactly one canonical stale takeover with an explicit reason identifying run `32129514869`. Require generation `12`, then rebind registration `3/11 -> 4/12` and perform immediate same-generation Gate B.

Only after current authority is restored may the programme resume helper staging, controlled helper-enabled runtime replacement and the owner-authorized:

```text
GitHub Secrets -> sealed memfd -> SCM_RIGHTS -> native auth helper
 -> TGameClient::onRequestLoginWithCredentials(QString,QString)
 -> original Tibia authentication state machine
```

2FA, CAPTCHA, device confirmation and all server/TLS validation remain genuine and must not be bypassed or fabricated.

```text
STATUS=waiting
RESULT=WAITING_FOR_CANONICAL_LEASE_EXPIRY
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
NEXT_ACTION=after 2026-08-18T13:43:05+02:00 verify expired gen11 + absent token + registration 3/11; perform one explicit stale takeover to gen12, rebind to 4/12, Gate B, then continue GitHub-Secrets native auth path
```
