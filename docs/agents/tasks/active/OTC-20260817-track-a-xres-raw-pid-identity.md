---
task_id: OTC-20260817-track-a-xres-raw-pid-identity
status: implementing
agent: ChatGPT
session_id: chatgpt-xres-raw-pid-identity-20260817
session_role: runtime_discriminator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: implement
branch: diag/OTC-20260817-track-a-xres-raw-pid-identity-physical-authorized-v1
base_branch: main
base_main: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
pr: 455
risk: high
updated: 2026-08-17T11:09:00+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: synology_physical_runtime
runner: synology-otclient-01
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-xres-raw-pid-identity
runtime_namespace: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260817-track-a-xres-raw-pid-identity/ephemeral-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
client_byte_mutation_authorized: false
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
owner_authorization_basis: current owner invocation 2026-08-17 requesting completion of the full follow-on task after the mutation-design closeout
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
prerequisites:
  raw_xres_helper_pr: 448
  raw_xres_helper_merge: d9529da35ada6ab2a7bf4d2e70205cc0dd7b14ab
  raw_xres_helper_path: .github/scripts/tibia-official-client-re-xres-wire.py
  prior_physical_discriminator: 31973388722
  prior_result: XRES_IDENTITY_UNRESOLVED_HELPER_UNAVAILABLE
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-xres-raw-pid-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/**
  - .github/scripts/tibia-official-client-re-xres-raw-pid-identity-patch.py
  - .github/scripts/tibia-official-client-re-xres-raw-pid-identity-patch-v2.py
  - .github/workflows/tibia-official-client-re-xres-raw-pid-identity.yml
modules_touched:
  - track-a-xres-runtime-discriminator
safety:
  canonical_state_access: forbidden
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  client_byte_mutation: false
  exact_client_launch_limit: 1
  track_b_access: false
  broad_process_cleanup: forbidden
uniqueness_proof:
  task_marker: OTCLIENT_TIBIA_RE_DIAG_TASK=OTC-20260817-track-a-xres-raw-pid-identity
  state_root_is_per_task: true
  state_leaf_is_run_and_attempt_scoped: true
  namespace_must_not_preexist: true
  x11_display_selected_only_from_free_231_250: true
  warp_port_selected_only_if_not_listening: true
  vnc_port_selected_only_if_not_listening: true
  cleanup_signals_only_processes_with_task_marker_and_role: true
  canonical_namespace_referenced: false
  inherited_canonical_task_marker_rebound_by_v2_adapter: true
acceptance:
  - fresh base-main and branch authorization fence passes immediately before physical execution
  - Track A runtime governance check passes on the exact PR head/base
  - immutable same-repository historical post-RHI harness and transforms pass exact blob fences
  - exactly one task-owned isolated exact fenced official Linux client is launched
  - target uniqueness is proven from the task-owned process/display namespace before observation is promoted
  - raw non-root full-display VIEWABLE X11 resource is rediscovered in this run
  - promoted transport-free XRes codec is used for QueryVersion and one-spec QueryClientIds(LocalClientPid)
  - QueryExtension is obtained from the same fresh XCB connection without libxcb-res/libXRes dependency
  - at least one VIEWABLE 1920x1080 XID directly returns the exact launched client PID
  - task-owned process/display state is cleaned completely
  - no canonical registration/lease/state, credentials, login or gameplay is touched
  - exact-head repository/governance CI passes before promotion/closeout
classification:
  desired: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  failure_is_evidence: true
validation:
  first_generation:
    head: 87e1bda874c5fdc48833c367054b5be9fcf96ad1
    run: 32013415890
    hosted_job: 95337663549
    result: FAILED_BEFORE_PHYSICAL_EXECUTION
    first_error: XRES_RAW_PATCH_REFUSED=SNAPSHOT_RAW_XRES_INSERT_COUNT:0
    physical_job: 95337705295
    physical_job_result: SKIPPED
    exact_client_launches: 0
  repair:
    hypothesis: post-RHI transform v2 shifts the PYALLX snapshot anchor indentation from two spaces to four spaces
    evidence: historical accepted XRes v2 adapter on source lineage applied the same two-to-four-space anchor correction
    action: v2 adapter now applies the indent correction and rebinds the inherited canonical task marker to this exact child task before any launch
    identical_retry: false
last_completed_step: the inherited transform ownership was rebound to this child task, the concrete run-scoped namespace and free-display/port/process-marker fences prove isolated target uniqueness, and no physical launch has yet been consumed
next_action: execute the new exact-head hosted preflight and then exactly one physical PID-identity discriminator if governance and base fences pass.
---

# Raw XRes PID identity discriminator

This child task performs the one physical discriminator unlocked by merged #448. It does not relax canonical window identity and does not perform login/gameplay. It reuses the previously proven isolated post-RHI launch harness but replaces the unavailable convenience `libxcb-res` path with the promoted pure XRes wire codec plus a minimal task-local transport over a fresh XCB connection.
