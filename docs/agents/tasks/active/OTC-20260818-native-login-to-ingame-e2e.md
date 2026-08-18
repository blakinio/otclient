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
phase: native-login-canonical-bootstrap
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v2
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
risk: critical
updated: 2026-08-18T11:58:42+02:00
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
runtime_access: canonical_bootstrap
runtime_owner_task: OTC-20260818-native-login-to-ingame-e2e
runtime_namespace: canonical-live-runtime
canonical_registration: ABSENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: PASS
target_uniqueness: UNKNOWN
mutation_authorized: true
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
controller_plane_observed_controller_task: null
controller_plane_observed_controller_session: null
controller_plane_observed_registration: ABSENT
controller_plane_control_metadata_unchanged: true
controller_plane_client_process_observation: false
controller_plane_x11_observation: false
controller_plane_network_observation: false
controller_plane_credentials: false
controller_plane_login: false
controller_plane_gameplay: false
canonical_bootstrap_attempts_consumed: 0
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — canonical bootstrap admission

This is the single current RUNTIME task for the canonical v3 native-login objective. It consumes the current trusted `main`, including merged #505/#507/#510, and inherits no runtime/session/credential/login authority from released PR #475.

## Fresh controller-plane result

The mandatory no-client inventory completed on `synology-otclient-01` as run `32124348434`, job `95671496871`, against exact current base `a518ceaef9135c05e36ffd7066b3acb2d81f8c4c` and semantic head `82d27d97fce047dbad648212428e0b3cdb7f6211`.

Direct facts:

```text
CANONICAL_LEASE=PRESENT
LEASE_STATUS=released
OBSERVED_LEASE_GENERATION=8
CONTROLLER_TASK=null
CONTROLLER_SESSION=null
CANONICAL_REGISTRATION=ABSENT
CONTROL_METADATA_UNCHANGED=true
CLIENT_PROCESS_OBSERVATION=false
X11_OBSERVATION=false
NETWORK_SESSION_OBSERVATION=false
CREDENTIAL_ACCESS=false
LOGIN_PERFORMED=false
GAMEPLAY_PERFORMED=false
```

Durable evidence: `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-controller-plane-admission-inventory.md`.

Ordinary canonical reuse/rebind is therefore unavailable from this checkpoint. The selected next legal transition is the already-promoted canonical bootstrap implementation.

## Authorized bootstrap transaction

Exactly one physical bootstrap attempt is authorized under this admission. The transaction may acquire current canonical lease authority, re-prove registration absence and official-client candidate uniqueness under the canonical flock, launch/register the exact client runtime through the trusted current worker, and require immediate same-generation Gate B before the runtime is accepted.

The bootstrap phase may create the runtime/control metadata required by the promoted transition, but it does not authorize account authentication, credentials, character selection, gameplay, client-byte mutation, a second logged-in session, or any GUI login fallback.

Required fail-closed conditions before/during this single attempt:

- live `main` must still equal the task's exact base immediately before the physical boundary;
- deterministic Track A admission must pass on the exact workflow head;
- canonical registration must still be absent when the transition rechecks it under lock;
- no other task may hold fresh controller authority;
- the official client must be unique and match the exact version/size/SHA fence;
- trusted worker bootstrap must establish its own X11/XRes, VNC and WARP/SOCKS runtime surfaces;
- immediate same-generation Gate B must pass;
- any new discriminator stops the phase with no blind retry.

## Secret boundary

Credentials remain forbidden during bootstrap. The merged protected credential source from #510 remains mandatory only if a later fresh admitted cold-auth phase proves retained native authentication/session state is unavailable.

If that later phase has no legal real controlling `/dev/tty` and no already-approved protected local secret broker, the task must stop at `EXTERNAL_ACTION_REQUIRED`; GitHub Actions secrets/environment, pseudo-TTY substitution and GUI credential entry are not fallbacks.

`gpt-5.3-codex-spark` remains authorized for bounded non-secret assistance, but it has not been invoked because no Codex Spark execution tool is exposed in this session.

## Acceptance

1. The single canonical bootstrap attempt either publishes a freshly fenced authoritative runtime and passes same-generation Gate B or fails closed with one concrete discriminator.
2. After successful bootstrap, reclassify through fresh canonical runtime admission before any observation/authentication.
3. Test retained native auth/session state before any credential request.
4. If cold auth is required, use only merged #505/#507/#510 with the legal protected local source.
5. Character selection uses the current native character model/controller and a semantically unique target, never the visual list.
6. Original game-server login progression must reach server acceptance, `FullMap`, at least 10 map-description strips, active gameplay/local player and selected character/world identity.
7. Only then may the task report `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES` and `CAUSAL_PROOF=COMPLETE`.

## Recovery checkpoint

```text
STATUS=validating
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
BRANCH=runtime/OTC-20260818-native-login-to-ingame-e2e-v2
RUNTIME_ACCESS=canonical_bootstrap
CANONICAL_REGISTRATION=ABSENT
OBSERVED_RELEASED_LEASE_GENERATION=8
MUTATION_AUTHORIZED=true
BOOTSTRAP_ATTEMPT_LIMIT=1
BOOTSTRAP_ATTEMPTS_CONSUMED=0
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
CURRENT_RUNTIME_IDENTITY=NOT_REGISTERED
FIRST_UNRESOLVED_EDGE=canonical bootstrap and immediate same-generation Gate B
NEXT_ACTION=after exact-head Track A governance PASS, run exactly one trusted-current-main canonical bootstrap with no credentials/login/gameplay
```
