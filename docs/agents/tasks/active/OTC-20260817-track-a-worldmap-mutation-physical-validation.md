---
task_id: OTC-20260817-track-a-worldmap-mutation-physical-validation
status: implementing
agent: ChatGPT
session_id: chatgpt-worldmap-mutation-physical-v1-20260817
session_role: runtime_mutation_validator
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: runtime_discriminator
phase: physical-canary-v1
branch: diag/OTC-20260817-track-a-worldmap-mutation-physical-authorized-v1
base_branch: main
base_main: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
risk: critical
updated: 2026-08-17T11:53:00+02:00
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_class: synology_physical_runtime
runner: synology-otclient-01
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
track_a_runtime_agent_admission_version: 1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-mutation-physical-validation
runtime_namespace: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260817-track-a-worldmap-mutation-physical-validation/ephemeral-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
client_byte_mutation_authorized: true
process_memory_access_authorized: true
persistent_session_role: none
physical_e2e_required: true
owner_funded_ai_api_authorized: false
owner_authorization_basis: current owner instruction in this conversation to continue the worldmap task autonomously to its final end after the mutation design and physical identity gates were completed
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
prerequisites:
  worldmap_static_consumer_pr: 367
  worldmap_static_producer_pr: 437
  worldmap_downstream_producer_pr: 446
  mutation_design_pr: 452
  mutation_design_merge: 1e6fcb5ab83c4bb8b762088326cc936857c8e64d
  mutation_design_report: docs/agents/reports/OTCLIENT-20260817-worldmap-mutation-design.md
  xres_identity_pr: 457
  xres_identity_merge: 16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc
  xres_identity_archive_merge: c55e3523e6e9d50df511e65dce9145a8f951a5f5
  xres_identity_classification: XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
  xres_helper_client_base_fix_merge: 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
mutation_contract:
  anchor_va: '0x01cdd958'
  preimage_16_hex: 120000000e0000000800000006000000
  source_pair: [18,14]
  canary_pair: [19,14]
  postimage_prefix_8_hex: 130000000e000000
  immutable_guard_pair: [8,6]
  expected_changed_source_bytes: 1
  derive_file_offset_from_elf_pt_load: true
  canonical_source_patch_in_place: forbidden
  additional_patch_sites_authorized: false
  final_target_extent: UNKNOWN
structural_targets:
  handler_vptr_va: '0x030871d8'
  handler_extent_offsets: ['0xb0','0xb4']
  handler_storage_member_offset: '0x10'
  storage_vptr_va: '0x0308ce70'
  storage_extent_offsets: ['0x48','0x4c']
  expected_handler_pair: [19,14]
  expected_storage_pair_after_slot12: [19,14]
  viewport_persistent_constructor_equality_required: false
safety:
  exact_client_launch_limit: 1
  exact_client_launches_consumed: 0
  patched_copy_only: true
  original_source_write_access: forbidden
  canonical_state_access: forbidden
  credentials_allowed: false
  login_allowed: false
  gameplay_allowed: false
  network_session_login_allowed: false
  process_memory_target: task_owned_patched_client_only
  process_memory_write_allowed: false
  broad_process_inventory: forbidden
  broad_process_cleanup: forbidden
  track_b_access: false
  rollback_required: true
uniqueness_proof:
  state_root_is_per_task: true
  state_leaf_is_run_and_attempt_scoped: true
  namespace_must_not_preexist: true
  x11_display_selected_only_from_free_231_250: true
  warp_port_selected_only_if_not_listening: true
  vnc_port_selected_only_if_not_listening: true
  cleanup_signals_only_processes_with_task_marker_and_role: true
  canonical_namespace_referenced: false
physical_attempts_before_launch:
  - run: 32017164791
    head: fb604a33c2cca6d39fcc3f9f90e3de340df79ef0
    result: REFUSED_BEFORE_SANDBOX_PATCH_OR_LAUNCH
    reason: inherited harness EVENT_BASE_SHA was not passed to generated script
    exact_client_launches: 0
  - run: 32017315080
    head: ea69f8607449cb9713d158e0f6955c8a8ee80ff4
    result: REFUSED_BEFORE_PATCH_OR_LAUNCH
    reason: live main advanced to 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
    exact_client_launches: 0
physical_v1_acceptance:
  - current main equals declared base immediately before physical boundary
  - Track A runtime governance passes for exact branch/base
  - exact source size and SHA pass before task copy
  - ELF64 little-endian x86-64 PT_LOAD mapping uniquely derives file offset for all 16 guard bytes at VA 0x01cdd958
  - exact 16-byte preimage passes
  - only task-owned copied client is patched
  - candidate pair is exactly [19,14], immutable [8,6] guard unchanged
  - full source-vs-copy diff has exactly one changed byte and zero bytes outside the first 8 target bytes
  - patched-copy SHA and path/inode are recorded
  - exactly one task-owned patched client process launches
  - live process executable path/inode/SHA equals declared patched copy
  - bounded process-memory observer targets only that PID and performs reads only
  - runtime load bias and exact Handler/Storage vptr candidates are recorded
  - Handler+0xb0/+0xb4 equals [19,14] if the Handler object is instantiated
  - Storage+0x48/+0x4c propagation is recorded if the accepted slot12 path occurs without login
  - no second patch site is introduced if propagation is absent
  - patched runtime is terminated, task-owned copy/state is removed, and untouched exact source rehashes to the exact source SHA
classification:
  desired_structural: CAUSAL_PROPAGATION_PROVEN
  desired_semantic: SEMANTICALLY_VALIDATED
  current: PHYSICAL_CANARY_V1_READMITTED_ON_CURRENT_MAIN
  semantic_live_login_required_if_startup_does_not_reach_slot12: UNKNOWN
  failure_is_evidence: true
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-mutation-physical-validation.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-mutation-physical-validation/**
  - .github/scripts/tibia-official-client-re-worldmap-copy-patch.py
  - .github/scripts/tibia-official-client-re-worldmap-mutation-physical-v1.py
  - .github/workflows/tibia-official-client-re-worldmap-mutation-physical-v1.yml
modules_touched:
  - track-a-worldmap-mutation-physical-validation
last_completed_step: two fail-closed pre-launch generations consumed zero client launches; current-main drift was reviewed as XRes/canonical-runtime-only and the same [19,14] canary is freshly re-admitted on trusted main 1eb4a8edecba3966aa1e6155e241b404eb4d30cb
next_action: restack the existing branch/PR onto current main without changing the canary, rerun hosted preflight and live-main admission, then consume at most one actual patched-client launch.
---

# Track A worldmap mutation physical validation

This task is the separately admitted executor required by the merged mutation design. It patches only a task-owned copy of the exact client and starts with the one-byte width-axis canary `[19,14]`. No login or second patch site is authorized in v1.
