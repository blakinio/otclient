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
phase: native-login-retained-session-probe
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v2
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
risk: critical
updated: 2026-08-18T12:24:00+02:00
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
gate_a: PASS_BY_REBIND_PROBE
generation_rebind: PASS
gate_b: PASS
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN_BY_REBIND_PROBE
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
canonical_bootstrap_attempts_consumed: 1
canonical_bootstrap_run: 32125054251
canonical_bootstrap_job: 95673637453
canonical_bootstrap_result: REGISTERED_GATE_B_PASS
post_bootstrap_inventory_run: 32125504315
post_bootstrap_inventory_job: 95675058329
canonical_rebind_attempt_limit: 1
canonical_rebind_attempts_consumed: 1
canonical_rebind_preacquire_failure_run: 32125796858
canonical_rebind_preacquire_failure_job: 95675952044
canonical_rebind_preacquire_failure_discriminator: invalid_ttl
canonical_rebind_run: 32125924194
canonical_rebind_job: 95676341318
canonical_rebind_head: f9ccc6f1d0aa60c188534c1e83f25cd915323b72
canonical_rebind_result: REBIND_GATE_B_PASS_ACTIVE_GEN10
canonical_rebind_registration_generation: 2
canonical_rebind_registration_lease_generation: 10
canonical_rebind_registered_pid: 2658
canonical_rebind_registered_process_start_ticks: 66643010
canonical_rebind_registered_boot_id_sha256: a7395225814c9a850ff7663d0bce2dd289cf300c37d78e286d5c7d31043653f9
canonical_rebind_registered_display: ':99'
canonical_rebind_registered_window_identity: x11-window:12582929
canonical_rebind_controller_task: OTC-20260818-native-login-to-ingame-e2e
canonical_rebind_controller_session: chatgpt-native-login-e2e-20260818
canonical_rebind_lease_left_active: true
retained_session_probe_limit: 1
retained_session_probe_attempts_consumed: 0
retained_session_probe_process_observation_authorized: true
retained_session_probe_memory_read_authorized: true
retained_session_probe_method_invocation_authorized: false
retained_session_probe_secret_value_read_authorized: false
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — retained native session discriminator

The current physical runtime is now authoritatively bound to active canonical lease generation `10` and registration generation `2` after fresh exact-client rebind and immediate same-generation Gate B:

```text
RUN=32125924194
JOB=95676341318
HEAD=f9ccc6f1d0aa60c188534c1e83f25cd915323b72
TRACK_A_CANONICAL_REBIND=PASS
TRACK_A_CANONICAL_GATE_B=PASS
LEASE_GENERATION=10
REGISTRATION_GENERATION=2
PID=2658
PROCESS_START_TICKS=66643010
DISPLAY=:99
WINDOW=x11-window:12582929
REMOTE_VIEW_MAPPING=PROVEN
```

Durable evidence:

- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-controller-plane-admission-inventory.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-canonical-bootstrap-gate-b.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-post-bootstrap-controller-inventory.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-canonical-rebind-gate-b.md`

## Current bounded authority

Exactly one **read-only retained-native-session discriminator** is admitted while the same generation-10 lease remains current. Before process observation, the workflow must:

1. prove live `main` still equals the exact task base;
2. renew the existing task/session lease with the existing task-local token, without acquiring a new generation;
3. require the renewed lease to remain active generation `10` for this exact task/session;
4. regenerate the promoted raw-XRes probe worker and rerun canonical Gate B against generation `10`;
5. recheck authoritative registration generation `2` / lease generation `10` and the exact official-client fence.

Only after those gates may the probe observe the current client process.

The discriminator may attach read-only to the exact registered PID and inspect only structural, non-secret current-native-model facts required to decide whether the client is already at/owns character-selection state. The strongest previously validated current-session discriminator is the exact `TCharacterSelectionController` primary vptr `0x308ed68` plus its native character-list cardinality boundary from the historical V17 work. For this fresh runtime the probe must independently derive PIE load bias, require exactly one current controller instance if present, verify the runtime vptr, and emit only cardinality/structural booleans. It must not print names, worlds, tokens, strings, raw buffers, screenshots, packets or arbitrary memory.

No native method may be invoked in this read-only phase. In particular `advanceStateMachineDirectlyToCharacterSelection()` remains a conditional next action only if current retained/native state is independently proven valid; the probe does not call it merely to see whether it works.

## Retained-session classification

```text
if exactly one current TCharacterSelectionController exists and native character-list cardinality >= 1:
    RETAINED_NATIVE_SESSION=PROVEN_AVAILABLE
    INITIAL_AUTH=NOT_NEEDED_SESSION_REUSED
    next step = separately admit native semantic unique-character confirmation under same current authority
else:
    RETAINED_NATIVE_SESSION=NOT_PROVEN_AVAILABLE
    next step = classify cold-auth requirement and test legal protected local credential ingress capability before requesting any secret
```

A zero/absent controller/model is not treated as proof about the unknown persistent-session storage implementation; it is sufficient only to establish that this running freshly bootstrapped client does not currently expose a valid native character-selection model that can be reused without authentication.

## Forbidden in this phase

- reading or emitting credentials, OTPs, cookies, session keys, `TPlaySessionData`, character names or world strings;
- native method calls, QMeta dispatch or process-memory writes;
- GUI/form interaction;
- OCR, screenshots, image matching or coordinate input;
- account login, character login or gameplay;
- a second retained-state probe if the first returns a new material discriminator without an evidence-backed repair.

## Recovery checkpoint

```text
STATUS=validating
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
BRANCH=runtime/OTC-20260818-native-login-to-ingame-e2e-v2
RUNTIME_ACCESS=canonical_reuse_or_mutation
CANONICAL_LEASE_STATUS=active
CANONICAL_LEASE_GENERATION=10
REGISTRATION_GENERATION=2
REGISTRATION_LEASE_GENERATION=10
GENERATION_REBIND=PASS
GATE_B=PASS
MUTATION_AUTHORIZED=false
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
RETAINED_SESSION_PROBE_LIMIT=1
RETAINED_SESSION_PROBE_ATTEMPTS_CONSUMED=0
FIRST_UNRESOLVED_EDGE=current native character-selection model/session availability
NEXT_ACTION=renew existing generation-10 lease, rerun same-generation Gate B, then perform one structural read-only current-native character-selection/model discriminator with no secret values and no method calls
```
