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
phase: native-login-post-bootstrap-admission
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v2
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
risk: critical
updated: 2026-08-18T12:09:00+02:00
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
canonical_lease_generation: 9
registration_lease_generation: 9
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: REQUIRED_NOT_PROVEN
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
client_byte_mutation_authorized: false
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
simultaneous_logged_in_sessions_max: 1
bootstrap_attempt_limit: 1
live_runtime_authorization_source: owner invocation of OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME on 2026-08-18
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
protected_secret_source_required_if_cold_auth: true
controller_plane_inventory_run: 32124348434
controller_plane_inventory_job: 95671496871
controller_plane_inventory_head: 82d27d97fce047dbad648212428e0b3cdb7f6211
controller_plane_observed_lease_status: released
controller_plane_observed_lease_generation: 8
controller_plane_observed_registration: ABSENT
controller_plane_control_metadata_unchanged: true
canonical_bootstrap_attempts_consumed: 1
canonical_bootstrap_run: 32125054251
canonical_bootstrap_job: 95673637453
canonical_bootstrap_head: d1ab020f11365abeab7a0c2cbd7eeea3e99de38b
canonical_bootstrap_result: REGISTERED_GATE_B_PASS
canonical_bootstrap_lease_generation: 9
canonical_bootstrap_registration_generation: 1
canonical_bootstrap_registered_pid: 2658
canonical_bootstrap_registered_process_start_ticks: 66643010
canonical_bootstrap_registered_boot_id_sha256: a7395225814c9a850ff7663d0bce2dd289cf300c37d78e286d5c7d31043653f9
canonical_bootstrap_registered_display: ':99'
canonical_bootstrap_registered_window_identity: x11-window:12582929
canonical_bootstrap_registered_remote_view_endpoint: 127.0.0.1:6082
canonical_bootstrap_registered_remote_view_mapping: PROVEN
canonical_bootstrap_registered_state: UNKNOWN
canonical_bootstrap_controller_released: true
canonical_bootstrap_credentials_used: false
canonical_bootstrap_login_performed: false
canonical_bootstrap_gameplay_performed: false
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — post-bootstrap admission

This is the single current RUNTIME task for the canonical v3 native-login objective. It consumes the current trusted `main`, including merged #505/#507/#510, and inherits no runtime/session/credential/login authority from released PR #475.

## Fresh physical bootstrap result

The one authorized canonical bootstrap attempt completed successfully on `synology-otclient-01`:

```text
RUN=32125054251
JOB=95673637453
HEAD=d1ab020f11365abeab7a0c2cbd7eeea3e99de38b
TRACK_A_CANONICAL_BOOTSTRAP=PASS
TRACK_A_CANONICAL_GATE_B=PASS
LEASE_GENERATION=9
REGISTRATION_GENERATION=1
CLIENT_VERSION=15.32.df7b29
CLIENT_SIZE=51965216
CLIENT_SHA256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
REMOTE_VIEW_MAPPING=PROVEN
NATIVE_LOGIN_BOOTSTRAP_RESULT=REGISTERED_GATE_B_PASS
```

The exact registration published by that transaction identified PID `2658`, start ticks `66643010`, boot hash `a7395225814c9a850ff7663d0bce2dd289cf300c37d78e286d5c7d31043653f9`, display `:99`, window `x11-window:12582929`, and loopback remote-view endpoint `127.0.0.1:6082`.

These values are historical evidence for the completed bootstrap transaction, not transferable authority. They must be freshly revalidated before any runtime observation/authentication.

Durable evidence:

- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-controller-plane-admission-inventory.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-canonical-bootstrap-gate-b.md`

The bootstrap workflow was removed after its one successful run. Bootstrap attempt budget is now fully consumed: `1/1`.

## Current released-controller checkpoint

After successful same-generation Gate B, the task explicitly released lease generation `9` and left the registered runtime idle:

```text
CANONICAL_REGISTRATION=PRESENT
CANONICAL_LEASE_STATUS=released
CANONICAL_LEASE_GENERATION=9
REGISTRATION_LEASE_GENERATION=9
CONTROLLER_TASK=null
CONTROLLER_SESSION=null
MUTATION_AUTHORIZED=false
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
```

This checkpoint deliberately does not authorize use of the recorded PID/display or assume that the persistent runtime is still alive. The next action is a fresh current-main, controller-plane-only post-bootstrap inventory under shared flock. If registration or released generation changed, fail closed and reclassify from direct evidence.

If the registration remains generation-bound to released lease `9`, the next controller acquisition will create a newer lease generation and therefore requires the promoted canonical generation-rebind path before any client mutation. No historical lease token, PID, XID, display or login budget is reused.

## Secret boundary

Credentials remain forbidden. Before any password request, the admitted runtime must first prove current exact runtime identity/Gate B and test whether legal retained native authentication/play-session state already exists.

If cold auth becomes necessary, only the merged #505/#507/#510 path may receive credentials locally from the legal protected source. If no real controlling `/dev/tty` or already-approved protected local broker is available at that point, the task stops at `EXTERNAL_ACTION_REQUIRED`; Actions secrets/env, pseudo-TTY substitution and GUI credential entry are forbidden fallbacks.

`gpt-5.3-codex-spark` remains authorized for bounded non-secret assistance but has not been invoked because no Codex Spark execution tool is exposed in this session.

## Acceptance

1. Fresh post-bootstrap controller metadata confirms the current registration/lease relationship without observing or mutating the client.
2. Current controller authority is acquired only through the next legal Track A generation transition; any lease-generation mismatch is resolved by the promoted rebind path and followed by same-generation Gate B.
3. Before native auth, freshly prove exact client identity, process start, namespace, display/XRes ownership, WARP/SOCKS confinement, registration/generation and target uniqueness.
4. Test retained native auth/session state before requesting credentials.
5. If cold auth is required, use only merged #505/#507/#510 with the legal protected local source.
6. Character selection uses the current native character model/controller and a semantically unique target, never the visual list.
7. Original game-server login progression must reach server acceptance, `FullMap`, at least 10 map-description strips, active gameplay/local player and selected character/world identity.
8. Only then may the task report `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES` and `CAUSAL_PROOF=COMPLETE`.

## Recovery checkpoint

```text
STATUS=validating
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
BRANCH=runtime/OTC-20260818-native-login-to-ingame-e2e-v2
RUNTIME_ACCESS=canonical_reuse_or_mutation
CANONICAL_REGISTRATION=PRESENT
CANONICAL_LEASE_GENERATION=9
REGISTRATION_LEASE_GENERATION=9
CONTROLLER_LEASE_STATUS=released
MUTATION_AUTHORIZED=false
BOOTSTRAP_ATTEMPT_LIMIT=1
BOOTSTRAP_ATTEMPTS_CONSUMED=1
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
LAST_PROVEN_BOOTSTRAP=REGISTERED_GATE_B_PASS
CURRENT_RUNTIME_IDENTITY=REQUIRES_FRESH_REVALIDATION
FIRST_UNRESOLVED_EDGE=current post-bootstrap registration/lease state and next-generation rebind requirement
NEXT_ACTION=run exactly one no-client shared-flock controller-plane inventory; if released generation 9 and registration generation binding still match, admit the next controller acquisition/rebind transaction without observing credentials/login/gameplay
```
