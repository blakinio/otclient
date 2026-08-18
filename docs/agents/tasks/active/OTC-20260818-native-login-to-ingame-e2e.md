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
phase: native-login-controller-plane-admission-probe
branch: runtime/OTC-20260818-native-login-to-ingame-e2e
base_branch: main
base_main: 4c17cea83421128a7fc709daba2e142dab44471e
risk: critical
updated: 2026-08-18T11:54:38+02:00
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
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: NOT_APPLICABLE
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
client_byte_mutation_authorized: false
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
simultaneous_logged_in_sessions_max: 1
bootstrap_attempt_limit: 0
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
controller_plane_probe_only: true
controller_plane_probe_mutation: false
controller_plane_probe_process_observation: false
controller_plane_probe_x11_observation: false
controller_plane_probe_network_observation: false
controller_plane_probe_credentials: false
controller_plane_probe_login: false
controller_plane_probe_gameplay: false
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — fresh physical E2E

This is the single current RUNTIME task for the canonical v3 native-login objective. It consumes the current trusted `main`, including merged #505/#507/#510, and inherits no runtime/session/credential/login authority from released PR #475.

## Current admission checkpoint

The initial `canonical_bootstrap` classification is **transition-discovery only**. It authorizes one non-mutating controller-plane inventory and does not authorize client observation, launch, bootstrap, registration write, lease mutation, authentication, character selection or gameplay.

Allowed before reclassification:

- read whether the canonical state root and existing coordination lock are present;
- acquire a nonblocking shared flock on the existing coordination lock;
- read only whitelisted non-secret fields from existing `lease.json` and `runtime-registration.json`;
- verify the read-only probe itself did not mutate controller metadata.

Forbidden before reclassification:

- `/proc` client/process inspection;
- X11/XRes/VNC/RFB observation;
- network/session probing;
- client launch/stop/signal/attach;
- lease acquire/renew/release;
- bootstrap/rebind/Gate-B mutation;
- credentials, native auth, 2FA, character selection or gameplay.

## Authority and non-claims

The owner invocation of `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` authorizes this bounded programme task, but live mutation remains fail-closed until the current Track A admission is updated from direct controller-plane evidence and passes current governance.

The merged protected credential source from #510 remains mandatory for cold auth. If the admitted physical environment lacks a legal real controlling `/dev/tty` and there is no already-approved local protected secret broker, the cold-auth boundary is `EXTERNAL_ACTION_REQUIRED`; GUI credential entry, Actions secrets/env ingress and pseudo-TTY substitution are not fallbacks.

`gpt-5.3-codex-spark` is authorized by repository governance for bounded non-secret assistance, but it has not been invoked in this session because no Codex Spark execution tool is exposed here.

## Acceptance

1. Fresh no-client controller-plane inventory completes on `synology-otclient-01` under current deterministic admission.
2. Current lease/registration/controller ownership state selects exactly one legal next Track A transition without historical PID/XID/session reuse.
3. Before any native auth, the same admitted runtime proves exact client identity, PID/start identity, runtime namespace, display/XRes ownership, WARP/SOCKS confinement, required registration/generation and current Gate A/Gate B state.
4. Retained native auth/session state is tested before requesting credentials.
5. If cold auth is required, only the merged protected native-auth path may receive credentials locally from the legal protected source.
6. Character selection uses the current native character model/controller and a semantically unique target, never the visual list.
7. Original game-server login progression is observed causally through server acceptance, `FullMap`, at least 10 map-description strips, active gameplay/local player and selected character/world identity.
8. Only then may the task report `CHARACTER_ACTUALLY_LOGGED_INTO_GAME=YES` and `CAUSAL_PROOF=COMPLETE`.

## Recovery checkpoint

```text
STATUS=validating
BASE_MAIN=4c17cea83421128a7fc709daba2e142dab44471e
BRANCH=runtime/OTC-20260818-native-login-to-ingame-e2e
RUNTIME_ACCESS=canonical_bootstrap transition-discovery only
MUTATION_AUTHORIZED=false
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
CURRENT_RUNTIME_IDENTITY=UNKNOWN
FIRST_UNRESOLVED_EDGE=current canonical controller-plane lease/registration state
NEXT_ACTION=run exactly one non-mutating Synology controller-plane inventory after PR creation and deterministic admission PASS
```
