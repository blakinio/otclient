---
task_id: OTC-20260818-native-login-to-ingame-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-native-login-e2e-20260818-v3-gen12
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: owner-authorized-github-secrets-native-login-execution
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v3
base_branch: main
base_main: 066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d
risk: critical
updated: 2026-08-18T13:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-native-login-to-ingame-e2e.md
  - docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/**
  - .github/workflows/tibia-official-client-re-native-login-*.yml
  - tools/tibia_runtime_bridge/CMakeLists.txt
  - tools/tibia_runtime_bridge/experimental_character_confirm.cpp
  - tools/tibia_runtime_bridge/experimental_character_confirm_client.py
modules_touched:
  - track-a-native-login-runtime
  - tibia-runtime-bridge-experimental-character-confirm
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
canonical_lease_generation: 12
registration_generation: 4
registration_lease_generation: 12
gate_a: PASS
generation_rebind: PASS
gate_b: PASS
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
runtime_mutation_capability: ACTIVE_GEN12_CURRENT_TASK
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
github_actions_secret_owner_override_of_prompt_section_5: true
github_actions_secret_email_name: TIBIA_TEST_EMAIL
github_actions_secret_password_name: TIBIA_TEST_PASSWORD
github_actions_secret_presence_run: 32128651952
github_actions_secret_presence_job: 95684712657
github_actions_secret_pair_ready: true
github_actions_secret_values_logged: false
github_actions_secret_values_persisted: false
secret_ingress_scope: one-shot normal account authentication only
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
gen12_recovery_run: 32133489401
gen12_recovery_job: 95699515238
gen12_recovery_result: PASS_ACTIVE_GEN12_REG4_12_GATE_B
gen12_recovery_head: acb5e556ae3c790157bcc136a30dea26c1e43e4f
gen12_registered_pid: 2658
gen12_registered_process_start_ticks: 66643010
gen12_registered_display: ':99'
gen12_registered_window_identity: x11-window:12582929
gen12_remote_view_mapping: PROVEN
gen12_lease_expires_at_epoch: 1787056382
gen12_lease_expires_at_utc: 2026-08-18T12:33:02Z
gen12_lease_expires_at_local: 2026-08-18T14:33:02+02:00
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
auth_helper_staged_on_synology: false
canonical_lease_token_present: true
canonical_lease_capability_usable: true
canonical_lease_status_probe_run: 32130384212
canonical_lease_status: active
canonical_lease_expired: false
canonical_lease_recovery: COMPLETED_STALE_TAKEOVER_GEN11_TO_GEN12
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

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — owner-authorized Secrets execution

The owner explicitly instructed this task to perform the real login using the existing GitHub Actions secrets `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. This current owner instruction intentionally overrides the older prompt prohibition on GitHub Actions secret/environment ingress for this bounded attempt only. It does not authorize logging, persisting, echoing, returning to ChatGPT, or reusing the secret values outside normal authentication.

The secret pair was already proven present, non-empty and shape-valid by `32128651952 / 95684712657`, with values masked by GitHub and never emitted.

Canonical authority recovery is complete. Run `32133489401`, job `95699515238` directly proved the expired generation-11 state, absent raw token and unchanged registration `3/11`; acquired generation `12` through the promoted stale-takeover mechanism with the explicit lost-token reason naming superseded run `32129514869 / 95687604400`; rebound registration to `4/12`; and passed immediate same-generation Gate B. The exact client remained PID `2658`, process start ticks `66643010`, exact SHA `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, display `:99`, XRes window `12582929`. No secret was accessed and no login was performed by recovery.

The completed one-shot generation-12 recovery workflow has been removed from the branch. A superseded duplicate recovery run triggered after the successful takeover and failed closed at the expected token-absent precondition; it made no runtime mutation and is not authority.

Next execution uses runtime-preserving helper activation rather than destructive canonical replacement. The promoted transition stack does not expose a reviewed canonical teardown/unregister primitive; manually deleting or editing `runtime-registration.json` is forbidden. Under the current generation-12 canonical `guard-run`, the exact already-admitted client may therefore receive only the verified opt-in native-auth shared object through a bounded debugger-mediated `dlopen`, with no client-byte mutation. The same guard remains held through one-shot auth dispatch and native character confirmation/world-entry observation so no mutation-capable interval escapes serialization. The helper receives no lease capability and the persistent client remains free of credential environment variables.

Execution plan:

```text
active gen12 + registration 4/12 + exact same PID/start/SHA + Gate B
 -> renew/validate current lease
 -> verify hosted auth-helper artifact digest + helper SHA/size
 -> canonical guard-run holds coordination lock
 -> bounded exact-PID debugger activation of opt-in native-auth helper
 -> verify helper mapping + one-shot mode-0600 auth socket + exact runtime identity
 -> separate one-shot GitHub Secrets producer
 -> RLIMIT_CORE=0 + PR_SET_DUMPABLE=0 + bounded source handling
 -> sealed anonymous memfd
 -> SCM_RIGHTS
 -> native TGameClient QMeta method 17
 -> original Tibia authentication state machine
 -> current native character model discriminator
 -> if exactly one current character: freshly revalidate V18 controller/QMeta confirmation and Qt affinity
 -> observe original game-server login chain and structural FullMap/map-description evidence
 -> prove active gameplay/local-player identity or stop at the first genuine external-action/state-machine blocker
```

No GUI login, OCR, image matching, coordinate input, blind keyboard/mouse action, auth bypass, TLS weakening or fabricated server/challenge response is authorized. Genuine 2FA/CAPTCHA/device confirmation remains fail-closed.

```text
STATUS=validating
RESULT=LOGIN_EXECUTION_AUTHORIZED_AND_GEN12_READY
CHARACTER_ACTUALLY_LOGGED_INTO_GAME=NO
CAUSAL_PROOF=INCOMPLETE
CREDENTIALS_ALLOWED=true
LOGIN_ALLOWED=true
MUTATION_AUTHORIZED=true
RUNTIME_MUTATION_CAPABILITY=ACTIVE_GEN12_CURRENT_TASK
```