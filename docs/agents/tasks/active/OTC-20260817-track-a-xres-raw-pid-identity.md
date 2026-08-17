---
task_id: OTC-20260817-track-a-xres-raw-pid-identity
status: implementing
agent: ChatGPT
session_id: chatgpt-xres-raw-pid-identity-v2-20260817
session_role: runtime_discriminator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: physical-v2
branch: diag/OTC-20260817-track-a-xres-raw-pid-identity-physical-authorized-v2
base_branch: main
base_main: 60ab740872d52f3f7c4802d49fd5275a9968d085
pr: pending
risk: high
updated: 2026-08-17T11:27:00+02:00
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
helper_fix_promoted:
  pr: 455
  merge: 60ab740872d52f3f7c4802d49fd5275a9968d085
  helper_blob: ac3c292087918d01e10006d153f84170210d81d5
  tests: 35/35 PASS
  transport_free: PASS
  strict_main_ci_run: 32015024172
  strict_main_required_job: 95342917833
  strict_main_required_result: SUCCESS
physical_v1:
  run: 32013868595
  exact_client_launches: 1
  xres_query_version: PROVEN_1_2
  xres_query_client_ids_pid_identity: NOT_PROVEN
  failure: promoted helper parsed CLIENTIDVALUE.length with wrong units
  cleanup: COMPLETE
  v1_retry_authorized: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-xres-raw-pid-identity.md
  - docs/agents/evidence/OTC-20260817-track-a-xres-raw-pid-identity/**
  - .github/scripts/tibia-official-client-re-xres-raw-pid-identity-v2-patch.py
  - .github/workflows/tibia-official-client-re-xres-raw-pid-identity-v2.yml
modules_touched:
  - track-a-xres-runtime-discriminator
safety:
  canonical_state_access: forbidden
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  process_memory_access: false
  client_byte_mutation: false
  v2_exact_client_launch_limit: 1
  v2_exact_client_launches_consumed: 0
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
acceptance:
  - fresh base-main and branch authorization fence passes immediately before physical execution
  - Track A runtime governance passes on the exact v2 head/base
  - same immutable post-RHI launch harness/transform blobs are fenced before generation
  - fixed trusted-main XRes helper blob ac3c292087918d01e10006d153f84170210d81d5 is used unchanged
  - exactly one v2 task-owned isolated exact client is launched
  - QueryVersion again proves XRes >=1.2 on the fresh XCB connection
  - raw reply hex is preserved for each final t35 candidate before parser interpretation
  - early t05/t15 snapshots do not abort the run; PID identity is evaluated only against t35 VIEWABLE 1920x1080 candidates
  - at least one t35 VIEWABLE 1920x1080 XID returns the exact launched client PID
  - task-owned process/display state is cleaned completely
  - no canonical registration/lease/state, credentials, login, gameplay or process-memory access is touched
  - one-shot v2 workflow/patcher are removed before terminal task merge
  - final evidence, fresh audit and exact-head CI pass before closeout
classification:
  desired: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  current: V2_PHYSICAL_READY
  failure_is_evidence: true
last_completed_step: #455 promoted the corrected XRes CLIENTIDVALUE byte-length parser to trusted main with 35/35 tests and strict-main required CI success; fresh v2 physical admission is now active with a new one-launch limit
next_action: stage the bounded t35-only raw-XRes v2 patcher/workflow, open a Draft PR, run hosted preflight, then consume at most one v2 isolated client launch if every fresh gate passes.
---

# Raw XRes PID identity discriminator — physical v2

V2 is a fresh admission after the helper repair reached trusted main. It deliberately does not rerun the consumed v1 workflow. The physical discriminator waits for the final t35 X11 state, records raw XRes reply bytes before parsing, and promotes ownership only for a VIEWABLE 1920x1080 resource whose LocalClientPid equals the exact task-owned client PID.
