---
task_id: OTC-20260816-track-a-canonical-runtime-e2e
status: validating
agent: ChatGPT
session_id: chatgpt-p0-canonical-admission-20260817
session_role: canonical_runtime_owner
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: e2e
phase: p0-canonical-control-plane-admission-probe
branch: runtime/OTC-20260816-track-a-canonical-runtime-p0-admission
base_branch: main
base_main: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
risk: high
updated: 2026-08-17T11:55:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-track-a-canonical-runtime-e2e.md
  - docs/agents/evidence/OTC-20260816-track-a-canonical-runtime-e2e/**
  - .github/workflows/tibia-official-client-re-p0-canonical-admission-inventory.yml
modules_touched:
  - track-a-canonical-control-plane-admission
blocks:
  - OTC-20260815-track-a-p0-direct-position
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-orchestrated-synology
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
validation_level: heavy
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: canonical_reuse_or_mutation
runtime_owner_task: OTC-20260816-track-a-canonical-runtime-e2e
runtime_namespace: canonical-live-runtime
canonical_registration: UNKNOWN
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: REQUIRED_NOT_PROVEN
gate_b: REQUIRED_NOT_PROVEN
bootstrap: REQUIRED_NOT_PROVEN
target_uniqueness: UNKNOWN
mutation_authorized: false
client_byte_mutation_authorized: false
persistent_session_role: canonical_runtime_owner
physical_e2e_required: true
owner_funded_ai_api_authorized: false
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
trusted_identity_chain:
  raw_xres_helper_promotion_pr: 448
  raw_xres_helper_promotion_merge: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  client_id_length_fix_pr: 455
  client_id_length_fix_merge: 60ab740872d52f3f7c4802d49fd5275a9968d085
  physical_identity_pr: 457
  physical_identity_merge: 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
  physical_identity_run: 32015479835
  physical_identity_job: 95344000918
  physical_identity: PROVEN_FOR_THAT_ISOLATED_RUN_ONLY
  physical_identity_cleanup: COMPLETE
  identity_archive_pr: 459
  identity_archive_merge: c55e3523e6e9d50df511e65dce9145a8f951a5f5
  xres_client_base_fix_pr: 461
  xres_client_base_fix_merge: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
current_nonclaims:
  historical_isolated_pid_13648_is_current: false
  historical_isolated_xid_0x00c00011_is_current: false
  historical_isolated_display_231_is_current: false
  current_exact_client_pid: NOT_REGISTERED_UNTIL_FRESH_GATE_B
  current_exact_client_session: NOT_REGISTERED_UNTIL_FRESH_GATE_B
p0_admission_probe:
  purpose: discover only current canonical controller metadata needed to decide whether legal reuse admission can continue
  state_root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
  coordination_lock: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/coordination.lock
  lease_record: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/lease.json
  runtime_registration: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
  allowed_observation:
    - existing canonical state-root presence
    - existing coordination-lock presence
    - nonblocking shared flock acquisition on the existing coordination lock
    - whitelist-only lease metadata snapshot under that shared flock
    - whitelist-only registration metadata snapshot under that shared flock
  forbidden_observation:
    - /proc client/process inspection
    - X11/window inspection
    - VNC/RFB probing
    - input
    - network/session probing
    - credentials/login/gameplay
  forbidden_mutation:
    - creating canonical state directory or coordination lock
    - acquiring/renewing/releasing controller lease
    - registration write/rebind/bootstrap
    - client launch/stop/signal/attach
  probe_can_authorize_runtime_reuse: false
  probe_can_only_select_next_admission_transition: true
safety:
  canonical_state_write: false
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  process_identity_observation_allowed_in_probe: false
  x11_observation_allowed_in_probe: false
  client_byte_mutation: false
  physical_identity_retry_authorized: false
  bootstrap_for_p0_authorized: false
  second_logged_in_session_authorized: false
  track_b_access: false
acceptance:
  - admission record exists before Synology control-plane observation
  - controller-plane probe creates no canonical files and writes no canonical metadata
  - if canonical namespace or registration is absent, ordinary reuse stops fail-closed and P0 does not bootstrap a session solely for validation
  - if registration exists, only its non-secret contract fields are read; no live identity claim is made until a later fresh Gate A/rebind/Gate B transition passes
  - any active lease owned by another task blocks takeover
  - current state is never inferred from historical PID/XID/display/session evidence
last_completed_step: PR #461 protected-merged the hosted XRes client-base helper correction; current physical P0 work has not begun and all current canonical identity facts remain unproven pending this fresh admission inventory
next_action: validate this admission checkpoint, run exactly one non-mutating Synology controller-plane inventory, remove the one-shot inventory workflow, persist its result, then either continue through the required current canonical transition or stop on the single real blocker without bootstrap solely for P0
---

# Track A canonical runtime E2E — fresh P0 admission

This phase does not yet observe the client. It first reconciles only the authoritative canonical controller namespace so the next runtime transition is selected from current facts rather than history.
