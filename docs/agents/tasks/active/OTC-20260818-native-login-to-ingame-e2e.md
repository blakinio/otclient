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
phase: native-login-canonical-rebind
branch: runtime/OTC-20260818-native-login-to-ingame-e2e-v2
base_branch: main
base_main: a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
risk: critical
updated: 2026-08-18T12:15:00+02:00
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
runtime_access: canonical_rebind
runtime_owner_task: OTC-20260818-native-login-to-ingame-e2e
runtime_namespace: canonical-live-runtime
canonical_registration: PRESENT
canonical_lease_generation: 10
registration_lease_generation: 9
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: REQUIRED_NOT_PROVEN
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
canonical_bootstrap_attempts_consumed: 1
canonical_bootstrap_run: 32125054251
canonical_bootstrap_job: 95673637453
canonical_bootstrap_head: d1ab020f11365abeab7a0c2cbd7eeea3e99de38b
canonical_bootstrap_result: REGISTERED_GATE_B_PASS
canonical_bootstrap_registration_generation: 1
canonical_bootstrap_registered_pid: 2658
canonical_bootstrap_registered_process_start_ticks: 66643010
canonical_bootstrap_registered_boot_id_sha256: a7395225814c9a850ff7663d0bce2dd289cf300c37d78e286d5c7d31043653f9
canonical_bootstrap_registered_display: ':99'
canonical_bootstrap_registered_window_identity: x11-window:12582929
post_bootstrap_inventory_run: 32125504315
post_bootstrap_inventory_job: 95675058329
post_bootstrap_inventory_head: 4b02606b585c5f02f7f2293c5916f2a66ee6ad8a
post_bootstrap_observed_lease_status: released
post_bootstrap_observed_lease_generation: 9
post_bootstrap_observed_registration_generation: 1
post_bootstrap_observed_registration_lease_generation: 9
post_bootstrap_control_metadata_unchanged: true
next_lease_generation_expected: 10
next_lease_generation_source: direct released generation 9 plus exactly one fail-closed acquire by this task/session
canonical_rebind_attempt_limit: 1
canonical_rebind_attempts_consumed: 0
success_result: CHARACTER_ACTUALLY_LOGGED_INTO_GAME
causal_proof: INCOMPLETE
---

# OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME — next-generation rebind admission

The fresh post-bootstrap controller inventory (`32125504315 / 95675058329`) proved that the authoritative registration still exists and is bound to released lease generation `9`; registration generation remains `1`, controller task/session are null, and the metadata was unchanged by the probe.

Durable evidence:

- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-controller-plane-admission-inventory.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-canonical-bootstrap-gate-b.md`
- `docs/agents/evidence/OTC-20260818-native-login-to-ingame-e2e/20260818-post-bootstrap-controller-inventory.md`

## Rebind transition selected

Exactly one next controller acquisition is admitted for task/session:

```text
TASK=OTC-20260818-native-login-to-ingame-e2e
SESSION=chatgpt-native-login-e2e-20260818
OBSERVED_RELEASED_GENERATION=9
EXPECTED_ACQUIRED_GENERATION=10
REGISTRATION_LEASE_GENERATION=9
```

`canonical_lease_generation: 10` in this checkpoint is the fail-closed generation expected from that one acquisition, derived from the directly observed released generation `9`; it is not a claim that generation `10` already existed before the workflow. The physical workflow must refuse before rebind if acquisition does not produce exactly generation `10` or if any controller/registration field drifted.

After exact acquisition, the promoted `canonical_rebind` transition must operate under the canonical flock, re-prove the same exact boot/PID/start/client fence/display/window/state and unique official-client target, atomically increment `registration_generation`, bind the registration to lease generation `10`, and perform no client mutation. Immediate Gate B must then pass against the same active generation `10`.

The controller lease is intentionally kept active after successful rebind/Gate B so later native-login admission can reuse the same current generation without gratuitously advancing to another generation. The lease capability remains only in the task-local protected runtime path on `synology-otclient-01`; it is never committed or logged.

## Forbidden in this phase

- account credentials or 2FA;
- login, character selection or gameplay;
- client-byte or process-memory mutation;
- GUI/form input;
- historical #475 PID/XID/session authority;
- a second rebind attempt if the first attempt returns a new discriminator.

## Recovery checkpoint

```text
STATUS=validating
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
BRANCH=runtime/OTC-20260818-native-login-to-ingame-e2e-v2
RUNTIME_ACCESS=canonical_rebind
CANONICAL_REGISTRATION=PRESENT
OBSERVED_RELEASED_LEASE_GENERATION=9
EXPECTED_NEXT_ACTIVE_LEASE_GENERATION=10
REGISTRATION_LEASE_GENERATION=9
GENERATION_REBIND=REQUIRED_NOT_PROVEN
MUTATION_AUTHORIZED=false
CREDENTIALS_ALLOWED=false
LOGIN_ALLOWED=false
GAMEPLAY_ALLOWED=false
FIRST_UNRESOLVED_EDGE=acquire exact generation 10, rebind registration 1/9 -> 2/10, immediate same-generation Gate B
NEXT_ACTION=run exactly one current-main fenced canonical acquire+rebind+Gate-B transaction and keep the proven generation-10 lease active on success
```
